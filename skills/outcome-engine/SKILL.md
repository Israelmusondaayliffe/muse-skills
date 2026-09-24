---
name: outcome-engine
description: "Turn a fuzzy idea into a verified result: clarify with a decision grill, write an outcome brief, slice it into verifiable work packages, and execute with check-change-verify evidence. Use when the user asks to run Outcome Engine, take an idea from start to finish, grill a decision, write a brief, break work into slices, prove execution, or review a system's structure."
---

# Outcome Engine

Coordinate the path from unclear idea to verified result across research, writing, operations, creative work, planning, and software. Adapted from the Outcome Engine plugin (MIT, Israelmusondaayliffe/plugins).

## Router

Route the request to the smallest useful phase. Chain phases only when the user asks for a larger outcome or the current phase clearly requires the next one.

- Unclear idea, unresolved tradeoffs, or a pressure test: read `references/decision-grill.md`.
- Mixed or ambiguous intake whose next mode is unclear: read `references/intake-triage.md`, then choose exactly one primary route.
- High-risk assumption that should be tested before a full brief or build: read `references/bounded-test.md`, define the decision rule, then run the test only through `references/evidence-driven-delivery.md`.
- Settled context that needs a durable brief: read `references/to-outcome-brief.md`.
- Approved brief or plan that needs tasks, tickets, or work packages: read `references/to-action-slices.md`.
- Approved slice that needs execution and proof: read `references/evidence-driven-delivery.md`.
- Repeated structural friction or an upkeep review: read `references/improve-system-architecture.md`.
- End-to-end request ("take this from fuzzy concept to verified execution"): run the full flow below.

When the request is a near match for several routes, read `references/routing-examples.md` before deciding. When two routes remain plausible after source inspection, ask one focused question; otherwise state the chosen route and proceed.

## Full flow

1. Clarify with `references/decision-grill.md` until material branches are resolved or explicitly deferred.
2. Synthesize the result with `references/to-outcome-brief.md`. Write the brief at a user-approved path (for example under `~/workspace/goals/<goal-slug>/files/` or a user-named directory) and validate it: `python3 scripts/validate_outcome_brief.py <path>`.
3. Break the approved brief down with `references/to-action-slices.md` and validate the plan: `python3 scripts/validate_action_slices.py <path>` (checks required fields, unique IDs, unknown blockers, and dependency cycles).
4. Execute one unblocked slice at a time with `references/evidence-driven-delivery.md`, reporting fresh proof before moving to the next slice.
5. Use `references/improve-system-architecture.md` when repeated friction points to a structural problem rather than a one-time task.

Run the validator scripts from this skill's directory (`~/workspace/skills/outcome-engine/`) so the relative `scripts/` paths resolve.

## Handoff gates

Do not move to the next phase until its gate passes:

- Do not synthesize a final brief while consequential decisions remain hidden.
- Do not create action slices from an unapproved or invalid brief.
- Do not execute a slice without an observable acceptance check and a named proof surface.
- Do not mark the plan complete until every required slice has fresh proof.
- Do not execute more than one fresh-context-sized slice unless the user explicitly authorizes the next slice.
- Do not publish, send, assign, purchase, delete, or change external state without task-specific authorization for that action.

## Durable handoff

When work must survive across sessions or be delegated (for example a slice handed to a subagent), write a self-contained handoff artifact using `assets/handoff-template.md`. Keep `continuity_vault` in mind: if it is installed, route the durable handoff through it. Otherwise write the handoff inside the user-approved output root; if no output root has been approved, ask for one first. The handoff must not rely on conversation history.

## Resume logic

Inspect the artifacts already present before restarting the flow. If the user has an approved brief, begin with action slices. If valid slices exist, begin with the first unblocked slice. If proof exists, verify it is fresh and covers the stated acceptance checks. Restate the chosen resume point and its evidence before proceeding.

## Completion checkpoints

Before claiming completion of any phase, run the phase's completion contract as a checklist:

- Grill: all material branches are resolved, discoverable, out of scope, or deferred with an owner.
- Brief: outcome, audience, success evidence, constraints, decisions, blockers, scope limits, and one next action are all present; no unresolved placeholders.
- Slices: every slice is independently demonstrable from brief plus slice alone; the plan passes the validator.
- Delivery: each acceptance check was run fresh through the real interface in the same phase where completion is claimed; untested risk is named.
- Review: every recommendation is backed by observed friction, with evidence and risk stated.

## Operating rules

- Ask the user when the work needs personal input: goals, preferences, names, business details, credentials, or any value you cannot source. Do not invent these.
- Inspect available files, memory, and connected sources before asking the user to restate discoverable facts.
- Keep results fresh: rerun the proving check in the same phase where completion is claimed.
- Parallelize independent slices by delegating them to subagents; sequential or dependent work stays in this context.
- For browser-visible behavior, delegate the check through the live-browser task (the skill itself does not open a browser).
- Keep the skill focused: use the references for phase detail and the templates and validators for artifacts. Do not re-explain a phase's whole method in chat.
