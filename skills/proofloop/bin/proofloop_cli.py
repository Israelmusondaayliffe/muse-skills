"""Shared JSON command runner for ProofLoop deterministic scripts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from proofloop_core import (
    detect_conflicts,
    evaluate_policy,
    generate_id,
    redact_record,
    run_regressions,
    transfer_records,
    validate_contract,
    validate_record,
)


OPERATIONS = {
    "validate-contract": validate_contract,
    "validate-record": validate_record,
    "generate-id": generate_id,
    "redact-record": lambda payload: {"record": redact_record(payload)},
    "detect-conflicts": lambda payload: detect_conflicts(payload.get("records", [])),
    "evaluate-policy": evaluate_policy,
    "run-regressions": run_regressions,
    "transfer-records": transfer_records,
}


def _load_input(input_value: str):
    if input_value == "-":
        return json.load(sys.stdin)
    path = Path(input_value)
    if not path.is_absolute():
        raise ValueError("input path must be absolute or - for standard input")
    return json.loads(path.read_text(encoding="utf-8"))


def main(operation: str | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="-")
    parser.add_argument("--timeout", type=int, default=30)
    args = parser.parse_args()
    selected = operation or Path(sys.argv[0]).name
    try:
        if args.timeout <= 0:
            print(json.dumps({"error": "timeout or cancellation"}, separators=(",", ":")))
            return 4
        payload = _load_input(args.input)
        result = OPERATIONS[selected](payload)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
        if result.get("valid") is False or result.get("allowed") is False:
            return 2
        return 0
    except (ValueError, json.JSONDecodeError, OSError) as error:
        print(json.dumps({"error": str(error)}, separators=(",", ":")))
        return 3
    except KeyboardInterrupt:
        print(json.dumps({"error": "timeout or cancellation"}, separators=(",", ":")))
        return 4


if __name__ == "__main__":
    raise SystemExit(main())
