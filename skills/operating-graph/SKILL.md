---
name: operating-graph
description: Run bounded, auditable multi-step agent workflows as an explicit operating graph — design typed node/edge topologies, execute with subagent workers and hash-chained runtime records, inspect state, propose and apply bounded topology rewrites, debug failures, and verify outcomes against immutable completion criteria. Invoke only when the user explicitly says to use Operating Graph (e.g. "Use Operating Graph", "Run this as an operating graph"). Do not activate from complexity alone.
---

# Operating Graph

A deterministic way to coordinate multi-step, parallel, or high-risk agent work: the goal and authority are immutable, work is split into typed nodes with explicit dependencies and budgets, every runtime change is a hash-chained event, subagent workers run from bounded packets with evidence receipts, and the terminal verdict is verified against the original completion criteria.

Ported from the public `operating-graph` plugin (MIT, see LICENSE). Host-neutral engine; this skill is the Hatch mapping.

## Roles on this host

- **Authority**: the user (the graph's `human-authority` node). Owns the goal, approvals, and the final decision. Never infer their approval.
- **Controller**: you, running this skill. Sole writer of runtime records; sole approver of state transitions; the only one who may issue a terminal verdict.
- **Worker**: a subagent (`subagent` nodes), you directly (`inline`), a shell command / web fetch / connected skill (`tool`), or the user answering a bounded question (`human`).

## Activation (explicit-only)

Activate only on a direct imperative: "Use Operating Graph", "Run this as an operating graph", or an explicit reference to this skill. Quoted, negated, conditional, incidental, complexity-only ("this is complicated"), or generic multi-step wording does **not** activate it.

Check fit before designing: a graph helps when work has multiple dependent steps, genuinely independent parallel lanes, separate checking, meaningful risk, or human approvals. A simple task stays on an inline path — do not build a graph around it.

## Workflow phases

Route the request to one phase. Never start a run during design, never mutate during inspection, and never infer approval for material external actions.

### 1. Design — topology before execution

1. Read `references/graph-contract.md`.
2. Restate the immutable goal: statement, typed deliverables, completion criteria, authority node, approvals, permissions, hard limits.
3. Choose the smallest sufficient typed node set. Separate authority, controller, production, shared state, and independent evaluation. Prefer the diamond pattern (planner → parallel specialists → independent skeptic → synthesis → final evaluation → human decision) when it fits.
4. Draw only real dependencies; fan out genuinely independent work in parallel.
5. Give every required deliverable an independent evaluator path and an approval predecessor for every external side-effect node. Use `next_epoch` for feedback cycles.
6. Start from `assets/templates/graph.json` (minimal) or `assets/templates/diamond-graph.json` (parallel diamond); examples in `references/examples/`.
7. Save `graph.json` plus a Mermaid view, then run `python3 scripts/graphctl.py validate <graph.json>` and fix every violation. Never change authority or weaken criteria to make validation pass.
8. Present the graph and get user approval before running when material external actions exist.

Writes design artifacts only. Does not start a run.

### 2. Run — execute with evidence

Run all commands from this skill's directory. Read `references/runtime-protocol.md` before mutating a run.

1. `validate`, then `init <graph.json> --run-root <dir>` (keep runs under `~/workspace/`).
2. `dispatch-preview <run-dir> --json` to see parallel work without mutation. Never silently downgrade a `subagent` node to inline work.
3. `prepare-dispatch <run-dir> --json` → task packets + controller-owned dispatch receipts.
4. For each ready `subagent` node, spawn a **fresh subagent**: no parent transcript, only the task packet path and bounded context. Record the launch exactly as `assets/templates/thread-launch-record.json` (request: `"tool": "subagent.spawn"`, `"threadMode": "fresh"`; response: `agentId`, success flag, timestamps), then `record-launch <run-dir> <record.json>`. The subagent must write its `NodeReturnPacket` at the packet's `returnPacketPath` before its result is ingested.
5. `ingest-return <run-dir> <return-packet.json>` per completed worker; the controller validates hashes, scope, criteria, and artifacts, and registers valid artifacts.
6. Handle `inline`, `tool`, and `human` nodes directly; use `transition`, `register-artifact`, and `signal` for explicit state changes, artifacts, and observed events.
7. Evaluate rewrite triggers only per `references/rewrite-policy.md`. Reject stale returns after a graph-version change.
8. Continue to completion, escalation, cancellation, or a hard limit. `resume-check <run-dir>` before resuming an interrupted run.
9. Finish with `verify <run-dir>` and report graph versions, thread evidence, artifacts, unresolved issues, and the exact verdict.

Stop automatic execution on event-chain corruption, missing thread evidence, stale packets, unavailable required models, unsafe scope, or exhausted limits. Do not synthesize approvals, exceed budgets, or let workers edit controller-owned files.

### 3. Inspect — read-only

1. `resume-check <run-dir>` (validates replay + integrity).
2. `status <run-dir>`, `ready <run-dir>`, then `inspect <run-dir> --format text` and `--format mermaid`.
3. Report version, epochs, attempts, budgets, node states, thread launch records, pending approvals, artifact lineage, rewrites, bottlenecks, unsatisfied dependencies.

Remain read-only: no transitions, no artifact registration, no rewrites, no repairs. If the event chain is broken, stop and move to Debug.

### 4. Rewrite — smallest bounded topology change

1. Read `references/rewrite-policy.md`. Diagnose the topology failure from triggering events.
2. Draft the smallest proposal using only `add_node`, `update_node`, `disable_node`, `add_edge`, `disable_edge`, `set_priority`. State evidence event IDs, predicted benefit, regressions, risk level, approval requirement, rollback version.
3. On user request to persist: `propose-rewrite <run-dir> <proposal.json>`.
4. Apply only when policy permits and every required approval exists: `apply-rewrite <run-dir> <proposal-id>`. Confirm with `status` and `validate <run-dir>/graph.json`.

Never change the goal, criteria, authority, permissions, approval boundaries, or hard limits without required approval. Preserve all prior graph versions.

### 5. Debug — read-only diagnosis

1. `replay <run-dir>`, `resume-check <run-dir>`, `inspect` (text + mermaid).
2. Reconstruct transitions and version changes from hash-chained events. Check missing/corrupt/invalidated/misowned artifacts. Detect same-epoch deadlocks, impossible dependencies, illegal transitions, policy blockage, exhausted budgets.
3. Classify the primary cause: node failure, edge failure, state corruption, policy blockage, or exhausted budget. Produce a bounded repair proposal **without applying it** unless the user explicitly requests a separate repair workflow.

A broken event chain or version mismatch is corruption: stop automatic execution.

### 6. Verify — terminal judgment

1. Disclose up front that verification writes controller-owned audit events.
2. `resume-check <run-dir>` first — stop if integrity fails.
3. Return to the immutable original goal; enumerate every completion criterion.
4. Verify deliverable existence, ownership, hash integrity, evidence provenance; each required deliverable has an independent evaluator and no node evaluated or approved its own output.
5. Check unresolved failed/blocked critical nodes, required approvals, prohibited mutations. For each executed `subagent` node: dispatch receipt, launch receipt, fresh-thread launch, matching agent identity, bounded return, graph-version binding.
6. `verify <run-dir>`. Return exactly `pass`, `conditional-pass`, or `fail` with criterion-level evidence and unresolved issues.

A worker return is evidence, not acceptance. Never repair evidence or relax criteria during verification. Read-only with respect to topology and worker output.

## Controller checklists

Before each run session (a resumed run or a fresh long run): `resume-check` the run, re-read `status`, confirm no pending approvals you are about to bypass, and confirm worker slots before `prepare-dispatch`.

Before a `subagent` launch: packet prepared and receipt anchored; launch record fields match the template exactly (`subagent.spawn` / `fresh`); the subagent task states its allowed write roots and the authority prohibitions (no spawning, no approving, no integrating, no controller-state writes, no answering the user, no terminal verdict).

Before a terminal verdict: every completion criterion evidenced, every required deliverable evaluator-independent, no unresolved failed/blocked critical nodes, approvals on record.

## Output contract

- Design → validated `graph.json` + Mermaid view + summary; no run started.
- Run → live run directory, `verify` result, verdict report with versions, thread evidence, artifacts, unresolved issues.
- Inspect → read-only status report; no mutations.
- Rewrite → proposal file (+ applied version on approval) with risk and rollback.
- Debug → classified root cause + bounded repair proposal; no automatic repairs.
- Verify → `pass` / `conditional-pass` / `fail` with criterion-level evidence.

## Operating rules

1. Controller-only runtime writes; workers touch only their `node-runs/<id>/attempt-<n>/worker/` and `artifacts/<id>/` roots. Write roots are an authority boundary — subagent threads share this VM's filesystem, so do not claim OS-level confinement.
2. No synthesized approvals. Approval = the user explicitly saying yes. Every external side-effect node needs an approval predecessor.
3. Never downgrade a `subagent` node to inline execution. Never rerun a succeeded node silently. Never mark a run complete because workers stopped.
4. Run directories live under `~/workspace/`; artifacts never leave the run directory; paths in records are run-relative.
5. Do not invent user-specific data (writing samples, business details, names, credentials). Design nodes that need personal input as `human` nodes and ask the user when reached.
6. Ask rather than assume on consequential actions; this skill is explicit-only end to end.
7. Engine scripts run locally with no network access; `python3 -m py_compile scripts/*.py scripts/graph_engine/*.py` after any script change.
