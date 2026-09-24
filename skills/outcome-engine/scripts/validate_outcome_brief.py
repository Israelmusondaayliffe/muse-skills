#!/usr/bin/env python3
"""Validate the required structure of an Outcome Engine brief."""

from __future__ import annotations

import re
import sys
from pathlib import Path


REQUIRED_SECTIONS = (
    "Outcome",
    "Audience or user",
    "Success evidence",
    "Constraints",
    "Decisions",
    "Blockers",
    "Out of scope",
    "Next action",
)

PLACEHOLDER_PATTERN = re.compile(
    r"\b(?:TODO|TBD)\b|\{\{[^}]+\}\}|"
    r"\[(?:insert|add|describe|placeholder|name|date)[^\]]*\]|"
    r"<[^>\n]+>",
    re.IGNORECASE,
)


def section_content(text: str, heading: str) -> str | None:
    heading_pattern = re.compile(
        rf"^#{{1,6}}\s+{re.escape(heading)}\s*$", re.IGNORECASE | re.MULTILINE
    )
    match = heading_pattern.search(text)
    if not match:
        return None

    remainder = text[match.end() :]
    next_heading = re.search(r"^#{1,6}\s+", remainder, re.MULTILINE)
    if next_heading:
        remainder = remainder[: next_heading.start()]
    return remainder.strip()


def validate(path: Path) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return [f"Could not read {path}: {exc}"]

    errors: list[str] = []
    for heading in REQUIRED_SECTIONS:
        content = section_content(text, heading)
        if content is None:
            errors.append(f"Missing section: {heading}")
        elif not content:
            errors.append(f"Section has no content: {heading}")

    placeholder = PLACEHOLDER_PATTERN.search(text)
    if placeholder:
        errors.append(f"Unresolved placeholder: {placeholder.group(0)}")

    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: validate_outcome_brief.py PATH", file=sys.stderr)
        return 2

    path = Path(argv[1]).expanduser()
    errors = validate(path)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"PASS: valid outcome brief: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
