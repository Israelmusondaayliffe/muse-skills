---
name: operating-graph
description: Run bounded, auditable multi-step agent workflows as an explicit operating graph. Design typed node/edge topologies, execute with subagent workers and hash-chained runtime records, inspect state, propose and apply bounded topology rewrites, debug failures, and verify outcomes against immutable completion criteria. Invoke only when the user explicitly says to use Operating Graph (e.g. "Use Operating Graph", "Run this as an operating graph"). Do not activate from complexity alone.
---

# Operating Graph

Coordinate multi-step, parallel, or high-risk agent work as a typed graph: the goal and authority are immutable, work is split into nodes with explicit dependencies and budgets, every runtime change is a hash-chained event, workers run from bounded packets with evidence receipts, and the terminal verdict is checked against the original completion criteria.

Ported from the public `operating-graph` plugin (MIT, see LICENSE). The engine is host-neutral; this skill is the Hatch mapping.

A request is finished when its phase's output exists: a validated graph for design, a `verify` verdict for a run, a read-only report for inspect or debug. Workers stopping is not completion.

## Start here

1. **Explicit only.** Activate on a direct imperative ("Use Operating Graph", "Run this as an operating graph"). Quoted, negated, conditional, or complexity-only wording does not activate it.
2. **Fit check.** A graph pays off with dependent steps, independent parallel lanes, separate evaluation, meaningful risk, or human approvals. A single-step task stays inline: say so and do the task without a graph if the user agrees.
3. **Read the contract.** `references/graph-contract.md` before design; `references/runtime-protocol.md` before touching a run.
4. **Pick the phase from the request and run its first command** (from this skill's directory):

| Request | Phase | First command | Writes |
|---|---|---|---|
| "design / plan this as a graph" | Design | `python3 scripts/graphctl.py validate <graph.json>` | graph files only |
| "run it", approved graph | Run | `python3 scripts/graphctl.py init <graph.json> --run-root <dir>` | controller records |
| "what's the status" | Inspect | `python3 scripts/graphctl.py resume-check <run>` | nothing |
| "change the topology" | Rewrite | read `references/rewrite-policy.md` | proposal, then apply on approval |
| "why did it fail" | Debug | `python3 scripts/graphctl.py replay <run>` | nothing |
| "is it done" | Verify | `python3 scripts/graphctl.py resume-check <run>`, then `verify <run>` | audit events only |

## Roles

- **Authority**: the user (`human-authority` node). Owns the goal, approvals, and the final decision. Approval is the user saying yes; never infer it.
- **Controller**: you. Sole writer of runtime records and the only one who issues a terminal verdict.
- **Worker**: a subagent (`subagent` node), you inline (`inline`), a tool call (`tool`), or the user answering a bounded question (`human`).

## Design

1. Restate the immutable goal: statement, typed deliverables, completion criteria, authority node, approvals, permissions, limits.
2. Choose the smallest typed node set. Separate authority, controller, production, and independent evaluation. The diamond pattern (planner, parallel specialists, independent skeptic, synthesis, final evaluation, human decision) fits parallel research or drafting.
3. Draw only real dependencies. Every required deliverable gets an independent evaluator path; every external side-effect node gets an approval predecessor. Feedback loops use a `next_epoch` edge, because the same-epoch projection must be acyclic.
4. Start from `assets/templates/graph.json` or `assets/templates/diamond-graph.json`; examples in `references/examples/`.
5. `validate` and fix each violation. Never change authority or weaken criteria to pass. After `init`, `inspect <run> --format mermaid` gives the Mermaid view.
6. With material external actions, present the graph and get approval before running.

## Run

1. `validate`, then `init <graph.json> --run-root <dir>` (runs live under `~/workspace/`).
2. `ready <run>` and `dispatch-preview <run> --json` show work without mutation. Never downgrade a `subagent` node to inline work.
3. `prepare-dispatch <run> --json` writes task packets and controller dispatch receipts.
4. For each ready `subagent` node, spawn a fresh subagent with only the packet path and bounded context. Record the launch exactly as `assets/templates/thread-launch-record.json`, then `record-launch <run> <record.json>`. The worker writes its `NodeReturnPacket` at the packet's `returnPacketPath`.
5. `ingest-return <run> <packet.json>` per worker; the controller checks hashes, scope, criteria, and artifacts.
6. Handle `inline`, `tool`, and `human` nodes directly with `transition <run> <node> <status>`, `register-artifact <run> <node> <type> <path>`, and `signal <run> <name> <value>`.
7. Rewrites only per `references/rewrite-policy.md`; reject stale returns after a graph-version change.
8. Continue to completion, escalation, cancellation, or a hard limit, then `verify <run>` and report versions, thread evidence, artifacts, unresolved issues, and the exact verdict.

## Inspect, rewrite, debug, verify

- **Inspect** (read-only): `resume-check`, `status`, `ready`, `inspect --format text` and `--format mermaid`. Report version, epochs, attempts, budgets, node states, launch records, pending approvals, artifacts, bottlenecks.
- **Rewrite**: smallest proposal using only `add_node`, `update_node`, `disable_node`, `add_edge`, `disable_edge`, `set_priority`, with evidence event IDs, risk, approval need, and rollback version. `propose-rewrite <run> <proposal.json>`, then `apply-rewrite <run> <proposal-id>` only when policy and approvals allow. Never change goal, criteria, authority, permissions, or limits without approval.
- **Debug** (read-only): `replay`, `resume-check`, `inspect`. Classify the cause as node failure, edge failure, state corruption, policy blockage, or exhausted budget. Propose a repair; do not apply it unless asked.
- **Verify**: disclose that it writes audit events; `resume-check` first; enumerate every original criterion; check deliverable ownership, hashes, evaluator independence, approvals, and launch evidence for each `subagent` node; `verify <run>`. Return exactly `pass`, `conditional-pass`, or `fail` with criterion-level evidence.

## Worked example (illustrative, synthetic)

Request: "Use Operating Graph. Validate this FAQ graph and fix what validation reports."

- `validate faq-graph.json` exits 2: `OGI-13` same-epoch cycle between `builder` and `independent-evaluator`; `OGI-14` the cycle lacks a `next_epoch` edge.
- Judgment: the evaluator-to-builder edge is a real revision loop the user wants. Deleting it would pass validation but drop the revision path. Change that edge's `temporal` to `next_epoch`, so a revision happens in epoch 2, bounded by `limits.maxEpochs`. Goal, criteria, and limits stay byte-identical.
- `validate` prints `Graph valid: tidewater-faq`. `init` creates `run-tidewater-faq/`; `ready` prints `Ready nodes: human-authority`, which is right: nothing runs before the authority node.

A wrong version would delete the feedback edge, raise `maxEpochs` without being asked, or dispatch before the user approved running.

## When something goes wrong

| Symptom | Likely cause | Next move | Stop when |
|---|---|---|---|
| `validate` exits 2 with `violated rule` | Bad kind, cycle, missing evaluator or approval edge | Fix the named element; re-validate | the fix would change goal, authority, or criteria: ask |
| `resume-check` not resumable | Broken event chain or version mismatch | Treat as corruption; switch to Debug | always stop automatic execution |
| `ingest-return` rejects a packet | Stale graph version, scope breach, missing artifact | Re-dispatch the node once from a fresh packet within its attempt budget | attempts exhausted: mark blocked |
| Subagent spawn unavailable | Host capability | Report the node as blocked; never run it inline instead | a critical node cannot run |
| `ready` shows only human nodes | Waiting on the user's decision | Ask the bounded question the node defines | no answer: run stays waiting |
| Limit reached (`maxNodeRuns`, `maxEpochs`) | Budget exhausted | Stop; report state and the smallest next action | always; do not raise limits yourself |

## Completion

- Design: validated `graph.json`, Mermaid view, short summary. No run started.
- Run: `verify` result with criterion-level evidence and unresolved issues. `conditional-pass` names each condition.
- Inspect and debug: read-only report; debug adds a classified cause and an unapplied repair proposal.
- Blocked: name the node, the cause, and what the user must decide.

## Operating rules

1. Controller-only runtime writes. Workers write only their `node-runs/<id>/attempt-<n>/worker/` and `artifacts/<id>/` roots. Subagents share this machine's filesystem, so write roots are an authority rule, not OS confinement.
2. No synthesized approvals. Never rerun a succeeded node silently.
3. Records use run-relative paths; artifacts stay in the run directory.
4. Do not invent user data (samples, business details, credentials). Model those needs as `human` nodes.
5. Scripts run locally without network. After any script change: `python3 -m py_compile scripts/*.py scripts/graph_engine/*.py`.

## Resources

- `scripts/graphctl.py`: `validate`, `init`, `status`, `ready`, `dispatch-preview`, `prepare-dispatch`, `record-launch`, `ingest-return`, `transition`, `register-artifact`, `signal`, `propose-rewrite`, `apply-rewrite`, `verify`, `inspect`, `replay`, `resume-check`. Engine in `scripts/graph_engine/`.
- `references/`: `graph-contract.md`, `runtime-protocol.md`, `node-packet.md`, `rewrite-policy.md`, and `references/examples/`.
- `assets/templates/`: `graph.json`, `diamond-graph.json`, `node-task-packet.json`, `node-return-packet.json`, `thread-launch-record.json`, `policies.json`.
