#!/usr/bin/env python3
"""Deterministic state, validation, and checkpoint primitives for LoopKit."""

from __future__ import annotations

import contextlib
import datetime as dt
import hashlib
import json
import os
import re
import tempfile
import time
from pathlib import Path
from typing import Any, Iterator


SCHEMA_VERSION = 1
TERMINAL_STATUSES = {"completed", "exhausted", "failed", "cancelled"}
ACTIVE_STATUSES = {"running", "waiting_input", "scheduled", "blocked"}
ALLOWED_TRANSITIONS = {
    "draft": {"ready", "cancelled", "failed"},
    "ready": {"running", "scheduled", "cancelled", "failed"},
    "running": {
        "completed",
        "waiting_input",
        "scheduled",
        "blocked",
        "exhausted",
        "failed",
        "cancelled",
    },
    "waiting_input": {"running", "blocked", "cancelled", "failed"},
    "scheduled": {"running", "blocked", "cancelled", "failed"},
    "blocked": {"running", "cancelled", "failed"},
    "completed": set(),
    "exhausted": set(),
    "failed": set(),
    "cancelled": set(),
}


class LoopKitError(RuntimeError):
    """Raised when a LoopKit invariant is violated."""


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def timestamp_slug() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def state_root() -> Path:
    override = os.environ.get("LOOPKIT_STATE_ROOT")
    if override:
        return Path(override).expanduser().resolve()
    # Hatch adaptation: durable state lives in the workspace so later chat
    # sessions, subagents, and cron runs share the same runs. The plugin's
    # ~/.claude/loopkit and ~/.codex/loopkit host roots do not apply here.
    return (Path.home() / "workspace" / "loopkit").resolve()


def workspace_id(workspace: Path | str) -> str:
    resolved = str(Path(workspace).expanduser().resolve())
    return hashlib.sha256(resolved.encode("utf-8")).hexdigest()[:12]


def safe_slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug[:48] or "run"


