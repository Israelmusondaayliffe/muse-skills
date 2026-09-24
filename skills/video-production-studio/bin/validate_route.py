#!/usr/bin/env python3
"""Validate a video production route for the Hatch video-production-studio skill."""

import json
import sys
from pathlib import Path

ROUTES = {
    "faceless-explainer", "product-launch", "pr-story", "website-capture",
    "music-visualization", "slideshow", "motion-graphics", "general-video",
    "ai-generation", "captions-only", "overlays-only",
}
# Production surfaces actually available on Hatch.
RUNTIMES = {"ffmpeg", "ai-generation", "browser-capture", "hybrid", "external", "none"}
COMPLETION_STATES = {"planning-complete", "rendered-delivery-complete"}
PLANNING_ARTIFACTS = {
    "video-brief.md", "storyboard.md", "shot-list.md", "asset-ledger.md",
    "runtime-requirements.md", "delivery-checklist.md",
}
NO_RENDERER_RUNTIMES = {"none"}


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_route.py ROUTE.json", file=sys.stderr)
        return 2
    try:
        data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"invalid input: {exc}", file=sys.stderr)
        return 2
    errors = []
    if data.get("route") not in ROUTES:
        errors.append("route is invalid")
    runtime = data.get("runtime")
    completion_state = data.get("completion_state")
    renderer_available = data.get("renderer_available")
    rendering_status = data.get("rendering_status")
    visual_qc_status = data.get("visual_qc_status")
    if runtime not in RUNTIMES:
        errors.append("runtime is invalid")
    if not isinstance(renderer_available, bool):
        errors.append("renderer_available must be a boolean")
    if completion_state not in COMPLETION_STATES:
        errors.append("completion_state is invalid")
    artifacts = data.get("planning_artifacts")
    if (
        not isinstance(artifacts, list)
        or len(artifacts) != len(PLANNING_ARTIFACTS)
        or not all(isinstance(item, str) for item in artifacts)
        or set(artifacts) != PLANNING_ARTIFACTS
    ):
        errors.append("planning_artifacts must contain the complete planning bundle")
    if rendering_status not in {"complete", "incomplete"}:
        errors.append("rendering_status is invalid")
    if visual_qc_status not in {"complete", "incomplete"}:
        errors.append("visual_qc_status is invalid")
    if renderer_available is False and runtime not in NO_RENDERER_RUNTIMES:
        errors.append("an unavailable renderer requires runtime none")
    if renderer_available is True and runtime in NO_RENDERER_RUNTIMES:
        errors.append("runtime none cannot claim an available renderer")
    if completion_state == "planning-complete":
        if rendering_status != "incomplete" or visual_qc_status != "incomplete":
            errors.append("planning-complete requires rendering and visual QC to remain incomplete")
    if completion_state == "rendered-delivery-complete":
        if renderer_available is not True:
            errors.append("rendered-delivery-complete requires an available renderer")
        if rendering_status != "complete" or visual_qc_status != "complete":
            errors.append("rendered-delivery-complete requires completed rendering and visual QC")
    for field in ("duration_seconds", "width", "height"):
        if not isinstance(data.get(field), int) or data[field] <= 0:
            errors.append(f"{field} must be a positive integer")
    skills = data.get("skills")
    if not isinstance(skills, list) or not skills:
        errors.append("skills must be a non-empty list")
    if completion_state == "rendered-delivery-complete" and (
        not isinstance(skills, list) or "video-delivery-qc" not in skills
    ):
        errors.append("rendered-delivery-complete requires video-delivery-qc")
    for field in ("objective", "rationale"):
        if not isinstance(data.get(field), str) or not data[field].strip():
            errors.append(f"{field} must be non-empty")
    print(json.dumps({"valid": not errors, "errors": errors}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
