---
name: "gauntlet-loop"
description: "Run the Gauntlet Loop: explicit-only governed execution for unusually large, consequential projects — plan grilling, compiled workstreams, fresh-critic reviews, durable handoffs, and independent verification. Trigger only when the user explicitly says to run the gauntlet (or gauntlet loop) on a project. Never infer it from difficulty, size, subagent use, or urgency."
---

# Gauntlet Loop

## Purpose

Run a mega-project as a durable, bounded state machine: grill the goal,
write an approved project constitution, compile bounded workstreams,
execute them with fresh critics, hand off state after every material
event, and finish with an independent verification verdict. The approved
plan is the constitution; missing evidence is failure, never a pass.

## Explicit-only contract

This skill runs **only** when the user explicitly asks for the gauntlet
(or "gauntlet loop"). Never activate from project size, difficulty,
subagent requests, urgency, or the word "gauntlet" in passing. Do not
change the model, reasoning effort, or cost profile. Resuming a
previously paused project in a new session also requires explicit
invocation.

## Capability mapping

| Plugin concept | Hatch/Muse equivalent |
|---|---|
| Fresh agent, no inherited turns (`fork_turns: "none"`) | Spawn a new subagent with a self-contained brief — fresh context is guaranteed by design; never resume an old task as a substitute |
| Bounded subagent threads | Subagents I spawn, with disjoint write targets or serialized writes |
| User-owned Codex tasks / external thread topologies | Not available; durable channels (cron, hooks, separate chats) need separate explicit user approval and are never critics |
| `.codex-plugin` / `.claude-plugin` manifests | Not used |
| Host hooks (PreCompact, SessionStart) | Replaced by the handoff checklist below — continuity is maintained eagerly in `.gauntlet/handoff.md` |

Record the live envelope at intake:

```bash
python3 ~/workspace/skills/gauntlet-loop/bin/gauntletctl.py capabilities \
  --project-root <root> --agent-tools available --max-concurrency <n> --fresh-isolation
```

## Workflow

State lives in `<project-root>/.gauntlet/`. Move only along the
transitions in `references/state-machine.md` (e.g.
`intake → grilling → plan_proposed → plan_approved → gauntlet_compiled →
executing → integrating → ready_for_verification → verifying →
verified | verified_with_caveats | failed_verification | unable_to_verify`).
`waiting_for_user`, `blocked`, `paused`, and `stopped` are valid holds.
Every transition records actor, reason, artifacts, and the exact next
action. Use `bin/gauntletctl.py` for `init`, `transition`, `validate`,
`handoff`, `validate-handoff`, `usage`, `capabilities`, and `evidence`.

### Stage 1 — Plan

1. Explore the project and its closest instructions first.
2. If no `.gauntlet/state.json` exists, initialize:
   `gauntletctl.py init --project-root <root> --name <name> --actor lead-agent`
3. Move to `grilling`. Use `references/grill-me-method.md`: one material
   question at a time, exposing ambiguity, tradeoffs, failure modes,
   authority boundaries, evidence standards, and irreversible choices.
   Stop when the plan can be written without dangerous ambiguity; don't
   ask the user to decide implementation details the lead can determine.
4. Draft `.gauntlet/plan.md` from `assets/plan.md`. Make concrete: scope
   and exclusions, evidence, acceptance criteria, stop conditions, and a
   finite resource envelope — elapsed time, subagent launches, max
   concurrency, critic rounds per workstream, and extension conditions.
   "No fixed round count" is invalid; any extension needs user approval.
5. Update `decisions.md`, `assumptions.md`, `risks.md`,
   `open-questions.md`, and `source-register.md` after each material
   event. Transition to `plan_proposed`.
6. **Hard stop:** present the plan and ask for explicit approval. Only an
   approval in the current task moves to `plan_approved`. Then validate:
   `gauntletctl.py validate --project-root <root>`.

### Stage 2 — Compile

Requires `plan_approved`. Turn the plan into an executable program —
no work starts yet.

1. Write `.gauntlet/gauntlet.yaml` as JSON-compatible YAML: for every
   workstream, unique ID, objective, owner role, dependencies, bounded
   inputs/outputs, exact write targets, evidence and acceptance criteria,
   builder and independent critic charters, max critic rounds, retry /
   block / stop rules.
2. Keep the dependency graph acyclic. Parallel work only with disjoint
   write targets; otherwise serialize. One integration owner controls
   shared files and shared decisions.
3. Compile an independent verification panel of at least three
   perspectives (acceptance/scope, evidence/correctness, integration /
   adversarial). Builders never issue the final verdict.
4. Produce `.gauntlet/threads/lead.md`,
   `.gauntlet/workstreams/<id>/charter.md` (from
   `assets/workstream-charter.md`),
   `.gauntlet/integration/integration-plan.md`, and
   `.gauntlet/verification/acceptance-matrix.md`. Transition to
   `gauntlet_compiled` and validate.

### Stage 3 — Run

Requires a compiled program. Execute within the approved scope, evidence
rules, and resource envelope.

1. Dispatch only dependency-ready workstreams to subagents, each with
   the bounded charter, allowed inputs, write targets, tests, evidence
   requirements, and stop conditions.
