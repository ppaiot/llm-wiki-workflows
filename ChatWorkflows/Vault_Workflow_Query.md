# Vault_Workflow_Query.md

> Operational procedure for answering substantive questions against the vault.
> Read by Claude Code when Pablo asks a question that draws on stored knowledge.
> The key principle: **good answers are filed back into the wiki as new pages.** This is what makes synthesis compound over time.

---

## Purpose

When Pablo asks a question against the vault:

1. Use the wiki as the **primary memory layer**. Read `index.md`, identify candidate pages, read them, follow links as needed.
2. Fall back to `/00 Raw/` only when the wiki is genuinely insufficient.
3. Answer with **wiki page citations**, not raw-source quotes.
4. After answering, decide whether the answer represents **new synthesis worth preserving**. If yes, propose a new wiki page (and create it after confirmation).

This is the Karpathy fileback principle: explorations compound in the wiki the same way ingested sources do.

---

## Named query types

### Research agenda — "what are my loose ends?"

**Trigger:** Pablo asks "what are my loose ends?", "what should I research next?", "what stubs are missing?", or a new ingest produces unresolved wikilinks worth surfacing.

**Procedure:**
1. Scan all pages in `/01 Wiki/` for outbound `[[wikilinks]]` that have no corresponding file.
2. Group unresolved links by domain.
3. For each stub, check whether an existing page already covers the concept under a different name — if so, it becomes an alias, not a new page.
4. Cross-reference existing pages: does the wiki already touch this concept without a dedicated page?
5. Produce a prioritized research agenda — grouped by domain, one line per stub explaining why it matters and what kind of source would fill it best (article, book chapter, conversation, experiment).

**Output:** A brief report in the conversation. If Pablo confirms the priorities, the agenda can be filed as a working note in `/02 Projects/` for ongoing tracking. Do not auto-file without confirmation.

---

## Trigger conditions

This workflow applies to **substantive questions**, not casual chat. Substantive means:

- The question asks for synthesis across multiple wiki pages.
- The question concerns a topic with at least one existing concept, entity, or comparison page.
- The answer would change or extend the wiki's current synthesis.
- Pablo explicitly invokes it: "query the vault", "what do my notes say about X", "/query".

**Skip this workflow for:**

- Quick factual lookups that don't require synthesis ("what's the symbol for the ESP32 deep sleep current draw") — just answer.
- Conversational asides.
- Coding help, debugging, or other task-mode interactions unrelated to vault knowledge.

If in doubt, follow the workflow.

---

## Quick reference

```
1. Parse the question → identify topic, scope, expected synthesis
2. Read index.md → list candidate pages
3. Read candidate pages → follow links as needed
4. Assess: is the wiki sufficient?
5. If yes → answer with citations
   If partial → answer + flag the gap (don't auto-retrieve from /00 Raw/)
   If no → ask Pablo whether to fall back to /00 Raw/
6. After answering → assess fileback potential
7. Check whether any raw source consulted lacks a source-summary → flag or ingest
8. If file-worthy → propose new page, confirm, create
9. If filed back → update index.md, append log.md
```

---

## Step 1 — Parse the question

Identify:

- **Topic.** What is being asked about? Map to candidate concept / entity / comparison pages.
- **Scope.** Single-page recall, multi-page synthesis, or contradiction-spotting across sources?
- **Expected output shape.** Plain answer, comparison table, timeline, list, recommendation?
- **Implicit constraints.** Domain (embedded / nutrition / finance), recency, specific sources Pablo has in mind.

If the question is ambiguous, ask one clarifying question — but only if genuinely necessary. Don't stall.

---

## Step 2 — Read `index.md`

Read `index.md` and list every page that plausibly bears on the question:

- Hubs that cover the topic.
- Concepts and entities matching the topic or its known aliases.
- Source summaries from sources known to cover this material.
- Comparisons addressing the topic.

Report the candidates briefly:

```
CANDIDATE PAGES
- [[ESP32 Deep Sleep]] (concept)
- [[ESP32]] (hub)
- [[Source: Espressif technical reference]]
```

Do this even if the answer seems obvious — surfaces gaps fast.

---

## Step 3 — Read candidates and follow links

Read the candidate pages. Follow `[[wikilinks]]` outward when:

- A page references a related concept whose claims matter for the answer.
- A claim is contested and the source-summary needs reading to assess.
- A comparison page references its underlying sources.

Stop following when additional pages stop adding information. Don't drag in everything.

---

## Step 4 — Assess sufficiency

Three outcomes:

| Outcome | Meaning | Action |
|---|---|---|
| **Sufficient** | Wiki pages contain everything needed | Proceed to answer |
| **Partial** | Wiki covers part of the question; clear gaps remain | Answer the covered part, name the gap explicitly |
| **Insufficient** | Wiki doesn't address the question meaningfully | Ask Pablo: fall back to `/00 Raw/`, or treat as a research task and ingest more sources first? |

**Never silently fall back to `/00 Raw/`.** Falling back means raw-source retrieval (closer to RAG), bypassing the synthesis layer. It's sometimes the right call, but the user must know it happened.

---

## Step 5 — Answer

Format depends on the question, but a few rules apply universally:

