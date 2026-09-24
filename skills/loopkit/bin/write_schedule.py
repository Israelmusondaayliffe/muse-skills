#!/usr/bin/env python3
"""Record a manually tested scheduled-task contract for a run."""

import argparse
from pathlib import Path

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from loopkit_core import LoopKitError, load_json, write_schedule


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("schedule", type=Path)
    args = parser.parse_args()
    try:
        print(write_schedule(args.run_dir, load_json(args.schedule)))
    except LoopKitError as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
