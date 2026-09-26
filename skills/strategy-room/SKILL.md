---
name: strategy-room
description: Pressure-test a consequential decision before resources are committed. Use when the user says "grill me", "interview me relentlessly", "pressure-test this", "challenge my assumptions", "what am I missing", "stress test this", "tear this apart", "walk the decision tree", or needs help choosing a path, mapping a large uncertain effort, generating distinct options, ranking rough ideas, matching a job to a candidate, productizing proven work, or producing an evidence-linked recommendation. This is the default owner of general decision interviews and pressure tests, including those phrases when no other skill is named. Routes the work to exactly one decision operation, keeps facts separate from judgment, and ends at a decision record with a named handoff. Never executes. Not for requests that explicitly name Matt or the Matt bundle (matt-partok-bundled-plugin-for-knowledge-work) or explicitly ask to run Outcome Engine end to end (outcome-engine).
---

# Strategy Room

Pre-commitment decision work. Every route ends at a decision record and a named handoff, never at execution. The work is finished when the user holds a decision record they can act on, or a clear statement of what decision is missing and who owns it.

## Start here

1. **Read what was supplied before asking anything.** Open every attached file and any workspace document the request points to. List what is already settled (budget, audience, constraints, answers the user gave). Settled items are not asked again.
2. **Write the decision frame** in a few lines: decision, owner, deadline, stakes and reversibility, evidence in hand, the commitment that would follow. If there is no real decision, return the missing decision statement and stop. Do not run a generic brainstorm.
3. **Pick exactly one route** from the table below and say which one. `references/routes.md` has each route's trigger and procedure.
4. **Run the route.** The interview and challenge routes read `references/grill-me.md` and `references/challenge-pipeline.md` first.
5. **Write the record and name the next owner.** Then stop.

When a material answer is missing, save the settled decision frame and requested draft records with the gap clearly marked, ask once, and yield. Do not run sleep loops, background polls, or timers waiting for a human answer. Resume from the saved draft when the answer arrives; unanswered does not mean approved.

A clear request authorizes the full decision pass. When options, evidence, and answers already exist, go to `synthesize` rather than re-interviewing. Ask only about choices the files cannot answer and that could change the recommendation. A destination named in the request counts as approval to write there.

## Routing table

| Observable signal | Route | Reference |
|---|---|---|
| The brief is vague, incomplete, or held in the user's head; user says "grill me" or "interview me" | `interview`: source-first interview | `references/grill-me.md` |
| The destination is clear but several dependent decisions obscure the path | `wayfind`: decision map, one blocking edge | `references/routes.md` |
| Hidden beliefs or external facts could reverse the choice | `challenge`: research-first adversarial review | `references/challenge-pipeline.md` |
| The option set is narrow or repetitive | `explore`: distinct option generation | `references/routes.md` |
| Options and evidence are ready for a recommendation | `synthesize`: one evidence-linked recommendation | `references/routes.md` |
| Uncertainty must stay visible after the decision | `register`: durable assumption register | `references/routes.md` |
| Ideas need a ranked focus for a framed decision | `prioritize`: criteria, viability floor, cheap first test | `references/routes.md` |
| The decision is who or what should do a bounded job | `match`: candidate comparison and handoff brief | `references/routes.md` |
| Proven or promising work may deserve a reusable form | `productize`: form choice and cheapest next validation | `references/routes.md` |

## Ownership and overlaps

Strategy Room is the terminal owner for a generic "grill me", "interview me", "pressure-test this decision", or "challenge my assumptions" request. Run the `interview` or `challenge` route here; do not hand the interview to another skill. Another skill owns the request only in these cases:

| Request | Owner |
|---|---|
| Names Matt, Matt Pocock, Matt's flow, or a Matt-prefixed step | `matt-partok-bundled-plugin-for-knowledge-work` |
| Asks to run Outcome Engine, or to take an idea through brief, slices, and verified execution | `outcome-engine` |
| Ranks ideas where a decision, owner, and stakes exist | here, `prioritize` |
| Ranks a messy idea pile with no decision yet, or names Curiosity Compass or Signal to System | `signal-to-system` (`curiosity-compass`) |
| Chooses who or what should do a job as a pre-commitment decision (`match`), or decides whether proven work deserves a reusable form (`productize`) | here, unless the user names Signal to System |

If a request still fits two owners after this table, ask one question naming both and proceed with the answer. The selected owner finishes the route; neither skill hands the same job back to the other.

## Worked example (illustrative, synthetic)

Request: "Grill me on moving our 30-member choir's weekly rehearsal from the church hall to a paid rehearsal studio next month. The budget sheet, the hall agreement, and my notes on what members said are attached. Write the decision record when we're done."

