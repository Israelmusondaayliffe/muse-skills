#!/usr/bin/env python3
"""Validate and atomically record one LoopKit iteration receipt."""

import argparse
import json
from pathlib import Path

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from loopkit_core import LoopKitError, record_receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("receipt", type=Path)
    parser.add_argument("--expected-generation", type=int, required=True)
    args = parser.parse_args()
    try:
        target, state = record_receipt(args.run_dir, args.receipt, args.expected_generation)
    except LoopKitError as exc:
        parser.error(str(exc))
    print(json.dumps({"receipt": str(target), "state": state}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
