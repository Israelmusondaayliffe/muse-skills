#!/usr/bin/env python3
"""Command-line control plane for the Operating Graph runtime."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
import mimetypes
import os
from pathlib import Path
import sys
import tempfile
from typing import Any, Optional, Sequence


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from scripts.graph_engine.artifacts import (  # noqa: E402
    ArtifactError,
    ArtifactIntegrityError,
    ArtifactRegistry,
    ArtifactUnavailableError,
    UnsafeArtifactPathError,
)
from scripts.graph_engine.constants import EventType, NodeStatus, RunStatus, VerificationStatus  # noqa: E402
from scripts.graph_engine.events import EventChainError, EventStore  # noqa: E402
from scripts.graph_engine.dispatch import (  # noqa: E402
    PacketValidationError,
    ingest_return,
    prepare_dispatch,
    preview_dispatch,
    record_launch,
    thread_evidence_summary,
    thread_history_issues,
)
from scripts.graph_engine.invariants import validate_graph_versions  # noqa: E402
from scripts.graph_engine.models import Approval, Graph, NodeRuntimeState, RewriteProposal, RuntimeState, VerificationResult  # noqa: E402
from scripts.graph_engine.reporting import render_mermaid, render_text  # noqa: E402
from scripts.graph_engine.rewrites import (  # noqa: E402
    ApprovalRequiredError,
    RewriteEngine,
    RewriteError,
    RewritePolicyError,
    RewriteValidationError,
    VersionMismatchError,
)
from scripts.graph_engine.scheduler import get_ready_nodes  # noqa: E402
from scripts.graph_engine.state import IllegalTransitionError, RetryRejectedError, StateMachine, replay_events  # noqa: E402
from scripts.graph_engine.validation import GraphValidationError, require_valid_graph  # noqa: E402
from scripts.graph_engine.verification import VerificationCorruptionError, Verifier  # noqa: E402


EXIT_OK = 0
EXIT_INTERNAL = 1
EXIT_POLICY = 2
EXIT_CORRUPT = 3
EXIT_APPROVAL = 4


class RuntimeCorruptionError(RuntimeError):
    """Raised when persisted runtime records disagree or cannot be parsed."""


@dataclass(frozen=True)
class CommandResult:
    payload: dict[str, Any]
    human: str
    exit_code: int = EXIT_OK


def _atomic_replace(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Optional[Path] = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix=f".{path.name}.", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def _json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
        + "\n"
    ).encode("utf-8")


def _read_json(path: Path, *, runtime: bool = False) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        if runtime:
            raise RuntimeCorruptionError(f"corrupt runtime file {path.name!r}: {error}") from error
        raise ValueError(f"cannot read JSON file {str(path)!r}: {error}") from error


def _runtime(run_directory: Path) -> tuple[RuntimeState, Graph, EventStore]:
    run_directory = Path(run_directory)
    try:
        state = RuntimeState.from_dict(_read_json(run_directory / "state.json", runtime=True))
        graph = Graph.from_dict(_read_json(run_directory / "graph.json", runtime=True))
    except RuntimeCorruptionError:
        raise
    except ValueError as error:
        raise RuntimeCorruptionError(f"corrupt runtime model: {error}") from error
    if state.graph_id != graph.graph_id:
        raise RuntimeCorruptionError("corrupt runtime: state graphId does not match graph.json")
    store = EventStore(run_directory, state.run_id)
    try:
        events = store.read_all()
    except EventChainError as error:
        raise RuntimeCorruptionError(f"corrupt event chain: {error}") from error
    try:
        reconstructed = replay_events(events)
    except (IllegalTransitionError, ValueError) as error:
        raise RuntimeCorruptionError(f"corrupt runtime replay: {error}") from error
    if reconstructed.to_dict() != state.to_dict():
        raise RuntimeCorruptionError("corrupt runtime: state.json differs from event replay")
    version_directory = run_directory / "graph-versions"
    versions: dict[int, Graph] = {}
    try:
        for path in sorted(version_directory.glob("v*.json")):
            versions[int(path.stem[1:])] = Graph.from_dict(_read_json(path, runtime=True))
        hashes = {
            int(key): str(value)
            for key, value in _read_json(version_directory / "hashes.json", runtime=True).items()
        }
    except (ValueError, AttributeError) as error:
        raise RuntimeCorruptionError(f"corrupt graph version registry: {error}") from error
    violations = validate_graph_versions(versions, immutable_hashes=hashes)
    if violations:
        raise RuntimeCorruptionError("corrupt graph versions: " + "; ".join(str(item) for item in violations))
    if state.graph_version not in versions or versions[state.graph_version].to_dict() != graph.to_dict():
        raise RuntimeCorruptionError("corrupt runtime: graph.json differs from the current immutable version")
    return state, graph, store


def _approvals(run_directory: Path, run_id: str) -> tuple[Approval, ...]:
    path = Path(run_directory) / "approvals.jsonl"
    if not path.exists():
        return ()
    records = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        try:
            approval = Approval.from_dict(json.loads(line))
        except (ValueError, TypeError, json.JSONDecodeError) as error:
            raise RuntimeCorruptionError(
                f"corrupt approval record on line {line_number}: {error}"
            ) from error
        if approval.run_id != run_id:
            raise RuntimeCorruptionError(
                f"corrupt approval {approval.approval_id!r}: run identifier mismatch"
            )
        records.append(approval)
    return tuple(records)


def _parse_value(value: str) -> Any:
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="graphctl")
    subparsers = parser.add_subparsers(dest="command", required=True)

    def command(name: str) -> argparse.ArgumentParser:
        child = subparsers.add_parser(name)
        child.add_argument("--json", action="store_true", dest="json_output")
        return child

    validate = command("validate")
    validate.add_argument("graph")
    initialize = command("init")
    initialize.add_argument("graph")
    initialize.add_argument("--run-root", required=True)
    status = command("status")
    status.add_argument("run_directory")
    ready = command("ready")
    ready.add_argument("run_directory")
    dispatch_preview = command("dispatch-preview")
    dispatch_preview.add_argument("run_directory")
    dispatch_preview.add_argument("--available-slots", type=int)
    prepare = command("prepare-dispatch")
    prepare.add_argument("run_directory")
    prepare.add_argument("--available-slots", type=int)
    launch = command("record-launch")
    launch.add_argument("run_directory")
    launch.add_argument("record")
    returned = command("ingest-return")
    returned.add_argument("run_directory")
    returned.add_argument("packet")
    transition = command("transition")
    transition.add_argument("run_directory")
    transition.add_argument("node_id")
    transition.add_argument("status")
    artifact = command("register-artifact")
    artifact.add_argument("run_directory")
    artifact.add_argument("node_id")
    artifact.add_argument("artifact_type")
    artifact.add_argument("path")
    signal = command("signal")
    signal.add_argument("run_directory")
    signal.add_argument("name")
    signal.add_argument("value")
    propose = command("propose-rewrite")
    propose.add_argument("run_directory")
    propose.add_argument("proposal")
    apply = command("apply-rewrite")
    apply.add_argument("run_directory")
    apply.add_argument("proposal_id")
    verify = command("verify")
    verify.add_argument("run_directory")
    inspect = command("inspect")
    inspect.add_argument("run_directory")
    inspect.add_argument("--format", choices=("text", "mermaid"), required=True)
    replay = command("replay")
    replay.add_argument("run_directory")
    resume = command("resume-check")
    resume.add_argument("run_directory")
    return parser


def _validate(args: argparse.Namespace) -> CommandResult:
    graph = require_valid_graph(_read_json(Path(args.graph)))
    return CommandResult(
        {"valid": True, "graphId": graph.graph_id},
        f"Graph valid: {graph.graph_id}\n",
    )


def _init(args: argparse.Namespace) -> CommandResult:
    graph = require_valid_graph(_read_json(Path(args.graph)))
    run_id = f"run-{graph.graph_id}"
    run_directory = Path(args.run_root).resolve() / run_id
    if run_directory.exists():
        raise RewritePolicyError(f"run directory {str(run_directory)!r} already exists")
    state = RuntimeState(
        run_id=run_id,
        graph_id=graph.graph_id,
        graph_version=1,
        epoch=1,
        status=RunStatus.RUNNING,
        node_states={
            node.id: NodeRuntimeState(node.id, NodeStatus.PENDING)
            for node in graph.nodes
        },
    )
    RewriteEngine.initialize(run_directory, graph, state)
    for directory in ("node-runs", "artifacts", "runtime"):
        (run_directory / directory).mkdir(parents=True, exist_ok=True)
    _atomic_replace(
        run_directory / "policies.json",
        _json_bytes(graph.rewrite_policy.to_dict() if graph.rewrite_policy else {}),
    )
    _atomic_replace(run_directory / "artifacts.jsonl", b"")
    _atomic_replace(run_directory / "approvals.jsonl", b"")
    payload = {"runId": run_id, "runDirectory": str(run_directory), "state": state.to_dict()}
    return CommandResult(payload, f"Run initialized: {run_directory}\n")


def _status(args: argparse.Namespace) -> CommandResult:
    state, graph, store = _runtime(Path(args.run_directory))
    payload = {
        "runId": state.run_id,
        "graphName": graph.name,
        "state": state.to_dict(),
        "eventCount": len(store.read_all()),
        "threads": thread_evidence_summary(Path(args.run_directory), graph, state),
    }
    return CommandResult(payload, json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


def _ready(args: argparse.Namespace) -> CommandResult:
    run_directory = Path(args.run_directory)
    state, graph, store = _runtime(run_directory)
    registry = ArtifactRegistry(run_directory, state.run_id, store)
    try:
        registry.read_all()
    except ArtifactIntegrityError as error:
        raise RuntimeCorruptionError(f"corrupt artifact registry: {error}") from error
    nodes = get_ready_nodes(
        graph,
        state,
        artifact_registry=registry,
        approvals=_approvals(run_directory, state.run_id),
    )
    ids = [node.id for node in nodes]
    return CommandResult(
        {"readyNodeIds": ids, "count": len(ids)},
        "Ready nodes: " + (", ".join(ids) if ids else "none") + "\n",
    )


def _dispatch_preview(args: argparse.Namespace) -> CommandResult:
    run_directory = Path(args.run_directory)
    state, graph, store = _runtime(run_directory)
    registry = ArtifactRegistry(run_directory, state.run_id, store)
    nodes = preview_dispatch(
        graph,
        state,
        registry,
        _approvals(run_directory, state.run_id),
        available_slots=args.available_slots,
    )
    payload = {
        "readySubagentNodeIds": [node.id for node in nodes],
        "count": len(nodes),
        "mutated": False,
    }
    return CommandResult(payload, json.dumps(payload, indent=2) + "\n")


def _prepare_dispatch(args: argparse.Namespace) -> CommandResult:
    run_directory = Path(args.run_directory)
    state, graph, store = _runtime(run_directory)
    registry = ArtifactRegistry(run_directory, state.run_id, store)
    launches = prepare_dispatch(
        run_directory,
        graph,
        state,
        store,
        registry,
        _approvals(run_directory, state.run_id),
        available_slots=args.available_slots,
    )
    payload = {"launches": launches, "count": len(launches)}
    return CommandResult(payload, json.dumps(payload, indent=2) + "\n")


def _record_launch(args: argparse.Namespace) -> CommandResult:
    run_directory = Path(args.run_directory)
    state, graph, store = _runtime(run_directory)
    result = record_launch(
        run_directory, graph, state, store, Path(args.record)
    )
    return CommandResult(result, json.dumps(result, indent=2) + "\n")


def _ingest_return(args: argparse.Namespace) -> CommandResult:
    run_directory = Path(args.run_directory)
    state, graph, store = _runtime(run_directory)
    registry = ArtifactRegistry(run_directory, state.run_id, store)
    result = ingest_return(
        run_directory, graph, state, store, registry, Path(args.packet)
    )
    return CommandResult(result, json.dumps(result, indent=2) + "\n")


def _transition(args: argparse.Namespace) -> CommandResult:
    run_directory = Path(args.run_directory)
    persisted, graph, store = _runtime(run_directory)
    replayed = replay_events(store.read_all())
    if replayed.to_dict() != persisted.to_dict():
        raise RuntimeCorruptionError("corrupt runtime: state.json differs from event replay")
    try:
        target = NodeStatus(args.status)
    except ValueError:
        raise IllegalTransitionError(f"unknown node status {args.status!r}") from None
    nodes = {node.id: node for node in graph.nodes}
    node = nodes.get(args.node_id)
    if node is None:
        raise IllegalTransitionError(f"unknown node {args.node_id!r}")
    approvals = _approvals(run_directory, persisted.run_id)
    granted = {
        value
        for item in approvals
        if item.status.value == "granted"
        for value in (item.approval_id, item.subject_id)
    }
    incoming_approvals = {
        approval_id
        for edge in graph.edges
        if edge.enabled and edge.required and edge.target == node.id and edge.activation is not None
        for approval_id in edge.activation.approvals
    }
    registry = ArtifactRegistry(run_directory, persisted.run_id, store)
    required_inputs = [item.artifact_type for item in node.inputs if item.required]
    machine = StateMachine(run_directory, replayed, store)
    updated = machine.transition_node(
        node.id,
        target,
        max_attempts=node.budget.max_attempts if node.budget else graph.limits.default_max_attempts,
        required_inputs_exist=registry.satisfies_activation(required_inputs),
        approval_outstanding=bool(incoming_approvals - granted),
    )
    payload = {"nodeId": node.id, "nodeStatus": updated.node_states[node.id].status.value, "state": updated.to_dict()}
    return CommandResult(payload, f"Node {node.id}: {payload['nodeStatus']}\n")


def _register_artifact(args: argparse.Namespace) -> CommandResult:
    run_directory = Path(args.run_directory).resolve()
    state, graph, store = _runtime(run_directory)
    if args.node_id not in {node.id for node in graph.nodes}:
        raise ArtifactUnavailableError(f"unknown artifact owner node {args.node_id!r}")
    source = Path(args.path)
    if source.is_absolute():
        try:
            relative = source.resolve().relative_to(run_directory).as_posix()
        except ValueError as error:
            raise UnsafeArtifactPathError("artifact path escapes the run directory") from error
    else:
        relative = source.as_posix()
    registry = ArtifactRegistry(run_directory, state.run_id, store)
    artifact_id = f"art-{len(registry.read_all()) + 1:06d}"
    media_type = mimetypes.guess_type(relative)[0] or "application/octet-stream"
    artifact = registry.register(
        artifact_id=artifact_id,
        node_id=args.node_id,
        graph_version=state.graph_version,
        artifact_type=args.artifact_type,
        path=relative,
        media_type=media_type,
    )
    return CommandResult({"artifact": artifact.to_dict()}, f"Artifact registered: {artifact.artifact_id}\n")


def _signal(args: argparse.Namespace) -> CommandResult:
    state, _, store = _runtime(Path(args.run_directory))
    value = _parse_value(args.value)
    event = store.append(
        EventType.SIGNAL_OBSERVED,
        {"name": args.name, "value": value},
        state.graph_version,
    )
    return CommandResult(
        {"name": args.name, "value": value, "eventId": event.event_id},
        f"Signal observed: {args.name}\n",
    )


def _propose_rewrite(args: argparse.Namespace) -> CommandResult:
    run_directory = Path(args.run_directory)
    state, _, _ = _runtime(run_directory)
    proposal = RewriteProposal.from_dict(_read_json(Path(args.proposal)))
    RewriteEngine(run_directory, state.run_id).propose(proposal)
    return CommandResult(
        {"proposalId": proposal.proposal_id, "riskLevel": proposal.risk_level.value},
        f"Rewrite proposed: {proposal.proposal_id}\n",
    )


def _apply_rewrite(args: argparse.Namespace) -> CommandResult:
    run_directory = Path(args.run_directory)
    state, _, _ = _runtime(run_directory)
    updated = RewriteEngine(run_directory, state.run_id).apply(
        args.proposal_id,
        approvals=_approvals(run_directory, state.run_id),
    )
    return CommandResult(
        {"proposalId": args.proposal_id, "graphVersion": updated.graph_version, "state": updated.to_dict()},
        f"Rewrite applied: {args.proposal_id}, graph version {updated.graph_version}\n",
    )


def _verify(args: argparse.Namespace) -> CommandResult:
    try:
        result = Verifier(Path(args.run_directory)).verify()
    except ValueError as error:
        raise RuntimeCorruptionError(f"corrupt runtime during verification: {error}") from error
    code = EXIT_POLICY if result.status == VerificationStatus.FAIL else EXIT_OK
    return CommandResult({"verification": result.to_dict()}, render_text(result), code)


def _inspect(args: argparse.Namespace) -> CommandResult:
    run_directory = Path(args.run_directory)
    state, graph, store = _runtime(run_directory)
    if args.format == "text":
        lines = [
            f"Run: {state.run_id}",
            f"Graph: {graph.name} (version {state.graph_version})",
            f"Status: {state.status.value}",
            f"Events: {len(store.read_all())}",
            "Nodes:",
        ]
        lines.extend(
            f"- {node_id}: {runtime.status.value}"
            for node_id, runtime in sorted(state.node_states.items())
        )
        threads = thread_evidence_summary(run_directory, graph, state)
        if threads:
            lines.append("Fresh threads:")
            lines.extend(
                f"- {item['nodeId']} attempt {item['attempt']}: {item['nodeStatus']}; "
                f"thread={item['threadMode']}; agent={item['agentId'] or 'unrecorded'}; "
                f"return={item['returnStatus'] or 'pending'}"
                for item in threads
            )
        report = "\n".join(lines) + "\n"
    else:
        verification_path = run_directory / "verification.json"
        if verification_path.exists():
            verification = VerificationResult.from_dict(_read_json(verification_path, runtime=True))
        else:
            verification = VerificationResult(
                VerificationStatus.CONDITIONAL_PASS,
                "1970-01-01T00:00:00Z",
                issues=["terminal verification has not run"],
            )
        report = render_mermaid(graph, state, verification)
    return CommandResult({"format": args.format, "report": report}, report)


def _replay(args: argparse.Namespace) -> CommandResult:
    persisted, _, store = _runtime(Path(args.run_directory))
    reconstructed = replay_events(store.read_all())
    matches = reconstructed.to_dict() == persisted.to_dict()
    if not matches:
        raise RuntimeCorruptionError("corrupt runtime: state.json differs from event replay")
    return CommandResult(
        {"state": reconstructed.to_dict(), "matchesPersistedState": True},
        json.dumps(reconstructed.to_dict(), indent=2, ensure_ascii=False) + "\n",
    )


def _resume_check(args: argparse.Namespace) -> CommandResult:
    run_directory = Path(args.run_directory)
    persisted, graph, store = _runtime(run_directory)
    reconstructed = replay_events(store.read_all())
    if reconstructed.to_dict() != persisted.to_dict():
        raise RuntimeCorruptionError("corrupt runtime: state.json differs from event replay")
    version_path = run_directory / "graph-versions" / f"v{persisted.graph_version:04d}.json"
    version = Graph.from_dict(_read_json(version_path, runtime=True))
    if version.to_dict() != graph.to_dict():
        raise RuntimeCorruptionError("corrupt runtime: current graph differs from immutable version")
    thread_issues = thread_history_issues(run_directory, graph, persisted)
    if thread_issues:
        raise PacketValidationError("; ".join(thread_issues))
    return CommandResult(
        {"resumable": True, "graphVersion": persisted.graph_version, "eventCount": len(store.read_all())},
        "Resume check: resumable\n",
    )


_HANDLERS = {
    "validate": _validate,
    "init": _init,
    "status": _status,
    "ready": _ready,
    "dispatch-preview": _dispatch_preview,
    "prepare-dispatch": _prepare_dispatch,
    "record-launch": _record_launch,
    "ingest-return": _ingest_return,
    "transition": _transition,
    "register-artifact": _register_artifact,
    "signal": _signal,
    "propose-rewrite": _propose_rewrite,
    "apply-rewrite": _apply_rewrite,
    "verify": _verify,
    "inspect": _inspect,
    "replay": _replay,
    "resume-check": _resume_check,
}


def _dispatch(args: argparse.Namespace) -> CommandResult:
    return _HANDLERS[args.command](args)


def _emit_error(message: str, code: int, json_output: bool) -> None:
    if json_output:
        print(json.dumps({"ok": False, "exitCode": code, "error": message}, sort_keys=True))
    else:
        print(f"violated rule: {message}", file=sys.stderr)


def main(argv: Optional[Sequence[str]] = None) -> int:
    arguments = list(argv) if argv is not None else sys.argv[1:]
    json_requested = "--json" in arguments
    try:
        args = _parser().parse_args(arguments)
        result = _dispatch(args)
        if args.json_output:
            envelope = {"ok": result.exit_code == 0, **result.payload}
            if result.exit_code:
                envelope["exitCode"] = result.exit_code
            print(json.dumps(envelope, sort_keys=True, ensure_ascii=False, allow_nan=False))
        else:
            stream = sys.stderr if result.exit_code else sys.stdout
            print(result.human, end="", file=stream)
        return result.exit_code
    except ApprovalRequiredError as error:
        _emit_error(str(error), EXIT_APPROVAL, json_requested)
        return EXIT_APPROVAL
    except (RuntimeCorruptionError, VerificationCorruptionError, EventChainError, ArtifactIntegrityError) as error:
        _emit_error(str(error), EXIT_CORRUPT, json_requested)
        return EXIT_CORRUPT
    except (
        GraphValidationError,
        RewritePolicyError,
        RewriteError,
        RewriteValidationError,
        VersionMismatchError,
        IllegalTransitionError,
        RetryRejectedError,
        ArtifactUnavailableError,
        UnsafeArtifactPathError,
        PacketValidationError,
        ValueError,
    ) as error:
        _emit_error(str(error), EXIT_POLICY, json_requested)
        return EXIT_POLICY
    except Exception:
        _emit_error("unexpected internal failure", EXIT_INTERNAL, json_requested)
        return EXIT_INTERNAL


if __name__ == "__main__":
    raise SystemExit(main())
