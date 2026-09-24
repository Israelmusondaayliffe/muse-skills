#!/usr/bin/env python3
"""Deterministic scan of persistent context files against the context doctrine.

Read-only. Reports findings; never edits a source file. See
references/context-doctrine.md for the audit test behind these patterns.

Read-only. Reports findings; never edits a source file.

Usage:
    python3 context_scan.py PATH [PATH ...] [--json OUT.json] [--long-run]

PATH may be a file or a directory. Directories are walked for .md files.
Pass --long-run to downgrade verification findings for a long-horizon autonomous
run, where the doctrine still permits fresh-context verifier subagents.

A file whose first 20 lines contain the HTML comment "context-scan: catalogue" is
exempt from the line rules, because a catalogue documents the patterns it bans. A
single line carrying "context-scan: ignore" is exempt on its own.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

FAIL, WARN, INFO = "FAIL", "WARN", "INFO"

# Category: (severity, reason, compiled patterns)
LINE_RULES = {
    "reasoning-echo": (
        FAIL,
        "Risks the reasoning extraction refusal classifier. Use structured thinking blocks or a send-to-user tool.",
        [
            r"show\s+your\s+(?:thinking|reasoning|thought\s+process|work)\b",
            r"explain\s+your\s+(?:internal\s+)?reasoning\s+in\s+(?:your|the)\s+(?:response|answer|output)",
            r"(?:echo|transcribe|reproduce|narrate)\s+your\s+(?:thinking|reasoning|thought\s+process)",
            r"reflect\s+on\s+your\s+reasoning",
            r"reasoning\s+first,\s+then\s+answer",
            r"think\s+out\s+loud\s+in\s+(?:your|the)\s+(?:response|answer)",
        ],
    ),
    "verification-instruction": (
        FAIL,
        "Claude 5 models verify and self-correct unprompted. Added instructions cause over-verification.",
        [
            r"final verification step",
            r"(?:verify|verifying|re-?verify)\s+(?:your|the|its)\s+(?:own\s+)?work",
            r"double[- ]check",
            r"re-?verify\s+(?:your|the|its)\s+(?:own\s+)?(?:work|answer|output|response|result)",
            r"re-?verify\s+before\s+(?:respond|answer|report|deliver)",
            r"subagent to (?:verify|double[- ]check|check)",
            r"verify (?:your|the) (?:answer|output|response) before",
            r"score\s+0\s*(?:to|-|through)\s*10",
        ],
    ),
    "anti-laziness": (
        WARN,
        "Compensates for 4.x early stopping. Residue now causes over-elaboration.",
        [
            r"\bbe thorough\b",
            r"do\s*n[o']t\s+stop\s+early",
            r"complete\s+ALL\b",
            r"leave\s+nothing\s+out",
            r"\bexhaustive(?:ly)?\b",
            r"do\s+not\s+be\s+lazy",
        ],
    ),
    "capitalised-emphasis": (
        WARN,
        "Strong instruction following makes plain statements sufficient.",
        [
            r"\bCRITICAL\b",
            r"\bYOU MUST\b",
            r"\bALWAYS\b",
            r"\bNEVER\b",
            r"\bIMPORTANT:",
            r"\bMANDATORY\b",
        ],
    ),
    "forced-summary": (
        WARN,
        "Compensates for 4.x opacity. Progress updates are a good default now.",
        [
            r"summar\w+\s+every\s+\d+",
            r"after\s+every\s+\d+\s+tool\s+calls",
            r"restate\s+the\s+(?:contract|task|plan)\s+each",
        ],
    ),
    "subagent-pressure": (
        WARN,
        "Compensates for 4.7 under-spawning. Keep only when-appropriate guidance.",
        [
            r"spawn\s+(?:multiple|several|many)\s+subagents",
            r"always\s+use\s+(?:a\s+)?subagents?",
        ],
    ),
    "tool-triggering-pressure": (
        WARN,
        "Tool guidance belongs in the tool description, once.",
        [
            r"you\s+MUST\s+(?:call|use)\s+the\s+\w+\s+tool",
            r"remember\s+to\s+(?:call|use)\s+the\s+\w+\s+tool",
        ],
    ),
}

PROHIBITION_LINE = re.compile(r"^\s*[-*\d.\s]*(?:Do not|Don't|Never|Avoid|No )\b", re.IGNORECASE)
EXAMPLE_HEADING = re.compile(r"^\s{0,3}#{1,6}\s*.*\bexamples?\b", re.IGNORECASE)
CODE_FENCE = re.compile(r"^\s*```")

# A line that names a banned pattern in order to forbid, remove, or describe it is not
# committing the offence. These cues downgrade a FAIL to INFO for human confirmation.
DESCRIPTIVE_CUES = re.compile(
    r"\b(?:not\b|never write|never add|avoid|remove|removing|removal|delete|deleting|strip"
    r"|without being told|unprompted|already does|instead of|rather than|no need to|absent"
    r"|legacy|deprune|anti-pattern|compensat|do not (?:use|add|write|instruct)|don't\b"
    r"|what not to|forbidden|banned|obsolete|stale|used to say|previously)\b",
    re.IGNORECASE,
)
HEADING = re.compile(r"^\s{0,3}#{1,6}\s|^\s*\|")

CATALOGUE_MARKER = "context-scan: catalogue"
IGNORE_MARKER = "context-scan: ignore"

PROHIBITION_THRESHOLD = 8
DISCLOSURE_THRESHOLD = 800
EXAMPLE_THRESHOLD = 3


def scan_text(path: Path, text: str, long_run: bool) -> list[dict]:
    findings: list[dict] = []
    lines = text.splitlines()
    # A catalogue file describes the banned patterns in order to teach them. Its prose
    # would otherwise match every rule it documents.
    catalogue = any(CATALOGUE_MARKER in line for line in lines[:20])
    in_fence = False
    prohibitions: list[int] = []
    examples: list[int] = []

    for number, line in enumerate(lines, start=1):
        if CODE_FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if catalogue or IGNORE_MARKER in line:
            continue
        for category, (severity, reason, patterns) in LINE_RULES.items():
            level = severity
            if category == "verification-instruction" and long_run:
                level = INFO
            flags = 0 if category == "capitalised-emphasis" else re.IGNORECASE
            for pattern in patterns:
                if re.search(pattern, line, flags):
                    reported, note = level, reason
                    if level in (FAIL, WARN) and (DESCRIPTIVE_CUES.search(line) or HEADING.match(line)):
                        reported = INFO
                        note = reason + " Reads as description, prohibition, or rubric rather than an instruction. Confirm by hand."
                    findings.append(
                        {
                            "file": str(path),
                            "line": number,
                            "category": category,
                            "severity": reported,
                            "text": line.strip()[:160],
                            "reason": note,
                            "action": "remove" if reported == FAIL else "confirm, then remove if instructive",
                        }
                    )
                    break
        if PROHIBITION_LINE.match(line):
            prohibitions.append(number)
        if EXAMPLE_HEADING.match(line):
            examples.append(number)

    words = len(text.split())

    if len(prohibitions) > PROHIBITION_THRESHOLD and not catalogue:
        findings.append(
            {
                "file": str(path),
                "line": prohibitions[0],
                "category": "prohibition-wall",
                "severity": WARN,
                "text": f"{len(prohibitions)} prohibition lines, first at line {prohibitions[0]}",
                "reason": "One brief instruction usually steers the whole behaviour class. Rewrite as the wanted shape.",
                "action": "collapse",
            }
        )
    if words > DISCLOSURE_THRESHOLD and path.name == "SKILL.md":
        findings.append(
            {
                "file": str(path),
                "line": 1,
                "category": "progressive-disclosure",
                "severity": INFO,
                "text": f"{words} words in a single SKILL.md",
                "reason": "Long skills split into linked reference files that load on demand.",
                "action": "split",
            }
        )
    if len(examples) > EXAMPLE_THRESHOLD:
        findings.append(
            {
                "file": str(path),
                "line": examples[0],
                "category": "example-heavy",
                "severity": INFO,
                "text": f"{len(examples)} example sections",
                "reason": "Examples constrain the exploration space. Consider expressing the contract as an interface instead.",
                "action": "review",
            }
        )
    if not findings:
        findings.append(
            {
                "file": str(path),
                "line": 0,
                "category": "clean",
                "severity": INFO,
                "text": f"{words} words, no deterministic findings",
                "reason": "Judgement checks in the doctrine still apply.",
                "action": "none",
            }
        )
    return findings


def collect(paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for raw in paths:
        path = Path(raw)
        if path.is_dir():
            files.extend(sorted(p for p in path.rglob("*.md") if p.is_file()))
        elif path.is_file():
            files.append(path)
        else:
            print(f"skipped, not found: {path}", file=sys.stderr)
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--json", dest="json_out")
    parser.add_argument("--long-run", action="store_true")
    args = parser.parse_args()

    findings: list[dict] = []
    for path in collect(args.paths):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            print(f"unreadable: {path}: {exc}", file=sys.stderr)
            continue
        findings.extend(scan_text(path, text, args.long_run))

    counts = {level: sum(1 for f in findings if f["severity"] == level) for level in (FAIL, WARN, INFO)}
    report = {"files": len({f["file"] for f in findings}), "counts": counts, "findings": findings}

    if args.json_out:
        Path(args.json_out).write_text(json.dumps(report, indent=2), encoding="utf-8")

    for finding in findings:
        if finding["category"] == "clean":
            continue
        print(f"{finding['severity']:4} {finding['file']}:{finding['line']} [{finding['category']}] {finding['text']}")
    print(json.dumps({"files": report["files"], "counts": counts}, indent=2))
    return 1 if counts[FAIL] else 0


if __name__ == "__main__":
    raise SystemExit(main())
