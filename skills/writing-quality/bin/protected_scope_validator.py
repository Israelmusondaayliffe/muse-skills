#!/usr/bin/env python3
"""Verify exact protected material while allowing delimiter-only unbolding."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys


STRUCTURED_SUFFIXES = {
    ".json",
    ".jsonl",
    ".yaml",
    ".yml",
    ".toml",
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".sh",
}


def _inline_code(text: str) -> list[str]:
    return [match.group(0) for match in re.finditer(r"(?<!`)`[^`\n]+`(?!`)", text)]


def _quoted_text(text: str) -> list[str]:
    spans: list[tuple[int, str]] = []
    for opening, closing in (("\"", "\""), ("“", "”"), ("‘", "’")):
        cursor = 0
        while cursor < len(text):
            start = text.find(opening, cursor)
            if start < 0:
                break
            end_marker = text.find(closing, start + len(opening))
            if end_marker < 0:
                break
            end = end_marker + len(closing)
            spans.append((start, text[start:end]))
            cursor = end
    return [value for _, value in sorted(spans)]


def _fenced_blocks(text: str) -> list[str]:
    lines = text.splitlines(keepends=True)
    blocks: list[str] = []
    start: tuple[str, int, int] | None = None
    for index, line in enumerate(lines):
        match = re.match(r"^\s{0,3}(`{3,}|~{3,})(.*)$", line.rstrip("\r\n"))
        if not match:
            continue
        marker = match.group(1)
        if start is None:
            start = (marker[0], len(marker), index)
        elif marker[0] == start[0] and len(marker) >= start[1] and not match.group(2).strip():
            blocks.append("".join(lines[start[2] : index + 1]))
            start = None
    if start is not None:
        blocks.append("".join(lines[start[2] :]))
    return blocks


def _table_lines(text: str) -> list[str]:
    lines = text.splitlines(keepends=True)
    selected: set[int] = set()
    separator = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?\s*$")
    for index, line in enumerate(lines):
        if not separator.fullmatch(line.rstrip("\r\n")):
            continue
        if index > 0 and "|" in lines[index - 1]:
            selected.add(index - 1)
        selected.add(index)
        cursor = index + 1
        while cursor < len(lines) and "|" in lines[cursor] and lines[cursor].strip():
            selected.add(cursor)
            cursor += 1
    return [lines[index] for index in sorted(selected)]


def protected_material(text: str, suffix: str = ".md") -> dict[str, list[str]]:
    if suffix.lower() in STRUCTURED_SUFFIXES:
        return {"structured_data_or_template": [text]}
    lines = text.splitlines(keepends=True)
    frontmatter: list[str] = []
    if lines and lines[0].rstrip("\r\n") == "---":
        for index in range(1, len(lines)):
            if lines[index].rstrip("\r\n") == "---":
                frontmatter = ["".join(lines[: index + 1])]
                break
    block_quotes = [line for line in lines if line.lstrip().startswith(">")]
    indented = [
        line for line in lines if line.strip() and (line.startswith("    ") or line.startswith("\t"))
    ]
    patterns = {
        "links": r"!?\[[^\]\n]*\]\([^\)\n]+\)",
        "urls": r"https?://[^\s<>\)\]]+",
        "paths": r"(?<![\w.])(?:~|/|\.{0,2}/)?(?:[A-Za-z0-9._+-]+/)+[A-Za-z0-9._+-]+",
        "citations": r"\[(?:\d+[\d,\s-]*|[^\]\n]+?\s+et al\.,?\s+\d{4})\]",
        "uuids": r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b",
        "digests": r"\b[0-9a-fA-F]{40,64}\b",
        "skill_tokens": r"\$[a-z0-9][a-z0-9-]*",
        "namespaced_identifiers": r"\b[a-z0-9][a-z0-9-]*:[a-z0-9][a-z0-9-]*\b",
    }
    result = {
        "frontmatter": frontmatter,
        "fenced_code_logs_or_prompts": _fenced_blocks(text),
        "block_quotes": block_quotes,
        "indented_code_or_commands": indented,
        "tables": _table_lines(text),
        "inline_code_commands_or_identifiers": _inline_code(text),
        "quoted_text": _quoted_text(text),
    }
    for name, pattern in patterns.items():
        result[name] = [match.group(0) for match in re.finditer(pattern, text)]
    return result


def _strong_requirements(text: str) -> Counter[str]:
    contents: list[str] = []
    for pattern in (
        r"(?<!\*)\*\*((?:(?!\*\*).)+?)\*\*(?!\*)",
        r"(?<!_)__((?:(?!__).)+?)__(?!_)",
    ):
        contents.extend(match.group(1) for match in re.finditer(pattern, text, re.DOTALL))
    required: Counter[str] = Counter()
    for content in contents:
        digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
        required[f"{len(content)}:{digest}"] = sum(
            1 for start in range(len(text) - len(content) + 1) if text[start : start + len(content)] == content
        )
    return required


def _available_strong_content(text: str, required: Counter[str]) -> Counter[str]:
    available: Counter[str] = Counter()
    for key in required:
        raw_length, digest = key.split(":", 1)
        length = int(raw_length)
        available[key] = sum(
            1
            for start in range(len(text) - length + 1)
            if hashlib.sha256(text[start : start + length].encode("utf-8")).hexdigest() == digest
        )
    return available


def compare_protected(before: str, after: str, suffix: str = ".md") -> dict[str, object]:
    before_material = protected_material(before, suffix)
    after_material = protected_material(after, suffix)
    changed = sorted(
        category for category in before_material if before_material[category] != after_material.get(category)
    )
    required = _strong_requirements(before)
    missing_strong = required - _available_strong_content(after, required)
    if missing_strong:
        changed.append("strong_text_content")
    return {
        "valid": not changed,
        "changed_categories": sorted(set(changed)),
        "before_counts": {key: len(value) for key, value in before_material.items()},
        "after_counts": {key: len(value) for key, value in after_material.items()},
    }


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: protected_scope_validator.py BEFORE AFTER", file=sys.stderr)
        return 2
    before_path = Path(sys.argv[1])
    after_path = Path(sys.argv[2])
    if before_path.suffix.lower() != after_path.suffix.lower():
        result = {"valid": False, "changed_categories": ["file_type"]}
    else:
        try:
            result = compare_protected(
                before_path.read_text(encoding="utf-8"),
                after_path.read_text(encoding="utf-8"),
                before_path.suffix,
            )
        except (OSError, UnicodeDecodeError) as exc:
            print(json.dumps({"valid": False, "error": str(exc)}, indent=2))
            return 2
    print(json.dumps(result, indent=2))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
