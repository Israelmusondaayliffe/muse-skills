---
name: "matt-partok-bundled-plugin-for-knowledge-work"
description: "Run Matt Pocock's idea-to-ship knowledge-work flow (grilling, domain modeling, bounded research or prototype, spec, tickets, TDD slices, review, handoff, teaching). Explicit-only: use only when the user selects it by name, for example Matt, Matt Pocock, Matt's flow, the Matt Partok bundle, or a Matt-prefixed step such as Matt grill, Matt to spec, Matt to tickets, Matt TDD, Matt code review, Matt triage, Matt wayfinder, or Matt teach. Not for generic grill me, interview me, or pressure-test this decision requests (use strategy-room), nor for ordinary specs, tickets, research, reviews, or bug fixes that do not name Matt."
---

# Knowledge-Work Flow (Matt Pocock bundle, adapted)

An end-to-end discipline for coding and knowledge work: clarify the idea, record
decisions, research or prototype what talk cannot settle, specify, slice into
bounded execution units, execute, hand off across sessions, and review against
evidence. Adapted from the public
`matt-partok-bundled-plugin-for-knowledge-work` Codex bundle for a Linux
terminal assistant with file tools, web search, subagents, cron/hooks, and
connected services. No Codex/Claude Code manifests, hooks, or slash commands —
the "hook" moments below are checklists and procedures instead.

