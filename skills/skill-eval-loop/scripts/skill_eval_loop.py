#!/usr/bin/env python3
"""Deterministic state and evidence controller for the skill-eval-loop workspace skill.

Local-only evaluator: validates suites, records supplied case and rubric
evidence, fingerprints sources and candidates, enforces limits and approval
gates, compares pass rates against a pinned baseline, and writes a terminal
receipt. There is no external analyzer on this host; receipts always run in
local mode.

CLI:
    python3 skill_eval_loop.py init TARGET
    python3 skill_eval_loop.py validate-suite SUITE.json
    python3 skill_eval_loop.py run TARGET --case-results cases.json --rubric-results rubric.json [--candidate STAGED]
    python3 skill_eval_loop.py pin-baseline TARGET RUN_ID
    python3 skill_eval_loop.py stage TARGET
    python3 skill_eval_loop.py promote TARGET STAGED RUN_ID --approval APPROVED --expected-source-fingerprint FP
    python3 skill_eval_loop.py state status|migrate [--from LEGACY_ROOT]

State lives at ~/workspace/skill-eval-loop/state, outside the replaceable skill
package (override with --state-root or SKILL_EVAL_LOOP_STATE). Earlier versions
wrote to the package's own state/ directory; `state migrate` copies that forward
and never deletes it.
"""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 1
EVALUATOR_STATUS = "unavailable"


class LoopError(RuntimeError):
    pass


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def run_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


SKILL_DIR = Path(__file__).resolve().parent.parent
STATE_ENV = "SKILL_EVAL_LOOP_STATE"
LEGACY_ENV = "SKILL_EVAL_LOOP_LEGACY_STATE"
MIGRATION_MARKER = "migrated-from.json"
IGNORED_STATE_FILES = {MIGRATION_MARKER, ".state.lock"}


def default_state_root() -> Path:
    """User state lives outside the replaceable skill package."""
    return (Path.home() / "workspace" / "skill-eval-loop" / "state").resolve()


def legacy_state_roots() -> list[Path]:
    """In-package state roots written by earlier versions. Read only; never deleted."""
    override = os.environ.get(LEGACY_ENV)
    if override:
        return [Path(override).expanduser().resolve()]
    candidates = [
        SKILL_DIR / "state",
        Path.home() / "workspace" / "skills" / "skill-eval-loop" / "state",
    ]
    unique: list[Path] = []
    for item in candidates:
        resolved = item.resolve()
        if resolved not in unique:
            unique.append(resolved)
    return unique


def state_files(root: Path) -> list[Path]:
    if not root.is_dir():
        return []
    return sorted(
        path for path in root.rglob("*")
        if path.is_file() and path.relative_to(root).parts[0] not in IGNORED_STATE_FILES
    )


