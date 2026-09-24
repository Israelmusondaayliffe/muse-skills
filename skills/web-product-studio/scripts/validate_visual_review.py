#!/usr/bin/env python3
"""Validate visual-review evidence and the hero-first state transition."""

from __future__ import annotations

import json
import hashlib
import importlib.util
import re
import sys
from pathlib import Path
from typing import Any


STATES = ("target-locked", "hero-spike", "visual-passed", "full-build", "final-reviewed")
PREVIOUS = {
    "target-locked": {None},
    "hero-spike": {"target-locked", "hero-spike"},
    "visual-passed": {"hero-spike"},
    "full-build": {"visual-passed"},
    "final-reviewed": {"full-build"},
}
GATE_STATES = {"pending", "passed", "failed", "blocked"}
FAIL_DECISIONS = {"repair", "method-switch", "incomplete"}
HASH_FIELDS = ("contract_hash", "source_hash", "artifact_hash")
VIEWABLE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".mp4", ".webm"}


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def hash_path(path: Path) -> str:
    digest = hashlib.sha256()
    if path.is_file():
        return hashlib.sha256(path.read_bytes()).hexdigest()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        relative = item.relative_to(path).as_posix().encode("utf-8")
        digest.update(len(relative).to_bytes(8, "big"))
        digest.update(relative)
        payload = item.read_bytes()
        digest.update(len(payload).to_bytes(8, "big"))
        digest.update(payload)
    return digest.hexdigest()


def hash_files(paths: list[Path]) -> str:
    if len(paths) == 1:
        return hashlib.sha256(paths[0].read_bytes()).hexdigest()
    digest = hashlib.sha256()
    for path in paths:
        encoded = str(path).encode("utf-8")
        digest.update(len(encoded).to_bytes(8, "big"))
        digest.update(encoded)
        payload = path.read_bytes()
        digest.update(len(payload).to_bytes(8, "big"))
        digest.update(payload)
    return digest.hexdigest()


def viewable_file(path: Path) -> bool:
    if not path.is_absolute() or not path.is_file() or path.suffix.lower() not in VIEWABLE_SUFFIXES:
        return False
    payload = path.read_bytes()[:512]
    suffix = path.suffix.lower()
    if suffix == ".png":
        return payload.startswith(b"\x89PNG\r\n\x1a\n")
    if suffix in {".jpg", ".jpeg"}:
        return payload.startswith(b"\xff\xd8\xff")
    if suffix == ".webp":
        return payload.startswith(b"RIFF") and payload[8:12] == b"WEBP"
    if suffix == ".gif":
        return payload.startswith((b"GIF87a", b"GIF89a"))
    if suffix == ".svg":
        return b"<svg" in payload.lower()
    if suffix == ".mp4":
        return len(payload) >= 12 and payload[4:8] == b"ftyp"
    if suffix == ".webm":
        return payload.startswith(b"\x1aE\xdf\xa3")
    return False


