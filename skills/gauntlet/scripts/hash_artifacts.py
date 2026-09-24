#!/usr/bin/env python3
"""SHA-256 every artifact file for a gauntlet run (SPEC 9.6 section 6, INV-5).

Hashes:
- every file under each piece's artifact_paths from pieces.json, resolved
  relative to the project root recorded in run.json under "project_root"
  (falling back to the run directory when absent). A path fragment after
  "#" is stripped before resolution. Directories are hashed file by file.
  A missing file is recorded with "missing": true, never skipped silently.
- every file under rounds/<piece>/<round>/artifact/ snapshots.

Writes artifact-hashes.json in the run directory and prints the same JSON
on stdout. Output is deterministic (sorted, no timestamps) so repeated runs
over unchanged files produce identical bytes.

Exit codes: 0 on success, 1 when run.json or pieces.json is missing or
invalid, 2 on usage errors.
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        print("Missing required state file: %s" % path, file=sys.stderr)
        raise SystemExit(1)
    except json.JSONDecodeError as exc:
        print("Invalid JSON in %s: %s" % (path, exc), file=sys.stderr)
        raise SystemExit(1)


def hash_artifact_paths(pieces, project_root):
    entries = []
    for piece in pieces:
        piece_id = piece.get("id") or "unknown"
        for raw in piece.get("artifact_paths") or []:
            file_part = raw.split("#", 1)[0]
            candidate = Path(file_part)
            resolved = (
                candidate if candidate.is_absolute() else project_root / file_part
            )
            if resolved.is_file():
                entries.append(
                    {
                        "piece_id": piece_id,
                        "path": raw,
                        "resolved_path": str(resolved),
                        "sha256": sha256_file(resolved),
                        "missing": False,
                    }
                )
            elif resolved.is_dir():
                for child in sorted(resolved.rglob("*")):
                    if child.is_file():
                        entries.append(
                            {
                                "piece_id": piece_id,
                                "path": raw,
                                "resolved_path": str(child),
                                "sha256": sha256_file(child),
                                "missing": False,
                            }
                        )
            else:
                entries.append(
                    {
                        "piece_id": piece_id,
                        "path": raw,
                        "resolved_path": str(resolved),
                        "sha256": None,
                        "missing": True,
                    }
                )
    return entries


def hash_round_snapshots(run_dir):
    entries = []
    rounds_dir = run_dir / "rounds"
    if not rounds_dir.is_dir():
        return entries
    for piece_dir in sorted(rounds_dir.iterdir()):
        if not piece_dir.is_dir():
            continue
        for round_dir in sorted(piece_dir.iterdir()):
            artifact_dir = round_dir / "artifact"
            if not artifact_dir.is_dir():
                continue
            for child in sorted(artifact_dir.rglob("*")):
                if child.is_file():
                    entries.append(
                        {
                            "piece_id": piece_dir.name,
                            "round": round_dir.name,
                            "path": str(child.relative_to(run_dir)),
                            "sha256": sha256_file(child),
                        }
                    )
    return entries


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="SHA-256 every artifact file and round snapshot for a run."
    )
    parser.add_argument(
        "--run-dir",
        required=True,
        help="Path to .gauntlet/runs/<run-id>.",
    )
    args = parser.parse_args(argv)

    run_dir = Path(args.run_dir).resolve()
    run = load_json(run_dir / "run.json")
    pieces_doc = load_json(run_dir / "pieces.json")

    project_root = Path(run.get("project_root") or run_dir).resolve()

    doc = {
        "run_id": run.get("run_id"),
        "project_root": str(project_root),
        "artifacts": hash_artifact_paths(pieces_doc.get("pieces") or [], project_root),
        "round_snapshots": hash_round_snapshots(run_dir),
    }

    text = json.dumps(doc, indent=2)
    (run_dir / "artifact-hashes.json").write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
