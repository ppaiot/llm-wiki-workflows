# Vault_Workflow_Ingest.md

> Operational procedure for ingesting a new source into the vault.
> Read by Claude Code at the start of any ingest session.
> Conventions, note schemas, frontmatter, and naming rules live in `Vault_Instructions.md` — referenced here, not duplicated.

---

## Purpose

Convert a raw source — file, pasted text, web clip, conversation output — into:

1. A **source-summary page** in `/01 Wiki/` recording what the source is and where it lives.
2. **Concept and entity pages** in `/01 Wiki/` capturing the synthesized knowledge.
3. **Enrichments** to existing wiki pages where the source extends or contradicts them.
4. Optionally, **project working notes** in `/02 Projects/<Project>/` if the source is project-specific.
5. An updated `index.md` and an append to `log.md`.

---

## Ingest modes

The workflow runs in two modes. The mode determines where it stops.

### Mode A — Interactive (default)
Full Steps 1–9 in a single session. Pablo is present and confirms at Step 3 before any files are written. Use when Pablo says "process this" or "/ingest" directly in a session.

### Mode B — Phased (scheduled, quota-optimized)

Splits the workflow across two sessions to move the expensive analysis work off-peak.

**Phase 1 — Scout (unattended, Steps 1–3 only):**
A scheduled agent scans `/00 Raw/` AND `/Clippings/` for unprocessed files (no corresponding entry in `log.md`), runs Steps 1–3 for each, and writes all proposals into `/02 Projects/Pending Ingests.md`. No wiki pages are created. Stops before Step 4. One entry per file, using the Step 3 report format. Clippings are tagged in the report as `[CLIPPING]` so Pablo can prioritize triage.

**Phase 2 — Execute (interactive, Steps 4–9):**
Pablo opens a session, reads `Pending Ingests.md`, confirms or adjusts the proposals, then triggers execution. The session is short — all analysis is pre-done.

### Auto-promote shortcut — `*_KN.md` files

Files named with the `_KN.md` suffix are pre-structured concept notes written by Pablo or a collaborator. They bypass the standard pipeline:
- Skip source-summary creation (the file IS the concept)
- Apply the **Promote** disposition (Step 7) automatically
- Still require: single `domain` value (fix if multi-valued), vault footer, index + log update
- In Mode A: still confirm with Pablo before writing
- In Mode B Phase 1: flag separately in `Pending Ingests.md` as `[AUTO-PROMOTE]` — Phase 2 execution requires only a quick confirmation

---

## Trigger conditions

- Pablo drops a file into `/00 Raw/` and says "process this" or "/ingest".
- Pablo captures a page via Obsidian Web Clipper — the file lands in `/Clippings/` and is treated as a `web-clip` source.
- Pablo pastes text or a URL directly into the conversation.
- Pablo points at an existing file in `/00 Raw/` or `/Clippings/` that has not been processed yet.
- A conversation produces a significant insight worth filing permanently (treat as a synthetic source: save the relevant excerpt to `/00 Raw/` first).
- A scheduled scout agent detects unprocessed files in `/00 Raw/` or `/Clippings/` (Mode B Phase 1).

---

## Quick reference (tl;dr for returning sessions)

**Mode A (interactive):** Steps 1–9 in one session.
**Mode B Phase 1 (scout):** Steps 1–3 only → write to `Pending Ingests.md` → stop.
**Mode B Phase 2 (execute):** Steps 4–9, driven by confirmed proposals.

```
1. Read source → classify type → identify concepts
2. Check vault for existing pages → report findings to Pablo
3. Confirm before writing anything          ← Mode B Phase 1 stops here
4. Create the source-summary page first (always; skip for *_KN.md promotes)
5. Create / enrich concept and entity pages
6. Link bidirectionally
7. Decide what to do with the source file
8. Update index.md and append to log.md
9. Verify
```

---

## Step 1 — Read and classify the source

Read the source in full. Then classify using the table below. The classification drives the rest of the workflow.

| Type | Description | Example |
|---|---|---|
| **Concept** | The whole document IS one concept | A note entirely about SHA-256 |
| **Multi-concept** | Contains several distinct, separable ideas | Karpathy's llm-wiki gist — RAG, wiki pattern, operations, tools |
| **Project document** | Spec, design notes, or working material for a specific project | FileAtlas spec v1.3 |
| **Brain dump** | Raw Pablo thinking, unstructured | Rough bullet list of ideas |
| **External reference** | Article, paper, web clip, book chapter | Copied article about BLAKE3 |

A source can be more than one type. Note all that apply.

