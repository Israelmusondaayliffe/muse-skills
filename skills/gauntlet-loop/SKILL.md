---
name: "gauntlet-loop"
description: "Run the Gauntlet Loop: explicit-only governed execution for a large, consequential multi-workstream project. Grill the plan, get it approved as the project constitution, compile bounded workstreams, run them with fresh critics, integrate in waves, hand off state durably, and finish with an independent verification panel. Use only when the user names the gauntlet loop or a governed gauntlet project (gauntlet loop, governed gauntlet, gauntlet workstreams, resume the gauntlet loop). A bare 'run the gauntlet' with no existing state gets one question choosing between this skill and the artifact gauntlet (blind critics against a bar). Never infer it from difficulty, size, subagent use, or urgency."
---

# Gauntlet Loop

Run a mega-project as a durable, bounded state machine: grill the goal, write an approved plan (the constitution), compile bounded workstreams, execute them with fresh critics, hand off state after every material event, and finish with an independent verdict. Missing evidence is failure, never a pass.

The project is finished only when an independent panel issued an evidence-based verdict, `reports/evidence-report.md` and `handoff.md` are current, `gauntletctl.py validate` passes, and the user has the artifact paths and caveats. A plan, a compiled program, or a builder's report is progress, not done.

## Start here

1. **Is this the gauntlet loop?** Existing `<root>/.gauntlet/state.json` means this skill; resume it. Existing `<root>/.gauntlet/runs/` means the artifact gauntlet (`gauntlet` skill); do not touch it. With no state: workstreams, a plan to govern, or "gauntlet loop" means this skill; a bar to beat or blind comparison means `gauntlet`. A bare "run the gauntlet" gets one choice question and nothing is initialized. Never mix the two editions' state; `gauntletctl.py init` refuses a root that holds `.gauntlet/runs/` or `.gauntlet/sealed/`, even with `--force`.
2. **Read before asking.** Read the project and its closest instructions, then `.gauntlet/state.json`, `project.md`, `handoff.md`, and `decisions.md` when they exist. Decisions already recorded are not re-asked.
3. **Record capabilities honestly.** `python3 bin/gauntletctl.py capabilities --project-root <root> --agent-tools available --max-concurrency <n>`. Add `--fresh-isolation --isolation-evidence "<observed check>"` only when you observed isolation, for example a spawned child could not produce a canary string that exists only in the parent turn. A host or model name is not proof. Without evidence the record says `unknown`, and the final verdict carries that caveat (`verified_with_caveats` at best).
4. **Route by state** (all commands run from this skill's directory):

| State | Stage | First command |
|---|---|---|
| none | Plan | `python3 bin/gauntletctl.py init --project-root <root> --name "<name>" --actor lead-agent` |
| `intake`, `grilling`, `plan_proposed` | Plan | `python3 bin/gauntletctl.py transition --project-root <root> --to grilling --actor lead-agent --reason "<why>" --next-action "<question>"` |
| `plan_approved` | Compile | write `.gauntlet/gauntlet.yaml`, then `transition --to gauntlet_compiled` |
| `gauntlet_compiled`, `executing`, `integrating` | Run | `python3 bin/gauntletctl.py validate --project-root <root>` |
| any material event or session end | Handoff | `python3 bin/gauntletctl.py handoff --project-root <root> --actor lead-agent ...` |
| `ready_for_verification`, `verifying` | Verify | `python3 bin/gauntletctl.py validate --project-root <root> --strict` |
| `paused`, `blocked`, `waiting_for_user` | Report the hold and the one thing needed | read `handoff.md` |

Transitions follow `references/state-machine.md`. Each records actor, reason, artifacts, and the exact next action.

## Stage 1: Plan

1. Move to `grilling`. Use `references/grill-me-method.md`: one material question at a time, only questions whose answer changes scope, evidence, authority, or the resource envelope. Implementation details the lead can decide are not questions. A general "grill me" outside a gauntlet project belongs to `strategy-room`.
2. Draft `.gauntlet/plan.md` from `assets/plan.md`: scope and exclusions, evidence, acceptance criteria, stop conditions, and a finite resource envelope (section 22): elapsed minutes, agent launches, max concurrency, critic rounds per workstream, metered cost (0 unless the user names a ceiling). Unedited `init` defaults are 30 minutes, 6 launches, concurrency 2, 2 critic rounds. "No fixed round count" is invalid.
3. Keep `decisions.md`, `assumptions.md`, `risks.md`, `open-questions.md`, `source-register.md` current. Transition to `plan_proposed`.
4. Present the plan and ask for approval once. Only the user's approval in the current task moves to `plan_approved`: add `Status: approved` to `plan.md` and an `Approval:` line to `decisions.md` quoting the user's words and date. The transition gate checks both. Then `validate`.

## Stage 2: Compile

Requires `plan_approved`. Write `.gauntlet/gauntlet.yaml` (JSON-compatible) with the approved envelope in `budget`: per workstream an ID, objective, dependencies, exact write targets, evidence and acceptance criteria, builder and critic charters, max critic rounds. Keep the dependency graph acyclic; parallel work only on disjoint write targets. Compile a verification panel of at least three perspectives (acceptance and scope, evidence and correctness, integration and adversarial). Write the charters (`assets/workstream-charter.md`), `integration/integration-plan.md`, and `verification/acceptance-matrix.md`. Transition to `gauntlet_compiled` and validate.

## Stage 3: Run

1. Before each dispatch, confirm `agent_launches` in `budget-ledger.json` plus the launches you are about to make stays within `budget.max_agent_launches`, and concurrency within `max_concurrency`. Record usage right after launching: `gauntletctl.py usage --project-root <root> --agent-launches <total> ...`. The command rejects a ledger over the limits. It cannot see launches you do not record and does not cap account-wide spend.
2. Dispatch only dependency-ready workstreams, each with its bounded charter (`references/multi-thread-execution.md`).
3. Critics get only the approved goal, the bar, artifact paths, constraints, evidence locations, and the verdict schema (`assets/critic-report.json`), never builder transcripts. Verdicts: `bar_wins`, `artifact_wins`, `tie`, `unable_to_evaluate` (`references/critic-contract.md`).
4. Integrate in waves (`references/integration-waves.md`). Progress means integrated deliverable change; new reports do not count. Stop and re-plan when support artifacts grow while deliverables stay flat.
5. When every workstream and wave passes its gate, transition to `ready_for_verification`. The lead never issues the verdict.

## Stage 4: Handoff

After every material event and before a likely session end: `gauntletctl.py handoff --project-root <root> --actor <actor> --objective <o> --completed <c> --failures <f> --next-action <a> --artifact <path> --evidence <path>`, then `validate-handoff`. Cover the 25 sections of `assets/handoff.md`, separating observed facts from assumptions (`references/session-handoffs.md`).

## Stage 5: Verify

Map every acceptance criterion to artifact, check, evidence path, and caveats (`assets/verifier-report.json`). Spawn at least three read-only judges with only the plan, program, artifacts, source register, evidence, acceptance matrix, and reproduction commands (`references/verification-panel.md`), within the envelope. Synthesize by re-examining evidence, not by vote. Then `gauntletctl.py evidence --project-root <root> --verdict <verdict>`, transition to the verdict, validate.

## Worked example (illustrative, synthetic)

Request: "Run the gauntlet loop on Harbor Handbook: three volunteer chapters and a table of contents."

- Routing: "gauntlet loop" plus workstreams, so this skill. No state exists; `init`, then `capabilities` without `--fresh-isolation` (nothing observed yet), then `transition --to grilling`.
- First question: "Who is the primary reader: new volunteers or returning ones?" The brief lists this as open and it changes tone and depth of all three chapters. Not asked: file format or chapter order, which the lead can decide.
- Envelope proposed with the plan: 3 chapter workstreams plus 1 integration owner; 2 critic rounds each; the panel needs 3 judges. That is 3 builders, up to 6 critics, 3 judges: 12 launches, 90 minutes, no metered spend. The init default of 6 launches cannot finish this, so the plan states 12 and the user approves or trims it.
- After approval: `Approval: 2026-09-25 user said "approved, 12 launches"` in `decisions.md`, `Status: approved` in `plan.md`, transition to `plan_approved`.

A wrong version would ask five questions at once, compile before approval, pass `--fresh-isolation` because the host is Hatch, or keep launching after the ledger reaches the cap.

## When something goes wrong

| Symptom | Likely cause | Next move | Stop when |
|---|---|---|---|
| `transition gate failed for plan_approved` | No `Status: approved` or no `Approval:` record | Ask for approval; record the user's words | the user has not approved |
| `budget ledger update rejected` | Recorded usage exceeds the approved limit | Stop dispatching; report used versus approved | extension needs a new recorded approval |
| `init` refuses: artifact gauntlet state exists | Root holds `.gauntlet/runs/` | Use another project root | always; never `--force` past it |
| Critic returns `unable_to_evaluate` | Missing artifact or evidence path | Fix the brief inputs once; re-run the critic within the round cap | second time: mark the workstream blocked |
| `validate` fails after compile | Cyclic dependencies, overlapping write targets, bad budget | Fix `gauntlet.yaml`; re-validate | the fix would change approved scope: back to plan |
| Capability drift (fewer slots, no subagents) | Host changed | Record new capabilities; recompile or ask | never improvise a broader program |

## Completion

- `verified` or `verified_with_caveats`: panel verdict, evidence report, current handoff, validation passing. Name every caveat, including unconfirmed isolation.
- `failed_verification` or `unable_to_verify`: identify the smallest repairable scope. Returning to execution needs explicit invocation and remaining envelope; more needs approval.
- `paused` on budget: report launches and minutes used against approved, and what finished. Resource exhaustion is not success.

## Operating rules

1. Invocation never authorizes publication, deployment, purchases, external messages, credential changes, new cron jobs or hooks, destructive actions, or model or effort changes.
2. Technical access is capability, not authority. A task list is not a constitution; a builder's report is not evidence.
3. A user may accept a result below the bar; record the override and the remaining gap in `decisions.md`.

## Resources

- `bin/gauntletctl.py`: `init`, `transition`, `validate`, `handoff`, `validate-handoff`, `usage`, `capabilities`, `evidence`.
- `references/`: `state-machine.md`, `gauntlet-method.md`, `grill-me-method.md`, `project-constitution.md`, `workstream-design.md`, `critic-contract.md`, `integration-waves.md`, `multi-thread-execution.md`, `session-handoffs.md`, `verification-panel.md`, `evidence-report.md`, `quality-bars.md`, `knowledge-work-bars.md`.
- `assets/`: `plan.md`, `project.md`, `handoff.md`, `workstream-charter.md`, `thread-charter.md`, `critic-report.json`, `verifier-report.json`, `evidence-report.md`. `schemas/` holds the JSON schemas.
- State: `<root>/.gauntlet/` (`state.json`, `plan.md`, `gauntlet.yaml`, `budget-ledger.json`, `runtime-capabilities.json`, `decisions.md`, `handoff.md`, `workstreams/`, `integration/`, `verification/`, `reports/`).