def tree_digest(root: Path) -> str | None:
    """Content hash of a state tree, or None when it holds no records."""
    files = state_files(root)
    if not files:
        return None
    digest = hashlib.sha256()
    for path in files:
        digest.update(str(path.relative_to(root)).encode("utf-8") + b"\0")
        digest.update(hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()


def state_status() -> dict[str, Any]:
    """Report the active default state root, legacy roots, and any needed action."""
    current = default_state_root()
    current_digest = tree_digest(current)
    marker = load_json(current / MIGRATION_MARKER) if (current / MIGRATION_MARKER).is_file() else {}
    legacy = []
    for root in legacy_state_roots():
        digest = tree_digest(root)
        if digest is None:
            continue
        migrated = digest == current_digest or (
            marker.get("legacy_path") == str(root) and marker.get("legacy_digest") == digest
        )
        legacy.append({"path": str(root), "digest": digest, "migrated": migrated})
    pending = [item for item in legacy if not item["migrated"]]
    result: dict[str, Any] = {
        "state_root": str(current),
        "state_has_records": current_digest is not None,
        "legacy_roots": legacy,
    }
    if current_digest is not None and pending:
        result["active"] = str(current)
        result["action"] = "conflict"
        result["detail"] = (
            "state and legacy records differ; commands are refused until the user picks one root "
            "with --state-root. Nothing was merged, overwritten, or deleted."
        )
    elif current_digest is not None:
        result["active"] = str(current)
        result["action"] = "none"
    elif len(pending) == 1:
        result["active"] = pending[0]["path"]
        result["action"] = "migrate"
        result["detail"] = "run: python3 scripts/skill_eval_loop.py state migrate"
    elif pending:
        result["active"] = None
        result["action"] = "conflict"
        result["detail"] = "several legacy roots hold different records; run state migrate --from <path> for the one to keep"
    else:
        result["active"] = str(current)
        result["action"] = "none"
    return result


def state_root(explicit: str | None) -> Path:
    """Resolve the state root: --state-root, then SKILL_EVAL_LOOP_STATE, then the default.

    Every command that uses the default root writes to it, so unmigrated or conflicting
    legacy in-package state stops the command instead of forking or overwriting it.
    """
    if explicit:
        return Path(explicit).expanduser().resolve()
    state_home = os.environ.get(STATE_ENV)
    if state_home:
        return Path(state_home).expanduser().resolve()
    status = state_status()
    if status["action"] == "none":
        return default_state_root()
    raise LoopError(
        f"state needs attention before writing ({status['action']}): "
        f"{status.get('detail', '')} Legacy roots: {[item['path'] for item in status['legacy_roots']]}"
    )


def cmd_state(args: argparse.Namespace) -> dict[str, Any]:
    if args.state_command == "status":
        return state_status()
    return migrate_state(getattr(args, "source", None))


def migrate_state(source: str | None = None) -> dict[str, Any]:
    """Copy one legacy state tree to the default root. Never deletes or overwrites."""
    target = default_state_root()
    if source:
        legacy = Path(source).expanduser().resolve()
    else:
        pending = [item for item in state_status()["legacy_roots"] if not item["migrated"]]
        if not pending:
            return {"migrated": False, "reason": "no unmigrated legacy state", "state_root": str(target)}
        if len(pending) > 1:
            raise LoopError("several legacy roots differ; pass --from <path> to choose one")
        legacy = Path(pending[0]["path"])
    legacy_digest = tree_digest(legacy)
    if legacy_digest is None:
        return {"migrated": False, "reason": f"no legacy records at {legacy}", "state_root": str(target)}
    if target.is_symlink():
        raise LoopError(f"state root is a symlink; refusing to write through it: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    with open(target.parent / ".state.lock", "a") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        current_digest = tree_digest(target)
        if current_digest is not None and current_digest != legacy_digest:
            raise LoopError(
                f"state root already holds different records; nothing overwritten: {target} (legacy kept at {legacy})"
            )
        if current_digest is None:
            staging = Path(tempfile.mkdtemp(prefix=".state.migrating.", dir=target.parent))
            for path in state_files(legacy):
                destination = staging / path.relative_to(legacy)
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, destination)
            if tree_digest(staging) != legacy_digest:
                raise LoopError(f"copy verification failed; staged copy left at {staging}")
            try:
                os.rename(staging, target)  # fails if a non-empty state root appeared meanwhile
            except OSError as error:
                raise LoopError(f"state root changed during migration; staged copy left at {staging}: {error}") from error
        atomic_json(target / MIGRATION_MARKER, {
            "legacy_path": str(legacy), "legacy_digest": legacy_digest, "migrated_at": now(),
        })
    return {
        "migrated": current_digest is None,
        "reason": "copied" if current_digest is None else "already identical; marker recorded",
        "state_root": str(target),
        "legacy_path_kept": str(legacy),
        "sha256": legacy_digest,
    }


def atomic_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")
        temp_name = handle.name
    os.replace(temp_name, path)


def append_jsonl(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + "\n")


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise LoopError(f"cannot read valid JSON from {path}: {error}") from error


def fingerprint(path: Path) -> str:
    path = path.resolve()
    digest = hashlib.sha256()
    if path.is_file():
        digest.update(path.name.encode())
        digest.update(path.read_bytes())
        return digest.hexdigest()
    if not path.is_dir():
        raise LoopError(f"target does not exist: {path}")
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        if any(part in {".git", "__pycache__", ".DS_Store"} for part in item.parts):
            continue
        digest.update(str(item.relative_to(path)).encode())
        digest.update(item.read_bytes())
    return digest.hexdigest()


def target_id(target: Path) -> str:
    clean = re.sub(r"[^a-z0-9]+", "-", target.name.lower()).strip("-") or "target"
    suffix = hashlib.sha256(str(target.resolve()).encode()).hexdigest()[:10]
    return f"{clean}-{suffix}"


def target_dir(target: Path, root: Path) -> Path:
    return root / "targets" / target_id(target)


def candidate_kind(candidate: Path, target: Path, directory: Path, source_fingerprint: str) -> str:
    if candidate == target:
        return "source"
    staging_root = (directory / "staging").resolve()
    try:
        candidate.relative_to(staging_root)
    except ValueError as error:
        raise LoopError("candidate must be the source or a staging copy created by this target") from error
    metadata_path = staging_root / f"{candidate.name}.json"
    if not metadata_path.is_file():
        raise LoopError(f"staging metadata is missing: {metadata_path}")
    metadata = load_json(metadata_path)
    if Path(metadata.get("staged_path", "")).resolve() != candidate:
        raise LoopError("staging metadata does not match the candidate path")
    if Path(metadata.get("source", "")).resolve() != target:
        raise LoopError("staging metadata does not match the source target")
    if metadata.get("source_fingerprint") != source_fingerprint:
        raise LoopError("staging copy was created from a different source fingerprint")
    return "staged"


def pass_rate(summary: Any) -> float | None:
    if not isinstance(summary, dict):
        return None
    value = summary.get("pass_rate")
    return float(value) if isinstance(value, (int, float)) else None


def validate_suite_payload(suite: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if suite.get("schema_version") != SCHEMA_VERSION:
        errors.append("schema_version must be 1")
    if not isinstance(suite.get("target"), str) or not suite["target"].strip():
        errors.append("target must be a non-empty path string")
    limits = suite.get("limits")
    if not isinstance(limits, dict):
        errors.append("limits must be an object")
    else:
        for key in ("max_iterations", "max_minutes"):
            value = limits.get(key)
            if not isinstance(value, int) or value <= 0:
                errors.append(f"limits.{key} must be a positive integer")
        token_limit = limits.get("max_tokens")
        if token_limit is not None and (not isinstance(token_limit, int) or token_limit <= 0):
            errors.append("limits.max_tokens must be null or a positive integer")
    trigger_cases = suite.get("trigger_cases")
    if not isinstance(trigger_cases, list):
        errors.append("trigger_cases must be an array")
        trigger_cases = []
    positives = sum(case.get("should_trigger") is True for case in trigger_cases if isinstance(case, dict))
    negatives = sum(case.get("should_trigger") is False for case in trigger_cases if isinstance(case, dict))
    if positives < 10:
        errors.append("trigger_cases requires at least 10 should_trigger cases")
    if negatives < 10:
        errors.append("trigger_cases requires at least 10 should-stay-silent cases")
    functional = suite.get("functional_cases")
    if not isinstance(functional, list) or not functional:
        errors.append("functional_cases requires at least one case")
        functional = []
    rubric = suite.get("rubric")
    if not isinstance(rubric, list) or not rubric:
        errors.append("rubric requires at least one criterion")
        rubric = []
    ids: list[str] = []
    for group_name, group in (("trigger_cases", trigger_cases), ("functional_cases", functional)):
        for case in group:
            if not isinstance(case, dict):
                errors.append(f"{group_name} entries must be objects")
                continue
            if not all(isinstance(case.get(key), str) and case[key].strip() for key in ("id", "prompt", "expected")):
                errors.append(f"{group_name} entries require non-empty id, prompt, and expected")
            else:
                ids.append(case["id"])
    rubric_ids: list[str] = []
    for criterion in rubric:
        if not isinstance(criterion, dict) or not all(
            isinstance(criterion.get(key), str) and criterion[key].strip()
            for key in ("id", "criterion", "ground_truth")
        ):
            errors.append("rubric entries require non-empty id, criterion, and ground_truth")
        else:
            rubric_ids.append(criterion["id"])
    combined = ids + rubric_ids
    if len(combined) != len(set(combined)):
        errors.append("case and rubric IDs must be unique")
    return errors


def validate_result_file(path: Path, expected_ids: set[str], label: str) -> tuple[list[dict[str, Any]], list[str]]:
    payload = load_json(path)
    results = payload.get("results") if isinstance(payload, dict) else None
    errors: list[str] = []
    if not isinstance(results, list):
        return [], [f"{label} must contain a results array"]
    seen: set[str] = set()
    for result in results:
        if not isinstance(result, dict):
            errors.append(f"{label} results must be objects")
            continue
        case_id = result.get("id")
        if not isinstance(case_id, str) or not case_id:
            errors.append(f"{label} result needs a non-empty string id")
        elif case_id not in expected_ids:
            errors.append(f"{label} contains unknown id {case_id!r}")
        elif case_id in seen:
            errors.append(f"{label} contains duplicate id {case_id!r}")
        else:
            seen.add(case_id)
        if not isinstance(result.get("passed"), bool):
            errors.append(f"{label} result {case_id!r} needs boolean passed")
        if not isinstance(result.get("evidence"), str) or not result["evidence"].strip():
            errors.append(f"{label} result {case_id!r} needs evidence")
    missing = expected_ids - seen
    if missing:
        errors.append(f"{label} is missing IDs: {', '.join(sorted(missing))}")
    return results, errors


def summarize_results(results: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(results)
    passed = sum(item.get("passed") is True for item in results)
    return {"total": total, "passed": passed, "failed": total - passed, "pass_rate": passed / total if total else None}


def load_state(target: Path, root: Path) -> tuple[Path, dict[str, Any]]:
    directory = target_dir(target, root)
    state_path = directory / "state.json"
    if not state_path.exists():
        raise LoopError(f"target is not initialized: {target}")
    return directory, load_json(state_path)


def cmd_init(args: argparse.Namespace) -> dict[str, Any]:
    target = Path(args.target).expanduser().resolve()
    if not target.exists():
        raise LoopError(f"target does not exist: {target}")
    root = state_root(args.state_root)
    directory = target_dir(target, root)
    directory.mkdir(parents=True, exist_ok=True)
    state_path = directory / "state.json"
    template = Path(__file__).resolve().parent.parent / "assets" / "suite-template.json"
    suite_path = directory / "suite.json"
    if not suite_path.exists():
        suite = load_json(template)
        suite["target"] = str(target)
        atomic_json(suite_path, suite)
    baseline_path = directory / "baseline.json"
    if not baseline_path.exists():
        atomic_json(baseline_path, {"schema_version": 1, "target": str(target), "pinned_run_id": None})
    if state_path.exists():
        state = load_json(state_path)
        return {
            "target_directory": str(directory),
            "suite": str(suite_path),
            "status": state.get("status"),
            "initialized": False,
        }
    state = {
        "schema_version": 1,
        "target": str(target),
        "target_id": target_id(target),
        "source_fingerprint": fingerprint(target),
        "status": "suite_required",
        "iteration": 0,
        "last_failure_signature": None,
        "repeated_failure_count": 0,
        "manual_success": False,
        "updated_at": now(),
    }
    atomic_json(state_path, state)
    return {
        "target_directory": str(directory),
        "suite": str(suite_path),
        "status": state["status"],
        "initialized": True,
    }


def cmd_validate_suite(args: argparse.Namespace) -> dict[str, Any]:
    suite_path = Path(args.suite).expanduser().resolve()
    errors = validate_suite_payload(load_json(suite_path))
    if errors:
        raise LoopError("suite validation failed: " + "; ".join(errors))
    return {"valid": True, "suite": str(suite_path)}


def cmd_run(args: argparse.Namespace) -> dict[str, Any]:
    target = Path(args.target).expanduser().resolve()
    root = state_root(args.state_root)
    directory, state = load_state(target, root)
    source_fingerprint = fingerprint(target)
    if source_fingerprint != state.get("source_fingerprint"):
        raise LoopError("source fingerprint changed after initialization")
    suite_path = Path(args.suite).expanduser().resolve() if args.suite else directory / "suite.json"
    suite = load_json(suite_path)
    suite_errors = validate_suite_payload(suite)
    if suite_errors:
        raise LoopError("suite validation failed: " + "; ".join(suite_errors))
    if Path(suite["target"]).expanduser().resolve() != target:
        raise LoopError("suite target does not match the initialized target")
    candidate = Path(args.candidate).expanduser().resolve() if args.candidate else target
    if not candidate.exists():
        raise LoopError(f"evaluation target does not exist: {candidate}")
    evaluated_kind = candidate_kind(candidate, target, directory, source_fingerprint)
    current_iteration = int(state.get("iteration", 0)) + 1
    limits = suite["limits"]
    token_usage = args.token_usage
    if token_usage is not None and token_usage < 0:
        raise LoopError("token usage must be zero or a positive integer")
    if current_iteration > limits["max_iterations"]:
        state.update({"status": "exhausted", "updated_at": now()})
        atomic_json(directory / "state.json", state)
        raise LoopError("maximum iterations reached")
    rid = args.run_id or run_id()
    run_directory = directory / "runs" / rid
    if run_directory.exists():
        raise LoopError(f"run already exists: {rid}")
    (run_directory / "artifacts").mkdir(parents=True)
    trace = run_directory / "trace.jsonl"
    append_jsonl(trace, {"at": now(), "event": "run_started", "run_id": rid, "candidate": str(candidate)})
    started = datetime.now(timezone.utc)
    trigger_ids = {case["id"] for case in suite["trigger_cases"]}
    functional_ids = {case["id"] for case in suite["functional_cases"]}
    rubric_ids = {criterion["id"] for criterion in suite["rubric"]}
    case_results: list[dict[str, Any]] = []
    case_errors: list[str] = []
    if args.case_results:
        case_results, case_errors = validate_result_file(
            Path(args.case_results).expanduser().resolve(), trigger_ids | functional_ids, "case results"
        )
    else:
        case_errors.append("case results were not supplied")
    rubric_results: list[dict[str, Any]] = []
    rubric_errors: list[str] = []
    if args.rubric_results:
        rubric_results, rubric_errors = validate_result_file(
            Path(args.rubric_results).expanduser().resolve(), rubric_ids, "rubric results"
        )
    else:
        rubric_errors.append("independent rubric results were not supplied")
    result_errors = case_errors + rubric_errors
    atomic_json(run_directory / "checks.json", {"evaluator_status": EVALUATOR_STATUS})
    case_payload = {"results": case_results, "errors": case_errors, "summary": summarize_results(case_results)}
    atomic_json(run_directory / "cases.json", case_payload)
    rubric_payload = {"results": rubric_results, "errors": rubric_errors, "summary": summarize_results(rubric_results)}
    atomic_json(run_directory / "rubric.json", rubric_payload)
    case_summary = summarize_results(case_results)
    rubric_summary = summarize_results(rubric_results)
    baseline = load_json(directory / "baseline.json")
    case_rate = pass_rate(case_summary)
    rubric_rate = pass_rate(rubric_summary)
    baseline_case_rate = pass_rate(baseline.get("case_summary"))
    baseline_rubric_rate = pass_rate(baseline.get("rubric_summary"))
    case_rate_delta = (
        case_rate - baseline_case_rate
        if case_rate is not None and baseline_case_rate is not None
        else None
    )
    rubric_rate_delta = (
        rubric_rate - baseline_rubric_rate
        if rubric_rate is not None and baseline_rubric_rate is not None
        else None
    )
    diff = {
        "baseline_run_id": baseline.get("pinned_run_id"),
        "current_run_id": rid,
        "case_summary": case_summary,
        "rubric_summary": rubric_summary,
        "case_pass_rate_delta": case_rate_delta,
        "rubric_pass_rate_delta": rubric_rate_delta,
        "evaluator_status": EVALUATOR_STATUS,
    }
    atomic_json(run_directory / "diff.json", diff)
    cases_pass = (
        bool(case_results)
        and case_summary["failed"] == 0
        and not any("case results" in item for item in result_errors)
    )
    rubric_pass = (
        bool(rubric_results)
        and all(item.get("passed") is True for item in rubric_results)
        and not any("rubric" in item for item in result_errors)
    )
    no_regression = (
        (case_rate_delta is None or case_rate_delta >= 0)
        and (rubric_rate_delta is None or rubric_rate_delta >= 0)
    )
    elapsed_minutes = (datetime.now(timezone.utc) - started).total_seconds() / 60
    within_time = elapsed_minutes <= limits["max_minutes"]
    token_limit = limits.get("max_tokens")
    token_evidence_present = token_limit is None or token_usage is not None
    within_tokens = token_limit is None or (token_usage is not None and token_usage <= token_limit)
    passed = cases_pass and rubric_pass and no_regression and within_time and within_tokens
    signature_payload = {
        "case_failed": case_summary["failed"],
        "rubric_failed": rubric_summary["failed"],
        "errors": result_errors,
    }
    signature = hashlib.sha256(json.dumps(signature_payload, sort_keys=True).encode()).hexdigest()
    repeated_count = (
        int(state.get("repeated_failure_count", 0)) + 1
        if state.get("last_failure_signature") == signature and not passed
        else 0
    )
    if passed:
        stop_reason = "local_pass"
        status = "passed"
    elif not within_time:
        stop_reason = "time_limit"
        status = "exhausted"
    elif not token_evidence_present:
        stop_reason = "missing_token_evidence"
        status = "needs_review"
    elif not within_tokens:
        stop_reason = "token_limit"
        status = "exhausted"
    elif repeated_count >= 2:
        stop_reason = "repeated_failure_signature"
        status = "exhausted"
    elif current_iteration >= limits["max_iterations"]:
        stop_reason = "iteration_limit"
        status = "exhausted"
    elif result_errors:
        stop_reason = "missing_or_invalid_evidence"
        status = "needs_review"
    else:
        stop_reason = "checks_failed"
        status = "needs_repair"
    receipt = {
        "schema_version": 1,
        "run_id": rid,
        "target": str(target),
        "evaluated_path": str(candidate),
        "evaluated_kind": evaluated_kind,
        "source_fingerprint": source_fingerprint,
        "candidate_fingerprint": fingerprint(candidate),
        "status": status,
        "stop_reason": stop_reason,
        "effective_evaluator_mode": "local",
        "evaluator_status": EVALUATOR_STATUS,
        "evaluator_error": None,
        "case_summary": case_summary,
        "rubric_summary": rubric_summary,
        "local_baseline_comparison": {
            "case_pass_rate_delta": case_rate_delta,
            "rubric_pass_rate_delta": rubric_rate_delta,
            "no_regression": no_regression,
        },
        "errors": result_errors,
        "elapsed_minutes": elapsed_minutes,
        "token_usage": token_usage,
        "token_limit": token_limit,
        "created_at": now(),
    }
    atomic_json(run_directory / "receipt.json", receipt)
    append_jsonl(trace, {"at": now(), "event": "run_stopped", "status": status, "reason": stop_reason})
    state.update({
        "status": status,
        "iteration": current_iteration,
        "last_run_id": rid,
        "last_failure_signature": None if passed else signature,
        "repeated_failure_count": repeated_count,
        "manual_success": bool(state.get("manual_success")) or passed,
        "updated_at": now(),
    })
    atomic_json(directory / "state.json", state)
    return {"run_directory": str(run_directory), "status": status, "stop_reason": stop_reason}


def cmd_pin_baseline(args: argparse.Namespace) -> dict[str, Any]:
    target = Path(args.target).expanduser().resolve()
    directory, state = load_state(target, state_root(args.state_root))
    run_directory = directory / "runs" / args.run_id
    receipt = load_json(run_directory / "receipt.json")
    if receipt.get("status") != "passed":
        raise LoopError("only a passing run can be pinned")
    if fingerprint(target) != receipt.get("source_fingerprint"):
        raise LoopError("source fingerprint changed after the passing run")
    diff = load_json(run_directory / "diff.json")
    baseline = {
        "schema_version": 1,
        "target": str(target),
        "pinned_run_id": args.run_id,
        "evaluator_status": receipt.get("evaluator_status"),
        "case_summary": receipt.get("case_summary"),
        "rubric_summary": receipt.get("rubric_summary"),
        "case_pass_rate_delta": diff.get("case_pass_rate_delta"),
        "rubric_pass_rate_delta": diff.get("rubric_pass_rate_delta"),
        "source_fingerprint": receipt.get("source_fingerprint"),
        "pinned_at": now(),
    }
    atomic_json(directory / "baseline.json", baseline)
    state.update({"status": "baseline_pinned", "updated_at": now()})
    atomic_json(directory / "state.json", state)
    return {"baseline": str(directory / "baseline.json"), "run_id": args.run_id}


def cmd_stage(args: argparse.Namespace) -> dict[str, Any]:
    target = Path(args.target).expanduser().resolve()
    directory, state = load_state(target, state_root(args.state_root))
    source_hash = fingerprint(target)
    if source_hash != state.get("source_fingerprint"):
        raise LoopError("source fingerprint changed after initialization")
    if state.get("status") not in {"needs_repair", "needs_review"}:
        raise LoopError("staging requires a failed or needs-review run")
    stage_id = args.stage_id or run_id()
    destination = directory / "staging" / stage_id
    if destination.exists():
        raise LoopError(f"staging destination exists: {destination}")
    if target.is_dir():
        shutil.copytree(
            target,
            destination,
            ignore=shutil.ignore_patterns(
                ".git", ".pytest_cache", "__pycache__", "*.pyc", ".DS_Store"
            ),
        )
    else:
        destination.mkdir(parents=True)
        shutil.copy2(target, destination / target.name)
    metadata = {
        "stage_id": stage_id,
        "source": str(target),
        "source_fingerprint": source_hash,
        "staged_path": str(destination),
        "created_at": now(),
    }
    atomic_json(destination.parent / f"{stage_id}.json", metadata)
    state.update({"status": "candidate_staged", "updated_at": now()})
    atomic_json(directory / "state.json", state)
    return metadata


def cmd_promote(args: argparse.Namespace) -> dict[str, Any]:
    if args.approval != "APPROVED":
        raise LoopError("promotion requires --approval APPROVED after explicit user approval")
    target = Path(args.target).expanduser().resolve()
    staged = Path(args.staged).expanduser().resolve()
    directory, state = load_state(target, state_root(args.state_root))
    if fingerprint(target) != args.expected_source_fingerprint:
        raise LoopError("source fingerprint changed after staging")
    receipt = load_json(directory / "runs" / args.run_id / "receipt.json")
    if receipt.get("status") != "passed" or Path(receipt.get("evaluated_path", "")).resolve() != staged:
        raise LoopError("promotion requires a passing receipt for the exact staged path")
    if fingerprint(staged) != receipt.get("candidate_fingerprint"):
        raise LoopError("staged candidate fingerprint changed after the passing run")
    baseline = load_json(directory / "baseline.json")
    if baseline.get("pinned_run_id") != args.run_id:
        raise LoopError("promotion requires the exact passing run to be pinned as the baseline")
    backup = directory / "backups" / f"{run_id()}-{target.name}"
    backup.parent.mkdir(parents=True, exist_ok=True)
    if target.is_dir():
        shutil.copytree(target, backup)
        replacement = target.parent / f".{target.name}.skill-eval-replacement"
        if replacement.exists():
            shutil.rmtree(replacement)
        shutil.copytree(staged, replacement)
        old = target.parent / f".{target.name}.skill-eval-old"
        if old.exists():
            shutil.rmtree(old)
        os.replace(target, old)
        os.replace(replacement, target)
        shutil.rmtree(old)
    else:
        shutil.copy2(target, backup)
        staged_file = staged / target.name if staged.is_dir() else staged
        with tempfile.NamedTemporaryFile(dir=target.parent, delete=False) as handle:
            handle.write(staged_file.read_bytes())
            replacement_file = handle.name
        os.replace(replacement_file, target)
    state.update({"status": "promoted", "source_fingerprint": fingerprint(target), "updated_at": now()})
    atomic_json(directory / "state.json", state)
    return {"promoted": str(target), "backup": str(backup), "run_id": args.run_id}


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    sub = result.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init")
    init.add_argument("target")
    init.add_argument("--state-root")
    init.set_defaults(func=cmd_init)
    validate = sub.add_parser("validate-suite")
    validate.add_argument("suite")
    validate.set_defaults(func=cmd_validate_suite)
    run = sub.add_parser("run")
    run.add_argument("target")
    run.add_argument("--candidate")
    run.add_argument("--suite")
    run.add_argument("--case-results")
    run.add_argument("--rubric-results")
    run.add_argument("--run-id")
    run.add_argument("--token-usage", type=int)
    run.add_argument("--state-root")
    run.set_defaults(func=cmd_run)
    pin = sub.add_parser("pin-baseline")
    pin.add_argument("target")
    pin.add_argument("run_id")
    pin.add_argument("--state-root")
    pin.set_defaults(func=cmd_pin_baseline)
    stage = sub.add_parser("stage")
    stage.add_argument("target")
    stage.add_argument("--stage-id")
    stage.add_argument("--state-root")
    stage.set_defaults(func=cmd_stage)
    promote = sub.add_parser("promote")
    promote.add_argument("target")
    promote.add_argument("staged")
    promote.add_argument("run_id")
    promote.add_argument("--approval", required=True)
    promote.add_argument("--expected-source-fingerprint", required=True)
    promote.add_argument("--state-root")
    promote.set_defaults(func=cmd_promote)
    state = sub.add_parser("state", help="report or migrate legacy in-package state")
    state_sub = state.add_subparsers(dest="state_command", required=True)
    state_sub.add_parser("status", help="show the active state root and any legacy records")
    migrate = state_sub.add_parser("migrate", help="copy legacy state to the default root; never deletes or overwrites")
    migrate.add_argument("--from", dest="source", help="legacy state root to migrate when several exist")
    state.set_defaults(func=cmd_state)
    return result


def main() -> int:
    args = parser().parse_args()
    try:
        payload = args.func(args)
    except LoopError as error:
        print(json.dumps({"ok": False, "error": str(error)}), file=sys.stderr)
        return 1
    print(json.dumps({"ok": True, **payload}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