def load_json(path: Path | str) -> dict[str, Any]:
    candidate = Path(path)
    try:
        data = json.loads(candidate.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise LoopKitError(f"missing JSON file: {candidate}") from exc
    except json.JSONDecodeError as exc:
        raise LoopKitError(f"invalid JSON in {candidate}: {exc}") from exc
    if not isinstance(data, dict):
        raise LoopKitError(f"expected a JSON object in {candidate}")
    return data


def atomic_write_text(path: Path | str, content: str) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{target.name}.", dir=target.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, target)
    finally:
        with contextlib.suppress(FileNotFoundError):
            os.unlink(temp_name)


def atomic_write_json(path: Path | str, payload: dict[str, Any]) -> None:
    atomic_write_text(Path(path), json.dumps(payload, indent=2, sort_keys=True) + "\n")


@contextlib.contextmanager
def run_lock(run_dir: Path | str, timeout: float = 5.0) -> Iterator[None]:
    lock_path = Path(run_dir) / ".loopkit.lock"
    deadline = time.monotonic() + timeout
    fd: int | None = None
    while fd is None:
        try:
            fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError:
            if time.monotonic() >= deadline:
                raise LoopKitError(f"run is locked: {run_dir}")
            time.sleep(0.05)
    try:
        os.write(fd, f"pid={os.getpid()}\n".encode("utf-8"))
        os.close(fd)
        fd = None
        yield
    finally:
        if fd is not None:
            os.close(fd)
        with contextlib.suppress(FileNotFoundError):
            lock_path.unlink()


def append_event(run_dir: Path | str, event_type: str, payload: dict[str, Any]) -> None:
    event = {"at": utc_now(), "type": event_type, "payload": payload}
    event_path = Path(run_dir) / "events.jsonl"
    with event_path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(event, sort_keys=True) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_contract(contract: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if contract.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")
    goal = contract.get("goal")
    if not isinstance(goal, dict):
        errors.append("goal must be an object")
    else:
        for field in ("title", "outcome"):
            if not _nonempty_string(goal.get(field)):
                errors.append(f"goal.{field} must be a non-empty string")
    evidence = contract.get("evidence")
    if not isinstance(evidence, dict):
        errors.append("evidence must be an object")
    else:
        checks = evidence.get("machine_checks")
        criteria = evidence.get("judgment_criteria")
        if not isinstance(checks, list) or not checks:
            errors.append("evidence.machine_checks must be a non-empty array")
        else:
            seen: set[str] = set()
            for index, check in enumerate(checks):
                if not isinstance(check, dict):
                    errors.append(f"evidence.machine_checks[{index}] must be an object")
                    continue
                check_id = check.get("id")
                if not _nonempty_string(check_id):
                    errors.append(f"evidence.machine_checks[{index}].id must be a non-empty string")
                elif check_id in seen:
                    errors.append(f"duplicate machine check id: {check_id}")
                else:
                    seen.add(check_id)
                if not _nonempty_string(check.get("command")):
                    errors.append(f"evidence.machine_checks[{index}].command must be a non-empty string")
        if not isinstance(criteria, list):
            errors.append("evidence.judgment_criteria must be an array")
        elif any(not _nonempty_string(item) for item in criteria):
            errors.append("every judgment criterion must be a non-empty string")
    boundaries = contract.get("boundaries")
    if not isinstance(boundaries, dict):
        errors.append("boundaries must be an object")
    else:
        for field in ("allowed_paths", "forbidden_paths", "external_actions"):
            if not isinstance(boundaries.get(field), list):
                errors.append(f"boundaries.{field} must be an array")
    iteration = contract.get("iteration")
    if not isinstance(iteration, dict):
        errors.append("iteration must be an object")
    else:
        for field in ("max_iterations", "no_progress_limit"):
            value = iteration.get(field)
            if not isinstance(value, int) or isinstance(value, bool) or value < 1:
                errors.append(f"iteration.{field} must be a positive integer")
    stops = contract.get("stops")
    if not isinstance(stops, dict):
        errors.append("stops must be an object")
    else:
        for field in ("success", "failure", "blocked", "exhausted"):
            if not _nonempty_string(stops.get(field)):
                errors.append(f"stops.{field} must be a non-empty string")
    return errors


def init_run(contract_path: Path | str, workspace: Path | str, slug: str | None = None) -> Path:
    source = load_json(contract_path)
    errors = validate_contract(source)
    if errors:
        raise LoopKitError("contract validation failed:\n- " + "\n- ".join(errors))
    workspace_path = Path(workspace).expanduser().resolve()
    title = source["goal"]["title"]
    run_name = f"{timestamp_slug()}-{safe_slug(slug or title)}"
    run_dir = state_root() / "runs" / workspace_id(workspace_path) / run_name
    run_dir.mkdir(parents=True, exist_ok=False)
    (run_dir / "evidence" / "receipts").mkdir(parents=True)
    run_id = hashlib.sha256(str(run_dir).encode("utf-8")).hexdigest()[:20]
    contract = dict(source)
    contract["run_id"] = run_id
    contract["workspace"] = {"path": str(workspace_path), "hash": workspace_id(workspace_path)}
    contract["created_at"] = utc_now()
    state = {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "status": "ready",
        "generation": 0,
        "iteration": 0,
        "no_progress_count": 0,
        "last_outcome": None,
        "next_action": "Start the first bounded iteration.",
        "updated_at": utc_now(),
    }
    atomic_write_json(run_dir / "contract.json", contract)
    atomic_write_json(run_dir / "state.json", state)
    atomic_write_text(run_dir / "events.jsonl", "")
    append_event(run_dir, "run_initialized", {"status": "ready", "generation": 0})
    refresh_checkpoint(run_dir)
    return run_dir


def transition_run(
    run_dir: Path | str,
    to_status: str,
    expected_generation: int,
    reason: str,
) -> dict[str, Any]:
    run_path = Path(run_dir).resolve()
    if not _nonempty_string(reason):
        raise LoopKitError("transition reason must be a non-empty string")
    if to_status == "completed":
        raise LoopKitError("completed status requires a validated completion receipt")
    with run_lock(run_path):
        state = load_json(run_path / "state.json")
        current = state.get("status")
        if state.get("generation") != expected_generation:
            raise LoopKitError(
                f"generation mismatch: expected {expected_generation}, found {state.get('generation')}"
            )
        if to_status not in ALLOWED_TRANSITIONS.get(str(current), set()):
            raise LoopKitError(f"invalid transition: {current} -> {to_status}")
        state["status"] = to_status
        state["generation"] = expected_generation + 1
        state["updated_at"] = utc_now()
        state["last_transition_reason"] = reason
        atomic_write_json(run_path / "state.json", state)
        append_event(
            run_path,
            "state_transition",
            {"from": current, "to": to_status, "generation": state["generation"], "reason": reason},
        )
    refresh_checkpoint(run_path)
    return state


def resolve_evidence_path(run_dir: Path, value: str) -> Path:
    candidate = Path(value).expanduser()
    return candidate.resolve() if candidate.is_absolute() else (run_dir / candidate).resolve()


def validate_receipt(receipt: dict[str, Any], run_dir: Path | str) -> list[str]:
    errors: list[str] = []
    run_path = Path(run_dir).resolve()
    contract = load_json(run_path / "contract.json")
    if receipt.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")
    if receipt.get("run_id") != contract.get("run_id"):
        errors.append("run_id does not match contract.json")
    iteration = receipt.get("iteration")
    if not isinstance(iteration, int) or isinstance(iteration, bool) or iteration < 1:
        errors.append("iteration must be a positive integer")
    if receipt.get("status") not in {
        "running",
        "completed",
        "waiting_input",
        "blocked",
        "exhausted",
        "failed",
    }:
        errors.append("status is not a receipt status")
    for field in ("action", "outcome", "next_action"):
        if not _nonempty_string(receipt.get(field)):
            errors.append(f"{field} must be a non-empty string")
    evidence_paths = receipt.get("evidence_paths")
    if not isinstance(evidence_paths, list):
        errors.append("evidence_paths must be an array")
    else:
        for item in evidence_paths:
            if not _nonempty_string(item):
                errors.append("every evidence path must be a non-empty string")
            elif not resolve_evidence_path(run_path, item).exists():
                errors.append(f"evidence path does not exist: {item}")
    checks = receipt.get("checks")
    if not isinstance(checks, list) or not checks:
        errors.append("checks must be a non-empty array")
    else:
        required_ids = {item["id"] for item in contract["evidence"]["machine_checks"]}
        seen_ids: set[str] = set()
        for index, check in enumerate(checks):
            if not isinstance(check, dict):
                errors.append(f"checks[{index}] must be an object")
                continue
            check_id = check.get("id")
            if not _nonempty_string(check_id):
                errors.append(f"checks[{index}].id must be a non-empty string")
            elif check_id in seen_ids:
                errors.append(f"duplicate check id: {check_id}")
            else:
                seen_ids.add(check_id)
            if not isinstance(check.get("passed"), bool):
                errors.append(f"checks[{index}].passed must be a boolean")
            if not _nonempty_string(check.get("evidence")):
                errors.append(f"checks[{index}].evidence must be a non-empty string")
        if receipt.get("status") == "completed":
            if not required_ids.issubset(seen_ids):
                errors.append("completed receipt is missing required machine checks")
            if any(check.get("passed") is not True for check in checks if isinstance(check, dict)):
                errors.append("completed receipt contains a failed check")
    criteria = contract["evidence"]["judgment_criteria"]
    judgments = receipt.get("judgments", [])
    if not isinstance(judgments, list):
        errors.append("judgments must be an array")
    else:
        seen_criteria: set[str] = set()
        for index, judgment in enumerate(judgments):
            if not isinstance(judgment, dict):
                errors.append(f"judgments[{index}] must be an object")
                continue
            criterion = judgment.get("criterion")
            if not _nonempty_string(criterion):
                errors.append(f"judgments[{index}].criterion must be a non-empty string")
            elif criterion in seen_criteria:
                errors.append(f"duplicate judgment criterion: {criterion}")
            else:
                seen_criteria.add(criterion)
            if not isinstance(judgment.get("passed"), bool):
                errors.append(f"judgments[{index}].passed must be a boolean")
            if not _nonempty_string(judgment.get("evidence")):
                errors.append(f"judgments[{index}].evidence must be a non-empty string")
        if receipt.get("status") == "completed":
            if not set(criteria).issubset(seen_criteria):
                errors.append("completed receipt is missing required judgment criteria")
            if any(judgment.get("passed") is not True for judgment in judgments if isinstance(judgment, dict)):
                errors.append("completed receipt contains a failed judgment")
    return errors


def record_receipt(
    run_dir: Path | str,
    receipt_path: Path | str,
    expected_generation: int,
) -> tuple[Path, dict[str, Any]]:
    run_path = Path(run_dir).resolve()
    receipt = load_json(receipt_path)
    errors = validate_receipt(receipt, run_path)
    if errors:
        raise LoopKitError("receipt validation failed:\n- " + "\n- ".join(errors))
    with run_lock(run_path):
        state = load_json(run_path / "state.json")
        if state.get("generation") != expected_generation:
            raise LoopKitError(
                f"generation mismatch: expected {expected_generation}, found {state.get('generation')}"
            )
        if receipt["iteration"] != state.get("iteration", 0) + 1:
            raise LoopKitError("receipt iteration must be exactly one greater than state.iteration")
        current = str(state.get("status"))
        receipt_status = receipt["status"]
        keeps_running = current == "running" and receipt_status == "running"
        if not keeps_running and receipt_status not in ALLOWED_TRANSITIONS.get(current, set()):
            raise LoopKitError(f"invalid receipt transition: {current} -> {receipt_status}")
        contract = load_json(run_path / "contract.json")
        progressed = receipt.get("progressed", True)
        next_no_progress = 0 if progressed else state.get("no_progress_count", 0) + 1
        if receipt_status == "running" and receipt["iteration"] >= contract["iteration"]["max_iterations"]:
            raise LoopKitError("iteration cap reached; record an exhausted or completed receipt")
        if receipt_status == "running" and next_no_progress >= contract["iteration"]["no_progress_limit"]:
            raise LoopKitError("no-progress limit reached; record an exhausted receipt")
        receipt_target = run_path / "evidence" / "receipts" / f"{receipt['iteration']:04d}.json"
        atomic_write_json(receipt_target, receipt)
        state["iteration"] = receipt["iteration"]
        state["status"] = receipt["status"]
        state["generation"] = expected_generation + 1
        state["no_progress_count"] = next_no_progress
        state["last_outcome"] = receipt["outcome"]
        state["next_action"] = receipt["next_action"]
        state["updated_at"] = utc_now()
        atomic_write_json(run_path / "state.json", state)
        append_event(
            run_path,
            "iteration_recorded",
            {
                "iteration": receipt["iteration"],
                "status": receipt["status"],
                "generation": state["generation"],
                "progressed": progressed,
                "receipt": str(receipt_target.relative_to(run_path)),
            },
        )
    refresh_checkpoint(run_path)
    return receipt_target, state


def checkpoint_text(run_dir: Path | str) -> str:
    run_path = Path(run_dir).resolve()
    contract = load_json(run_path / "contract.json")
    state = load_json(run_path / "state.json")
    goal = contract["goal"]
    lines = [
        "# LoopKit checkpoint",
        "",
        f"Run: {contract['run_id']}",
        f"Workspace: {contract['workspace']['path']}",
        f"Goal: {goal['title']}",
        f"Outcome: {goal['outcome']}",
        f"Status: {state['status']}",
        f"Generation: {state['generation']}",
        f"Iteration: {state['iteration']}",
        f"Last outcome: {state.get('last_outcome') or 'No completed iteration yet.'}",
        f"Next action: {state.get('next_action') or 'Read the contract and choose one bounded action.'}",
        "",
        "Resume protocol:",
        "1. Re-read contract.json and state.json from this run directory.",
        "2. Confirm the current generation before writing state.",
        "3. Verify fresh workspace state before acting.",
        "4. Record the next receipt before reporting progress.",
        "",
        f"Run directory: {run_path}",
    ]
    content = "\n".join(lines) + "\n"
    encoded = content.encode("utf-8")
    if len(encoded) > 4096:
        content = encoded[:4093].decode("utf-8", errors="ignore") + "..."
    return content


def refresh_checkpoint(run_dir: Path | str) -> Path:
    target = Path(run_dir).resolve() / "checkpoint.md"
    atomic_write_text(target, checkpoint_text(run_dir))
    return target


def newest_active_run(workspace: Path | str) -> Path | None:
    parent = state_root() / "runs" / workspace_id(workspace)
    if not parent.exists():
        return None
    candidates: list[tuple[str, Path]] = []
    for run_dir in parent.iterdir():
        if not run_dir.is_dir() or not (run_dir / "state.json").exists():
            continue
        try:
            state = load_json(run_dir / "state.json")
        except LoopKitError:
            continue
        if state.get("status") in ACTIVE_STATUSES:
            candidates.append((str(state.get("updated_at", "")), run_dir))
    return max(candidates, default=("", None), key=lambda item: item[0])[1]


def write_schedule(run_dir: Path | str, schedule: dict[str, Any]) -> Path:
    required = ("cadence", "task_prompt", "manual_tested_at", "stop_condition")
    missing = [field for field in required if not _nonempty_string(schedule.get(field))]
    if missing:
        raise LoopKitError("schedule is missing: " + ", ".join(missing))
    schedule["schema_version"] = SCHEMA_VERSION
    schedule["updated_at"] = utc_now()
    target = Path(run_dir).resolve() / "schedule.json"
    atomic_write_json(target, schedule)
    return target


def diagnose_run(run_dir: Path | str) -> dict[str, Any]:
    run_path = Path(run_dir).resolve()
    contract = load_json(run_path / "contract.json")
    state = load_json(run_path / "state.json")
    findings: list[dict[str, str]] = []
    if state.get("no_progress_count", 0) >= contract["iteration"]["no_progress_limit"]:
        findings.append({"code": "stagnation", "severity": "high", "message": "No-progress limit reached."})
    if state.get("iteration", 0) >= contract["iteration"]["max_iterations"] and state.get("status") not in TERMINAL_STATUSES:
        findings.append({"code": "iteration-cap", "severity": "high", "message": "Iteration cap reached without a terminal state."})
    if state.get("status") == "completed":
        receipts = sorted((run_path / "evidence" / "receipts").glob("*.json"))
        if not receipts:
            findings.append({"code": "missing-receipt", "severity": "critical", "message": "Completed run has no receipt."})
        else:
            errors = validate_receipt(load_json(receipts[-1]), run_path)
            if errors:
                findings.append({"code": "invalid-receipt", "severity": "critical", "message": "; ".join(errors)})
    return {
        "schema_version": SCHEMA_VERSION,
        "run_id": contract["run_id"],
        "status": state["status"],
        "finding_count": len(findings),
        "findings": findings,
        "diagnosed_at": utc_now(),
    }
