# Vault_Workflow_Research.md

> Operational procedure for the **deepening loop**: turning an open question on a wiki page into a research prompt, a new raw document, and re-ingested synthesis.
> Read by Claude Code at the start of any research / deepen session.
> Conventions, note schemas, frontmatter, and naming rules live in `Vault_Instructions.md` -- referenced here, not duplicated.

---

## Purpose

Close the wiki's growth loop. The other workflows handle one direction each:

- `Vault_Workflow_Ingest.md` -- external input → wiki
- `Vault_Workflow_Query.md` -- wiki → answer (with optional fileback)
- `Vault_Workflow_Research.md` (this one) -- **wiki → research prompt → new raw doc → re-ingest**

The wiki is not a static archive. The "Open questions" section on every page is a productive output: it names what is missing. This workflow turns those gaps into deliberate inquiry and folds the result back in, so synthesis evolves over time rather than freezing at first-ingest.

Karpathy's llm-wiki frames the wiki as a compilation device. This workflow extends it into a **research agenda generator**.

---

## Trigger conditions

- Pablo points at an open question on a wiki page and says "let's deepen this" or "/research".
- A `/query` session surfaces a gap, contradiction, or thin spot that the existing wiki cannot resolve, and Pablo elects to spawn research instead of filing a partial answer.
- A periodic lint pass flags pages with open questions older than a threshold (currently informal; see `Vault_Workflow_Lint.md`).
- Pablo finishes a primary-source ingest and notices the source itself raises questions worth pursuing.

Not every open question warrants a research loop. See Step 1 for the ripeness criteria.

---

## Quick reference (tl;dr for returning sessions)

```
1. Identify a ripe question        ← not every open question deserves research
2. Frame the research prompt        ← compose from existing wiki context
3. Mark question as `researching`   ← on the originating page
4. Choose research mode             ← LLM / paper / bench / sit-and-think
5. Execute and capture output       ← lands in /00 Raw/ with research provenance
6. Ingest the research doc          ← standard Vault_Workflow_Ingest.md
7. Close the loop                   ← flip question status; enrich origin page
8. Append to log.md                 ← operation: `deepen`
9. Verify
```

---

## Step 1 -- Identify a ripe question

Not every open question deserves a research loop. Most are deliberately parked, or are placeholders for thinking that will happen organically. Spawn research only when:

| Criterion | What it looks like |
|---|---|
| **Gravity** | The same question recurs across two or more concept pages -- the gap pulls multiple pages out of shape |
| **Decision-blocking** | The answer would change a practical choice Pablo is currently making (programming, position sizing, training, hardware) |
| **Page-changing** | The answer would visibly rewrite an existing concept page, not just add a footnote |
| **Interest pull** | Pablo is intellectually drawn to it -- the question won't let go |

If none of these apply, leave the question `open` and move on. The wiki is allowed to have unresolved questions; they're features, not bugs.

---

## Step 2 -- Frame the research prompt

This is where the wiki does work. Before any external research begins, compose the prompt **from the existing wiki context**. A good prompt names:

1. **What's already established** -- cite the relevant `[[Wiki Page]]`s and quote their existing claims briefly.
2. **The specific gap or contradiction** -- not a vague topic, a focused question.
3. **What kind of answer would close it** -- empirical evidence? Definitional clarification? Synthesis across schools? Personal experiment?
4. **Scope and stop condition** -- one-hour LLM dive? A week of paper-reading? Open-ended until satisfied?

Write this as a short prompt block (under 200 words) that could be handed to a deep-research tool, a paper search, or yourself in a focused thinking session.

**Example skeleton:**

```
RESEARCH PROMPT — [[Mobility vs Flexibility]] Q1
Established (from wiki):
- Ido Portal: mobility = always-available ROM; flexibility = warmup-dependent static range. [[Mobility vs Flexibility]]
- FRC operationalizes mobility via end-range loaded ROM (CARs, PAILs/RAILs). [[Functional Range Conditioning]]

Gap:
- The wiki's claim that "flexibility requires warmup" is a paraphrase of Portal's framing, not a substantiated empirical claim. Is this physiologically accurate, or a useful simplification?
- Specifically: what does the literature say about cold vs warm ROM availability, and how does PNF / contract-relax stretching map onto the mobility-vs-flexibility axis?

Closing condition:
- A paragraph in the wiki page citing 2+ physiological sources (textbook or peer-reviewed) that either supports the warmup-dependency claim or qualifies it.

Mode: LLM deep-dive (1-2 hours), supplemented by 1 textbook reference if the LLM output is thin.
Scope: not a meta-analysis; enough to update the page with calibrated confidence.
```

---

## Step 3 -- Mark the originating question as `researching`

Edit the originating page to update the status of the open question being investigated.

**Open Questions status convention:**

