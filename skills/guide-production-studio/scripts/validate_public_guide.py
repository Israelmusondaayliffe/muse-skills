#!/usr/bin/env python3
"""Scan public guide text for private paths and internal production commentary.

Adapted for Muse on Hatch: flags home-directory paths, memory references,
skill/workspace internals, credential references, and agent-production
commentary that must never appear in a public guide.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


PATTERNS = {
    "local home path": re.compile(r"/home/[^\s)]+"),
    "internal home path": re.compile(
        r"~/(?:memory|\.ssh|\.aws|\.gnupg|workspace/skills)\b",
        re.IGNORECASE,
    ),
    "memory system reference": re.compile(
        r"\b(?:MEMORY\.md|memory bank|memory search|memory_search)\b",
        re.IGNORECASE,
    ),
    "skill or workspace internal path": re.compile(
        r"(?:\.claude-plugin/|\.codex-plugin/|/workspace/skills/|plugin://|"
        r"CLAUDE-OUTPUTS/|CODEX-OUTPUTS/|HATCH-OUTPUTS/)",
        re.IGNORECASE,
    ),
    "credential reference": re.compile(
        r"\[(?:credential|secret):[^\]]+\]",
        re.IGNORECASE,
    ),
    "internal source ledger": re.compile(
        r"\b(?:claim ledger|source ledger|private research notes)\b",
        re.IGNORECASE,
    ),
    "internal release evidence": re.compile(
        r"\b(?:release receipt|publication receipt|validator passed|validation receipt)\b",
        re.IGNORECASE,
    ),
    "model commentary": re.compile(
        r"\b(?:the model should|the agent should|the audit proves|worker thread|"
        r"model routing|subagent assignment)\b",
        re.IGNORECASE,
    ),
    "private operating label": re.compile(
        r"\b(?:private plugin|private skill|internal plugin|internal skill)\b",
        re.IGNORECASE,
    ),
    "unresolved placeholder": re.compile(r"\[(?:TODO|TBD)[:\]]|replace-with-", re.IGNORECASE),
}


def scan(text: str) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    for label, pattern in PATTERNS.items():
        for match in pattern.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            findings.append({"type": label, "line": line, "evidence": match.group(0)[:120]})
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("guide", type=Path)
    args = parser.parse_args()
    try:
        text = args.guide.read_text(encoding="utf-8")
        findings = scan(text)
        if not text.strip():
            findings.append({"type": "empty guide", "line": 1, "evidence": ""})
    except OSError as exc:
        findings = [{"type": "read error", "line": 0, "evidence": str(exc)}]
    print(json.dumps({"valid": not findings, "findings": findings}, indent=2))
    return 0 if not findings else 1


if __name__ == "__main__":
    raise SystemExit(main())
