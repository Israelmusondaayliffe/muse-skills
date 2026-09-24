#!/usr/bin/env python3
"""Read-only ingestion and reporting for bounded agent-loop evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


TERMINAL_STATUSES = {"completed", "complete", "passed", "pass", "failed", "failure", "cancelled", "canceled", "exhausted", "blocked", "stopped", "terminal"}
POSITIVE = {"pass", "passed", "success", "successful", "complete", "completed", "accepted", "approve", "approved", "true"}
NEGATIVE = {"fail", "failed", "failure", "rejected", "reject", "false", "blocked", "exhausted"}
EXHAUSTION_MARKERS = ("iteration", "budget", "time_limit", "timeout", "token_limit", "cost_limit", "exhaust")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def state_root() -> Path:
    """Observatory state. Override with LOOP_OBSERVATORY_HOME for isolated runs/tests."""
    base = os.environ.get("LOOP_OBSERVATORY_HOME", str(Path.home() / "workspace" / "loop-observatory"))
    return Path(base).expanduser()


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temp.replace(path)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_json_files(root: Path) -> list[Any]:
    values: list[Any] = []
    for path in sorted(root.rglob("*.json")):
        values.append(load_json(path))
    for path in sorted(root.rglob("*.jsonl")):
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            try:
                values.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise json.JSONDecodeError(f"{path}:{number}: {exc.msg}", exc.doc, exc.pos) from exc
    return values


def tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        digest.update(str(path.relative_to(root)).encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def safe_id(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9._-]+", "-", value).strip("-") or "run"


def walk(value: Any) -> Iterable[tuple[str, Any]]:
    if isinstance(value, dict):
        for key, item in value.items():
            yield str(key).lower(), item
            yield from walk(item)
    elif isinstance(value, list):
        for item in value:
            yield from walk(item)


def first(values: list[Any], keys: tuple[str, ...]) -> Any:
    for wanted in (key.lower() for key in keys):
        for value in values:
            for key, item in walk(value):
                if key == wanted and item is not None:
                    return item
    return None


def bool_value(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)) and value in (0, 1):
        return bool(value)
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in POSITIVE:
            return True
        if lowered in NEGATIVE:
            return False
    return None


def number_value(value: Any) -> float | int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return value
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return None
    return None


def normalize(engine: str, root: Path, values: list[Any], source_hash: str) -> dict[str, Any]:
    status_raw = first(values, ("status", "run_status"))
    status = str(status_raw).lower() if status_raw is not None else "unknown"
    terminal_raw = first(values, ("terminal", "is_terminal"))
    terminal = bool_value(terminal_raw)
    if terminal is None:
        terminal = status in TERMINAL_STATUSES

    machine_raw = first(values, ("machine_completion", "machine_complete", "verified", "success"))
    judge_raw = first(values, ("judge_verdict", "verdict", "evaluation_verdict"))
    machine_completion = bool_value(machine_raw)
    if machine_completion is None:
        machine_completion = bool_value(judge_raw)
    if machine_completion is None and terminal:
        if status in {"completed", "complete", "passed", "pass"}:
            machine_completion = True
        elif status in {"failed", "failure", "blocked", "exhausted"}:
            machine_completion = False

    human_label = first(values, ("human_label", "acceptance_label", "human_verdict"))
    human_raw = first(values, ("human_acceptance", "accepted_by_human", "human_accepted"))
    human_acceptance = bool_value(human_raw)
    if human_acceptance is None:
        human_acceptance = bool_value(human_label)

    run_id = first(values, ("run_id", "id", "execution_id")) or root.name
    stop_reason = first(values, ("stop_reason", "termination_reason", "reason"))
    escalation_reason = first(values, ("escalation_reason", "blocked_reason", "escalation"))
    iteration = number_value(first(values, ("iteration", "iterations", "iteration_count", "attempt")))
    duration = number_value(first(values, ("duration_seconds", "elapsed_seconds", "duration")))
    tokens = number_value(first(values, ("tokens", "total_tokens", "token_count")))
    cost = number_value(first(values, ("cost", "cost_usd", "total_cost")))

    record_id = safe_id(f"{engine}-{run_id}-{source_hash[:12]}")
    return {
        "schema_version": "1.0",
        "record_id": record_id,
        "engine": engine,
        "run_id": str(run_id),
        "source_path": str(root.resolve()),
        "source_hash": source_hash,
        "goal": first(values, ("goal", "objective", "name", "title")),
        "model": first(values, ("model", "model_id")),
        "version": first(values, ("version", "loop_version", "graph_version")),
        "status": status,
        "terminal": terminal,
        "iteration": iteration,
        "duration_seconds": duration,
        "machine_completion": machine_completion,
        "human_acceptance": human_acceptance,
        "tokens": tokens,
        "cost": cost,
        "stop_reason": str(stop_reason) if stop_reason is not None else None,
        "escalation_reason": str(escalation_reason) if escalation_reason is not None else None,
        "judge_verdict": str(judge_raw) if judge_raw is not None else None,
        "human_label": str(human_label) if human_label is not None else None,
        "ingested_at": utc_now(),
    }


def discover_loopkit(root: Path) -> list[Path]:
    if not root.exists():
        return []
    candidates = {path.parent for path in root.rglob("state.json") if (path.parent / "contract.json").exists()}
    if (root / "state.json").exists() and (root / "contract.json").exists():
        candidates.add(root)
    return sorted(candidates)


def discover_graph(root: Path) -> list[Path]:
    if not root.exists():
        return []
    candidates = {path.parent for path in root.rglob("state.json") if (path.parent / "graph.json").exists()}
    if (root / "state.json").exists() and (root / "graph.json").exists():
        candidates.add(root)
    return sorted(candidates)


def roots_config() -> dict[str, Any]:
    path = state_root() / "registered-roots.json"
    return load_json(path) if path.exists() else {"operating_graph": []}


def register_root(path: Path) -> dict[str, Any]:
    resolved = path.expanduser().resolve()
    if not resolved.is_dir():
        raise ValueError(f"not a directory: {resolved}")
    config = roots_config()
    roots = set(config.get("operating_graph", []))
    roots.add(str(resolved))
    config = {"operating_graph": sorted(roots), "updated_at": utc_now()}
    atomic_json(state_root() / "registered-roots.json", config)
    return config


def record_index() -> dict[str, Any]:
    path = state_root() / "index.json"
    return load_json(path) if path.exists() else {"sources": {}, "records": {}}


def ingest(loopkit_root: Path | None = None) -> dict[str, Any]:
    root = loopkit_root or Path(os.environ.get("LOOPKIT_STATE_ROOT", str(Path.home() / "workspace" / "loopkit"))).expanduser()
    sources: list[tuple[str, Path]] = [("loopkit", path) for path in discover_loopkit(root)]
    for registered in roots_config().get("operating_graph", []):
        sources.extend(("operating-graph", path) for path in discover_graph(Path(registered)))

    index = record_index()
    counts = Counter(discovered=len(sources), ingested=0, unchanged=0, duplicate=0, incomplete=0, corrupt=0)
    errors: list[dict[str, str]] = []
    for engine, source in sources:
        key = f"{engine}:{source.resolve()}"
        try:
            before = tree_hash(source)
            values = read_json_files(source)
            after = tree_hash(source)
            if before != after:
                raise RuntimeError("source changed during read")
            if index.get("sources", {}).get(key) == before:
                counts["unchanged"] += 1
                continue
            record = normalize(engine, source, values, before)
            if not record["terminal"]:
                counts["incomplete"] += 1
                continue
            record_path = state_root() / "runs" / f"{record['record_id']}.json"
            if record_path.exists():
                index.setdefault("sources", {})[key] = before
                index.setdefault("records", {})[key] = record["record_id"]
                counts["duplicate"] += 1
                continue
            atomic_json(record_path, record)
            index.setdefault("sources", {})[key] = before
            index.setdefault("records", {})[key] = record["record_id"]
            counts["ingested"] += 1
        except (OSError, ValueError, json.JSONDecodeError, RuntimeError) as exc:
            counts["corrupt"] += 1
            errors.append({"source": str(source), "error": str(exc)})
    index["updated_at"] = utc_now()
    atomic_json(state_root() / "index.json", index)
    result = {"status": "ok", "counts": dict(counts), "errors": errors, "completed_at": utc_now()}
    atomic_json(state_root() / "last-ingest.json", result)
    return result


def records() -> list[dict[str, Any]]:
    root = state_root() / "runs"
    if not root.exists():
        return []
    return [load_json(path) for path in sorted(root.glob("*.json"))]


def is_exhausted(record: dict[str, Any]) -> bool:
    text = " ".join(str(record.get(key) or "").lower() for key in ("status", "stop_reason", "escalation_reason"))
    return any(marker in text for marker in EXHAUSTION_MARKERS)


def report(scheduled: bool = False) -> dict[str, Any]:
    all_records = records()
    cursor_path = state_root() / "report-cursor.json"
    cursor = load_json(cursor_path) if cursor_path.exists() else {"record_ids": []}
    seen = set(cursor.get("record_ids", []))
    new_records = [record for record in all_records if record["record_id"] not in seen]
    if scheduled and not new_records:
        return {"status": "no-op", "reason": "no-new-terminal-runs", "new_terminal_runs": 0}

    labeled = [record for record in all_records if record.get("human_acceptance") is not None]
    accepted = [record for record in labeled if record["human_acceptance"] is True]
    acceptance_rate = len(accepted) / len(labeled) if labeled else None
    accepted_with_cost = [record for record in accepted if record.get("cost") is not None]
    cost_per_accepted = None
    if accepted and len(accepted_with_cost) == len(accepted):
        cost_per_accepted = sum(float(record["cost"]) for record in accepted) / len(accepted)
    engines: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in all_records:
        engines[record["engine"]].append(record)

    result = {
        "schema_version": "1.0",
        "status": "ok",
        "generated_at": utc_now(),
        "new_terminal_runs": len(new_records),
        "total_terminal_runs": len(all_records),
        "metrics": {
            "human_acceptance_known": len(labeled),
            "human_acceptance_rate": acceptance_rate,
            "cost_per_accepted_result": cost_per_accepted,
            "accepted_results_with_cost": len(accepted_with_cost),
            "exhausted_runs": sum(1 for record in all_records if is_exhausted(record)),
        },
        "groups": [
            {
                "engine": engine,
                "runs": len(group),
                "accepted": sum(1 for record in group if record.get("human_acceptance") is True),
                "exhausted": sum(1 for record in group if is_exhausted(record)),
            }
            for engine, group in sorted(engines.items())
        ],
    }
    reports_dir = state_root() / "reports"
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    json_path = reports_dir / f"portfolio-{stamp}.json"
    md_path = reports_dir / f"portfolio-{stamp}.md"
    atomic_json(json_path, result)
    lines = [
        "# Loop Portfolio Report",
        "",
        f"Generated: {result['generated_at']}",
        f"Terminal runs: {len(all_records)}",
        f"New terminal runs: {len(new_records)}",
        f"Human acceptance rate: {acceptance_rate if acceptance_rate is not None else 'unknown'}",
        f"Cost per accepted result: {cost_per_accepted if cost_per_accepted is not None else 'unknown'}",
        f"Exhausted runs: {result['metrics']['exhausted_runs']}",
        "",
        "## Engines",
        "",
    ]
    lines.extend(f"- {group['engine']}: {group['runs']} runs, {group['accepted']} accepted, {group['exhausted']} exhausted" for group in result["groups"])
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    result["report_paths"] = {"json": str(json_path), "markdown": str(md_path)}
    atomic_json(cursor_path, {"record_ids": sorted(record["record_id"] for record in all_records), "updated_at": utc_now()})
    return result


def audit() -> dict[str, Any]:
    all_records = records()
    comparable = [record for record in all_records if record.get("machine_completion") is not None and record.get("human_acceptance") is not None]
    false_passes = [record["record_id"] for record in comparable if record["machine_completion"] is True and record["human_acceptance"] is False]
    false_failures = [record["record_id"] for record in comparable if record["machine_completion"] is False and record["human_acceptance"] is True]
    escalation_counts = Counter(str(record["escalation_reason"]) for record in all_records if record.get("escalation_reason"))
    result = {
        "schema_version": "1.0",
        "generated_at": utc_now(),
        "comparable_runs": len(comparable),
        "false_passes": false_passes,
        "false_failures": false_failures,
        "disagreement_rate": (len(false_passes) + len(false_failures)) / len(comparable) if comparable else None,
        "exhausted_runs": [record["record_id"] for record in all_records if is_exhausted(record)],
        "escalation_clusters": [{"reason": reason, "count": count} for reason, count in escalation_counts.most_common() if count > 1],
    }
    atomic_json(state_root() / "last-audit.json", result)
    return result


def owner_class_for(record: dict[str, Any]) -> str:
    engine = record.get("engine")
    if engine == "loopkit":
        return "loopkit"
    if engine == "operating-graph":
        return "operating-graph"
    return "loop-owner"


def preferred_destinations_for(record: dict[str, Any]) -> list[str]:
    """Hatch-native repair owners: workspace skills, not plugin references."""
    owner_class = owner_class_for(record)
    if owner_class == "loopkit":
        return ["loopkit skill (Diagnose phase)"]
    if owner_class == "operating-graph":
        return ["agent-ops workspace skill"]
    return ["agent-ops workspace skill"]


def disagreement_for(record: dict[str, Any]) -> str:
    machine = record.get("machine_completion")
    human = record.get("human_acceptance")
    if machine is True and human is False:
        return "false-pass"
    if machine is False and human is True:
        return "false-failure"
    if is_exhausted(record):
        return "exhaustion"
    return "unresolved-run-evidence"


def repair_handoff(record_id: str) -> dict[str, Any]:
    """Build a complete handoff without repairing or relabeling the source run."""

    match = next((record for record in records() if record.get("record_id") == record_id), None)
    if match is None:
        raise ValueError(f"unknown normalized record: {record_id}")
    owner_class = owner_class_for(match)
    disagreement = disagreement_for(match)
    return {
        "schema_version": "loop-observatory/repair-handoff/v1",
        "handoff_status": "unresolved",
        "repair_performed": False,
        "source_run": {
            "record_id": match.get("record_id"),
            "engine": match.get("engine"),
            "run_id": match.get("run_id"),
            "source_path": match.get("source_path"),
            "source_hash": match.get("source_hash"),
        },
        "normalized_evidence": {
            "status": match.get("status"),
            "terminal": match.get("terminal"),
            "machine_completion": match.get("machine_completion"),
            "human_acceptance": match.get("human_acceptance"),
            "judge_verdict": match.get("judge_verdict"),
            "human_label": match.get("human_label"),
            "stop_reason": match.get("stop_reason"),
            "escalation_reason": match.get("escalation_reason"),
        },
        "disagreement": disagreement,
        "owner_class": owner_class,
        "requested_outcome": (
            "Inspect the owning loop or judge, apply an authorized repair if needed, "
            "and produce a new terminal run that resolves this evidence gap."
        ),
        "preferred_destinations": preferred_destinations_for(match),
        "unresolved_proof": {
            "reason": "Loop Observatory is read-only and has not changed the source run or its judge.",
            "required_next_proof": (
                "A repair receipt from the owning capability and a newly ingested terminal run "
                "whose source hash differs from this record."
            ),
        },
    }


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    sub = root.add_subparsers(dest="command", required=True)
    register = sub.add_parser("register-root", help="Register an Operating Graph run root")
    register.add_argument("path", type=Path)
    ingest_parser = sub.add_parser("ingest", help="Ingest terminal runs")
    ingest_parser.add_argument("--loopkit-root", type=Path)
    report_parser = sub.add_parser("report", help="Write JSON and Markdown portfolio reports")
    report_parser.add_argument("--scheduled", action="store_true")
    sub.add_parser("audit", help="Audit judge calibration")
    handoff_parser = sub.add_parser("repair-handoff", help="Build a read-only generic repair handoff")
    handoff_parser.add_argument("record_id")
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        if args.command == "register-root":
            result = register_root(args.path)
        elif args.command == "ingest":
            result = ingest(args.loopkit_root)
        elif args.command == "report":
            result = report(args.scheduled)
        elif args.command == "audit":
            result = audit()
        else:
            result = repair_handoff(args.record_id)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