- **Cite wiki pages by name.** `According to [[Concept X]], ...` or `[[Source: Foo]] argues ...`.
- **Don't quote raw sources directly** beyond the under-15-word, one-quote-per-source limit. The wiki is the synthesis layer; if a quote is essential, it should already be in the relevant source-summary's `## Quotes worth keeping`.
- **Surface contradictions** when present. If two pages disagree, say so and cite both.
- **Name gaps explicitly** when the wiki is partial. "The wiki has nothing on Y" is a useful signal — it points to a missing page.

Format guidance by question shape:

- Single-concept lookup → plain prose answer, citing the relevant page.
- Cross-source synthesis → consider a brief comparison table; recommend filing it back as a `Comparison:` page.
- Recommendation / decision support → state Pablo's options as they appear in the wiki, surface tradeoffs, note where the wiki is silent.

---

## Step 6 — Assess fileback potential

After answering, ask: **does this answer represent new synthesis the wiki doesn't already contain?**

File back if **any** of these are true:

- The answer integrated information from 2+ wiki pages in a way no single existing page captures.
- The answer surfaced a contradiction not yet documented in a comparison page.
- The answer drew a comparison or analogy not present in the wiki.
- Pablo's question itself encoded an insight (a way of framing things) that future queries could benefit from.
- The answer extended an existing concept in a substantive way.

Do **not** file back if:

- The answer is a straightforward recall of one existing page.
- The synthesis is trivial or transient.
- Pablo signals the question was casual or one-off.

When in doubt, err toward filing back. A wiki that doesn't accumulate is a vector DB with worse retrieval.

---

## Step 7 — Check for unprocessed raw sources

After answering, check whether any file in `/00 Raw/` or `/Clippings/` that you read during this query has been formally ingested.

**How to check:** For each raw file you actually opened, look for a matching entry in `index.md` under `## Source summaries`. A missing entry means the source was read but never ingested.

**Decision table:**

| Situation | Action |
|---|---|
| Source has a source-summary | No action needed |
| Source read, no source-summary, content fully captured in fileback | Flag to Pablo: "I used `<file>` but it has no source-summary -- worth a formal ingest for completeness?" |
| Source read, no source-summary, content NOT fully captured | Strong prompt: propose running `Vault_Workflow_Ingest.md` before closing the session |

**Do not silently skip this check.** A query that reads a raw source and produces a fileback without a source-summary leaves the source in an ambiguous state -- mined but not recorded as ingested. This creates maintenance debt (discovered via a real clippings gap, May 2026).

---

## Step 8 — Propose and create the fileback page

If fileback is warranted:

1. **Propose the page to Pablo.** Title, type (most often `comparison`, sometimes a new `concept`), one-line description, list of pages it would link to.
2. **Wait for confirmation.** *"Should I file this back as [[Proposed Title]]? Type: comparison. Links to: A, B, C."*
3. **If approved**, create the page using the appropriate schema from `Vault_Instructions.md §4`:
   - Comparison → `§4d`
   - New concept → `§4a`
   - Synthesis that doesn't fit comparison or concept → propose to Pablo what schema to use.
4. **Required fields:** `source: claude`, today's date in `created` and `updated`, full frontmatter per spec.
5. **Link bidirectionally** to all pages cited in the answer. Update those pages' `## Related` sections to point back to the new page.
6. **Add to source-summary `## Extracted into` lists** if the fileback drew on specific sources.

The new page is not a transcript of the conversation. It is a clean synthesis Pablo could read in six months and understand.

---

## Step 9 — Update `index.md` and append `log.md`

### 8a. `index.md`

Add the new page to the relevant section. Bump `Last updated:`.

### 8b. `log.md`

Append at the **end of the file** (newest entry always last):

```markdown
## [YYYY-MM-DD HH:MM] query | <short question summary>
- Read: [[Page A]], [[Page B]], [[Page C]]
- Wiki sufficiency: sufficient | partial (gap: ...) | insufficient (fell back to /00 Raw/)
- Filed back: [[New Page Title]]   (or: not filed back)
```

If the query produced no fileback, still log it if it surfaced a gap or contradiction worth knowing about. Routine recall queries don't need logging — use judgment.

---

## Fallback to `/00 Raw/`

Only when Pablo confirms. When you do fall back:

- Read the raw source(s) directly.
- Answer with **both** wiki citations (where they apply) **and** raw-source attribution.
- Treat this as a strong signal that the wiki has a gap. Propose ingesting the source properly (run `Vault_Workflow_Ingest.md`) after answering, so the gap closes.

---

## Verify

Before closing the query session:

- [ ] All claims in the answer are traceable to a wiki page or a clearly-attributed raw source.
- [ ] If a comparison or synthesis page was created, it follows the schema and is fully linked.
- [ ] `index.md` updated (if a page was created).
- [ ] `log.md` appended (if filed back, or if the query exposed a notable gap).
- [ ] Bidirectional links updated.
- [ ] Any raw source consulted during this query either has a source-summary or has been flagged to Pablo for ingest.
- [ ] Pablo has been told what happened: pages read, fileback decision, gaps identified.

---

## Reference

| Topic | Location |
|---|---|
| Comparison page schema | `Vault_Instructions.md §4d` |
| Concept page schema | `Vault_Instructions.md §4a` |
| Linking rules | `Vault_Instructions.md §7` |
| `index.md` format | `Vault_Instructions.md §8` |
| `log.md` format | `Vault_Instructions.md §9` |

---

*Updated by Claude - 25-May-2026, 07:46 EST*
