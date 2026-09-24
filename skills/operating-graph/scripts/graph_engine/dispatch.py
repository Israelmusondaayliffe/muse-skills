"""Bounded fresh-thread packet preparation, launch attestation, and return ingestion."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import mimetypes
import os
from pathlib import Path, PurePosixPath
import re
import tempfile
from typing import Any, Iterable, Optional, Sequence

from .artifacts import ArtifactRegistry, resolve_artifact_path
from .constants import Confidence, EventType, ExecutionMode, NodeStatus
from .events import EventStore
from .models import Approval, Evidence, Graph, Node, RuntimeState
from .scheduler import get_ready_nodes
from .state import StateMachine


PROTOCOL_VERSION = 1
TASK_PACKET_TYPE = "NodeTaskPacket"
LAUNCH_RECORD_TYPE = "ThreadLaunchRecord"
RETURN_PACKET_TYPE = "NodeReturnPacket"
DISPATCH_RECEIPT_TYPE = "DispatchReceipt"
LAUNCH_RECEIPT_TYPE = "LaunchReceipt"
RETURN_STATUSES = frozenset({"succeeded", "blocked", "failed", "escalate"})
CRITERION_RESULTS = frozenset({"met", "not_met", "blocked", "failed", "escalate"})


class PacketValidationError(ValueError):
    """Raised when a thread packet or runtime attestation is not trustworthy."""


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _timestamp(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.endswith("Z"):
        raise PacketValidationError(f"{label} must be a canonical UTC timestamp")
    try:
        datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as error:
        raise PacketValidationError(f"{label} must be a canonical UTC timestamp") from error
    return value


def _object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise PacketValidationError(f"{label} must be an object")
    return value


def _string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise PacketValidationError(f"{label} must be a non-empty string")
    return value


def _integer(value: Any, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise PacketValidationError(f"{label} must be a positive integer")
    return value


def _list(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise PacketValidationError(f"{label} must be an array")
    return value


def _json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
        + "\n"
    ).encode("utf-8")


def _atomic_replace(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Optional[Path] = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix=f".{path.name}.", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(_json_bytes(value))
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_json(path: Path, label: str) -> dict[str, Any]:
    try:
        return _object(json.loads(Path(path).read_text(encoding="utf-8")), label)
    except (OSError, json.JSONDecodeError) as error:
        raise PacketValidationError(f"cannot read {label}: {error}") from error


def _run_relative_path(run_directory: Path, value: Any, label: str) -> tuple[str, Path]:
    text = _string(value, label)
    if "\\" in text or any(ord(character) < 32 or ord(character) == 127 for character in text):
        raise PacketValidationError(f"{label} is not a safe POSIX path")
    relative = PurePosixPath(text)
    if relative.is_absolute() or ".." in relative.parts:
        raise PacketValidationError(f"{label} escapes the run directory")
    root = Path(run_directory).resolve()
    candidate = (root / Path(*relative.parts)).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as error:
        raise PacketValidationError(f"{label} escapes the run directory") from error
    return relative.as_posix(), candidate


def _owned_write_path(run_directory: Path, node_id: str, attempt: int, value: Any, label: str) -> tuple[str, Path]:
    relative, candidate = _run_relative_path(run_directory, value, label)
    parts = PurePosixPath(relative).parts
    worker_root = ("node-runs", node_id, f"attempt-{attempt}", "worker")
    artifact_root = ("artifacts", node_id)
    allowed = (
        len(parts) >= 5 and parts[:4] == worker_root
    ) or (
        len(parts) >= 3 and parts[:2] == artifact_root
    )
    if not allowed:
        raise PacketValidationError(f"{label} is outside node {node_id!r} write authority")
    return relative, candidate


def _attempt_paths(run_directory: Path, node_id: str, attempt: int) -> dict[str, Path]:
    attempt_directory = Path(run_directory) / "node-runs" / node_id / f"attempt-{attempt}"
    worker_directory = attempt_directory / "worker"
    return {
        "directory": attempt_directory,
        "worker_directory": worker_directory,
        "task": attempt_directory / "task-packet.json",
        "dispatch_receipt": attempt_directory / "dispatch-receipt.json",
        "launch": attempt_directory / "thread-launch.json",
        "launch_receipt": attempt_directory / "launch-receipt.json",
        "return": worker_directory / "return-packet.json",
    }


def _task_name(run_id: str, node_id: str, attempt: int, run_directory: Path) -> str:
    run_token = hashlib.sha256(str(Path(run_directory).resolve()).encode("utf-8")).hexdigest()[:8]
    value = f"og_{run_id}_{run_token}_{node_id}_{attempt}".lower()
    return "_".join(part for part in re.split(r"[^a-z0-9]+", value) if part)


def _launch_spec(paths: dict[str, Path], state: RuntimeState, node: Node, attempt: int, run_directory: Path) -> dict[str, Any]:
    return {
        "tool": "subagent.spawn",
        "taskName": _task_name(state.run_id, node.id, attempt, run_directory),
        "threadMode": "fresh",
        "model": node.execution.model_hint,
        "message": (
            f"Execute only the bounded Operating Graph node packet at {paths['task'].resolve()}. "
            f"Write node-owned artifacts only under the packet's allowed roots and return a "
            f"{RETURN_PACKET_TYPE} at {paths['return'].resolve()}. Do not spawn workers, approve, "
            "integrate, answer the user, or issue a terminal verdict. Before writing the return "
            "packet, wait for the controller-owned thread-launch.json in the attempt directory "
            "and bind the return to its exact agentId and SHA-256."
        ),
    }


def _required_inputs(node: Node, registry: ArtifactRegistry) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for requirement in node.inputs:
        artifacts = registry.active_artifacts(requirement.artifact_type)
        if requirement.required and not artifacts:
            raise PacketValidationError(
                f"node {node.id!r} is missing required artifact type {requirement.artifact_type!r}"
            )
        records.extend(item.to_dict() for item in artifacts)
    records.sort(key=lambda item: (str(item["type"]), str(item["artifactId"])))
    return records


def _task_packet(run_directory: Path, graph: Graph, state: RuntimeState, node: Node, registry: ArtifactRegistry, attempt: int) -> dict[str, Any]:
    paths = _attempt_paths(run_directory, node.id, attempt)
    dependencies = sorted(
        edge.source
        for edge in graph.edges
        if edge.enabled and edge.required and edge.target == node.id
    )
    return {
        "packetType": TASK_PACKET_TYPE,
        "protocolVersion": PROTOCOL_VERSION,
        "runId": state.run_id,
        "graphId": graph.graph_id,
        "graphVersion": state.graph_version,
        "epoch": state.epoch,
        "nodeId": node.id,
        "attempt": attempt,
        "task": {
            "kind": node.kind.value,
            "objective": node.purpose,
            "dependencies": dependencies,
        },
        "requiredInputs": _required_inputs(node, registry),
        "successCriteria": list(node.success_criteria),
        "expectedOutputs": [item.to_dict() for item in node.outputs],
        "execution": {
            "mode": node.execution.mode.value,
            "skill": node.execution.skill,
            "modelHint": node.execution.model_hint,
        },
        "authorization": {
            "maySpawnWorkers": False,
            "mayApprove": False,
            "mayIntegrate": False,
            "mayUpdateControllerState": False,
            "mayAnswerUser": False,
            "mayIssueTerminalVerdict": False,
        },
        "scope": {
            "allowedWriteRoots": [
                str(paths["worker_directory"].resolve()),
                str((Path(run_directory) / "artifacts" / node.id).resolve()),
            ],
            "returnPacketPath": str(paths["return"].resolve()),
            "enforcement": {
                "mode": "controller-validated-authority",
                "hostFilesystemSandbox": False,
                "tamperDetection": ["dispatch-receipt", "launch-receipt", "declared-write-validation"],
            },
        },
        "context": {
            "delivery": "bounded_packet_only",
            "includeParentTranscript": False,
            "includeHiddenReasoning": False,
            "referencePaths": [
                str((Path(run_directory) / item["path"]).resolve())
                for item in _required_inputs(node, registry)
            ],
        },
        "limits": {
            "maxAttempts": node.budget.max_attempts if node.budget else graph.limits.default_max_attempts,
            "workUnits": node.budget.work_units if node.budget else 1,
            "localLoopIterations": node.local_loop.max_iterations if node.local_loop else 1,
        },
    }


def preview_dispatch(
    graph: Graph,
    state: RuntimeState,
    registry: ArtifactRegistry,
    approvals: Sequence[Approval],
    *,
    available_slots: Optional[int] = None,
) -> tuple[Node, ...]:
    ready = get_ready_nodes(
        graph,
        state,
        artifact_registry=registry,
        approvals=approvals,
        detected_available_worker_slots=available_slots,
    )
    return tuple(node for node in ready if node.execution.mode == ExecutionMode.SUBAGENT)


def prepare_dispatch(
    run_directory: Path,
    graph: Graph,
    state: RuntimeState,
    store: EventStore,
    registry: ArtifactRegistry,
    approvals: Sequence[Approval],
    *,
    available_slots: Optional[int] = None,
    timestamp: Optional[str] = None,
) -> list[dict[str, Any]]:
    selected = preview_dispatch(
        graph, state, registry, approvals, available_slots=available_slots
    )
    machine = StateMachine(Path(run_directory), state, store)
    launches: list[dict[str, Any]] = []
    for node in selected:
        runtime = machine.state.node_states[node.id]
        attempt = runtime.attempts + 1
        paths = _attempt_paths(run_directory, node.id, attempt)
        packet = _task_packet(run_directory, graph, machine.state, node, registry, attempt)
        _atomic_replace(paths["task"], packet)
        packet_hash = sha256_file(paths["task"])
        launch_spec = _launch_spec(paths, machine.state, node, attempt, run_directory)
        _atomic_replace(
            paths["dispatch_receipt"],
            {
                "packetType": DISPATCH_RECEIPT_TYPE,
                "protocolVersion": PROTOCOL_VERSION,
                "runId": machine.state.run_id,
                "graphVersion": machine.state.graph_version,
                "epoch": machine.state.epoch,
                "nodeId": node.id,
                "attempt": attempt,
                "taskPacketPath": paths["task"].relative_to(run_directory).as_posix(),
                "taskPacketSha256": packet_hash,
                "launchSpec": launch_spec,
                "launchSpecSha256": hashlib.sha256(_json_bytes(launch_spec)).hexdigest(),
                "recordedAt": timestamp or _utc_now(),
            },
        )
        try:
            machine.transition_node(
                node.id,
                NodeStatus.READY,
                timestamp=timestamp,
                max_attempts=node.budget.max_attempts if node.budget else graph.limits.default_max_attempts,
                required_inputs_exist=True,
                approval_outstanding=False,
            )
        except BaseException:
            paths["task"].unlink(missing_ok=True)
            paths["dispatch_receipt"].unlink(missing_ok=True)
            raise
        store.append(
            EventType.THREAD_DISPATCH_PREPARED,
            {
                "nodeId": node.id,
                "attempt": attempt,
                "taskPacketPath": paths["task"].relative_to(run_directory).as_posix(),
                "taskPacketSha256": packet_hash,
            },
            machine.state.graph_version,
            timestamp=timestamp,
        )
        launches.append(
            {
                "nodeId": node.id,
                "attempt": attempt,
                "taskPacketPath": str(paths["task"].resolve()),
                "taskPacketSha256": packet_hash,
                "launchSpec": launch_spec,
            }
        )
    return launches


def _validate_task_binding(run_directory: Path, graph: Graph, state: RuntimeState, node: Node, attempt: int, packet_path_value: Any, packet_hash_value: Any) -> tuple[dict[str, Any], Path, str]:
    paths = _attempt_paths(run_directory, node.id, attempt)
    expected_relative = paths["task"].relative_to(run_directory).as_posix()
    supplied_relative, supplied_path = _run_relative_path(run_directory, packet_path_value, "taskPacketPath")
    if supplied_relative != expected_relative or supplied_path != paths["task"].resolve():
        raise PacketValidationError("taskPacketPath does not identify the canonical node attempt packet")
    expected_hash = _string(packet_hash_value, "taskPacketSha256")
    receipt_path = paths["dispatch_receipt"]
    if not receipt_path.is_file():
        raise PacketValidationError("canonical dispatch receipt is missing")
    receipt = _read_json(receipt_path, DISPATCH_RECEIPT_TYPE)
    receipt_binding = {
        "packetType": DISPATCH_RECEIPT_TYPE,
        "protocolVersion": PROTOCOL_VERSION,
        "runId": state.run_id,
        "graphVersion": state.graph_version,
        "epoch": state.epoch,
        "nodeId": node.id,
        "attempt": attempt,
        "taskPacketPath": expected_relative,
    }
    if any(receipt.get(key) != value for key, value in receipt_binding.items()):
        raise PacketValidationError("dispatch receipt does not match the current node attempt")
    anchored_hash = _string(receipt.get("taskPacketSha256"), "DispatchReceipt.taskPacketSha256")
    if expected_hash != anchored_hash:
        raise PacketValidationError("taskPacketSha256 does not match the dispatch receipt")
    if not supplied_path.is_file() or sha256_file(supplied_path) != anchored_hash:
        raise PacketValidationError("taskPacketSha256 does not match the canonical packet")
    packet = _read_json(supplied_path, "NodeTaskPacket")
    expected = {
        "packetType": TASK_PACKET_TYPE,
        "protocolVersion": PROTOCOL_VERSION,
        "runId": state.run_id,
        "graphId": graph.graph_id,
        "graphVersion": state.graph_version,
        "epoch": state.epoch,
        "nodeId": node.id,
        "attempt": attempt,
    }
    for key, value in expected.items():
        if packet.get(key) != value:
            raise PacketValidationError(f"NodeTaskPacket.{key} does not match current runtime state")
    return packet, supplied_path, expected_hash


def record_launch(
    run_directory: Path,
    graph: Graph,
    state: RuntimeState,
    store: EventStore,
    record_path: Path,
    *,
    timestamp: Optional[str] = None,
) -> dict[str, Any]:
    record = _read_json(record_path, LAUNCH_RECORD_TYPE)
    if record.get("packetType") != LAUNCH_RECORD_TYPE or record.get("protocolVersion") != PROTOCOL_VERSION:
        raise PacketValidationError("launch record type or protocolVersion is invalid")
    node_id = _string(record.get("nodeId"), "ThreadLaunchRecord.nodeId")
    nodes = {node.id: node for node in graph.nodes}
    node = nodes.get(node_id)
    if node is None or node.execution.mode != ExecutionMode.SUBAGENT:
        raise PacketValidationError("launch record node is not a declared subagent node")
    attempt = _integer(record.get("attempt"), "ThreadLaunchRecord.attempt")
    runtime = state.node_states.get(node_id)
    if runtime is None or runtime.status != NodeStatus.READY or attempt != runtime.attempts + 1:
        raise PacketValidationError("launch record does not match a ready node attempt")
    for key, value in {
        "runId": state.run_id,
        "graphVersion": state.graph_version,
        "epoch": state.epoch,
    }.items():
        if record.get(key) != value:
            raise PacketValidationError(f"ThreadLaunchRecord.{key} does not match current runtime state")
    _validate_task_binding(
        run_directory, graph, state, node, attempt,
        record.get("taskPacketPath"), record.get("taskPacketSha256"),
    )
    request = _object(record.get("request"), "ThreadLaunchRecord.request")
    if request.get("tool") != "subagent.spawn" or request.get("threadMode") != "fresh":
        raise PacketValidationError("thread launch must be a fresh subagent.spawn launch")
    receipt = _read_json(_attempt_paths(run_directory, node_id, attempt)["dispatch_receipt"], DISPATCH_RECEIPT_TYPE)
    launch_spec = _object(receipt.get("launchSpec"), "DispatchReceipt.launchSpec")
    spec_hash = _string(receipt.get("launchSpecSha256"), "DispatchReceipt.launchSpecSha256")
    if hashlib.sha256(_json_bytes(launch_spec)).hexdigest() != spec_hash:
        raise PacketValidationError("dispatch receipt launch specification hash is invalid")
    if any(request.get(key) != value for key, value in launch_spec.items()):
        raise PacketValidationError("thread launch request does not match the prepared launch specification")
    _timestamp(request.get("requestedAt"), "ThreadLaunchRecord.request.requestedAt")
    if node.execution.model_hint is not None and request.get("model") != node.execution.model_hint:
        raise PacketValidationError("thread launch model does not match the node modelHint")
    response = _object(record.get("response"), "ThreadLaunchRecord.response")
    successful = response.get("successful")
    if not isinstance(successful, bool):
        raise PacketValidationError("ThreadLaunchRecord.response.successful must be boolean")
    _timestamp(response.get("respondedAt"), "ThreadLaunchRecord.response.respondedAt")
    machine = StateMachine(Path(run_directory), state, store)
    canonical_path = _attempt_paths(run_directory, node_id, attempt)["launch"]
    _atomic_replace(canonical_path, record)
    launch_hash = sha256_file(canonical_path)
    receipt_path = _attempt_paths(run_directory, node_id, attempt)["launch_receipt"]
    _atomic_replace(
        receipt_path,
        {
            "packetType": LAUNCH_RECEIPT_TYPE,
            "protocolVersion": PROTOCOL_VERSION,
            "runId": state.run_id,
            "graphVersion": state.graph_version,
            "epoch": state.epoch,
            "nodeId": node_id,
            "attempt": attempt,
            "launchRecordPath": canonical_path.relative_to(run_directory).as_posix(),
            "launchRecordSha256": launch_hash,
            "recordedAt": timestamp or _utc_now(),
        },
    )
    if successful:
        _string(response.get("agentId"), "ThreadLaunchRecord.response.agentId")
        _string(response.get("canonicalTaskName"), "ThreadLaunchRecord.response.canonicalTaskName")
        updated = machine.transition_node(node_id, NodeStatus.RUNNING, timestamp=timestamp)
        event_type = EventType.THREAD_LAUNCHED
    else:
        error = _string(response.get("error"), "ThreadLaunchRecord.response.error")
        updated = machine.transition_node(node_id, NodeStatus.BLOCKED, blocker=error, timestamp=timestamp)
        event_type = EventType.THREAD_LAUNCH_FAILED
    store.append(
        event_type,
        {
            "nodeId": node_id,
            "attempt": attempt,
            "launchRecordPath": canonical_path.relative_to(run_directory).as_posix(),
            "launchRecordSha256": launch_hash,
        },
        updated.graph_version,
        timestamp=timestamp,
    )
    return {
        "nodeId": node_id,
        "attempt": attempt,
        "status": updated.node_states[node_id].status.value,
        "launchRecordPath": str(canonical_path.resolve()),
    }


def _validate_evidence(run_directory: Path, node_id: str, attempt: int, evidence: Iterable[Any]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for index, value in enumerate(evidence):
        record = _object(value, f"evidence[{index}]")
        relative, path = _owned_write_path(run_directory, node_id, attempt, record.get("path"), f"evidence[{index}].path")
        digest = _string(record.get("sha256"), f"evidence[{index}].sha256")
        _string(record.get("kind"), f"evidence[{index}].kind")
        if not path.is_file() or sha256_file(path) != digest:
            raise PacketValidationError(f"evidence[{index}] path or SHA-256 is invalid")
        records.append({**record, "path": relative})
    return records


def ingest_return(
    run_directory: Path,
    graph: Graph,
    state: RuntimeState,
    store: EventStore,
    registry: ArtifactRegistry,
    return_path: Path,
    *,
    timestamp: Optional[str] = None,
) -> dict[str, Any]:
    returned = _read_json(return_path, RETURN_PACKET_TYPE)
    if returned.get("packetType") != RETURN_PACKET_TYPE or returned.get("protocolVersion") != PROTOCOL_VERSION:
        raise PacketValidationError("return packet type or protocolVersion is invalid")
    node_id = _string(returned.get("nodeId"), "NodeReturnPacket.nodeId")
    nodes = {node.id: node for node in graph.nodes}
    node = nodes.get(node_id)
    if node is None or node.execution.mode != ExecutionMode.SUBAGENT:
        raise PacketValidationError("return packet node is not a declared subagent node")
    attempt = _integer(returned.get("attempt"), "NodeReturnPacket.attempt")
    runtime = state.node_states.get(node_id)
    if runtime is None or runtime.status != NodeStatus.RUNNING or attempt != runtime.attempts:
        raise PacketValidationError("return packet does not match the running node attempt")
    for key, value in {
        "runId": state.run_id,
        "graphVersion": state.graph_version,
        "epoch": state.epoch,
    }.items():
        if returned.get(key) != value:
            raise PacketValidationError(f"NodeReturnPacket.{key} does not match current runtime state")
    _validate_task_binding(
        run_directory, graph, state, node, attempt,
        returned.get("taskPacketPath"), returned.get("taskPacketSha256"),
    )
    paths = _attempt_paths(run_directory, node_id, attempt)
    launch_relative, launch_path = _run_relative_path(run_directory, returned.get("launchRecordPath"), "launchRecordPath")
    if launch_path != paths["launch"].resolve() or not launch_path.is_file():
        raise PacketValidationError("launchRecordPath is not the canonical successful launch record")
    launch_hash = _string(returned.get("launchRecordSha256"), "launchRecordSha256")
    receipt_path = paths["launch_receipt"]
    if not receipt_path.is_file():
        raise PacketValidationError("canonical launch receipt is missing")
    receipt = _read_json(receipt_path, LAUNCH_RECEIPT_TYPE)
    anchored_launch_hash = _string(receipt.get("launchRecordSha256"), "LaunchReceipt.launchRecordSha256")
    expected_launch_binding = {
        "packetType": LAUNCH_RECEIPT_TYPE,
        "protocolVersion": PROTOCOL_VERSION,
        "runId": state.run_id,
        "graphVersion": state.graph_version,
        "epoch": state.epoch,
        "nodeId": node_id,
        "attempt": attempt,
        "launchRecordPath": paths["launch"].relative_to(run_directory).as_posix(),
    }
    if any(receipt.get(key) != value for key, value in expected_launch_binding.items()):
        raise PacketValidationError("launch receipt does not match the current node attempt")
    if launch_hash != anchored_launch_hash or sha256_file(launch_path) != anchored_launch_hash:
        raise PacketValidationError("launchRecordSha256 does not match the launch record")
    launch = _read_json(launch_path, LAUNCH_RECORD_TYPE)
    response = _object(launch.get("response"), "ThreadLaunchRecord.response")
    if response.get("successful") is not True or returned.get("agentId") != response.get("agentId"):
        raise PacketValidationError("return packet agentId does not match the successful launch")
    status = _string(returned.get("status"), "NodeReturnPacket.status")
    if status not in RETURN_STATUSES:
        raise PacketValidationError("NodeReturnPacket.status is invalid")
    _string(returned.get("summary"), "NodeReturnPacket.summary")
    authority = _object(returned.get("authority"), "NodeReturnPacket.authority")
    prohibited = (
        "maySpawnWorkers", "mayApprove", "mayIntegrate", "mayUpdateControllerState",
        "mayAnswerUser", "mayIssueTerminalVerdict",
    )
    if any(authority.get(key) is not False for key in prohibited):
        raise PacketValidationError("NodeReturnPacket authority must deny every controller-only action")
    actual_write_paths = _list(returned.get("actualWritePaths"), "NodeReturnPacket.actualWritePaths")
    for index, value in enumerate(actual_write_paths):
        _owned_write_path(run_directory, node_id, attempt, value, f"actualWritePaths[{index}]")
    evidence = _validate_evidence(
        run_directory, node_id, attempt,
        _list(returned.get("evidence"), "NodeReturnPacket.evidence"),
    )
    evidence_paths = {item["path"] for item in evidence}
    criteria = _list(returned.get("criteria"), "NodeReturnPacket.criteria")
    expected_criteria = list(node.success_criteria)
    if len(criteria) != len(expected_criteria):
        raise PacketValidationError("NodeReturnPacket.criteria must cover every node success criterion exactly once")
    criterion_results: list[str] = []
    seen_criteria: set[str] = set()
    for index, value in enumerate(criteria):
        item = _object(value, f"criteria[{index}]")
        criterion = _string(item.get("criterion"), f"criteria[{index}].criterion")
        result = _string(item.get("result"), f"criteria[{index}].result")
        if criterion not in expected_criteria or criterion in seen_criteria or result not in CRITERION_RESULTS:
            raise PacketValidationError(f"criteria[{index}] has an invalid criterion or result")
        cited = _list(item.get("evidencePaths"), f"criteria[{index}].evidencePaths")
        if any(path not in evidence_paths for path in cited):
            raise PacketValidationError(f"criteria[{index}] cites unvalidated evidence")
        seen_criteria.add(criterion)
        criterion_results.append(result)
    if status == "succeeded" and any(result != "met" for result in criterion_results):
        raise PacketValidationError("a succeeded return requires every criterion result to be met")
    if status != "succeeded" and status not in criterion_results:
        raise PacketValidationError(f"status {status!r} requires matching criterion evidence")
    artifact_records = _list(returned.get("artifacts"), "NodeReturnPacket.artifacts")
    prepared_artifacts: list[dict[str, Any]] = []
    for index, value in enumerate(artifact_records):
        item = _object(value, f"artifacts[{index}]")
        artifact_type = _string(item.get("artifactType"), f"artifacts[{index}].artifactType")
        relative = _string(item.get("path"), f"artifacts[{index}].path")
        resolved = resolve_artifact_path(run_directory, node_id, relative)
        digest = _string(item.get("sha256"), f"artifacts[{index}].sha256")
        if not resolved.is_file() or sha256_file(resolved) != digest:
            raise PacketValidationError(f"artifacts[{index}] path or SHA-256 is invalid")
        prepared_artifacts.append(
            {
                "artifactType": artifact_type,
                "path": relative,
                "mediaType": item.get("mediaType") or mimetypes.guess_type(relative)[0] or "application/octet-stream",
            }
        )
    required_outputs = {item.artifact_type for item in node.outputs if item.required}
    returned_outputs = {item["artifactType"] for item in prepared_artifacts}
    if status == "succeeded" and not required_outputs.issubset(returned_outputs):
        raise PacketValidationError("a succeeded return is missing required node outputs")
    canonical_relative, canonical_return = _owned_write_path(
        run_directory,
        node_id,
        attempt,
        paths["return"].relative_to(run_directory).as_posix(),
        "canonical return packet",
    )
    supplied = Path(return_path).resolve()
    if supplied != canonical_return:
        raise PacketValidationError("NodeReturnPacket must be written to the canonical attempt path")
    _atomic_replace(canonical_return, returned)
    registered = []
    provenance = [
        Evidence(item["path"], f"Validated {item['kind']} for node {node_id}.", Confidence.HIGH)
        for item in evidence
    ]
    existing_count = len(registry.read_all())
    for offset, artifact in enumerate(prepared_artifacts, 1):
        registered.append(
            registry.register(
                artifact_id=f"art-{existing_count + offset:06d}",
                node_id=node_id,
                graph_version=state.graph_version,
                artifact_type=artifact["artifactType"],
                path=artifact["path"],
                media_type=artifact["mediaType"],
                evidence=provenance,
                timestamp=timestamp,
            )
        )
    store.append(
        EventType.NODE_RETURN_INGESTED,
        {
            "nodeId": node_id,
            "attempt": attempt,
            "status": status,
            "returnPacketPath": canonical_relative,
            "returnPacketSha256": sha256_file(canonical_return),
            "artifactIds": [item.artifact_id for item in registered],
        },
        state.graph_version,
        timestamp=timestamp,
    )
    target = {
        "succeeded": NodeStatus.SUCCEEDED,
        "failed": NodeStatus.FAILED,
        "blocked": NodeStatus.BLOCKED,
        "escalate": NodeStatus.BLOCKED,
    }[status]
    machine = StateMachine(Path(run_directory), state, store)
    updated = machine.transition_node(
        node_id,
        target,
        timestamp=timestamp,
        error=None if target != NodeStatus.FAILED else returned["summary"],
        blocker=None if target not in (NodeStatus.BLOCKED,) else returned["summary"],
    )
    return {
        "nodeId": node_id,
        "attempt": attempt,
        "returnStatus": status,
        "nodeStatus": updated.node_states[node_id].status.value,
        "artifactIds": [item.artifact_id for item in registered],
        "returnPacketPath": str(canonical_return),
    }


def thread_history_issues(run_directory: Path, graph: Graph, state: RuntimeState) -> list[str]:
    issues: list[str] = []
    for node in graph.nodes:
        runtime = state.node_states.get(node.id)
        if node.execution.mode != ExecutionMode.SUBAGENT or runtime is None:
            continue
        if runtime.attempts == 0:
            continue
        paths = _attempt_paths(run_directory, node.id, runtime.attempts)
        for key in ("task", "dispatch_receipt", "launch", "launch_receipt"):
            if not paths[key].is_file():
                issues.append(f"subagent node {node.id!r} attempt {runtime.attempts} lacks {key} evidence")
        if runtime.status == NodeStatus.SUCCEEDED and not paths["return"].is_file():
            issues.append(f"succeeded subagent node {node.id!r} lacks a validated return packet")
        packet: dict[str, Any] = {}
        launch: dict[str, Any] = {}
        returned: dict[str, Any] = {}
        if paths["task"].is_file():
            packet = _read_json(paths["task"], TASK_PACKET_TYPE)
            if runtime.status in (NodeStatus.READY, NodeStatus.RUNNING) and packet.get("graphVersion") != state.graph_version:
                issues.append(f"active subagent node {node.id!r} task packet is stale for graph version {state.graph_version}")
        if paths["launch"].is_file():
            launch = _read_json(paths["launch"], LAUNCH_RECORD_TYPE)
            request = launch.get("request", {})
            if request.get("tool") != "subagent.spawn" or request.get("threadMode") != "fresh":
                issues.append(f"subagent node {node.id!r} launch is not a fresh subagent thread")
        if paths["return"].is_file():
            returned = _read_json(paths["return"], RETURN_PACKET_TYPE)
        bound_versions = {
            record.get("graphVersion")
            for record in (packet, launch, returned)
            if record
        }
        if len(bound_versions) > 1:
            issues.append(f"subagent node {node.id!r} attempt {runtime.attempts} has mismatched graph-version evidence")
    return sorted(set(issues))


def thread_evidence_summary(run_directory: Path, graph: Graph, state: RuntimeState) -> list[dict[str, Any]]:
    """Return a read-only summary of canonical fresh-thread evidence."""
    records: list[dict[str, Any]] = []
    for node in sorted(graph.nodes, key=lambda item: item.id):
        runtime = state.node_states.get(node.id)
        if node.execution.mode != ExecutionMode.SUBAGENT or runtime is None or runtime.attempts == 0:
            continue
        paths = _attempt_paths(run_directory, node.id, runtime.attempts)
        task = _read_json(paths["task"], TASK_PACKET_TYPE) if paths["task"].is_file() else {}
        launch = _read_json(paths["launch"], LAUNCH_RECORD_TYPE) if paths["launch"].is_file() else {}
        returned = _read_json(paths["return"], RETURN_PACKET_TYPE) if paths["return"].is_file() else {}
        response = launch.get("response", {}) if isinstance(launch.get("response"), dict) else {}
        request = launch.get("request", {}) if isinstance(launch.get("request"), dict) else {}
        records.append(
            {
                "nodeId": node.id,
                "attempt": runtime.attempts,
                "nodeStatus": runtime.status.value,
                "graphVersion": task.get("graphVersion"),
                "threadMode": request.get("threadMode"),
                "agentId": response.get("agentId"),
                "returnStatus": returned.get("status"),
                "taskPacketPresent": bool(task),
                "launchRecordPresent": bool(launch),
                "returnPacketPresent": bool(returned),
            }
        )
    return records


__all__ = [
    "LAUNCH_RECORD_TYPE",
    "PROTOCOL_VERSION",
    "PacketValidationError",
    "RETURN_PACKET_TYPE",
    "TASK_PACKET_TYPE",
    "ingest_return",
    "prepare_dispatch",
    "preview_dispatch",
    "record_launch",
    "sha256_file",
    "thread_history_issues",
]