Trigger this skill only when the user selects it by name ("use Matt's flow",
"Matt grill me", "Matt wayfinder", "Matt to spec / tickets", "run Matt TDD /
code review / triage", "teach me via Matt teach"). A generic "grill me",
"interview me", or "pressure-test this decision" without Matt belongs to the
`strategy-room` skill; ordinary research, planning, specs, and review stay out
of this skill too. Once the user has selected Matt, run the requested step
here to completion; do not hand it back to another skill.

## Start here

1. **Confirm the explicit selection and the step.** Name the Matt step the
   user asked for (for example To tickets, Triage, TDD, Teach). If they asked
   for "Matt's flow" with no step, start at the Main flow below.
2. **Read the live state** that step needs: the spec, ticket files, or issue;
   `CONTEXT.md` and `docs/adr/` when they exist; the repo's test command.
   Missing domain docs are fine; proceed without them.
3. **Use the configured tracker, or local Markdown by default**
   (`references/issue-tracker-setup.md`). Setup is for a project about to run
   the full flow; a single named step does not wait for it.
4. **Run only that step's section** below, to its stated output. When a spec
   or decision is already approved, do not re-grill it.
5. **Report the artifact, the check you ran, and the next step** in the flow,
   without starting that step unless asked.

A named step with its inputs authorizes that step. A step that says "quiz the
user" or "wait for direction" pauses once; if the user already pre-approved
the result in the request, show it and continue.

## Main flow

1. **Settle decisions** — [Grilling](#grilling) one question at a time. With a
   durable workspace, also [domain-model](#domain-modeling) as you go.
2. **Resolve unknowns** — [bounded research](#research) for facts that need
   primary sources; a [prototype](#prototype) for questions that need a
   concrete artifact. Nothing else.
3. **Branch on size:**
   - One bounded session with an agreed acceptance surface → go straight to
     [Implement](#implement). No spec or tickets as ceremony.
   - Multi-session or a durable contract → [To spec](#to-spec), then
     [To tickets](#to-tickets) when there is more than one execution slice.
   - Large, foggy effort → [Wayfinder](#wayfinder) first, then rejoin at To spec.
4. **Execute one slice at a time** ([Implement](#implement)), one session per
   slice with a durable brief.
5. **[Handoff](#handoff)** before changing sessions or delegating a slice.
6. **Close** coding work with [Code review](#code-review); close knowledge work
   against its evidence and the originating brief.

**Handoff gates (never violate):**
- Do not turn unresolved consequential decisions into hidden assumptions.
- Do not execute from an unapproved spec or an invalid slice.
- Do not publish, send, assign, commit, purchase, delete, or change external
  state unless the task authorizes it.
- Do not call work complete without fresh evidence against the original brief.

## Setup

Before a project runs the full flow, configure the workspace (Setup procedure):
1. Discover: work tracker (default: local Markdown), durable paths for
   context/glossary/decisions/specs/evidence/handoffs, verification surfaces
   (test/build/lint commands, renderers, review gates), permission-gated
   external actions.
2. Recommend the project's existing conventions. When none exist, recommend
   local Markdown tracking and one durable context file before any external
   tracker.
3. Confirm the exact proposed changes with the user before editing project
   contract files. Record the smallest workable config: where specs/tickets
   live, how blocking edges are represented, where terms and decisions live,
   where handoffs and evidence live, which checks prove a slice complete.
   See `references/issue-tracker-setup.md` for the local-Markdown conventions
   and triage label mapping. Never invent user data — ask.

## Grilling

The interview primitive. Ask **one question at a time**, wait for the answer
before continuing. Never batch questions.

- If a **fact** can be found (filesystem, tools, web), look it up; never ask.
  **Decisions** belong to the user — put each one to them and wait.
- For each question, give your recommended answer.
- Walk each branch of the decision tree, resolving dependencies one by one.
- Do not act until the user confirms a shared understanding.

With a durable workspace (grill-with-docs mode): run domain modeling
concurrently — challenge fuzzy terms, update `CONTEXT.md` inline as terms
resolve, offer ADRs only when all three hold (hard to reverse, surprising
without context, a real trade-off was made). See
`references/context-format.md` and `references/adr-format.md`.

## Domain modeling

The active discipline of building the project's shared language while you
design — not just reading it.

- **Challenge against the glossary:** when the user's term conflicts with
  `CONTEXT.md`, call it out immediately and pick one.
- **Sharpen fuzzy language:** propose a precise canonical term when a word is
  vague or overloaded.
- **Stress-test with concrete scenarios:** invent edge cases that force
  precision about boundaries between concepts.
- **Cross-reference with code:** when the code contradicts what the user says,
  surface it.
- **Update `CONTEXT.md` inline** the moment a term resolves (format in
  `references/context-format.md`). Never implementation details — glossary only.
- **Offer ADRs sparingly** per the three-part test (format in
  `references/adr-format.md`).

## Research

One bounded, decision-blocking question per run. Use official docs, specs,
source code, first-party datasets, and other primary sources first.

1. State the question, the decision it informs, and the stop condition.
2. Inspect local sources before public web search.
3. Trace each material claim to the source that owns it.
4. Separate sourced fact, inference, uncertainty, and recommendation.
5. Save findings to the user-approved durable location, citing each material
   claim near the statement it supports.
6. Return the answer, unresolved uncertainty, the artifact path, and the next
   decision now unblocked.

## Prototype

A prototype answers **one question**. Keep the answer; discard or isolate the
artifact. Rules: write the question and success signal before building; mark
the artifact temporary and keep it out of production paths unless the user
approves promotion; provide one simple way to inspect or run it; skip polish
and unrelated edge cases; record the verdict and remaining uncertainty in the
durable decision artifact.

- **Logic/state question** → smallest runnable terminal interaction; isolate
  the logic in a portable pure module (reducer, state machine, or pure
  functions) the throwaway UI calls into.
- **UI question** → 3 meaningfully different variants (cap 5) on one
  inspectable surface, switchable via a `?variant=` param; prefer embedding in
  an existing page over a new route.
- **Knowledge-work question** → lowest-cost artifact that produces feedback:
  source sample, outline, draft fragment, worked example, small analysis.

Details in `references/prototype-modes.md`.

## To spec

Synthesize what is already known — do not restart the interview. If
consequential decisions are unresolved, list them as blockers, never as
hidden assumptions.

1. Read the conversation, project instructions, terminology, decisions,
   prototypes, and research artifacts.
2. Name the observable outcome and its real verification surface.
3. Software: affected modules, interfaces, seams, behavior, migration needs,
   operational risks, testing decisions — no brittle file-by-file prescriptions.
4. Knowledge work: audience, decision or use case, evidence requirements,
   deliverable shape, review criteria, delivery constraints.
5. Write the spec to the configured tracker or user-approved durable path
   (local Markdown default, `.scratch/<feature>/spec.md`). Publish externally
   only with authorization, then verify.

Template sections: Problem or opportunity · Desired outcome (observably true)
· Users and uses · Scope and requirements (numbered, independently checkable)
· Decisions already made · Verification plan · Out of scope · Open blockers.

## To tickets

Break an approved spec into **tracer-bullet tickets**: each a narrow but
complete vertical slice that yields one observable, demoable result, with
explicit blocking edges.

1. Work from the conversation/spec; explore the codebase first so titles use
   the domain glossary and respect ADRs. Look for prefactoring that makes the
   change easy first ("make the change easy, then make the easy change").
2. Draft slices: each crosses everything needed for one result (schema→API→UI→
   tests, or source→analysis→draft→verification), sized for one fresh session.
   A **wide refactor** (mechanical change with codebase-wide blast radius) is
   the exception — sequence it expand → migrate in batches → contract instead
   of forcing it into tracer bullets.
3. **Quiz the user:** present the numbered list (title, blocked-by, what it
   delivers) and iterate on granularity, edges, and merges/splits until approved.
4. **Publish** to the configured tracker — local default: one file per ticket
   under `.scratch/<feature>/issues/<NN>-<slug>.md` in dependency order
   (blockers first); external trackers only with authorization. Verify every
   item and edge. Work the frontier (all blockers done) one ticket at a time
   with Implement, clearing session state between tickets.

Ticket template: title · what to build (end-to-end behavior, user's
perspective, not implementation steps) · blocked by · acceptance criteria
(checkable). Never file paths or code snippets, unless a prototype produced a
decision-rich snippet that prose cannot capture.

## Implement

Execute one approved, unblocked slice.

1. Restate the slice, blockers, allowed paths, and acceptance checks.
2. Re-read live state — never trust a stale handoff.
3. Make the smallest complete change that produces the observable result.
4. Run the narrowest useful check after each meaningful change; repair
   failures before adding scope.
5. Software: use the TDD loop at agreed seams; knowledge work: preserve source
   and claim evidence, verify the artifact on its real surface, review against
   the originating brief.
6. Run final checks against the spec; return evidence, remaining risks, and
   the next unblocked slice.

Never commit, publish, send, assign, or close tracker items without explicit
authorization — then verify.

## Handoff

When changing sessions or delegating a slice, write a durable handoff to the
user-approved location (not a volatile temp dir). Reference artifacts by path
or URL instead of duplicating them. Include: next objective and active slice;
exact first action for the receiver; canonical artifact paths/URLs; decisions
and assumptions not recorded elsewhere; blockers, approval boundaries, and
forbidden actions; current state; commands/checks already run with results;
latest proof and remaining untested risks; which flow phase comes next.
Redact secrets, credentials, and private personal data.

## Triage

Move incoming issues/requests through a small state machine. Reading and
recommending are safe; posting comments, changing labels, assigning, or
closing needs task-specific authorization and post-action verification.
External AI-generated comments must start with `> *This was generated by AI
during triage.*`

Roles — categories: `bug`, `enhancement`; states: `needs-triage`,
`needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. Every item
carries exactly one of each; an unlabeled item goes to `needs-triage` first.

1. **Show what needs attention:** unlabeled first, then `needs-triage`, then
   `needs-info` with reporter activity since last notes — oldest first, one
   line each. Let the maintainer pick.
2. **Gather context:** read the full item (body, comments, labels, dates);
   check codebase for **redundancy** (already implemented → wontfix, do not
   write to `.out-of-scope/`) and **prior rejection** in `.out-of-scope/*.md`
   (format in `references/out-of-scope-kb.md`).
3. **Recommend** category/state with reasoning; wait for direction.
4. **Verify the claim** before grilling: reproduce a bug from the reporter's
   steps; confirm a claim holds. Confirmed verification makes a much stronger
   brief.
5. **Grill if needed** (Grilling + Domain modeling) to flesh the request out.
6. **Apply:** `ready-for-agent` → post an agent brief (durable, behavioral,
   interface-level, with complete acceptance criteria and explicit scope
   boundaries — see `references/agent-brief.md`); `ready-for-human` → same
   structure plus why it can't be delegated; `needs-info` → post specific,
   actionable questions (never "please provide more info"); `wontfix` → for a
   rejected enhancement, record it in `.out-of-scope/` then close.

## Wayfinder

For efforts too large and foggy to specify in one session. Plan the route as
a **shared map** of decision tickets — questions whose resolution is a
*decision*, not build slices — then resolve one frontier ticket per fresh
session. Default: local Markdown map; a real issue tracker only when already
configured and authorized. See `references/issue-tracker-setup.md` for map
and ticket conventions.

- **Plan, don't do:** tickets resolve decisions; the map is done when nothing
  is left to decide before someone executes. The pull to just do the work is
  the signal you've reached the map's edge.
- **Name the destination first** (a spec, a locked decision, a change in
  place) — it fixes the scope.
- **Refer by name**, never bare ids, in everything the human reads.
- **Fog of war:** the map is deliberately incomplete. Sharp questions become
  tickets; dim views stay in **Not yet specified** until they graduate. Beyond
  the destination is **Out of scope** — closed, never graduates.
- Ticket types: `research` (AFK fact-finding), `prototype` (HITL artifact to
  react to), `grilling` (HITL conversation, the default), `task` (HITL or AFK
  — enabling work that must happen before a decision, e.g. provisioning access).
- Never resolve more than one ticket per session (research excepted). Claim a
  ticket in local state before any work so parallel sessions skip it.

## Coding track

### TDD

Red → green, one slice at a time. Test behavior through public interfaces,
never internals. **Agree the seams up front** — no test is written at an
unconfirmed seam. Each cycle: one seam, one failing test, the smallest code
to pass it; refactor only while green. Anti-patterns: implementation-coupled
tests, tautological assertions (expected values must come from an independent
source of truth), horizontal slicing (all tests first) — work in vertical
tracer bullets instead. Examples and mocking rules in
`references/tdd-details.md`.

### Code review

Review a diff from a fixed point on two independent axes — keep them
separate.

1. Pin the review surface: commit, branch, or merge base; ask one focused
   question if ambiguous. Verify the diff is non-empty.
2. Find sources: originating spec/issue/ticket for Spec Fidelity; `AGENTS.md`,
   standards, ADRs, test conventions for Code Standards. If a source is
   absent, say so and lower confidence — never fabricate a spec or standard.
3. Run both axes — parallel subagents when delegation is permitted, otherwise
   sequentially with separate notes. Standards: documented rules, test
   quality, naming, duplication, scattered change, error behavior (documented
   rules are hard requirements; general smell guidance is judgment). Fidelity:
   missing/partial requirements, unauthorized scope, incorrect behavior,
   acceptance criteria without proof — cite the exact spec section per finding.
4. Report each axis with severity, hunk, evidence, and the smallest corrective
   action; give each axis its own verdict (pass / pass with fixes / fail).
   Fix only the authorized findings, rerun checks, repeat both axes. Never
   commit or post review comments without authorization.

### Codebase design (deep modules)

Design **deep modules**: a lot of behavior behind a small interface, at a
clean seam, testable through that interface. Use the vocabulary in
`references/deep-module-design.md` exactly — module, interface, depth, seam,
adapter, payoff, locality — not "component/service/API/boundary". Principles:
depth is a property of the interface (depth-as-payoff, not lines); the
deletion test (if deleting it, does complexity vanish or reappear across
callers?); the interface is the test surface; one adapter means a hypothetical
seam, two means a real one. Deepening rules and the design-it-twice parallel
pattern are in the same reference.

### Architecture improvement

Scan a codebase for deepening opportunities; present candidates; grill through
the chosen one.

1. **Scope before you scan:** weight hot spots from `git log`, or take the
   user's named direction. Read `CONTEXT.md` and ADRs in the area first.
2. Present candidates in a self-contained **HTML report** (scaffold in
   `references/html-report.md`): before/after visuals, problem, solution,
   benefits in locality/payoff terms, recommendation strength badge
   (`Strong` / `Worth exploring` / `Speculative`), ending with a top
   recommendation. Verify the file; give the user its path or inspect it in
   the browser surface. Do not propose interfaces yet — ask which candidate to
   explore.
3. **Grilling loop** on the chosen candidate (Grilling + Domain modeling):
   keep `CONTEXT.md` current, offer ADRs only for load-bearing rejections,
   use design-it-twice for alternative interfaces.

### Diagnosing bugs

A six-phase discipline for hard bugs — skip phases only when explicitly
justified.

1. **Feedback loop:** the whole skill. Build one tight, red-capable command
   (failing test → curl/HTTP script → CLI invocation with fixture → headless
   browser → replayed trace → throwaway harness → fuzz loop → bisection
   harness → differential loop → HITL script last resort; template in
   `scripts/hitl-loop.template.sh`). Completion bar: it drives the actual bug
   path and asserts the user's exact symptom, is deterministic and fast
   (seconds), and you have already run it once. No red-capable command, no
   Phase 2.
2. **Reproduce + minimize:** confirm it's the user's failure mode, shrink to
   the smallest scenario that still goes red — every remaining element
   load-bearing.
3. **Hypothesize:** 3–5 ranked, falsifiable hypotheses ("If X is the cause,
   then changing Y will make it disappear"); show the user before testing.
4. **Instrument:** debugger/REPL first, then targeted logs tagged with a
   unique prefix (e.g. `[DEBUG-a4f2]`) — never "log everything and grep".
   Perf regressions: baseline measurement and bisection, not logs.
5. **Fix + regression test:** write the regression test before the fix, but
   only at a correct seam (if none exists, that absence is the finding —
   flag for architecture improvement).
6. **Cleanup + post-mortem:** repro gone, test green, debug logs removed,
   throwaways deleted, confirmed hypothesis recorded durably. Then ask what
   would have prevented it — if the answer is architectural, hand off to
   Architecture improvement.

### Resolving merge conflicts

On a repository already in a conflicted state: see current state and history;
trace each conflict's both sides to intent (commit messages, PRs, issues);
resolve each hunk preserving both intents where possible — where incompatible,
pick the one matching the merge's stated goal and note the trade-off; never
invent new behavior, never `--abort`; run the project's automated checks
(typecheck → tests → format) and fix what the merge broke; stage and continue
only if completing the operation is authorized, otherwise leave the resolved
tree ready for review and report the exact remaining commands. Never push
without separate authorization.

## Teaching workspace

A stateful, multi-session learning program. The workspace is a directory:

- `MISSION.md` — the reason (format in `references/teach-formats.md`)
- `reference/*.html` — compressed reference docs (cheat sheets, algorithms)
- `RESOURCES.md` — curated high-trust sources + communities (annotated)
- `learning-records/*.md` — `NNNN-slug.md`; non-obvious lessons and insights,
  ADR-style, used to compute the zone of proximal development
- `lessons/*.html` — `NNNN-slug.html`; one tightly-scoped, beautiful lesson
  per file, tied to the mission, each with one tangible win, a primary-source
  recommendation, and a reminder to ask follow-up questions
- `assets/*` — reusable components (start with a shared stylesheet); never
  inline what a future lesson could reuse
- `NOTES.md` — user preferences and working notes

Philosophy: build knowledge from trusted resources (never parametric guesses
alone), skills through interactive lessons with tight feedback loops
(retrieval practice, spacing, interleaving — desirable difficulty), wisdom via
high-reputation communities (respect an opt-out). Design for storage strength,
not fluency. Knowledge lessons minimize difficulty; skill lessons use
difficulty as the tool.

## Worked example (illustrative, synthetic)

Request: "Matt triage: issue 14 says CSV export drops the last row. Recommend
what to do with it."

- Step: Triage, read and recommend only. No labels change, and nothing is
  posted.
- Gather: read the issue and comments. Search the code for an existing fix and
  check `.out-of-scope/` for a prior rejection. Neither is found.
- Verify before grilling: reproduce with the reporter's steps on a 3-row
  file. The export has 2 rows, so the bug is confirmed. A 1-row file exports
  correctly, so the bug is narrower than reported, which matters for the
  brief.
- Recommend `bug` + `ready-for-agent`, with a draft agent brief. The brief
  covers the behavior (every data row exported), acceptance criteria for 0,
  1, 3, and 1,000-row files, and the boundary (the export format itself is
  unchanged). It stays a draft until the maintainer authorizes posting.

A wrong version would grill the reporter before trying to reproduce, change
labels without authorization, or write a brief that names files and line
numbers instead of behavior.

## When something goes wrong

| Symptom | Likely cause | Next move | Stop when |
|---|---|---|---|
| The user did not name Matt | Wrong skill | Say that generic interviews belong to `strategy-room` and other work to its own skill | always; do not run this bundle |
| The spec has unresolved consequential decisions | Grilling incomplete | List them as blockers in the output; grill only those, one question at a time | the user defers or decides each one |
| The test command or build fails before any change | Pre-existing breakage | Record the failing output as the baseline; do not fix it inside an unrelated slice | the slice depends on it; report it as a blocker |
| A bug does not reproduce | Missing steps or environment | Try the reporter's exact steps once more with the stated versions; move to `needs-info` with specific questions | the second attempt fails |
| A ticket cannot be demoed alone | Horizontal slice | Merge it into the vertical slice that uses it, or split along user-visible behavior | the maintainer accepts the new split |
| The step would write to a tracker, commit, or post | External state | Prepare the content locally; stop | the task explicitly authorizes that action |

## Completion

- **Step done:** the step's artifact exists where the tracker convention puts
  it, the step's check ran (tests, reproduction, validation of edges), and
  the next flow step is named.
- **Blocked:** the blocker, its owner, and what was completed without it.
  Unresolved decisions are listed as blockers, never as hidden assumptions.

## Attribution

Adapted from the public community bundle
`matt-partok-bundled-plugin-for-knowledge-work` (adapting Matt Pocock's skills
workflow) for use on this assistant. The Codex/Claude Code manifest, hook,
and agent formats from the original do not apply here and were translated
into terminal/browser/filesystem procedures. See `NOTICE.md` in the original
repo for upstream attribution and licensing terms.
