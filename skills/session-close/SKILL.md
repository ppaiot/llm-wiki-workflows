---
name: session-close
description: Close a work session by distilling it into durable notes — continuation handoffs, wiki entries, decision records, or learnings. Use this skill whenever the user wants to end, wrap up, close, or summarize a session; asks for a handoff, session summary, or journal entry from the session; says things like "let's close this out", "capture this before we stop", "make a handoff", or "/session-close". Also use it when the user asks to turn the current conversation into a note for their vault.
---

# Session Close

Distill the current session into durable, atomic notes so nothing is lost between sessions. Two failure modes motivate this skill: losing the context needed to continue work in a fresh session, and losing learnings that never get written down. The close is a distillation ritual, not a continuation of the work.

**Cardinal rule — no new work.** Summarize the session as it stands. Do not solve one more sub-problem, improve the code once more, or extend the analysis during the close. If an obvious improvement comes to mind, record it as an open thread or follow-up instead.

## Step 0: Detect environment

Check whether the user's Obsidian vault filesystem is directly writable (Claude Code / local file access).

- **Vault writable → write mode**: create note files directly in the vault, following its conventions (read the vault's `CLAUDE.md` first if not already in context).
- **Vault not reachable (chat session) → paste mode**: emit each note as a single fenced code block, ready for one-gesture copy into 1Writer/Obsidian.

Do not ask the user which mode applies — detect it.

## Step 1: Triage

Two paths, depending on how the skill was invoked:

**Directive invocation** (user named the output, e.g. "create a journal entry from this session"): skip full triage. Produce what was asked. Add at most one line if triage would clearly have caught something else: "Note: there's also an unresolved continuation thread (X) — want a handoff too?" Do not re-litigate the user's choice.

**Open invocation** ("close this session"): classify the session and *propose* the classification — don't ask an open-ended question. Possible outputs, one or several:

| Type | Signal | Output |
|---|---|---|
| Continuation | work is unfinished, will resume in a fresh session | Handoff note |
| Learning | session produced insight/knowledge worth keeping | Atomic wiki note(s) |
| Decision | session ended in a choice between options | Decision record (wiki note with the reasoning and rejected alternatives) |
| Nothing durable | routine Q&A, no lasting artifact | Say so — produce nothing |

Most real sessions are mixed. Propose the full set: "This looks like one continuation thread (X) plus two atomic learnings (Y, Z). Proceed?" Prefer several small atomic notes over one long summary.

The "nothing durable" exit is legitimate. Do not manufacture a note to seem useful — vault pollution is worse than an empty close.

## Step 2: Epistemic audit (always, even in directive mode)

Before writing any note, answer these two questions honestly, about the session's actual content:

1. **What am I least confident about right now?** Identify the specific claims, numbers, or recommendations from the session that rest on assumptions, unverified sources, or reasoning that could be wrong.
2. **What is the user likely missing about the situation?** Step outside the session's momentum. What angle, risk, or alternative did the conversation's framing make invisible?

Answer these *before* generating output, then embed the results in the notes themselves — not as a throwaway chat reply:

- In a **handoff**: a `## Caveats & unverified` section.
- In a **wiki/decision note**: a `confidence:` frontmatter field (`high` / `medium` / `low`) plus a short caveats line where warranted.

This audit is the point of the skill. Resist end-of-session agreeableness — a caveat found now saves a fresh session from inheriting a wrong assumption as fact.

## Step 3: Generate output

### Handoff notes (format owned by this skill)

Filename: `Handoff_<slug>.md` where `<slug>` is a short kebab-case name derived from the session's dominant topic (e.g. `Handoff_carport-snow-load.md`). Propose the slug; the user may override. In write mode, save to the vault's `Handoffs/` folder (create it if absent). Handoffs are disposable — the user purges the folder periodically.

Hard length budget: roughly one screen. State + open threads, not an essay. Template:

```markdown
---
type: handoff
date: <YYYY-MM-DD>
topic: <one line>
source: claude
review-by: <YYYY-MM-DD, optional — when this handoff goes stale>
---

# Handoff: <topic>

## Current state
<Where the work stands. 3–6 bullets max.>

## Decisions made
<Choices settled this session, one line each, with the deciding reason.>

## Dead ends
<Approaches explored and ruled out, and WHY. This is the most valuable
section — it stops a fresh session from re-exploring them.>

## Open threads
<What remains, in priority order.>

## Context a fresh session needs
<File paths, URLs, constraints, key numbers, relevant tools.>

## Caveats & unverified
<Output of the epistemic audit.>
```

### Wiki notes (formats owned by the workflow files — never by this skill)

This skill decides *what* notes to produce; the workflow/template files define *how each note type is formatted*. Do not improvise or reproduce note formats from memory.

Fetch the relevant definition from GitHub (raw URLs — deterministic, no search):

- Journal entry: `https://raw.githubusercontent.com/ppaiot/llm-wiki-workflows/main/Templates/Journal Note.md`
- Project hub: `https://raw.githubusercontent.com/ppaiot/llm-wiki-workflows/main/Templates/Project Hub.md`
- Other note-type templates: `https://raw.githubusercontent.com/ppaiot/llm-wiki-workflows/main/Templates/<type>.md`

In write mode (Claude Code), prefer reading the same files from the local vault if present; the repo is the fallback and the chat-mode source.

**Fail loud.** If a fetch returns 404 or errors, tell the user the workflow file is missing at that URL and ask how to proceed. As a last resort, offer this degraded skeleton — clearly labeled as a fallback, never silently substituted:

```markdown
---
type: <note-type>
date: <YYYY-MM-DD>
tags: []
confidence: <high|medium|low>
source: claude
---

# <Title>

<Atomic content — one idea per note.>
```

### Output hygiene

- All output is markdown. Escape `$` as `\$` throughout.
- **Paste mode**: one fenced code block per note, frontmatter included, nothing outside the fence that belongs in the note. Multiple notes → multiple blocks, each preceded by its intended filename.
- **Write mode**: create the files, then report what was written and where.

## Step 4: Triage-out

After the notes, briefly flag anything that doesn't belong *in* a note:

- **Action items** (calls to make, questions to send someone): list them separately; in chat mode offer to add them to Reminders.
- **Memory / CLAUDE.md updates**: if the session established a stable fact or preference worth persisting, *propose* the update. Never apply it silently.

Keep this step to a few lines. If there's nothing to triage out, skip it without comment.