| Status | Meaning |
|---|---|
| `(open)` | Default. Not yet investigated. |
| `(researching, YYYY-MM-DD)` | Active research loop in progress. Date is when it started. |
| `(resolved → [[Source - ...]])` | Closed. Link points to the source-summary that closed it. |
| `(parked: <one-line rationale>)` | Deliberately deferred. Rationale required so it doesn't drift back into ambient `open` status. |

Render in the page as a parenthetical suffix on the bullet:

```markdown
## Open questions
- Where do PNF stretching and contract-relax techniques sit in this frame? (researching, 2026-05-19)
- Yoga is not monolithic -- different lineages hit different points. (open)
- Is "flexibility requires warmup" universally true, or training-dependent? (researching, 2026-05-19)
```

Bump `updated:` in the page frontmatter. No footer change required for status-only edits.

---

## Step 4 -- Choose research mode

| Mode | When to use | Output character |
|---|---|---|
| **LLM deep-dive** | Established literature exists; need synthesis fast; question is bounded enough to fit in a session | Synthesis with cited sources; treat LLM citations skeptically -- spot-check |
| **Paper read** | Specific empirical evidence needed; LLM synthesis is likely to be shallow or wrong | Reading notes from a primary source |
| **Bench / self-experiment** | Embedded test, self-experiment, options backtest -- the answer is in *data Pablo generates* | Lab notes, test results, plots |
| **Sit-and-think** | Conceptual / philosophical questions where no external data exists; the answer is Pablo's own working position | A working note that captures the reasoning |

