---
name: outcome-engine
description: "Turn a fuzzy idea into a verified result: clarify with a decision grill, write an outcome brief, slice it into verifiable work packages, and execute with check-change-verify evidence. Use when the user asks to run Outcome Engine, take an idea from start to finish, write a brief from settled context, break an approved brief into slices, execute a slice with proof, resume a multi-phase workflow, or review a system's structure. Not for a standalone grill me, interview me, or pressure-test this decision request; that belongs to strategy-room."
---

# Outcome Engine

Coordinate the path from unclear idea to verified result across research, writing, operations, creative work, planning, and software. Adapted from the Outcome Engine plugin (MIT, Israelmusondaayliffe/plugins).

A phase is finished only when its artifact exists and its check has been run fresh. A brief is not the outcome, and a slice plan is not delivered work.

## Start here

1. **Inspect what already exists.** Open the supplied brief, plan, slice file, proof records, and source data. Note which are approved (the user says so, or the file records it).
2. **Pick the resume point from that state** (table below) and say it in one line. Do not restart earlier phases whose artifacts already exist and are approved.
3. **Read that phase's reference** and produce its artifact.
4. **Run the phase check** (validator or acceptance check) and read the full result.
5. **Report the proof and name the next unblocked step.** Continue only if the request authorized it.

A clear request authorizes the phases it names. "Slice and execute the first slice" means write the slices, validate them, show the breakdown, and execute S1 in the same run, without waiting for a separate approval. The granularity check in `references/to-action-slices.md` gates external tickets and assignment to other people, not a local plan the user asked you to execute. A destination named in the request is the approved output root.

| Observable state | Resume point | Reference |
|---|---|---|
| Idea is unclear or tradeoffs block the brief, inside an Outcome Engine run | Decision grill | `references/decision-grill.md` |
| Mixed intake; the next mode is not clear from the files | Intake triage, then one route | `references/intake-triage.md` |
| One high-risk assumption should be tested before a full brief or build | Bounded test | `references/bounded-test.md`, then `references/evidence-driven-delivery.md` |
| Decisions settled, no brief yet | Outcome brief | `references/to-outcome-brief.md` |
| Approved brief, no valid slices | Action slices | `references/to-action-slices.md` |
| Valid slices exist | First unblocked slice | `references/evidence-driven-delivery.md` |
| Proof exists | Check it is fresh and covers the acceptance checks | `references/evidence-driven-delivery.md` |
| Repeated structural friction, or an upkeep review | System review | `references/improve-system-architecture.md` |

A standalone "grill me" or "pressure-test this decision" with no Outcome Engine run or execution goal belongs to the `strategy-room` skill; do not start one here. For near matches, read `references/routing-examples.md`. When two routes remain plausible after inspecting the sources, ask one focused question; otherwise state the chosen route and proceed.

## Full flow

For "take this from fuzzy concept to verified execution":

1. Clarify with `references/decision-grill.md` until material branches are resolved or explicitly deferred.
2. Write the brief with `references/to-outcome-brief.md` and validate it.
3. Break it down with `references/to-action-slices.md` and validate the plan (required fields, unique IDs, unknown blockers, dependency cycles).
4. Execute one unblocked slice at a time with `references/evidence-driven-delivery.md`, reporting fresh proof before the next slice.
5. Use `references/improve-system-architecture.md` when repeated friction points to a structural problem.

