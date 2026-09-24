# Continuity Vault — extraction moves

Adapted from the frontier-extraction pattern: bank judgment into artifacts a less
capable setup can still use. On Hatch the "frontier model" is whichever model is
about to lose its window — an access change, a model switch, or a session about
to end.

## The gate: the irreversibility test

Before doing anything, ask: **can a cheaper model redo this tomorrow?** If yes,
decline and redirect to what passes. What passes: a standard written down, a
roadmap already reasoned through, a distilled knowledge vault, a skill that
fires on its own.

Shared rules for every artifact:

1. Write for a *less capable* reader: checkable criteria, not adjectives. Named
   failure modes with the rule that prevents each. Exact escalation triggers.
2. Write reasoning down in full at creation time — rationale, evidence,
   tradeoffs. The document, not the conversation, is the deliverable.
3. Atomize rather than summarize: many linked one-insight notes beat one long
   report. Use [assets/learnings-note-template.md](../assets/learnings-note-template.md).
4. Ask the user for anything personal this needs (their projects, pricing, time
   use); never invent business details or writing samples.

## Move 1 — WORKSPACE: write the operating standard

1. Read how the user works in the project: standing instruction files, recent
   outputs, corrections they've made, conventions visible in the work itself.
2. Rewrite the project's operating guidance (in `AGENTS.md` and, where
   appropriate, `SOUL.md`) as the manual a less capable model needs:
   conventions followed plus ones you'd add, with reasoning; mistakes a weaker
   model will make, named one by one, each with the rule that prevents it;
   quality bars per deliverable type as checkable criteria ("every claim has a
   source link" not "professional"); exact escalation rules — when to ask, when
   to state an assumption and proceed.
3. Propose the 3 skills that would save the most hours in this workspace and
   write them in full. Check trigger phrases against existing skill descriptions
   for collisions first.
4. Present the change as a diff against the current files. Never overwrite
   silently. Editing standing instruction files always needs an explicit user
   request and a backup of the current version.

## Move 2 — AUDIT: consultant-grade business audit

1. Gather context from authorized connectors and workspace files first (Gmail,
   Calendar, financial accounts via their skills); interview the user only for gaps.
2. Audit and rank findings by expected return.
3. Deliver a roadmap a less capable model can execute: ranked moves, highest
   expected return first; per move the why (reasoning in full), exact steps,
   what done looks like as checkable criteria; the three things the user should
   stop doing, reasoning written out in full.
4. Save the roadmap as a file. The conversation is not the deliverable.
   Quality check: could a competent-but-ordinary assistant execute each move
   from the document alone? If a step needs judgment to interpret, write the
   judgment in.

## Move 3 — VAULT: atomized research vault

1. Run or collect the deep research; if reports, threads, or transcripts
   already exist, mine them instead of redoing them.
2. Atomize: one insight per note, title states the insight as a claim (not a
   topic), 3–10 lines of body, source, links to related notes.
3. Link deliberately, both directions. An unlinked note is an orphan and will
   never be resurfaced.
4. Deliver as a folder of markdown files (Obsidian-compatible) plus a short
   index note per topic cluster. Agree one stable location with the user and
   don't move it — retrieval depends on it.
   Quality check: pick three random notes. Each standalone? Title a claim?
   Links to at least one neighbor?

## Move 4 — GOALS: fire capped goal runs

Spend unattended hours on the highest-value locked-up backlog, safely.

1. With the user, pick 2–3 backlog items with the most locked-up value.
   Gnarly migrations, test coverage, the architecture decision they keep circling.
2. Route execution to an existing loop mechanism (`loopkit` skill, cron-scheduled
   runs, or a tracked goal) rather than inventing loop mechanics here.
3. Every goal gets two non-negotiable safety properties:
   - **Pasted proof in the finish line.** The judge can't run tests or open
     files: the finish condition demands the green run pasted, never promised.
   - **A hard cap.** Turns or wall-clock, written into the condition itself.
4. Mind the meter: confirm the user accepts the burn before firing multiple goals.

Example shape: "every module in this repo has a test file, the full test suite
passes with the complete green run pasted in the report, and migration-notes.md
documents every change. Or stop after 25 turns and paste the failures."

## Move 5 — RECORDER: install the extract-approach habit

The compounding move — install first when time is short, so remaining time
converts automatically into assets.

1. Install the learning law in `AGENTS.md`:
   > After every non-trivial solved problem, write a learnings note before
   > moving on. A solution without its learnings note is unfinished work.
2. Notes land in one stable `learnings/` folder (workspace or repo), atomized
   and linked, using the learnings-note template.
3. **Non-trivial** means: more than one plausible approach existed, the first
   attempt failed, or the solve took real diagnosis. Routine edits get no note.
4. Capture outcomes and next-time procedure — what the problem actually was once
   understood, what to try first next time, the checkable reusable rule — not a
   replay of internal reasoning.

## Prompt sources

Move prompts are distilled from Machina's "Do this on your last day with Fable";
the wording here is adapted for Hatch and for reuse beyond any single model
deadline. The RECORDER prompt is the learning-law block above; the AUDIT and
GOALS prompts follow the move workflows verbatim.