- Frame: decision is the rehearsal venue; owner is the choir director; reversible at a cost; the budget sheet caps venue spend.
- Settled from the files, so not asked: budget cap, member count, rehearsal night preference in the notes.
- The hall agreement requires 90 days' notice. Moving "next month" is not possible without breaking it, so say so and cite the clause instead of asking whether next month still works. The real options are "move after notice" or "stay".
- The only open branch that changes the answer: whether the section leaders accept the studio's only free slot, Thursday. Ask that one question with a recommended default ("give notice only after they agree").
- Record: recommend the studio from the first date after the notice period, conditional on the Thursday slot; the case against is cost within the cap. Confidence medium. The handoff names the director. `execution_authorized: false`.

A wrong version would ask about the budget, keep "next month" on the table, run a ten-question interview when one gap remained, or send the notice letter.

## When something goes wrong

| Symptom | Likely cause | Next move | Stop when |
|---|---|---|---|
| No decision can be stated | The request is a topic, not a choice | Return a one-line missing decision statement with two candidate framings | the user has not named a decision |
| The user answers a question the files already settled differently | Conflicting sources | Show both and ask which governs | resolved; never silently pick one |
| `validate_record.py` reports errors | Missing required field or wrong enum | Fix the named fields and rerun once | the second run fails; report the errors verbatim |
| `dossier_check.py` fails in the challenge pipeline | Too few, stale, or single-domain sources | Research the named gaps once, then rerun | the second failure; downgrade to the `register` route and mark claims untested |
| The user keeps adding options mid-interview | Scope drift | Checkpoint the working model and ask whether the decision changed | the user confirms the frame |
| The user asks to build, send, or buy | Execution request | Finish the record, then write `execution-handoff.md` | always; this skill does not execute |

## Completion

- **Decision recorded:** a recommendation (or "no option clears the bar") with options, evidence, risks, conditions, confidence, and a named handoff owner. Structured records pass `bin/validate_record.py`.
- **Missing decision:** the missing decision statement, what is known, and who must decide. This is a valid outcome, not a failure.
- **Blocked:** name the missing fact or access, the smallest question that clears it, and deliver every settled part of the record.

## Output contract

- **Decision-only boundary.** Every route ends at a decision record and a named handoff. The routing record enforces it: `execution_authorized` must be `false`.
- **Facts, assumptions, and judgment stay visibly separate.** Cite or qualify every material factual claim. Never convert an opinion into a supported assumption without evidence.
- **One blocking decision per context** on the wayfind route. Wayfinding does not become a generic project plan.
- **Recommend, don't force.** The synthesizer and prioritizer may end with "no option clears the bar" or "no candidate qualifies".

## File output

Write where the request says. With no destination named, ask once; a sensible default is `~/workspace/your_files/strategy-room/`, or a goal's `files/` directory for goal-related decisions. Do not overwrite an existing record; add a version suffix. Suggested files:

- `decision-map.md` from `assets/decision-map-template.md` (wayfind route; durable decision state)
- `execution-handoff.md`: the accepted decision, rationale, assumptions, evidence, risks, conditions, acceptance checks, next actions, and owner. Self-contained, so another authorized task can pick it up without this conversation.
- `decision-record.json`, `route.json`, `assumption-register.json`: structured artifacts validated with `bin/validate_record.py`. The human-readable record stays primary.

## Tooling: `bin/`

Set `SKILL=~/workspace/skills/strategy-room` (or this skill's actual folder). This self-check runs from any directory and writes nothing:

```bash
python3 "$SKILL/bin/validate_record.py" "$SKILL/assets/route-template.json" "$SKILL/assets/route-schema.json"
```

- `bin/validate_record.py ARTIFACT.json SCHEMA.json`: validates against `assets/route-schema.json`, `assets/decision-record-schema.json`, or `assets/assumption-register-schema.json`. Prints `{"valid": ...}` and exits non-zero on failure.
- `bin/check_option_count.py FILE [MINIMUM]`: counts numbered or bulleted options; the explore route uses it to enforce breadth (default minimum 10).
- `bin/dossier_check.py DOSSIER.md --effort {light,standard,deep} --pace {fast,standard,slow}`: gate between research and challenge in the challenge pipeline. Do not proceed past research until it passes.

## Companion workspace skills

Optional; they never block owned work. Check `~/workspace/skills/` for availability and use the local handoff when one is missing.

- `knowledge-work-superpowers`: deeper evidence-led research when the challenge route's own research is insufficient
- `outcome-engine`: execution after an accepted decision (separate explicit authorization required)
- `proofloop`: extended verification of a consequential decision
- `writing-quality`: final prose review of user-facing reports
- `continuity-vault`: cross-task continuity for multi-session wayfinding

## Operating rules

1. Pick one route and stick to it. Do not blend interview, challenge, and synthesis into one pass.
2. Investigate before asking. Never replace a user-owned decision with research; evidence narrows a choice, it does not decide values.
3. Match depth to stakes, reversibility, and cost. Exhaust material ambiguity, not trivia.
4. Read-only by default. No external changes, messages, purchases, or plan execution without separate authority.
5. Report honestly when the user's input is well-grounded. Do not manufacture concerns.
6. Register load-bearing assumptions, mark what is untested, and name what evidence would change the recommendation.
