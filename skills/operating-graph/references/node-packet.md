# Node Packet

`prepare-dispatch` creates a `NodeTaskPacket` before dispatch and anchors its SHA-256 in a controller-owned `DispatchReceipt`. It binds the run, graph version, epoch, node attempt, dependencies, hashed inputs, success criteria, expected outputs, execution mode, authority prohibitions, allowed write roots, bounded context references, and finite limits. `record-launch` anchors the canonical launch record in a separate controller-owned `LaunchReceipt`.

Use the canonical examples in `assets/templates/node-task-packet.json`, `thread-launch-record.json`, and `node-return-packet.json`.

The controller records each actual fresh subagent launch as a `ThreadLaunchRecord`. The request must carry `"tool": "subagent.spawn"` and `"threadMode": "fresh"` — a new subagent thread that receives only the bounded packet context and none of the parent transcript. `record-launch` rejects any record that does not match this launch spec.

Require the worker result to be a `NodeReturnPacket` containing the source task and launch hashes, agent identity, exact status, summary, actual write paths, artifacts, evidence, criterion mapping, unresolved issues, risks, signals, and explicit denial of controller authority. Validate every binding before transitioning the node.

Ingest valid returns with `python3 scripts/graphctl.py ingest-return <run-directory> <return-packet.json>`. The controller registers valid artifacts automatically. Reject paths outside the run directory or outside the node's `attempt-<number>/worker/` and artifact directories. Reject any task or launch hash that differs from its controller receipt.