def validate_contract(contract: dict[str, Any]) -> list[str]:
    """Run the sibling contract validator against the review's bound contract."""
    validator_path = Path(__file__).with_name("validate_visual_contract.py")
    spec = importlib.util.spec_from_file_location("visual_contract_validator", validator_path)
    if spec is None or spec.loader is None:
        return ["contract validator could not be loaded"]
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.validate(contract)


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if data.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    state = data.get("state")
    previous = data.get("previous_state")
    if state not in STATES:
        errors.append("state is invalid")
    elif previous not in PREVIOUS[state]:
        errors.append(f"invalid transition from {previous!r} to {state!r}")

    reviewer = data.get("reviewer")
    if not isinstance(reviewer, dict):
        errors.append("reviewer must be an object")
    else:
        if not nonempty(reviewer.get("id")) or not nonempty(reviewer.get("role")):
            errors.append("reviewer id and role must be non-empty")
        if reviewer.get("independent") is not True:
            errors.append("reviewer must be independent of the builder")

    contract_path_value = data.get("contract_path")
    contract_path = Path(contract_path_value) if nonempty(contract_path_value) else None
    contract: dict[str, Any] | None = None
    if contract_path is None or not contract_path.is_absolute() or not contract_path.is_file():
        errors.append("contract_path must be an absolute existing file")
    else:
        try:
            loaded = json.loads(contract_path.read_text(encoding="utf-8"))
            contract = loaded if isinstance(loaded, dict) else None
        except (OSError, json.JSONDecodeError):
            contract = None
        if contract is None:
            errors.append("contract_path must contain a JSON object")

    reference_paths: list[Path] = []
    rendered_paths: list[Path] = []
    comparison = data.get("comparison")
    if not isinstance(comparison, dict):
        errors.append("comparison must be an object")
    else:
        if not nonempty(comparison.get("viewport")):
            errors.append("comparison.viewport must be non-empty")
        for field in ("reference_paths", "rendered_paths"):
            values = comparison.get(field)
            if not isinstance(values, list) or not values or not all(nonempty(value) for value in values):
                errors.append(f"comparison.{field} must contain viewable evidence paths")
            else:
                parsed = [Path(value) for value in values]
                if not all(viewable_file(path) for path in parsed):
                    errors.append(f"comparison.{field} must contain absolute, existing, viewable assets")
                if field == "reference_paths":
                    reference_paths = parsed
                else:
                    rendered_paths = parsed

    score = data.get("visual_score")
    if not isinstance(score, (int, float)) or isinstance(score, bool) or not 0 <= score <= 10:
        errors.append("visual_score must be a number from 0 to 10")
        score = -1
    differences = data.get("differences")
    if not isinstance(differences, list):
        errors.append("differences must be a list")
        differences = []
    else:
        for index, difference in enumerate(differences):
            if not isinstance(difference, dict) or difference.get("severity") not in {"P0", "P1", "P2", "P3"} or not nonempty(difference.get("description")):
                errors.append(f"differences[{index}] must contain severity P0-P3 and a description")

    for field in ("functional_gate", "visual_gate"):
        if data.get(field) not in GATE_STATES:
            errors.append(f"{field} must be pending, passed, failed, or blocked")
    if not isinstance(data.get("secondary_features_started_before_visual_pass"), bool):
        errors.append("secondary_features_started_before_visual_pass must be boolean")
    if data.get("secondary_features_started_before_visual_pass") is True:
        errors.append("secondary features started before visual acceptance")
    control_case = data.get("control_case", False)
    if not isinstance(control_case, bool):
        errors.append("control_case must be boolean")
        control_case = False
    if control_case:
        if score != 10:
            errors.append("a mechanics-only control case must score 10")
        if not nonempty(data.get("control_limitation")) or "does not prove" not in data["control_limitation"].lower():
            errors.append("a mechanics-only control case must state that it does not prove visual quality")
        if len(reference_paths) != 1 or len(rendered_paths) != 1:
            errors.append("a mechanics-only control case must use one reference and one rendered path")
        elif reference_paths[0].read_bytes() != rendered_paths[0].read_bytes():
            errors.append("a mechanics-only control case must use the same reference and rendered bytes")
    for field in HASH_FIELDS:
        if not (isinstance(data.get(field), str) and re.fullmatch(r"[0-9a-f]{64}", data[field])):
            errors.append(f"{field} must be a 64-character lowercase sha256")

    if contract_path is not None and contract_path.is_file():
        expected_contract_hash = hashlib.sha256(contract_path.read_bytes()).hexdigest()
        if data.get("contract_hash") != expected_contract_hash:
            errors.append("contract_hash does not match contract_path")
    if contract is not None:
        errors.extend(f"contract: {error}" for error in validate_contract(contract))
        if contract.get("secondary_features_started") is not False:
            errors.append("contract must preserve the secondary-feature freeze")
        if contract.get("visual_gate") == "passed":
            errors.append("contract cannot self-declare visual acceptance")
        allowed_references = {
            item.get("evidence_path")
            for item in contract.get("references", [])
            if isinstance(item, dict)
        }
        if reference_paths and any(str(path) not in allowed_references for path in reference_paths):
            errors.append("comparison.reference_paths must be declared by the contract")
        viewport_names = {
            item.get("name")
            for item in (contract.get("viewports") or {}).values()
            if isinstance(item, dict)
        }
        if isinstance(comparison, dict) and comparison.get("viewport") not in viewport_names:
            errors.append("comparison.viewport must match a named contract viewport")
        source_path_value = contract.get("source_path")
        source_path = Path(source_path_value) if nonempty(source_path_value) else None
        if source_path is None or not source_path.is_absolute() or not source_path.exists():
            errors.append("contract source_path must be an absolute existing file or directory")
        else:
            expected_source_hash = hash_path(source_path)
            if contract.get("source_hash") != expected_source_hash:
                errors.append("contract source_hash does not match contract source_path")
            if data.get("source_hash") != expected_source_hash:
                errors.append("source_hash does not match contract source_path")
        hero_path_value = contract.get("hero_spike_path")
        hero_path = Path(hero_path_value) if nonempty(hero_path_value) else None
        if hero_path is None or not hero_path.is_absolute() or not hero_path.exists():
            errors.append("contract hero_spike_path must exist for review")
        elif rendered_paths:
            resolved_hero = hero_path.resolve()
            if hero_path.is_file() and all(path.resolve() != resolved_hero for path in rendered_paths):
                errors.append("a rendered comparison must match the contract hero_spike_path")
            if hero_path.is_dir() and all(resolved_hero not in path.resolve().parents for path in rendered_paths):
                errors.append("a rendered comparison must be inside the contract hero_spike_path")
    if rendered_paths and all(path.is_file() for path in rendered_paths):
        if data.get("artifact_hash") != hash_files(rendered_paths):
            errors.append("artifact_hash does not match comparison.rendered_paths")

    passing_state = state in {"visual-passed", "full-build", "final-reviewed"}
    high_severity = any(item.get("severity") in {"P0", "P1", "P2"} for item in differences if isinstance(item, dict))
    if passing_state:
        if score < 7:
            errors.append("visual-passed and later states require a score of at least 7")
        if high_severity:
            errors.append("visual-passed and later states cannot contain P0, P1, or P2 gaps")
        if data.get("visual_gate") != "passed":
            errors.append("visual-passed and later states require visual_gate passed")
        if data.get("decision") not in {"proceed", "complete"}:
            errors.append("visual-passed and later states require a proceed or complete decision")
    if data.get("visual_gate") == "passed" and state not in {"visual-passed", "full-build", "final-reviewed"}:
        errors.append("visual_gate cannot be passed before the visual-passed state")
    if score < 7:
        if state not in {"target-locked", "hero-spike"}:
            errors.append("a score below 7 cannot advance beyond hero-spike")
        if data.get("decision") not in FAIL_DECISIONS:
            errors.append("a score below 7 requires repair, method-switch, or incomplete")
        if data.get("visual_gate") == "passed":
            errors.append("a score below 7 cannot pass the visual gate")
        if not nonempty(data.get("incomplete_wording")):
            errors.append("a score below 7 requires honest incomplete wording")
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_visual_review.py REVIEW.json", file=sys.stderr)
        return 2
    try:
        data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"valid": False, "errors": [str(exc)]}, indent=2))
        return 2
    errors = validate(data) if isinstance(data, dict) else ["review root must be an object"]
    review_hash = hashlib.sha256(Path(sys.argv[1]).read_bytes()).hexdigest()
    print(json.dumps({"valid": not errors, "errors": errors, "review_hash": review_hash}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