2. Criticize integrated waves: one fresh subagent critic may cover
   several completed low-risk workstreams; high-risk work gets its own
   critic. The critic brief contains only the approved goal, the bar,
   artifact paths, constraints, evidence locations, and the verdict
   schema (`assets/critic-report.json`) — never builder transcripts.
3. The critic inspects the real artifact and returns `bar_wins`,
   `artifact_wins`, `tie`, or `unable_to_evaluate`, identifying the
   largest meaningful gap. Accept, revise, block, or fail per
   `references/critic-contract.md`. Builders do not judge their own work.
4. After launches, rounds, target changes, or meaningful elapsed time,
   record usage: `gauntletctl.py usage --project-root <root> ...`
   Progress means integrated deliverable delta — new reports and receipts
   don't count. Stop and re-plan when support artifacts grow while
   target changes stay flat.
5. Integrate in waves: inspect for contradictions, terminology drift,
   incompatible formats, uneven evidence, and incoherence
   (`references/integration-waves.md`). Repair only within the approved
   plan and budget; preserve competing evidence until resolved.
6. When all workstreams and waves satisfy their gates, transition to
   `ready_for_verification`. Never issue the final verdict yourself.

### Stage 4 — Handoff

Update `.gauntlet/handoff.md` eagerly after every material event —
approval, state transition, completed or failed workstream, integration
wave, new risk or blocker, verification finding — and before any likely
session boundary. Never depend on hidden conversation context.

1. Generate: `gauntletctl.py handoff --project-root <root>
   --actor <actor> --objective <o> --completed <c> --failures <f>
   --next-action <a> --artifact <path> --evidence <path> ...`
   Cover all 25 template sections (`assets/handoff.md`): plan and state,
   completed work, changed artifacts, evidence and weaknesses, decisions,
   assumptions, risks, open findings, workstream/source/integration
   status, exact next actions, read-first files, commands, what not to
   redo, what not to assume, user instructions, provenance. Separate
   observed facts from assumptions.
2. Validate: `gauntletctl.py validate-handoff --project-root <root>`.
3. Comprehension check: spawn one bounded reader subagent with only the
   project root; ask it to state objective, state, completed work,
   unresolved risks, exact next action, forbidden redo, and forbidden
   assumptions from `project.md` + `handoff.md`. The reader must not
   edit files or continue the project. Repair discrepancies, re-validate.

### Stage 5 — Verify

Requires `ready_for_verification` (or a repairable post-verification
state). Issue the verdict from independent evidence, never builder
confidence.

1. Map every acceptance criterion to the artifact, the observable check,
   the evidence path, and known caveats
   (`assets/verifier-report.json`, `schemas/verifier-report.schema.json`).
   A criterion without inspectable evidence is not passed.
2. Spawn at least three bounded judge subagents (acceptance/scope,
   evidence/correctness, integration/adversarial) with only the plan,
   program, artifacts, source register, evidence archive, acceptance
   matrix, and reproduction commands. Read-only unless the user
   separately authorizes repair. Builders and integration owners cannot
   judge.
3. Synthesize by re-examining evidence, not by vote. Verdicts:
   `verified` | `verified_with_caveats` | `failed_verification` |
   `unable_to_verify` (missing evidence/access/isolation ⇒ the latter).
4. Generate the report: `gauntletctl.py evidence --project-root <root>
   --verdict <verdict>`. Transition state to the verdict and validate.
5. For failed/unable: identify the smallest repairable scope. Returning
   to execution needs explicit invocation and remaining budget; scope or
   budget expansion needs user approval. A new panel re-checks repairs.

## Output contract

- `.gauntlet/project.md`, `brief.md`, `plan.md`, `state.json`,
  `gauntlet.yaml`, `decisions.md`, `assumptions.md`, `risks.md`,
  `open-questions.md`, `progress.md`, `source-register.md`,
  `artifact-register.md`, `budget-ledger.json`, `runtime-capabilities.json`
- `workstreams/<id>/charter.md`, `workstreams/<id>/current-state.md`,
  builder artifacts, test evidence, fresh critic reports
- `integration/integration-plan.md`, `synthesis-report.md`,
  `contradiction-register.md`
- `verification/acceptance-matrix.md`, `verifier-reports/`,
  `unresolved-findings.md`
- `reports/evidence-report.md`, `handoff.md`, `sessions/` records

## Operating rules

1. Invocation never authorizes publication, deployment, purchases,
   external messages or uploads, permission or credential changes, new
   cron jobs or hooks, destructive actions, Goal creation, or silent
   model/effort escalation. Those retain normal approval requirements.
2. Capability drift stops execution: recompile or ask the user; never
   improvise a broader program.
3. A user may accept a result below the original bar — record the
   override and remaining gap in `decisions.md`.
4. Technical access is capability, not authority. A task list is not a
   constitution; a builder's report is not evidence; resource exhaustion
   is not success.
5. Complete only when the independent panel has issued an
   evidence-based verdict, the evidence report and handoff are current,
   validation passes, and the user receives exact artifact paths and
   caveats.
