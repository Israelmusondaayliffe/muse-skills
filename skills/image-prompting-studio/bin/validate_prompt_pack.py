#!/usr/bin/env python3
"""Validate a saved Midjourney prompt pack against the bundled model profile."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


TEXT_BLOCK = re.compile(r"```text\s*\n(.*?)\n```", re.DOTALL | re.IGNORECASE)
PARAMETER = re.compile(r"(?<!\S)--([a-z][a-z-]*)\b", re.IGNORECASE)
URL = re.compile(r"https://\S+", re.IGNORECASE)
PLACEHOLDER = re.compile(r"\[(?:complete|include|prompt|placeholder|todo)[^\]]*\]", re.IGNORECASE)


def load_profile(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("model profile must be a JSON object")
    return payload


def alias_map(profile: dict[str, Any]) -> tuple[dict[str, str], set[str]]:
    known: dict[str, str] = {}
    unsupported: set[str] = set()
    groups = profile.get("parameters", {})
    for group_name in ("supported", "documented_controls_not_added_automatically", "unsupported"):
        for item in groups.get(group_name, []):
            canonical = item["name"]
            for alias in item.get("aliases", []):
                normalized = alias.removeprefix("--").lower()
                known[normalized] = canonical
                if group_name == "unsupported":
                    unsupported.add(normalized)
    return known, unsupported


def numeric_value(prompt: str, aliases: list[str]) -> float | None:
    names = "|".join(re.escape(alias.removeprefix("--")) for alias in aliases)
    match = re.search(rf"(?<!\S)--(?:{names})\s+(-?\d+(?:\.\d+)?)\b", prompt, re.IGNORECASE)
    return float(match.group(1)) if match else None


def validate_range(prompt: str, aliases: list[str], limits: dict[str, Any], label: str, errors: list[str]) -> None:
    value = numeric_value(prompt, aliases)
    if value is not None and not limits["min"] <= value <= limits["max"]:
        errors.append(f"{label} value {value:g} is outside {limits['min']} to {limits['max']}")


def aspect_ratio(prompt: str) -> tuple[float, str] | None:
    match = re.search(r"(?<!\S)--(?:ar|aspect)\s+(\d+(?:\.\d+)?):(\d+(?:\.\d+)?)\b", prompt, re.IGNORECASE)
    if not match:
        return None
    left, right = float(match.group(1)), float(match.group(2))
    if left == 0 or right == 0:
        return float("inf"), match.group(0)
    return max(left / right, right / left), match.group(0)


def validate_parameter_suffix(prompt: str, matches: list[re.Match[str]], errors: list[str], label: str) -> None:
    """Check fixed-arity parameters so descriptive text cannot resume after them."""
    one_value = {
        "v", "version", "ar", "aspect", "c", "chaos", "seed", "s", "stylize",
        "sw", "iw", "w", "weird", "exp", "r", "repeat",
    }
    optional_value = set()
    no_value = {"raw", "tile", "sd", "hd", "fast", "relax", "public", "stealth", "turbo", "draft", "niji"}
    free_value = {"sref", "no", "oref", "cref"}

    for index, match in enumerate(matches):
        next_start = matches[index + 1].start() if index + 1 < len(matches) else len(prompt)
        values = prompt[match.end():next_start].strip().split()
        name = match.group(1).lower()
        if name in one_value and len(values) != 1:
            errors.append(f"{label}: --{name} expects exactly one value and parameters must stay at the end")
        elif name in optional_value and len(values) > 1:
            errors.append(f"{label}: --{name} accepts at most one value and parameters must stay at the end")
        elif name in no_value and values:
            errors.append(f"{label}: text appears after flag --{name}; keep the description before all parameters")
        elif name in free_value and not values:
            errors.append(f"{label}: --{name} requires a value")


def validate_prompt(prompt: str, profile: dict[str, Any] | None, number: int, expected_refs: list[str]) -> list[str]:
    errors: list[str] = []
    label = f"prompt {number}"
    if "\n" in prompt.strip():
        errors.append(f"{label}: prompt must stay on one line for copy and paste")
    if PLACEHOLDER.search(prompt):
        errors.append(f"{label}: placeholder remains")
    if profile and "::" in prompt:
        errors.append(f"{label}: multi-prompt or weighted separator is unsupported by the current model profile")

    known, unsupported = alias_map(profile) if profile else ({}, set())
    parameter_matches = list(PARAMETER.finditer(prompt))
    aliases = [match.group(1).lower() for match in parameter_matches]
    for alias in aliases:
        if profile and alias not in known:
            errors.append(f"{label}: unknown parameter --{alias}")
        elif profile and alias in unsupported:
            errors.append(f"{label}: unsupported parameter --{alias}")

    first_parameter = PARAMETER.search(prompt)
    if first_parameter and not prompt[: first_parameter.start()].strip():
        errors.append(f"{label}: image description is missing before parameters")
    validate_parameter_suffix(prompt, parameter_matches, errors, label)

    if any(alias in aliases for alias in ("sw",)) and "sref" not in aliases:
        errors.append(f"{label}: --sw requires --sref")
    if "iw" in aliases:
        prefix = prompt[: first_parameter.start()] if first_parameter else prompt
        if not URL.search(prefix):
            errors.append(f"{label}: --iw requires an Image Prompt URL before the text description")

    if profile:
        limits = profile["limits"]
        validate_range(prompt, ["--s", "--stylize"], limits["stylize"], f"{label}: stylize", errors)
        validate_range(prompt, ["--c", "--chaos"], limits["chaos"], f"{label}: chaos", errors)
        validate_range(prompt, ["--w", "--weird"], limits["weird"], f"{label}: weird", errors)
        validate_range(prompt, ["--sw"], limits["style_weight"], f"{label}: style weight", errors)
        validate_range(prompt, ["--iw"], limits["image_weight"], f"{label}: image weight", errors)

        ratio = aspect_ratio(prompt)
        if ratio and ratio[0] > 14:
            errors.append(f"{label}: {ratio[1]} exceeds the current SD 14:1 limit")
        if ratio and "hd" in aliases and ratio[0] > 4:
            errors.append(f"{label}: {ratio[1]} exceeds the current HD 4:1 limit")

        version = re.search(r"(?<!\S)--(?:v|version)\s+(\S+)", prompt, re.IGNORECASE)
        if version and version.group(1) != profile["default_model"]["version_value"]:
            errors.append(f"{label}: version {version.group(1)} is not covered by the bundled current-model profile")

    for reference in expected_refs:
        if reference not in prompt:
            errors.append(f"{label}: expected reference was not preserved exactly: {reference}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prompt_pack", type=Path)
    parser.add_argument("--profile", type=Path)
    parser.add_argument("--count", type=int)
    parser.add_argument("--expect-reference", action="append", default=[])
    parser.add_argument("--require-current-version", action="store_true")
    args = parser.parse_args()

    profile_path = args.profile
    try:
        profile = load_profile(profile_path) if profile_path else None
        text = args.prompt_pack.read_text(encoding="utf-8")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(json.dumps({"valid": False, "errors": [str(exc)]}, indent=2))
        return 2

    prompts = [block.strip() for block in TEXT_BLOCK.findall(text)]
    errors: list[str] = []
    if args.count is not None and len(prompts) != args.count:
        errors.append(f"expected {args.count} text prompt blocks, found {len(prompts)}")
    if not prompts:
        errors.append("prompt pack contains no complete text prompt blocks")
    if args.count is not None and args.count < 1:
        errors.append("expected count must be positive")
    if args.require_current_version and not profile:
        errors.append("--require-current-version requires an explicit --profile snapshot")
    if len(set(prompts)) != len(prompts):
        errors.append("prompt pack contains duplicate prompts")
    for index, prompt in enumerate(prompts, 1):
        errors.extend(validate_prompt(prompt, profile, index, args.expect_reference))
        if args.require_current_version and profile:
            version = profile["default_model"]["version_value"]
            if not re.search(rf"(?<!\S)--(?:v|version)\s+{re.escape(version)}(?:\s|$)", prompt, re.IGNORECASE):
                errors.append(f"prompt {index}: current version --v {version} is required")

    result = {
        "valid": not errors,
        "prompt_count": len(prompts),
        "expected_count": args.count,
        "profile_model": profile["default_model"]["name"] if profile else None,
        "profile_checked_on": profile["checked_on"] if profile else None,
        "parameter_validation": "explicit_profile_snapshot_only" if profile else "structural_only",
        "live_model_verified": False,
        "errors": errors,
    }
    print(json.dumps(result, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
