#!/usr/bin/env python3
"""Validate reviewer independence, gate evidence, and human-approval state."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SCHEMA = "guide-production-studio/guide-review/v1"
GATES = [
    "purpose", "context", "vocabulary", "action", "evidence",
    "provenance_privacy", "examples_reuse", "troubleshooting",
    "structure_visuals", "voice_value",
]
STATUSES = {"blocked", "rejected", "ready_for_human_review", "human_approved"}


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate(data: Any, require_human: bool = False) -> list[str]:
    errors: list[str] = []
    required = {
        "schema_version", "guide_contract_id", "producer_id", "reviewer_id",
        "status", "gates", "critical_failures", "first_confusion_point",
        "cold_reader", "human_approval", "next_action",
    }
    if not isinstance(data, dict):
        return ["review root must be an object"]
    if set(data) != required:
        errors.append(
            f"review fields mismatch: missing={sorted(required - set(data))} "
            f"extra={sorted(set(data) - required)}"
        )
    if data.get("schema_version") != SCHEMA:
        errors.append(f"schema_version must be {SCHEMA}")
    for field in ("guide_contract_id", "producer_id", "reviewer_id", "next_action"):
        if not nonempty(data.get(field)) or "replace-with" in str(data.get(field, "")):
            errors.append(f"{field} must be resolved")
    if data.get("producer_id") == data.get("reviewer_id"):
        errors.append("producer and reviewer must be different")
    status = data.get("status")
    if status not in STATUSES:
        errors.append(f"status must be one of {sorted(STATUSES)}")

    gates = data.get("gates")
    passed_all = True
    if not isinstance(gates, list) or len(gates) != len(GATES):
        errors.append("gates must contain exactly ten records")
        gates = []
        passed_all = False
    seen: list[str] = []
    for index, gate in enumerate(gates):
        if not isinstance(gate, dict) or set(gate) != {"id", "passed", "evidence"}:
            errors.append(f"gates[{index}] has invalid fields")
            passed_all = False
            continue
        seen.append(gate.get("id"))
        if not isinstance(gate.get("passed"), bool):
            errors.append(f"gates[{index}].passed must be boolean")
            passed_all = False
        if gate.get("passed") is True and not nonempty(gate.get("evidence")):
            errors.append(f"gates[{index}] passed without evidence")
        if gate.get("passed") is not True:
            passed_all = False
    if seen != GATES:
        errors.append("gates must use the ten ordered gate ids")

    critical = data.get("critical_failures")
    if not isinstance(critical, list) or any(not nonempty(item) for item in critical):
        errors.append("critical_failures must be a list of non-empty strings")
        critical = []

    cold = data.get("cold_reader")
    if not isinstance(cold, dict) or set(cold) != {"observed", "completed_first_action", "evidence"}:
        errors.append("cold_reader has invalid fields")
        cold = {}
    else:
        for field in ("observed", "completed_first_action"):
            if not isinstance(cold.get(field), bool):
                errors.append(f"cold_reader.{field} must be boolean")
        if cold.get("observed") and not nonempty(cold.get("evidence")):
            errors.append("observed cold-reader work requires evidence")

    human = data.get("human_approval")
    if not isinstance(human, dict) or set(human) != {"owner", "confirmed", "approved_at", "evidence"}:
        errors.append("human_approval has invalid fields")
        human = {}
    else:
        if not nonempty(human.get("owner")):
            errors.append("human_approval.owner must be non-empty")
        if not isinstance(human.get("confirmed"), bool):
            errors.append("human_approval.confirmed must be boolean")

    if status == "ready_for_human_review" and (not passed_all or critical):
        errors.append("ready_for_human_review requires every gate to pass and no critical failures")
    if status == "human_approved":
        if not passed_all or critical:
            errors.append("human_approved requires every gate to pass and no critical failures")
        has_human_evidence = (
            human.get("confirmed") is True
            and nonempty(human.get("approved_at"))
            and nonempty(human.get("evidence"))
        )
        if not has_human_evidence:
            errors.append("human_approved requires explicit human confirmation, time, and evidence")
        has_cold_reader_evidence = (
            cold.get("observed") is True
            and cold.get("completed_first_action") is True
            and nonempty(cold.get("evidence"))
        )
        if not has_cold_reader_evidence:
            errors.append("human_approved baseline requires a completed cold-reader observation")
    if human.get("confirmed") is True and status != "human_approved":
        errors.append("confirmed human approval requires status human_approved")
    if require_human and status != "human_approved":
        errors.append("human approval is required but not present")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("review", type=Path)
    parser.add_argument("--require-human-approval", action="store_true")
    args = parser.parse_args()
    try:
        data = json.loads(args.review.read_text(encoding="utf-8"))
        errors = validate(data, args.require_human_approval)
    except (OSError, json.JSONDecodeError) as exc:
        errors = [str(exc)]
    print(json.dumps({"valid": not errors, "errors": errors}, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
