---
name: strategy-room
description: Pressure-test a consequential decision before resources are committed. Use when the user says "grill me", "interview me relentlessly", "pressure-test this", "challenge my assumptions", "what am I missing", "stress test this", "tear this apart", "walk the decision tree", or needs help choosing a path, mapping a large uncertain effort, generating distinct options, ranking rough ideas, matching a job to a candidate, productizing proven work, or producing an evidence-linked recommendation. Routes the work to exactly one decision operation, keeps facts separate from judgment, and ends at a decision record with a named handoff. Never executes.
---

# Strategy Room

Pre-commitment decision work only. Everything here ends with a decision record and a named handoff, never with execution.

## Purpose

Turn vague plans into shared, decision-ready specifications; map large uncertain efforts to their next blocking decision; challenge assumptions against current evidence; generate meaningfully distinct options; rank rough ideas against visible criteria; match bounded work to the right person, tool, or service; assess whether proven work deserves a reusable form; and converge on one evidence-linked recommendation. Track load-bearing assumptions so uncertainty stays visible after the decision.

## Workflow

1. **Establish the decision frame.** State in a few lines: the decision (or ask the user to name it), the decision owner, the deadline, the stakes and reversibility, evidence already available, and what commitment would follow. If there is no real decision, return the missing decision statement instead of running a generic brainstorm.
2. **Pick exactly one route** from the routing table below. See `references/routes.md` for the full trigger conditions and each route's procedure.
3. **Run the route.** Most routes run inline in the current conversation. The challenge route runs as a staged pipeline; spawn subagents with the phase briefs in `references/challenge-pipeline.md` (or run it inline at light effort).
4. **Validate structured artifacts** with the bundled scripts (see `bin/` section).
5. **Deliver the decision record and name the next owner.** Then stop. A recommendation does not authorize execution.

## Routing table

| Signal | Route | Reference |
|---|---|---|
| The brief is vague, incomplete, or held in the user's head | `interview` — source-first interview | `references/grill-me.md` |
| The destination is meaningful but the route is obscured by several dependent decisions | `wayfind` — decision map, one blocking edge | `references/routes.md` |
| Hidden beliefs or external facts could reverse the choice | `challenge` — research-first adversarial review | `references/challenge-pipeline.md` |
| The option set is narrow or repetitive | `explore` — distinct option generation | `references/routes.md` |
| Options and evidence are ready for a recommendation | `synthesize` — one evidence-linked recommendation | `references/routes.md` |
| Uncertainty must stay visible after the decision | `register` — durable assumption register | `references/routes.md` |
| Messy ideas, questions, or opportunities need a ranked focus | `prioritize` — criteria, viability floor, cheap first test | `references/routes.md` |
| The decision is who or what should do a bounded job | `match` — candidate comparison and handoff brief | `references/routes.md` |
| Existing proven or promising work may deserve a reusable form | `productize` — form choice and cheapest next validation | `references/routes.md` |

If the user asks for execution (building, publishing, contacting, buying, installing, sending), finish the decision phase first, then either hand off to the `outcome-engine` skill under separate explicit authorization, or emit the self-contained execution handoff described below and stop.

## Output contract

- **Decision-only boundary.** Every route ends at a decision record and a named handoff. The routing record enforces it: `execution_authorized` must be `false`.
- **Facts, assumptions, and judgment stay visibly separate.** Cite or qualify every material factual claim. Never convert an opinion into a supported assumption without evidence.
- **One blocking decision per context** on the wayfind route. Wayfinding does not become a generic project plan.
- **Recommend, don't force.** The synthesizer and prioritizer may end with "no option clears the bar" or "no candidate qualifies" — that is a valid outcome, not a failure.

## File output

Ask the user to approve a destination before writing. A sensible default is `~/workspace/your_files/strategy-room/`; for goal-related decisions, that goal's `files/` directory. Suggested files:

- `decision-map.md` — from `assets/decision-map-template.md` (wayfind route; keeps durable decision state)
- `execution-handoff.md` — the accepted decision, rationale, assumptions, evidence, risks, conditions, acceptance checks, next actions, and owner. Self-contained: another authorized task can pick it up without this conversation.
- `decision-record.json`, `assumption-register.json` — structured artifacts validated with `bin/validate_record.py` (optional; keep the human-readable record as primary)

If no destination is authorized, keep the complete record in the current task until one is approved. Do not substitute conversation history for a durable file.

## Tooling: `bin/`

- `bin/validate_record.py ARTIFACT.json SCHEMA.json` — validates a JSON artifact against one of `assets/route-schema.json`, `assets/decision-record-schema.json`, or `assets/assumption-register-schema.json`. Prints `{"valid": ...}` and exits non-zero on failure.
- `bin/check_option_count.py FILE [MINIMUM]` — counts numbered/bulleted options in a file; the explore route uses it to enforce breadth (default minimum 10).
- `bin/dossier_check.py DOSSIER.md --effort {light,standard,deep} --pace {fast,standard,slow}` — deterministic gate between research and challenge in the challenge pipeline. Do not proceed past research until it passes.

## Companion workspace skills

These are optional and never block owned work:

- `knowledge-work-superpowers` — deeper evidence-led research when the challenge route's own research is insufficient
- `outcome-engine` — execution after an accepted decision (separate explicit authorization required)
- `proofloop` — extended verification of a consequential decision
- `writing-quality` — final prose review of user-facing reports
- `continuity-vault` — cross-task continuity for multi-session wayfinding

If a companion is needed, check `~/workspace/skills/` for availability. Missing companions never block the decision work; use the local handoff instead.

## Operating rules

1. Pick one route and stick to it. Do not blend interview, challenge, and synthesis into one pass.
2. Investigate before asking: check workspace files, project documents, and authorized connected sources for facts the user should not have to retrieve. Never replace a user-owned decision with research — evidence narrows a choice, it does not decide values.
3. Match depth to stakes, reversibility, and cost. Exhaust material ambiguity, not trivia.
4. Keep read-only by default. No external changes, messages, purchases, or plan execution without separate authority.
5. Report honestly when the analysis finds the user's input is well-grounded. Do not manufacture concerns to justify the work.
6. Surface uncertainty instead of hiding it: register load-bearing assumptions, mark what is untested, and name what evidence would change the recommendation.
