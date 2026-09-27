---
name: matt-pocock-knowledge-work
description: "Use when the user says 'Matt' or 'ask Matt', names a Matt Pocock method (grill me, grill with docs, to-spec, to-tickets, implement, tdd, code review, wayfinder, triage, diagnosing bugs, domain modeling, teach, wizard, retro, wait-what, loop me, handoff), or asks which method fits their situation (what should I use, which skill). It routes over 38 method briefs in subagents/: the idea-to-ship flow, on-ramps, writing and teaching methods, and standalone utilities. User-invoked only; never auto-dispatch."
---

# Matt Pocock knowledge work

Router over 38 method briefs in `subagents/`. Triggers and routing only; each brief carries its own procedure.

## Invocation

- This skill is user-invoked only. Never auto-dispatch or self-trigger on task content.
- Each brief states its own `Invocation` line (`user-invoked only` or `model or user`). For `user-invoked only` briefs, dispatch only on an explicit user request for that method.

## Decision map

Read the named brief from `subagents/` and execute it.

- **Which method fits:** `ask-matt.md`.
- **Main flow:** `grill-with-docs.md` (or `grill-me.md` for a plan or decision without docs; both run the `grilling.md` interview primitive) → optional `prototype.md` detour via `handoff.md` → `to-spec.md` → `to-tickets.md` → `implement.md` (or `implement-spec.md`) with `tdd.md` inside → `code-review.md`.
- **On-ramps:** `triage.md` (issues and external PRs), `diagnosing-bugs.md` (broken, throwing, slow), `wayfinder.md` (work bigger than one session).
- **Codebase health and vocabulary:** `improve-codebase-architecture.md` (scan then grill), `domain-modeling.md` (terms, CONTEXT.md, ADRs), `codebase-design.md` (deep modules, seams).
- **Writing:** `writing-fragments.md` (mine raw material) → `writing-beats.md` or `writing-shape.md`; `writing-for-agents.md` for agent-facing docs.
- **Teaching:** `teach.md`.
- **Standalone:** `research.md`, `to-questionnaire.md`, `wait-what.md`, `retro.md`, `wizard.md`, `handoff.md`, `claude-handoff.md`, `loop-me.md`, `resolving-merge-conflicts.md`, `pr.md`, `migrate-to-shoehorn.md`, `scaffold-exercises.md`, `git-guardrails-claude-code.md`, `setup-matt-pocock-skills.md`, `setup-ts-deep-modules.md`, `setup-pre-commit.md`.

## Phase boundaries

At a phase boundary (grilling done, spec done, implementation done), work this tree top to bottom. First yes wins.

1. **Continue:** the next phase needs this one as a primary source, or ~150k tokens of smart zone remain. Default for grill to implement.
2. **`/clear`:** everything in this session is disposable.
3. **`/handoff`:** the work travels (new harness, new directory, a colleague, a mid-phase fork). Use `handoff.md` or `claude-handoff.md`.
4. **Subagent:** the next phase is tightly scoped and AFK-safe.
5. **`/compact`:** with an instruction naming the next phase, so the summary keeps what it needs.

Keep main-flow steps 1 to 3 (grill, prototype, spec) in one unbroken context window.

## Dispatch

- Read the named brief from `subagents/` and execute it directly. For long work, spawn a subagent with the brief content as its instructions.
- Eleven briefs carry a **Knowledge-work port** addendum; when the task is not code, prefer the port over the code default: `code-review.md`, `codebase-design.md`, `diagnosing-bugs.md`, `implement-spec.md`, `implement.md`, `improve-codebase-architecture.md`, `pr.md`, `prototype.md`, `resolving-merge-conflicts.md`, `setup-ts-deep-modules.md`, `tdd.md`.

## Attribution

Adapted from Matt Pocock's skill collection. See NOTICE.md at the skill root.
