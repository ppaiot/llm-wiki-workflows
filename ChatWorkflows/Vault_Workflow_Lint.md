# Vault_Workflow_Lint.md

> Operational procedure for periodic maintenance passes over the vault.
> Read by Claude Code when Pablo asks for "lint", "maintenance pass", or "health check".
> Lint **produces a report**. It does not auto-fix. Pablo reviews findings and approves changes before any file is edited.

---

## Purpose

Without scheduled maintenance, LLM-Wikis accumulate the failure modes their architecture allows: orphan pages, broken links, stale claims, undocumented contradictions, schema drift, missing entries for repeatedly-mentioned concepts. Lint is the third Karpathy operation — the one that keeps the wiki healthy as it grows.

This workflow runs eight checks, produces a structured report, and walks Pablo through approving fixes.

---

## Scope

**Lint audits `/01 Wiki/` only.** The wiki is the synthesis layer; its internal integrity is what every query and every future ingest depends on.

The other tiers are out of scope by design:

- `/00 Raw/` — immutable sources. Nothing to audit.
- `/02 Projects/` — working notes and project hubs whose job is to link *outward* to the wiki. A project working note with no inbound link from the wiki is not an orphan; it is a working note doing exactly what it should.
- `/03 Journal/` — Pablo's daily notes. Human-owned. Not Claude's territory.

The asymmetry is intentional: wiki pages participate in a dense bidirectional graph; the other tiers are leaf-like consumers of that graph. Auditing the leaves for inbound links from the wiki would generate noise and miss the actual integrity question, which is whether the wiki itself holds together.

If a project note repeatedly references a term that lacks a wiki page, that signal surfaces at the next ingest (`Vault_Workflow_Ingest.md` Step 2). Lint doesn't need to catch it.

---

## Trigger conditions

- Pablo says "lint the vault", "maintenance pass", "health check", "/lint".
- Pablo asks for a status / shape report on the vault.
- Recommended cadence: weekly for an active vault, monthly otherwise.

---

## Quick reference

```
1. Read index.md and scan /01 Wiki/
2. Run eight checks (orphans, broken links, missing pages, schema drift,
   stale content, contradictions, index consistency, source coverage)
3. Produce a structured report
4. Wait for Pablo to approve fixes
5. Apply approved fixes
6. Append to log.md
```

---

## The eight checks

### 1. Orphan detection

A page with **zero inbound links** is an orphan. It exists but is unreachable from the wiki graph.

For each orphan:

- Suggest at least one inbound link from a plausible existing page.
- If nothing plausible exists, recommend either creating a link from the relevant hub, or flagging for removal.

Output:

```
ORPHANS (N)
- [[Page Title]]
  Suggest linking from: [[Hub]] (recommended), [[Other Page]]
```

### 2. Broken link detection

Any `[[wikilink]]` *in a `/01 Wiki/` page* that does not resolve to an existing page or registered alias.

For each broken link:

- Identify the source page and the broken target.
- Suggest: rename the target to match, fix the source's link, or mark as a missing-page candidate (Check 3).

Broken links from project working notes or daily journal entries to wiki pages are not in scope — those are the project's or journal's concern, not the wiki's.

Output:

```
BROKEN LINKS (N)
- [[Source Page]] → [[Nonexistent Target]]
  Suggest: rename target, fix link, or create page
```

### 3. Missing-page detection

A term mentioned in **3+ wiki pages** without its own canonical page is a missing-page candidate.

How to detect:

- Scan `/01 Wiki/` page bodies for capitalized noun phrases and recognized domain terms (use the keyword map in `Vault_Instructions.md §10` as a starting set).
- Count occurrences across distinct wiki pages.
- Anything at 3+ occurrences with no existing page or alias gets flagged.

Output:

```
MISSING PAGES (N)
- "MQTT" mentioned in [[Page A]], [[Page B]], [[Page C]]
  Suggest: create concept page; domain: embedded
- "PFIC" mentioned in [[Page A]], [[Page D]], [[Page F]]
  Suggest: create concept page; domain: finance
```

### 4. Schema drift

Wiki pages whose frontmatter doesn't conform to `Vault_Instructions.md §5`:

- Missing required fields (`type`, `domain`, `created`, `updated`, `source`).
- Unknown fields not in the spec.
- `type` values not in the approved list.
- Inconsistent date formats.
- Missing or outdated `*Updated by Claude*` footer.

Output:

```
SCHEMA DRIFT (N)
- [[Page Title]]
  - Missing field: `updated`
  - Unknown field: `priority`
  - Type "knowledge" not in spec (should be: concept, entity, source-summary, comparison, hub, project, working-note, daily)
```

### 5. Stale content

Wiki pages where `updated` is more than **90 days** old AND one of:

- A newer source-summary cites the same topic.
- The page is in a fast-moving domain (finance, AI tooling, current events).

Stale isn't automatically wrong. The check surfaces pages that may have been superseded so Pablo can decide.

Output:

```
STALE CONTENT (N)
- [[Page Title]] (updated: 2025-12-04)
  Possibly superseded by: [[Source: Newer source]] (ingested 2026-04-22)
  Recommend: review and update, or confirm still current
```

### 6. Contradiction detection

Pairs of pages whose claims appear to conflict.

