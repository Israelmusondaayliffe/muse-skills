#!/usr/bin/env python3
"""Report deterministic structural failures for one LoopKit run."""

import argparse
import json
from pathlib import Path

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from loopkit_core import LoopKitError, diagnose_run


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir", type=Path)
    args = parser.parse_args()
    try:
        report = diagnose_run(args.run_dir)
    except LoopKitError as exc:
        parser.error(str(exc))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if any(item["severity"] == "critical" for item in report["findings"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
