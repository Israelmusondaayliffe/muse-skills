#!/usr/bin/env python3
"""Refresh a LoopKit checkpoint from durable run files."""

import argparse
from pathlib import Path

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from loopkit_core import LoopKitError, refresh_checkpoint


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir", type=Path)
    args = parser.parse_args()
    try:
        print(refresh_checkpoint(args.run_dir))
    except LoopKitError as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
