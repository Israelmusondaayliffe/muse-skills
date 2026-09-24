#!/usr/bin/env python3
"""Validate an iteration receipt against its run contract."""

import argparse
from pathlib import Path

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from loopkit_core import LoopKitError, load_json, validate_receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("receipt", type=Path)
    args = parser.parse_args()
    try:
        errors = validate_receipt(load_json(args.receipt), args.run_dir)
    except LoopKitError as exc:
        parser.error(str(exc))
    if errors:
        for error in errors:
            print(error)
        return 1
    print("receipt valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
