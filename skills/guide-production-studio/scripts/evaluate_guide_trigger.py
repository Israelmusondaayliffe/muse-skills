#!/usr/bin/env python3
"""Classify whether a request belongs to Guide Production Studio."""

from __future__ import annotations

import argparse
import json
import re


GUIDE_NOUNS = re.compile(
    r"\b(?:guide|manual|how-to|reference|playbook|documentation)\b",
    re.IGNORECASE,
)
GUIDE_ACTIONS = re.compile(
    r"\b(?:build|create|design|map|redo|redesign|review|rewrite|study|turn|write)\b",
    re.IGNORECASE,
)
GUIDE_METHODS = re.compile(
    r"\b(?:beginner|cold reader|child pages|example|source-grounded|source lineage|"
    r"teaching structure|troubleshooting|workflow)\b",
    re.IGNORECASE,
)
GUIDE_INTENT = re.compile(
    r"\b(?:source lineage|taught publicly|teaching structure)\b",
    re.IGNORECASE,
)
OUT_OF_SCOPE = (
    re.compile(r"\b(?:clean up|copyedit|grammar)\b", re.IGNORECASE),
    re.compile(r"\bpublish\b.*\b(?:approved|notion)\b", re.IGNORECASE),
    re.compile(r"\bworkshop\b.*\b(?:slides|presenter notes)\b", re.IGNORECASE),
    re.compile(r"\b(?:generate|create)\b.*\b(?:film assets|first shot)\b", re.IGNORECASE),
    re.compile(r"\b(?:audit|check)\b.*\b(?:claims|plugin installation|routing registry)\b", re.IGNORECASE),
    re.compile(r"\b(?:downloadable pdf|convert to pdf)\b", re.IGNORECASE),
    re.compile(r"\bteach me\b.*\b(?:interactively|sessions)\b", re.IGNORECASE),
    re.compile(r"\bresearch\b.*\b(?:latest|documentation|source ledger)\b", re.IGNORECASE),
)
EXPLICIT_REJECTION = re.compile(r"\b(?:do not|don't) want (?:a )?guide\b", re.IGNORECASE)


def evaluate(query: str) -> dict[str, object]:
    """Return a local, deterministic routing decision with evidence."""

    guide_noun = bool(GUIDE_NOUNS.search(query))
    guide_action = bool(GUIDE_ACTIONS.search(query))
    guide_method = bool(GUIDE_METHODS.search(query))
    guide_intent = bool(GUIDE_INTENT.search(query))
    rejected = bool(EXPLICIT_REJECTION.search(query))
    exclusions = [pattern.pattern for pattern in OUT_OF_SCOPE if pattern.search(query)]
    should_trigger = (guide_noun or guide_intent) and guide_action
    if rejected or exclusions:
        should_trigger = False
    return {
        "should_trigger": should_trigger,
        "evidence": {
            "guide_noun": guide_noun,
            "guide_action": guide_action,
            "guide_method": guide_method,
            "guide_intent": guide_intent,
            "explicit_rejection": rejected,
            "out_of_scope_matches": exclusions,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", required=True)
    args = parser.parse_args()
    print(json.dumps(evaluate(args.task), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