**Clippings (`/Clippings/`):** Files written by Obsidian Web Clipper carry their own frontmatter schema (`title`, `source` as URL, `author`, `published`, `description`, `tags: [clippings]`). Read these fields but **do not edit the file** — they're immutable raw input. Map the Web Clipper frontmatter into the source-summary's `source_url`, `source_author`, `source_date`, and `source_path` fields (see `Vault_Instructions.md §4c`). `source_type` is always `web-clip`. If the clipping lacks a clean `published` date, fall back to the `created` field or leave `source_date` empty.

---

## Step 2 — Identify concepts

List every distinct concept, entity, tool, or idea in the source. For each one:

- Assign a **canonical name** following `Vault_Instructions.md §6`.
- Classify its weight: `core` / `supporting` / `tool mention` / `historical reference`.
- Check `index.md` and `/01 Wiki/` for an existing page with that name or a registered alias.

Produce a structured findings list before moving on:

```
SOURCE
- Proposed source-summary title: Source: <Original Title>
- Domain: <electronics | nutrition | finance | IT | math | health | movement | general>
- Type: <article | pdf | conversation | youtube | web-clip | paper | book-chapter>

CONCEPTS / ENTITIES FOUND
- [[LLM-Wiki Pattern]]        [NEW]      core concept
- [[RAG]]                     [EXISTS]   enrich with contrast
- [[Obsidian Web Clipper]]    [NEW]      tool mention (stub)
- [[Dataview]]                [NEW]      tool mention (stub)
- [[Ingest-Query-Lint]]       [NEW]      sub-concept (consider folding into LLM-Wiki Pattern)

CONTRADICTIONS DETECTED
- Source claims X about RAG; existing [[RAG]] page implies not-X.
  → Recommend creating [[Comparison: ...]] OR updating [[RAG]] with new section.

LINKS TO HUBS
- All concepts above link to [[LLM-Wiki Pattern]] hub? No — needs new hub.
  Recommend: do NOT create hub now; revisit after 3+ related sources.
```

---

## Step 3 — Report and confirm

**Do not write any files yet.**

Present to Pablo:

- 2–3 sentence summary of the source.
- Proposed source-summary title.
- Proposed new pages (canonical name + one-line description each).
- Existing pages to enrich (what would be added).
- Contradictions detected, if any.
- Recommended disposition of the source file (see Step 7).

Ask: *"Should I proceed with these? Any to skip, rename, merge, or defer?"*

**Wait for explicit confirmation before Step 4.**

**Mode B Phase 1 exit point:** In scouting mode, stop here. Write the Step 3 report into `/02 Projects/Pending Ingests.md` under a dated header and end the session. Do not create any wiki files.

---

## Step 4 — Create the source-summary page

Always created. This is the canonical record that this source has been ingested, and it's the link target every extracted page will cite.

Use the `source-summary` schema in `Vault_Instructions.md §4c`:

- Title: `Source: <Original Title>`
- Required frontmatter: `type: source-summary`, `domain`, `source_type`, `source_url`, `source_path`, `source_author`, `source_date`, `created`, `updated`, `source: claude`.
- Required sections: Citation, Summary (3-5 sentences), Key claims (each linked to the concept page where the claim lives), Extracted into (list of all pages created or enriched from this source), Quotes worth keeping (each under 15 words, max one per source — see copyright rules below), Open questions raised.

Lives in `/01 Wiki/`.

---

## Step 5 — Create and enrich concept / entity pages

For each approved item, use the appropriate schema from `Vault_Instructions.md §4`.

### 5a. New concept or entity page

Use `concept` or `entity` schema. Required frontmatter and sections per `Vault_Instructions.md §4a` / §4b.

Lives in `/01 Wiki/`. Flat — no subfolders.

Always link the new page to:

- The relevant **hub** for its domain (`Vault_Instructions.md §11`).
- The **source-summary** page from Step 4.
- Any related existing pages, bidirectionally.

### 5b. Enriching an existing page

- Read the existing page first — always.
- Add only what is genuinely new. Do not paraphrase content already present.
- Add the source-summary link to `## Sources`.
- Bump `updated:` in frontmatter.
- Update the footer timestamp.
- If the addition is substantial (over a paragraph or changes a claim), show Pablo the diff before saving.

### 5c. Depth calibration

| Concept type | Treatment |
|---|---|
| Core concept | Full page — all schema sections |
| Supporting concept | Full page if it stands alone; section within a parent page if it doesn't |
| Tool mention | Stub page (Summary + Relevance only) unless Pablo asks for more |
| Historical reference | One-paragraph mention inside the most relevant concept page |

### 5d. Comparisons

If the source contradicts an existing page, or if it triangulates with two or more prior sources, consider creating a `comparison` page (`Vault_Instructions.md §4d`).

Default behavior: **propose the comparison page; do not auto-create.** Comparison pages are high-value but easy to over-produce. Ask Pablo whether the contradiction warrants a dedicated page or just a section in the relevant concept page.