Validators, with `SKILL=~/workspace/skills/outcome-engine` (or this skill's actual folder). This self-check runs from any directory and writes nothing:

```bash
python3 "$SKILL/scripts/validate_action_slices.py" "$SKILL/assets/action-slices-template.json"
```

For your own files: `python3 "$SKILL/scripts/validate_outcome_brief.py" BRIEF.md` and `python3 "$SKILL/scripts/validate_action_slices.py" SLICES.json`.

## Worked example (illustrative, synthetic)

Request: "Run Outcome Engine on the approved brief: merge the two newsletter signup exports into one mailing list. Slice it, validate, and execute the first slice only, with proof."

- Resume point: the brief is approved, so start at action slices. No grill, no new brief.
- Slices: S1 merged list plus exceptions; S2 per-interest counts, `blocked_by: ["S1"]`, because counts must come from the merged list. Validator passes.
- S1 check first: count addresses that match after trimming and lowercasing across both files, and rows whose consent column is empty. That is the domain judgment. `Sam@Example.org ` and `sam@example.org` are one subscriber, and a row without consent goes to an exceptions file for follow-up, not onto the list and not silently deleted.
- Change: a short standard-library script writes `merged-list.csv` and `exceptions.csv` beside the exports, never over them.
- Verify: rerun the same counts on the output. There are zero duplicate addresses, every exception row appears exactly once, and merged + exceptions + dropped duplicates equals the input row total.
- Report: the proof, and "Next unblocked slice: S2 (not run; only S1 was authorized)."

A wrong version would re-interview the user about an approved brief, execute S2 too, overwrite an export, dedupe on exact strings only, or report "done" without rerunning the counts.

## When something goes wrong

| Symptom | Likely cause | Next move | Stop when |
|---|---|---|---|
| `validate_outcome_brief.py` reports an unresolved placeholder | Template text left in | Replace it with the real value or write `None` | the value needs user input; ask for that one value |
| `validate_action_slices.py` reports a cycle or unknown blocker | Slices depend on each other both ways, or a typo in an ID | Merge or reorder the slices, then rerun | second failure; show the validator output |
| The acceptance check already passes before any change | The check does not observe the new work | Tighten the check so it fails on the current state | a failing check cannot be defined; report the slice as unprovable |
| The check still fails after the change | Wrong change or wrong expected value | Diagnose once from the full output; fix and rerun | the second failure has an unknown cause; stop and report |
| The slice needs data, credentials, or a decision the user holds | Personal input | Finish the independent parts; ask for the specific item | always; never invent it |
| A step needs a live browser | Rendered or logged-in state | Run it as the host's live-browser task with the user's confirmation, or mark the check `unchecked: needs live browser` | the browser task is unavailable |

## Handoff gates

- Do not synthesize a final brief while consequential decisions remain hidden.
- Do not create action slices from an unapproved or invalid brief.
- Do not execute a slice without an observable acceptance check and a named proof surface.
- Do not mark the plan complete until every required slice has fresh proof.
- Do not execute more than one fresh-context-sized slice unless the user explicitly authorizes the next slice.
- Do not publish, send, assign, purchase, delete, or change external state without task-specific authorization for that action.

## Durable handoff

When work must survive across sessions or be delegated (for example a slice handed to a subagent), write a self-contained handoff artifact using `assets/handoff-template.md`. The `continuity-vault` skill is an optional companion: if it is installed (`~/workspace/skills/continuity-vault/SKILL.md` exists), it owns the durable cross-task handoff. When it is absent, write the handoff inside the approved output root; if none was named or approved, ask for one first. The handoff must not rely on conversation history.

## Completion

- **Phase done:** the artifact exists, its validator or acceptance check was run in this phase, and the result is shown.
- **Slice done:** the acceptance check failed before the change and passes after it, run through the real interface, with any untested risk named.
- **Plan done:** every required slice has fresh proof. One passing slice does not complete the plan.
- **Blocked:** name the blocker, its owner, and the evidence or decision that clears it. Deliver the parts that do not depend on it.

## Operating rules

- Ask the user when the work needs personal input: goals, preferences, names, business details, credentials, or any value you cannot source. Do not invent these.
- Inspect available files, memory, and connected sources before asking the user to restate discoverable facts.
- Never overwrite source inputs; write outputs beside them or in the output root.
- Parallelize independent slices by delegating them to subagents; sequential or dependent work stays in this context.
- Keep the skill focused: use the references for phase detail and the templates and validators for artifacts.
