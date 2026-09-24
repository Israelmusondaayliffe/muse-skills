#!/usr/bin/env python3
"""Apply one generation-checked LoopKit state transition."""

import argparse
import json
from pathlib import Path

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from loopkit_core import ALLOWED_TRANSITIONS, LoopKitError, transition_run


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("to_status", choices=sorted(ALLOWED_TRANSITIONS))
    parser.add_argument("--expected-generation", type=int, required=True)
    parser.add_argument("--reason", required=True)
    args = parser.parse_args()
    try:
        state = transition_run(args.run_dir, args.to_status, args.expected_generation, args.reason)
    except LoopKitError as exc:
        parser.error(str(exc))
    print(json.dumps(state, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