### 5e. Copyright on extracted material

When pulling text from sources:

- **Maximum one short quote per source**, under 15 words, in quotation marks.
- **Never reproduce song lyrics, poems, or large paragraph blocks** even when present in the raw source.
- **Summaries must be substantially shorter than the original** and use Claude's own wording — no close paraphrase of structure or phrasing.
- If a chunk of the source seems important and exceeds these limits, cite the source and the location, and tell Pablo where to read the original.

---

## Step 6 — Link bidirectionally

After all pages are written:

- Every new page links to **at least one existing page** (no orphans).
- Every concept or entity page links to the relevant **hub**.
- Every page extracted from the source links to the **source-summary** page.
- Source-summary `## Extracted into` lists every page created or enriched from this source.
- Update `## Related` sections bidirectionally: if A links to B, B links back to A.
- Use only canonical link names — `[[Canonical Page Name]]`. No aliases, no paraphrases.

---

## Step 7 — Handle the source file

| Disposition | When to use |
|---|---|
| **Keep in `/00 Raw/`** | Default for Pablo-curated raw sources. Source-summary points at it via `source_path`. |
| **Keep in `/Clippings/`** | Default for Web Clipper output. Never move or rename clipping files. Source-summary points at `Clippings/<filename>.md` via `source_path`. |
| **Move to project** | Source is project-specific working material → move to `/02 Projects/<Project>/` as a working note. Update `source_path` in the source-summary accordingly. (Does not apply to clippings — leave them in place.) |
| **Promote** | Source IS exactly one concept and adds no metadata worth preserving separately → fold into the concept page itself, omit the source-summary (rare; ask Pablo). |
| **Flag for deletion** | Source fully extracted, no preservation value → flag for Pablo to delete manually. **Never delete a file.** |

When unclear, ask Pablo. Default to keeping clippings in `/Clippings/` and curated raw in `/00 Raw/`.

---

## Step 8 — Update `index.md` and append to `log.md`

### 8a. `index.md`

Add the new pages to the appropriate sections (`Vault_Instructions.md §8`):

- Source summary → `## Source summaries`, chronological, newest first.
- Concepts → `## Concepts` under the right domain, alphabetical.
- Entities → `## Entities` under the right domain, alphabetical.
- Comparisons → `## Comparisons`.
- New hub (rare) → `## Hubs`, and also update `Vault_Instructions.md §11`.

Bump `Last updated:` at the top of `index.md`.

### 8b. `log.md`

Append a single entry:

```markdown
## [YYYY-MM-DD HH:MM] ingest | Source: <Original Title>
- Source-summary: [[Source: <Original Title>]]
- Created: [[Page A]], [[Page B]]
- Enriched: [[Existing Page]]
- Comparison proposed: [[Comparison: ...]] (declined / created)
- Source disposition: kept in /00 Raw/<filename>
```

Use the exact prefix format `## [YYYY-MM-DD HH:MM] ingest | ...` so `grep "^## \[" log.md` stays clean.

---

## Step 9 — Verify

Run this checklist before closing the ingest session:

- [ ] Source-summary page exists with complete frontmatter.
- [ ] Every new wiki page has complete frontmatter (`type`, `domain`, `tags`, `created`, `updated`, `source`).
- [ ] Every new wiki page has the footer: `*Updated by Claude - DD-MMM-YYYY, HH:MM EST*`.
- [ ] All `[[links]]` use canonical names matching actual page titles exactly.
- [ ] No new page is an orphan.
- [ ] Every extracted page links back to the source-summary.
- [ ] Source-summary `## Extracted into` lists every page touched.
- [ ] Hub link present on every concept and entity page.
- [ ] `index.md` updated.
- [ ] `log.md` appended.
- [ ] No new top-level folder created without approval.
- [ ] Source file disposition confirmed.

Report to Pablo: *"Ingest complete. N new pages, M enriched, source archived to <path>. Index and log updated."*

---

## Reference — where to find conventions

| Topic | Location |
|---|---|
| Note schemas (concept, entity, source-summary, comparison, hub, project, working-note, daily) | `Vault_Instructions.md §4` |
| Frontmatter spec | `Vault_Instructions.md §5` |
| Naming conventions | `Vault_Instructions.md §6` |
| Linking rules | `Vault_Instructions.md §7` |
| `index.md` format | `Vault_Instructions.md §8` |
| `log.md` format | `Vault_Instructions.md §9` |
| Domain keyword map | `Vault_Instructions.md §10` |
| Active hubs | `Vault_Instructions.md §11` |
| Never-do list | `Vault_Instructions.md §13` |

---

*Updated by Claude - 19-May-2026, 10:25 EST*
