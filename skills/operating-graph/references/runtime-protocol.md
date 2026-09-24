# Runtime Protocol

## Storage and ownership

Each run contains `graph.json`, `policies.json`, `state.json`, `events.jsonl`, `artifacts.jsonl`, `approvals.jsonl`, rewrite proposals and applications, immutable graph versions, node-run attempts, fresh-thread launch records, and node-owned artifacts.

The controller is the sole writer of state, events, artifact registry records, approvals, graph versions, rewrite records, task packets, dispatch receipts, launch records, and launch receipts. Workers write only inside `node-runs/<node-id>/attempt-<number>/worker/` and `artifacts/<node-id>/`. Write structured runtime files through temporary files and atomic replacement.

## Integrity

Every runtime state change emits a canonical JSON event with a sequence number, previous hash, and SHA-256 event hash. Inspection, replay, resume, debugging, and verification validate the full chain. Stop automatic execution on any break.

Artifacts must remain inside the run directory, exist, match their registered hash, and belong to the declaring node. Failed, invalidated, superseded, missing, corrupt, or wrongly owned artifacts cannot activate or complete downstream work.

## Scheduling

A ready node is enabled, dependency-complete, approval-complete, within node and run budgets, and valid for the current epoch. Sort by higher priority, critical before optional, more downstream required nodes released, then lexical node ID. Runtime concurrency is the lower of the graph limit and available worker slots, reserving a controller slot in fixed pools.

Use `dispatch-preview` to inspect parallel work without mutation. `prepare-dispatch` creates task packets for ready `subagent` nodes and anchors each packet hash in a controller-owned dispatch receipt before launch. Each such node must launch as a fresh subagent thread with no parent transcript; missing subagent support blocks the node and never authorizes inline substitution.

The controller records the actual launch request and response, including the subagent identity and any requested model, then anchors the canonical launch hash in a controller-owned launch receipt. Workers receive bounded packet context only, cannot spawn workers, and write only inside their node-owned worker and artifact roots. A return is ingested only when its task and launch hashes match both controller receipts and its agent identity, graph version, criteria, evidence, and actual paths validate.

Hatch subagent threads share the host VM filesystem, so there is no per-agent OS confinement. Operating Graph enforces write scope as an authority boundary with controller-owned tamper receipts and return-ingestion checks, not as an operating-system confinement claim. If a task requires hostile-code isolation or hard filesystem containment, stop before launch and require a separate sandboxed execution surface.

## State transitions

Allowed transitions are `pending` to `ready`, `blocked`, `skipped`, or `cancelled`; `ready` to `running`, `blocked`, or `cancelled`; `running` to `succeeded`, `failed`, or `blocked`; `failed` to retryable `ready`; and `blocked` to `ready` or `cancelled`.

A retry requires remaining attempts, valid inputs, a recorded retry event, and no pending approval. Never silently rerun a succeeded node.

Use `status`, `ready`, `transition`, `register-artifact`, `signal`, `replay`, `resume-check`, `inspect`, and `verify` through `python3 scripts/graphctl.py`.
