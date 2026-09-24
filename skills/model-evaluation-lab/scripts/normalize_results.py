#!/usr/bin/env python3
"""Normalize raw case results and calculate stable candidate aggregates."""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path
from statistics import mean


def fail(message: str) -> int:
    print(json.dumps({"valid": False, "errors": [message]}, indent=2), file=sys.stderr)
    return 2


def main() -> int:
    if len(sys.argv) not in (2, 3):
        print("usage: normalize_results.py RAW.json [NORMALIZED.json]", file=sys.stderr)
        return 2
    try:
        raw = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return fail(f"raw input is invalid: {exc}")
    if not isinstance(raw, dict):
        return fail("raw input must be a JSON object")
    for field in ("run_id", "plan_hash", "environment", "metric_name"):
        if not isinstance(raw.get(field), str) or not raw[field].strip():
            return fail(f"{field} must be a non-empty string")
    cases = raw.get("cases")
    if not isinstance(cases, list) or not cases:
        return fail("cases must be a non-empty list")
    required = ("id", "candidate", "passed", "score", "latency_ms", "cost_usd")
    identifiers: set[str] = set()
    groups: dict[str, list[dict[str, object]]] = defaultdict(list)
    normalized_cases: list[dict[str, object]] = []
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            return fail(f"cases[{index}] must be an object")
        missing = [field for field in required if field not in case]
        if missing:
            return fail(f"cases[{index}] missing fields: {missing}")
        identifier = case["id"]
        candidate = case["candidate"]
        if not isinstance(identifier, str) or not identifier.strip() or identifier in identifiers:
            return fail(f"cases[{index}].id must be non-empty and unique")
        if not isinstance(candidate, str) or not candidate.strip():
            return fail(f"cases[{index}].candidate must be a non-empty string")
        if not isinstance(case["passed"], bool):
            return fail(f"cases[{index}].passed must be boolean")
        for field in ("score", "latency_ms", "cost_usd"):
            value = case[field]
            if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
                return fail(f"cases[{index}].{field} must be a non-negative number")
        record = {field: case[field] for field in required}
        identifiers.add(identifier)
        normalized_cases.append(record)
        groups[candidate].append(record)
    aggregates = []
    for candidate in sorted(groups):
        records = groups[candidate]
        aggregates.append({
            "id": candidate,
            "candidate": candidate,
            "case_count": len(records),
            "pass_rate": round(sum(1 for item in records if item["passed"]) / len(records), 6),
            "mean_score": round(mean(float(item["score"]) for item in records), 6),
            "mean_latency_ms": round(mean(float(item["latency_ms"]) for item in records), 6),
            "total_cost_usd": round(sum(float(item["cost_usd"]) for item in records), 6),
        })
    execution_errors = raw.get("execution_errors", [])
    expected = raw.get("expected_case_count", len(normalized_cases))
    complete = isinstance(expected, int) and expected == len(normalized_cases) and not execution_errors
    output = {
        "run_id": raw["run_id"],
        "plan_hash": raw["plan_hash"],
        "environment": raw["environment"],
        "metric_name": raw["metric_name"],
        "results": normalized_cases,
        "aggregates": aggregates,
        "failures": [
            {"id": item["id"], "candidate": item["candidate"]}
            for item in normalized_cases
            if not item["passed"]
        ]
        + (execution_errors if isinstance(execution_errors, list) else []),
        "execution_status": "complete" if complete else "partial",
        "results_complete": complete,
    }
    rendered = json.dumps(output, indent=2, sort_keys=True) + "\n"
    if len(sys.argv) == 3:
        Path(sys.argv[2]).write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
