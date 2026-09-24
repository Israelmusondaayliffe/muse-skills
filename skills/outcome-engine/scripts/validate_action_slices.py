#!/usr/bin/env python3
"""Validate Outcome Engine action slices and their dependency graph."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


def nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def nonempty_string_list(value: Any) -> bool:
    return (
        isinstance(value, list)
        and bool(value)
        and all(nonempty_string(item) for item in value)
    )


def has_cycle(graph: dict[str, list[str]]) -> bool:
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> bool:
        if node in visiting:
            return True
        if node in visited:
            return False

        visiting.add(node)
        for dependency in graph.get(node, []):
            if dependency in graph and visit(dependency):
                return True
        visiting.remove(node)
        visited.add(node)
        return False

    return any(visit(node) for node in graph)


def load_payload(path: Path) -> tuple[Any | None, list[str]]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), []
    except OSError as exc:
        return None, [f"Could not read {path}: {exc}"]
    except json.JSONDecodeError as exc:
        return None, [f"Invalid JSON: {exc}"]


def validate_boundaries(label: str, value: Any) -> list[str]:
    if not isinstance(value, dict):
        return [f"{label} needs boundaries"]

    errors: list[str] = []
    for key in ("in_scope", "out_of_scope"):
        entries = value.get(key)
        if not isinstance(entries, list) or not all(
            nonempty_string(entry) for entry in entries
        ):
            errors.append(f"{label} boundaries.{key} must be an array of text")
    return errors


def validate_slice(item: Any, index: int) -> tuple[str | None, list[str]]:
    label = f"slice {index}"
    if not isinstance(item, dict):
        return None, [f"{label} must be an object"]

    errors: list[str] = []
    identifier = item.get("id")
    if not nonempty_string(identifier):
        errors.append(f"{label} needs a non-empty id")
        identifier = None
    else:
        label = identifier

    required_text = ("title", "outcome", "proof")
    for key in required_text:
        if not nonempty_string(item.get(key)):
            errors.append(f"{label} needs a non-empty {key}")

    if not nonempty_string_list(item.get("acceptance_checks")):
        errors.append(f"{label} needs at least one acceptance check")

    blockers = item.get("blocked_by")
    if not isinstance(blockers, list) or not all(
        nonempty_string(blocker) for blocker in blockers
    ):
        errors.append(f"{label} blocked_by must be an array of IDs")

    errors.extend(validate_boundaries(label, item.get("boundaries")))
    return identifier, errors


def dependency_errors(slices: list[Any], identifiers: list[str]) -> list[str]:
    known = set(identifiers)
    graph: dict[str, list[str]] = {}
    errors: list[str] = []

    for item in slices:
        if not isinstance(item, dict) or not nonempty_string(item.get("id")):
            continue

        blockers = item.get("blocked_by")
        if not isinstance(blockers, list):
            blockers = []
        valid_blockers = [blocker for blocker in blockers if nonempty_string(blocker)]
        graph[item["id"]] = valid_blockers
        for blocker in valid_blockers:
            if blocker not in known:
                errors.append(f"{item['id']} references unknown blocker: {blocker}")

    if has_cycle(graph):
        errors.append("Dependency graph contains a cycle")
    return errors


def validate(path: Path) -> list[str]:
    payload, errors = load_payload(path)
    if errors:
        return errors

    if not isinstance(payload, dict):
        return ["Top-level JSON value must be an object"]

    slices = payload.get("slices")
    if not isinstance(slices, list) or not slices:
        return ["slices must be a non-empty array"]

    identifiers: list[str] = []
    for index, item in enumerate(slices, start=1):
        identifier, slice_errors = validate_slice(item, index)
        errors.extend(slice_errors)
        if identifier:
            identifiers.append(identifier)

    if len(identifiers) != len(set(identifiers)):
        errors.append("Slice IDs must be unique")

    errors.extend(dependency_errors(slices, identifiers))
    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: validate_action_slices.py PATH", file=sys.stderr)
        return 2

    path = Path(argv[1]).expanduser()
    errors = validate(path)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"PASS: valid action slices: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