How to detect:

- For each pair of pages on related topics (via shared links or shared keyword-map terms), scan for negation or opposing claims.
- This is heuristic, not exhaustive. False positives are expected. Surface candidates; let Pablo judge.

Output:

```
POSSIBLE CONTRADICTIONS (N)
- [[Page A]] claims X about Y.
  [[Page B]] claims not-X about Y.
  Recommend: review; if real, create [[Comparison: ...]] page.
```

### 7. Index consistency

Compare `index.md` against the actual contents of `/01 Wiki/`:

- Pages in `/01 Wiki/` not listed in `index.md` → missing index entries.
- `index.md` entries pointing to nonexistent pages → stale index entries.
- Domain mismatches between page frontmatter and index categorization.

Output:

```
INDEX INCONSISTENCY (N)
- [[Page Title]] exists but not in index.md
- index.md lists [[Nonexistent Page]] (no such page)
- [[Page Title]] frontmatter says domain=finance, index lists under embedded
```

### 8. Source-summary coverage

Wiki pages cite sources via `## Sources`. Check that every cited source has a corresponding source-summary page:

- For each `## Sources` entry in `/01 Wiki/`, verify a matching `Source: <Title>` page exists.
- Flag missing source-summaries.

Output:

```
MISSING SOURCE SUMMARIES (N)
- [[Page A]] cites a source with no source-summary
- [[Page C]] cites two sources without source-summaries
```

This check catches sources that were referenced informally without going through `Vault_Workflow_Ingest.md`. Each missing source-summary is a candidate ingest.

---

## The report

Structure the report as eight sections matching the checks above, plus a one-line summary at the top.

```markdown
# Lint Report — YYYY-MM-DD

Vault state: <total wiki pages> pages, <hubs> hubs, <projects> active projects, last ingest <date>.

## Orphans (N)
...

## Broken links (N)
...

## Missing pages (N)
...

## Schema drift (N)
...

## Stale content (N)
...

## Possible contradictions (N)
...

## Index inconsistency (N)
...

## Missing source summaries (N)
...

## Suggested next actions
- Top 3-5 highest-value fixes, ranked.
```

Present the report inline (don't write it as a file unless Pablo asks). Pablo reads it and tells you which fixes to apply.

---

## Applying fixes

Once Pablo approves, batch the fixes by type for efficiency:

1. **Schema drift fixes first** — bring all pages to current spec. These are mechanical and safe.
2. **Index updates next** — close the index/wiki gap.
3. **Link fixes** — fix broken links Pablo has triaged.
4. **New pages** — create missing source-summaries and missing concept pages, in that order. Source-summaries first so the concept pages can cite them.
5. **Contradiction resolution last** — create comparison pages or update existing pages. These are the highest-judgment items, so review each one with Pablo before applying.

**Never apply fixes that require synthesis without explicit per-item confirmation.** Mechanical fixes (frontmatter, links, index entries) can be batched after a single approval. Anything that creates or rewrites a wiki page goes through the standard confirmation step.

---

## Append to `log.md`

After the lint pass, append a single entry summarizing the outcome:

```markdown
## [YYYY-MM-DD HH:MM] lint | <weekly | monthly | ad-hoc>
- Orphans: N (M fixed, K deferred)
- Broken links: N (M fixed)
- Missing pages: N candidates, M created
- Schema drift: N pages (M brought to spec)
- Stale content: N flagged (M updated, K confirmed current)
- Contradictions: N flagged, M resolved as [[Comparison: ...]]
- Index updates: N
- Missing source summaries: N (M ingested)
```

---

## Verify

Before closing the lint session:

- [ ] Report covered all eight checks (even if some sections reported zero findings).
- [ ] Every approved fix was applied.
- [ ] No file was deleted (deletions flagged for Pablo to handle manually).
- [ ] `index.md` updated to reflect any new or removed pages.
- [ ] `log.md` appended with the summary.
- [ ] Pablo has the report (in chat or saved as `Lint-Report-YYYY-MM-DD.md` if requested).

---

## Notes on cadence and sub-scoping

- **Weekly** lints catch drift early. Recommended for an actively-ingesting vault.
- **Monthly** lints are enough for a stable vault.
- **Ad-hoc** lints are appropriate after a large ingest session, before a long break, or when something feels off.
- Within the wiki, lint can be **sub-scoped**: "lint only the finance domain", "lint only pages updated since X". Reduce the eight checks to the sub-scoped set when requested. The vault-tier scope (`/01 Wiki/` only) remains fixed; sub-scoping narrows further within that.

---

## Reference

| Topic              | Location                    |
| ------------------ | --------------------------- |
| Note schemas       | `Vault_Instructions.md §4`  |
| Frontmatter spec   | `Vault_Instructions.md §5`  |
| Naming conventions | `Vault_Instructions.md §6`  |
| Linking rules      | `Vault_Instructions.md §7`  |
| `index.md` format  | `Vault_Instructions.md §8`  |
| `log.md` format    | `Vault_Instructions.md §9`  |
| Domain keyword map | `Vault_Instructions.md §10` |
| Active hubs        | `Vault_Instructions.md §11` |
| Never-do list      | `Vault_Instructions.md §13` |

---

*Updated by Claude - 15-May-2026, 14:00 EST*