A research loop may combine modes (LLM dive to map the territory, then a paper read for the load-bearing claim, then a self-experiment to verify on Pablo's body / portfolio / hardware). When combined, the final raw doc consolidates them.

---

## Step 5 -- Execute the research and capture output

The output lands in `/00 Raw/` (not `/Clippings/` -- this is deliberate, curated Pablo work, not browser capture).

**Filename pattern:**

```
Research - <Topic> - YYYY-MM-DD.md
```

Examples:
- `Research - Mobility vs Flexibility - 2026-05-22.md`
- `Research - PFIC reporting for ETFs - 2026-06-15.md`
- `Research - ESP32 deep sleep current draw - 2026-07-01.md`

**Research-doc frontmatter (convention, not strict schema):**

Raw docs are generally schema-agnostic, but research docs born from the deepening loop benefit from carrying their own provenance. The convention:

```yaml
---
research_origin: [[Originating Concept Page]]
research_question: "One-line statement of the focused question"
research_mode: llm-deep-dive | paper-read | bench | self-experiment | sit-and-think | combined
created: YYYY-MM-DD
author: pablo | claude | <other>
---
```

This frontmatter is read by the ingest workflow (Step 6) and copied into the source-summary. Other `/00 Raw/` files (downloaded papers, PDF conversions, miscellaneous external content) do **not** require this -- it is specific to internally-generated research output.

**Content structure (suggested, not enforced):**

```markdown
# Research - <Topic>

## Question
(Verbatim from research_question above, plus any clarifying scope notes)

## What the wiki already said
(Brief recap of established context from Step 2)

## Findings
(The actual research output. Cite sources inline. Be honest about confidence.)

## Implications for the wiki
- [[Originating Page]] -- specific claim X should change to Y
- [[Related Page]] -- add a new "..." subsection
- New page worth creating: [[Possible New Concept]] (or: not worth a page)

## Sources cited
- Author, Title, Year, URL or location
- ...

## New open questions surfaced
- (These will become the next iteration of the loop)
```

---

## Step 6 -- Ingest the research doc

Standard ingest per `Vault_Workflow_Ingest.md`, with these specifics:

- `source_type` on the source-summary: `research` (new value for research-loop output). Pre-existing `source_type` values still apply for other raw docs.
- Source-summary title: `Source - Research - <Topic>` (matches existing source-summary naming pattern).
- The source-summary **must** carry the `research_origin` field, copied from the raw doc's frontmatter into the source-summary frontmatter. This is what makes the loop traceable in both directions.
- The source-summary's `## Extracted into` section MUST include the originating page (since the ingest will enrich it as part of Step 7).

Otherwise the ingest proceeds normally: create source-summary, create or enrich concept / entity pages, link bidirectionally, update `index.md`.

---

## Step 7 -- Close the loop on the originating page

After ingest, return to the page that prompted the research and:

1. **Flip the open-question status** from `(researching, YYYY-MM-DD)` to `(resolved → [[Source - Research - <Topic>]])`.
2. **Update the page body** with the new claims, if substantive. Show Pablo the diff before saving substantive changes (per the never-do list in `Vault_Instructions.md §13`).
3. **Add the source-summary** to the page's `## Sources` section.
4. **Bump `updated:`** in frontmatter and append a fresh footer timestamp.
5. **Capture any new open questions** the research raised, with `(open)` status. These feed the next loop iteration.

A research loop that does not close the originating page's open question is incomplete -- the wiki silently goes stale. Verification (Step 9) checks for this.

---

## Step 8 -- Append to `log.md`

New operation type for this workflow: `deepen`.

```markdown
## [YYYY-MM-DD HH:MM] deepen | <originating question, short form>
- Origin: [[Originating Page]] -- question on <topic>
- Mode: llm-deep-dive | paper-read | bench | self-experiment | sit-and-think | combined
- Raw output: 00 Raw/Research - <Topic> - YYYY-MM-DD.md
- Source-summary: [[Source - Research - <Topic>]]
- Pages enriched: [[Originating Page]] (question closed), [[Other Page]] (claim updated)
- New open questions raised: N
```

Use the exact prefix format `## [YYYY-MM-DD HH:MM] deepen | ...` so `grep "^## \[" log.md` stays clean.

The `deepen` entry is in addition to the standard `ingest` entry that Step 6 produced -- both should appear in the log for one full loop. They share the same source-summary link, making the loop traceable from either direction.

---

## Step 9 -- Verify

Run this checklist before closing the research session:

- [ ] Research raw doc exists in `/00 Raw/` with the convention frontmatter.
- [ ] Source-summary created with `research_origin` field populated.
- [ ] `source_type: research` on the source-summary.
- [ ] Originating page's open question status is now `(resolved → [[...]])` -- not still `(researching, ...)`.
- [ ] Originating page's `## Sources` includes the new source-summary.
- [ ] Originating page's `updated:` and footer reflect the loop close.
- [ ] Any new open questions surfaced by the research are captured on the originating page (or new pages) with `(open)` status.
- [ ] `index.md` updated (new source-summary entry; any new concept/entity pages listed).
- [ ] `log.md` has both an `ingest` entry (from Step 6) and a `deepen` entry (this step).
- [ ] No orphan pages created.

Report to Pablo: *"Loop closed. Question '<X>' resolved via [[Source - Research - <Topic>]]. N new open questions surfaced for the next iteration."*

---

## Anti-patterns

Watch for these failure modes:

- **Spawning research on every open question.** Most open questions are deliberately parked or pre-thinking. Apply the Step 1 ripeness criteria honestly.
- **Closing a question with thin evidence to clear it.** A research loop that resolves a question with weaker grounding than the original framing is net-negative. Better to leave it `researching` or downgrade to `(parked: needs better evidence)`.
- **Letting research docs accumulate in `/00 Raw/` without ingesting.** Same anti-pattern as a raw-doc backlog -- the loop is only closed by re-ingestion. The Mode B scout (`Vault_Workflow_Ingest.md`) will eventually catch these, but the discipline is to close fast while the context is fresh.
- **Forgetting to close the originating page after ingest.** Leaves the loop open: the new knowledge lives in the source-summary but the originating page still advertises the question as open. Step 7 is non-optional.
- **Treating LLM citations as ground truth.** LLM deep-dives produce plausible-looking citations that may not exist or may misrepresent the cited source. Spot-check load-bearing citations against the actual source.
- **Conflating "I researched this myself and learned nothing new" with "no result."** A sit-and-think loop that confirms the existing wiki position is still a closed loop -- record it with mode `sit-and-think` and status `(resolved → [[Source - Research: ...]], no change to claim)`.

---

## Reference -- where to find conventions

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
| Standard ingest procedure (Step 6) | `Vault_Workflow_Ingest.md` |
| Query and fileback procedure | `Vault_Workflow_Query.md` |
| Lint procedure (stale-question detection) | `Vault_Workflow_Lint.md` |
| Never-do list | `Vault_Instructions.md §13` |

---

## Open implementation questions

Items not yet resolved -- to be settled in practice or in a follow-up edit to `Vault_Instructions.md`:

- Should `source_type: research` be added to the formal enum in `Vault_Instructions.md §4c`? Currently this workflow introduces it; the schema needs to acknowledge it.
- Should the "Open questions status convention" (`open` / `researching` / `resolved` / `parked`) be lifted into `Vault_Instructions.md §4a` (concept schema) as a documented format? Currently free-form prose is the norm; the loop benefits from structure, but it's a vault-wide style change.
- Should `Vault_Workflow_Lint.md` get a check for "open questions older than 90 days" to surface research candidates automatically? Hook into the existing lint pass.
- Naming: `Research - <Topic> - YYYY-MM-DD.md` includes the date in the filename, which differs from other raw docs. Worth confirming this is desirable (it makes the loop iterations distinguishable when the same topic is revisited).

---

*Updated by Claude - 19-May-2026, 12:58 EST*
