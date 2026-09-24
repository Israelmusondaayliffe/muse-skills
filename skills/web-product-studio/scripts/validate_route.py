#!/usr/bin/env python3
"""Validate a web product route."""

import json
import sys
from pathlib import Path

ROUTES = {"greenfield", "redesign", "image-first", "targeted-fix", "quality-assurance"}

HIGH_VISUAL_PATTERNS = (
    "named visual reference", "match the reference", "match this screenshot", "reference image",
    "supplied reference", "approved frame", "film frame", "reference frame", "likeness",
    "look recognizably", "recognizable", "first-glance", "first glance", "photoreal",
    "cinematic", "material realism", "procedural", "shader", "webgl", "webgpu", "3d",
    "simulation", "motion-led", "motion hero", "video hero", "full-screen video",
    "immersive hero", "extreme state", "maximum intensity state",
)


def objective_requires_visual_gate(data: dict) -> bool:
    text = " ".join(str(data.get(field, "")) for field in ("objective", "rationale")).lower()
    return any(pattern in text for pattern in HIGH_VISUAL_PATTERNS)


def validate(data: dict) -> list[str]:
    errors = []
    if data.get("route") not in ROUTES:
        errors.append("route is invalid")
    for field in ("objective", "acceptance_flow", "rationale"):
        if not isinstance(data.get(field), str) or not data[field].strip():
            errors.append(f"{field} must be non-empty")
    constitution = data.get("design_constitution")
    if constitution is not None and (not isinstance(constitution, str) or not constitution.strip()):
        errors.append("design_constitution must be a non-empty string or null")
    skills = data.get("implementation_skills")
    if not isinstance(skills, list) or not all(isinstance(value, str) and value.strip() for value in skills):
        errors.append("implementation_skills must be a list")
        skills = []
    gate_required = data.get("visual_gate_required")
    if not isinstance(gate_required, bool):
        errors.append("visual_gate_required must be boolean")
    if objective_requires_visual_gate(data) and gate_required is not True:
        errors.append("the objective requires visual_gate_required true")
    visual_contract = data.get("visual_contract")
    if gate_required is True:
        if not isinstance(visual_contract, str) or not visual_contract.strip():
            errors.append("visual_contract must be non-empty when the visual gate is required")
        if "visual-fidelity-gate" not in skills:
            errors.append("a required visual gate must include visual-fidelity-gate")
    elif visual_contract is not None:
        errors.append("visual_contract must be null when the visual gate is not required")
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_route.py ROUTE.json", file=sys.stderr)
        return 2
    try:
        data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"invalid input: {exc}", file=sys.stderr)
        return 2
    errors = validate(data)
    print(json.dumps({"valid": not errors, "errors": errors}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
