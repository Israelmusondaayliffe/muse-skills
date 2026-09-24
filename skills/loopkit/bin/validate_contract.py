#!/usr/bin/env python3
"""Validate a LoopKit contract without changing state."""

import argparse
from pathlib import Path

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from loopkit_core import LoopKitError, load_json, validate_contract


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("contract", type=Path)
    args = parser.parse_args()
    try:
        errors = validate_contract(load_json(args.contract))
    except LoopKitError as exc:
        parser.error(str(exc))
    if errors:
        for error in errors:
            print(error)
        return 1
    print("contract valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
