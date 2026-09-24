#!/usr/bin/env python3
"""Initialize a validated LoopKit run directory."""

import argparse
from pathlib import Path

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from loopkit_core import LoopKitError, init_run


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("contract", type=Path)
    parser.add_argument("--workspace", type=Path, default=Path.cwd())
    parser.add_argument("--slug")
    args = parser.parse_args()
    try:
        print(init_run(args.contract, args.workspace, args.slug))
    except LoopKitError as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
