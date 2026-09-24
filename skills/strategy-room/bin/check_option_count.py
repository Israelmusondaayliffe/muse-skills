#!/usr/bin/env python3
import pathlib
import re
import sys


def main():
    if len(sys.argv) not in (2, 3):
        print("Usage: check_option_count.py <file> [minimum]", file=sys.stderr)
        return 2
    path = pathlib.Path(sys.argv[1]).expanduser()
    minimum = int(sys.argv[2]) if len(sys.argv) == 3 else 10
    text = path.read_text(encoding="utf-8")
    count = len(re.findall(r"(?m)^\s*(?:\d+\.|-)\s+", text))
    if count >= minimum:
        print(f"PASS {path}: {count} options")
        return 0
    print(f"FAIL {path}: found {count} options, need {minimum}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
