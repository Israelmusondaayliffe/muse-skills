#!/usr/bin/env python3
"""Validate a source-bound visual contract before hero implementation."""

from __future__ import annotations

import json
import hashlib
import re
import sys
from pathlib import Path
from typing import Any


GATE_STATES = {"pending", "passed", "failed", "blocked"}
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


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if data.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    for field in ("objective", "first_glance", "hero_spike_path"):
        if not nonempty(data.get(field)):
            errors.append(f"{field} must be non-empty")

    references = data.get("references")
    if not isinstance(references, list) or not 1 <= len(references) <= 3:
        errors.append("references must contain one to three items")
    else:
        for index, reference in enumerate(references):
            if not isinstance(reference, dict):
                errors.append(f"references[{index}] must be an object")
                continue
            for field in ("source", "permission_status", "evidence_path"):
                if not nonempty(reference.get(field)):
                    errors.append(f"references[{index}].{field} must be non-empty")
            evidence_path = reference.get("evidence_path")
            if nonempty(evidence_path) and not viewable_file(Path(evidence_path)):
                errors.append(f"references[{index}].evidence_path must be an absolute, existing, viewable asset")

    for field in ("non_negotiable_traits", "forbidden_failure_modes"):
        values = data.get(field)
        if not isinstance(values, list) or len(values) != 3 or not all(nonempty(value) for value in values):
            errors.append(f"{field} must contain exactly three non-empty strings")

    viewports = data.get("viewports")
    if not isinstance(viewports, dict):
        errors.append("viewports must be an object")
    else:
        for kind in ("desktop", "mobile"):
            viewport = viewports.get(kind)
            if not isinstance(viewport, dict):
                errors.append(f"viewports.{kind} must be an object")
                continue
            for field in ("name", "framing"):
                if not nonempty(viewport.get(field)):
                    errors.append(f"viewports.{kind}.{field} must be non-empty")
            for field in ("width", "height"):
                if not isinstance(viewport.get(field), int) or viewport[field] <= 0:
                    errors.append(f"viewports.{kind}.{field} must be a positive integer")

    medium = data.get("medium")
    if not isinstance(medium, dict):
        errors.append("medium must be an object")
    else:
        for field in ("selected", "rationale", "switch_condition"):
            if not nonempty(medium.get(field)):
                errors.append(f"medium.{field} must be non-empty")
        rejected = medium.get("rejected")
        if not isinstance(rejected, list) or not all(nonempty(value) for value in rejected):
            errors.append("medium.rejected must be a list of non-empty strings")

    states = data.get("states")
    if not isinstance(states, list) or not states or "default" not in states or not all(nonempty(value) for value in states):
        errors.append("states must contain at least the default state")
    if data.get("secondary_features_started") is not False:
        errors.append("secondary features must not be started in the pre-implementation contract")
    for field in ("functional_gate", "visual_gate"):
        if data.get(field) not in GATE_STATES:
            errors.append(f"{field} must be pending, passed, failed, or blocked")
    if data.get("visual_gate") == "passed":
        errors.append("the pre-implementation contract cannot self-declare visual_gate passed; record acceptance in a review")
    if data.get("visual_gate") != "passed" and not nonempty(data.get("incomplete_wording")):
        errors.append("incomplete_wording is required until the visual gate passes")

    conflicts = data.get("constraint_conflicts")
    if not isinstance(conflicts, list) or not all(nonempty(value) for value in conflicts):
        errors.append("constraint_conflicts must be a list of non-empty strings")
        conflicts = []
    if not isinstance(data.get("conflicts_resolved"), bool):
        errors.append("conflicts_resolved must be boolean")
    if conflicts and data.get("conflicts_resolved") is not True:
        errors.append("all declared constraint conflicts must be resolved before implementation")

    wording = " ".join(
        str(value)
        for value in [
            data.get("objective", ""),
            data.get("first_glance", ""),
            *(data.get("non_negotiable_traits") or []),
            *(data.get("forbidden_failure_modes") or []),
        ]
    ).lower()
    kerr_request = "interstellar" in wording or "kerr" in wording
    nonspinning_request = "schwarzschild" in wording or "non-spinning" in wording or "nonspinning" in wording
    if kerr_request and nonspinning_request and not conflicts:
        errors.append("Kerr or Interstellar and non-spinning Schwarzschild requirements need an explicit resolved conflict record")

    source_path_value = data.get("source_path")
    source_path = Path(source_path_value) if nonempty(source_path_value) else None
    if source_path is None or not source_path.is_absolute() or not source_path.exists():
        errors.append("source_path must be an absolute existing file or directory")

    hero_path_value = data.get("hero_spike_path")
    if nonempty(hero_path_value) and not Path(hero_path_value).is_absolute():
        errors.append("hero_spike_path must be absolute")

    source_hash = data.get("source_hash")
    if source_hash != "pending" and not (isinstance(source_hash, str) and re.fullmatch(r"[0-9a-f]{64}", source_hash)):
        errors.append("source_hash must be pending or a 64-character lowercase sha256")
    elif source_hash != "pending" and source_path is not None and source_path.exists():
        if source_hash != hash_path(source_path):
            errors.append("source_hash does not match source_path")
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_visual_contract.py CONTRACT.json", file=sys.stderr)
        return 2
    try:
        data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"valid": False, "errors": [str(exc)]}, indent=2))
        return 2
    errors = validate(data) if isinstance(data, dict) else ["contract root must be an object"]
    print(json.dumps({"valid": not errors, "errors": errors}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
