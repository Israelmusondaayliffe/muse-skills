#!/usr/bin/env python3
"""Validate prompt JSON structure and explicit constraints, not image quality."""
import argparse
import json
import re
import sys
from pathlib import Path


def object_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError(f"non-JSON numeric constant: {value}")


def parse_json(text):
    return json.loads(text, object_pairs_hook=object_pairs, parse_constant=reject_constant)


def prompt_objects(value, label, issues):
    items = value if isinstance(value, list) else [value]
    if not items:
        issues.append(f"{label}: empty prompt array")
    prompts = []
    for index, item in enumerate(items, 1):
        if not isinstance(item, dict) or not item:
            issues.append(f"{label}, item {index}: expected a nonempty JSON object")
        else:
            prompts.append(item)
    return prompts


def load_prompts(text, label):
    issues = []
    prompts = []
    stripped = text.strip()
    if not stripped:
        return [], [f"{label}: input is empty"]
    if stripped.startswith(("{", "[")):
        try:
            value = parse_json(stripped)
            prompts.extend(prompt_objects(value, label, issues))
        except (ValueError, TypeError) as exc:
            issues.append(f"{label}: invalid JSON: {exc}")
        return prompts, issues
    lines = text.splitlines()
    fence = None
    language = ""
    start_line = 0
    body = []
    candidates = 0
    for number, line in enumerate(lines, 1):
        if fence is None:
            match = re.match(r"^\s*(`{3,}|~{3,})\s*([^\s]*)\s*$", line)
            if match:
                fence = match.group(1)
                language = match.group(2).lower()
                start_line = number
                body = []
        elif re.match(r"^\s*" + re.escape(fence[0]) + r"{" + str(len(fence)) + r",}\s*$", line):
            block = "\n".join(body).strip()
            is_json = language == "json" or (not language and block.startswith(("{", "[")))
            if is_json:
                candidates += 1
                block_label = f"{label}:line {start_line}"
                try:
                    value = parse_json(block)
                    prompts.extend(prompt_objects(value, block_label, issues))
                except (ValueError, TypeError) as exc:
                    issues.append(f"{block_label}: invalid JSON: {exc}")
            fence = None
        else:
            body.append(line)
    if fence is not None:
        block = "\n".join(body).strip()
        if language == "json" or (not language and block.startswith(("{", "["))):
            issues.append(f"{label}:line {start_line}: unclosed JSON fence")
    if not candidates and not issues:
        issues.append(f"{label}: no JSON prompt objects found")
    return prompts, issues


def at_path(value, dotted):
    """Resolve simple dot-separated object keys and zero-based array indices."""
    for part in dotted.split("."):
        if isinstance(value, dict) and part in value:
            value = value[part]
        elif isinstance(value, list) and part.isdigit() and int(part) < len(value):
            value = value[int(part)]
        else:
            raise KeyError(dotted)
    return value


def populated(value):
    return value is not None and value != "" and value != [] and value != {} and not (
        isinstance(value, str) and not value.strip()
    )


def validate(prompts, expected_count=None, required=(), equal=()):
    issues = []
    if not prompts:
        issues.append("no valid prompt objects found")
    if expected_count is not None and len(prompts) != expected_count:
        issues.append(f"expected {expected_count} prompt objects, found {len(prompts)}")
    for dotted in dict.fromkeys([*required, *equal]):
        values = []
        for index, prompt in enumerate(prompts, 1):
            try:
                value = at_path(prompt, dotted)
            except KeyError:
                issues.append(f"prompt {index}: missing path {dotted}")
                continue
            if not populated(value):
                issues.append(f"prompt {index}: empty required path {dotted}")
            values.append((index, value))
        if dotted in equal and values:
            baseline_index, baseline = values[0]
            for index, value in values[1:]:
                if json.dumps(value, sort_keys=True) != json.dumps(baseline, sort_keys=True):
                    issues.append(f"prompt {index}: {dotted} differs from prompt {baseline_index}")
    return issues


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="JSON/Markdown file, a directory of JSON files, or - for stdin")
    parser.add_argument("--expect-count", type=int, default=None, help="Requested number of prompt objects")
    parser.add_argument("--require-path", action="append", default=[], help="Required populated dotted path; repeat as needed")
    parser.add_argument("--equal-path", action="append", default=[], help="Dotted path that must match exactly across prompts")
    args = parser.parse_args(argv)
    if args.expect_count is not None and args.expect_count < 1:
        parser.error("--expect-count must be positive")
    if any(not p or any(not part for part in p.split(".")) for p in args.require_path + args.equal_path):
        parser.error("paths must contain nonempty dot-separated components")
    prompts, issues = [], []
    try:
        if args.input == "-":
            documents = [("stdin", sys.stdin.read())]
        else:
            path = Path(args.input)
            files = sorted(path.glob("*.json")) if path.is_dir() else [path]
            if not files:
                raise ValueError(f"{path}: no JSON files found")
            documents = [(str(file), file.read_text(encoding="utf-8")) for file in files]
        for label, text in documents:
            found, failures = load_prompts(text, label)
            prompts.extend(found)
            issues.extend(failures)
    except (OSError, ValueError) as exc:
        issues.append(str(exc))
    issues.extend(validate(prompts, args.expect_count, args.require_path, args.equal_path))
    print(json.dumps({"valid": not issues, "prompt_count": len(prompts), "issues": issues,
                      "scope": "JSON structure and explicit constraints only; no visual or creative acceptance"}, indent=2))
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
