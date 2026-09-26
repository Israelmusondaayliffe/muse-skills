#!/usr/bin/env python3
"""Check a guide's runnable example against what the guide claims about it.

This is NOT a sandbox. The example runs as an ordinary Python process with your
permissions and could write anywhere. Read the example before running this
helper. The helper only observes files inside the run folder it creates, so it
can prove "no pre-existing file in the work folder was changed", nothing wider.

Example interface (required for --collide and --seed):
  The example takes its work folder as its last command-line argument.
  Run with no argument, it creates its own unique folder (for readers).
  Run with a folder, it works only inside that folder and must not write over
  files already there. Pass --workdir-arg so the helper supplies the folder.

Checks, reported in JSON:
  displayed_code       the script text appears verbatim in a fenced block of --guide
  exit_code            the run exited with --expect-exit (default 0)
  expectations         every --expect-output string appears in stdout or stderr
  no_overwrite         no file present before the run was changed or removed
  no_symlinks          the run folder contains no symlinks after the run
  collision_exercised  (--collide, --collide-at) at least one sentinel was planted
                       at a path the example writes, so a collision really happened

Cases:
  normal     python3 check_guide_example.py ex.py --guide g.md --workdir-arg --expect-output "..."
  collision  add --collide (a probe run finds the files the example leaves
             behind; the checked run starts with sentinel files at those paths).
             A probe cannot see names used only in passing, such as a rename
             destination that is renamed back. Add each one with --collide-at REL.
  malformed  add --seed data.csv=@bad.csv (or --seed data.csv=TEXT with \\n)
             and --expect-output naming the bad item; seeding requires it

An example without the folder interface can only be checked for the normal
case plus whatever failure cases it runs and prints itself (--expect-output).
The report labels that as "self-reported cases only".
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath

SCRIPT_NAME = "__guide_example__.py"
RUN_SUBDIR = "work"


class UsageError(Exception):
    pass


def safe_rel(rel: str) -> PurePosixPath:
    path = PurePosixPath(rel)
    if not rel or path.is_absolute() or ".." in path.parts or rel.startswith("~"):
        raise UsageError(f"seed path must be relative and stay inside the work folder: {rel!r}")
    return path


def plant(root: Path, rel: str, data: bytes) -> None:
    target = root.joinpath(*safe_rel(rel).parts)
    current = root
    for part in safe_rel(rel).parts[:-1]:
        current = current / part
        if current.is_symlink():
            raise UsageError(f"refusing to plant through a symlink: {current}")
    target.parent.mkdir(parents=True, exist_ok=True)
    if os.path.commonpath([str(root.resolve()), str(target.parent.resolve())]) != str(root.resolve()):
        raise UsageError(f"seed path escapes the work folder: {rel!r}")
    with open(target, "xb") as handle:  # never replaces an existing file
        handle.write(data)


def snapshot(root: Path) -> tuple[dict[str, str], list[str]]:
    files: dict[str, str] = {}
    links: list[str] = []
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        for name in dirnames + filenames:
            path = Path(dirpath) / name
            rel = str(path.relative_to(root))
            if path.is_symlink():
                links.append(rel)
            elif name in filenames:
                files[rel] = hashlib.sha256(path.read_bytes()).hexdigest()
    return files, sorted(links)


def seed_data(value: str) -> bytes:
    if value.startswith("@"):
        source = Path(value[1:])
        if source.is_symlink() or not source.is_file():
            raise UsageError(f"seed source must be a regular file: {source}")
        return source.read_bytes()
    return value.replace("\\n", "\n").encode("utf-8")


def displayed(script_text: str, guide_text: str) -> bool:
    body = script_text.rstrip("\n")
    for match in re.finditer(r"^(```+|~~~+)[^\n]*\n(.*?)^\1[ \t]*$", guide_text, re.M | re.S):
        if match.group(2).rstrip("\n") == body:
            return True
    return False


def run_once(script: Path, seeds: list[tuple[str, bytes]], sentinels: list[str],
             args: argparse.Namespace) -> dict:
    base = Path(tempfile.mkdtemp(prefix="guide-example-"))
    shutil.copyfile(script, base / SCRIPT_NAME)
    work = base / RUN_SUBDIR
    work.mkdir()
    for rel, data in seeds:
        plant(work, rel, data)
    planted = []
    for rel in sentinels:
        if not (work / rel).exists():
            plant(work, rel, f"SENTINEL {rel}: existed before the run; must survive.\n".encode("utf-8"))
            planted.append(rel)
    before, _ = snapshot(work)
    command = [sys.executable, str(base / SCRIPT_NAME), *args.arg]
    if args.workdir_arg:
        command.append(str(work))
    try:
        proc = subprocess.run(command, cwd=work, capture_output=True, text=True, timeout=args.timeout)
        stdout, stderr, code, timed_out = proc.stdout, proc.stderr, proc.returncode, False
    except subprocess.TimeoutExpired as exc:
        out, err = exc.stdout or "", exc.stderr or ""
        stdout = out.decode() if isinstance(out, bytes) else out
        stderr = err.decode() if isinstance(err, bytes) else err
        code, timed_out = None, True
    after, links = snapshot(work)
    return {
        "run_dir": str(work),
        "exit_code": code,
        "timed_out": timed_out,
        "stdout": stdout,
        "stderr": stderr,
        "changed": sorted(rel for rel in before if after.get(rel) != before[rel]),
        "new_files": sorted(set(after) - set(before)),
        "symlinks": links,
        "sentinels_planted": planted,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("script", type=Path, help="the exact example file the guide displays")
    parser.add_argument("--guide", type=Path, help="guide Markdown that must display the script verbatim")
    parser.add_argument("--workdir-arg", action="store_true",
                        help="pass the run's work folder as the example's last argument")
    parser.add_argument("--seed", action="append", default=[], metavar="REL=@SRC|REL=TEXT")
    parser.add_argument("--collide", action="store_true",
                        help="probe run, then plant sentinels at every file the probe wrote")
    parser.add_argument("--collide-at", action="append", default=[], metavar="REL",
                        help="also plant a sentinel here (names the example uses only in passing)")
    parser.add_argument("--arg", action="append", default=[], help="extra argument for the example")
    parser.add_argument("--expect-output", action="append", default=[], metavar="TEXT")
    parser.add_argument("--expect-exit", type=int, default=0)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--case", default="normal", help="label for this case in the report")
    args = parser.parse_args()

    try:
        if not args.script.is_file() or args.script.is_symlink():
            raise UsageError(f"script must be a regular file: {args.script}")
        for rel in args.collide_at:
            safe_rel(rel)
        collision = args.collide or bool(args.collide_at)
        if (collision or args.seed) and not args.workdir_arg:
            raise UsageError("--collide, --collide-at, and --seed need an example that takes its work folder "
                             "(--workdir-arg); otherwise check only the cases the example runs itself")
        if args.seed and not args.expect_output:
            raise UsageError("--seed is for malformed-input cases; add --expect-output naming the reported item")
        seeds = []
        for spec in args.seed:
            rel, sep, value = spec.partition("=")
            if not sep:
                raise UsageError(f"bad --seed (use REL=@SRC or REL=TEXT): {spec}")
            safe_rel(rel)
            seeds.append((rel, seed_data(value)))

        script_text = args.script.read_text(encoding="utf-8")
        probe = None
        sentinels: list[str] = []
        seeded = {rel for rel, _ in seeds}
        if args.collide:
            probe = run_once(args.script, seeds, [], args)
            sentinels = [rel for rel in probe["new_files"] if rel not in seeded]
        sentinels += [rel for rel in args.collide_at if rel not in seeded and rel not in sentinels]
        result = run_once(args.script, seeds, sentinels, args)
    except UsageError as exc:
        print(json.dumps({"valid": False, "error": str(exc)}, indent=2))
        return 2

    combined = result["stdout"] + result["stderr"]
    missing = [text for text in args.expect_output if text not in combined]
    checks = {
        "exit_code": (not result["timed_out"]) and result["exit_code"] == args.expect_exit,
        "expectations": not missing,
        "no_overwrite": not result["changed"],
        "no_symlinks": not result["symlinks"],
    }
    if collision:
        checks["collision_exercised"] = bool(result["sentinels_planted"])
    if args.guide:
        checks["displayed_code"] = displayed(script_text, args.guide.read_text(encoding="utf-8"))
    if not args.workdir_arg:
        coverage = "self-reported cases only: the example chose its own folder, so the helper saw no writes"
    elif collision:
        coverage = "collision injected at paths the probe run wrote" + (
            " plus --collide-at names" if args.collide_at else "")
    elif args.seed:
        coverage = "malformed input injected into the work folder"
    else:
        coverage = "normal run in an injected work folder"
    report = {
        "valid": all(checks.values()),
        "case": args.case,
        "coverage": coverage,
        "checks": checks,
        "limits": "not a sandbox; only files inside run_dir were observed",
        "script_sha256": hashlib.sha256(script_text.encode("utf-8")).hexdigest(),
        "run_dir": result["run_dir"],
        "exit_code": result["exit_code"],
        "timed_out": result["timed_out"],
        "probe_new_files": probe["new_files"] if probe else None,
        "sentinels_planted": result["sentinels_planted"],
        "preexisting_changed_or_removed": result["changed"],
        "new_files": result["new_files"],
        "symlinks": result["symlinks"],
        "missing_expected_output": missing,
        "stdout": result["stdout"][-4000:],
        "stderr": result["stderr"][-4000:],
    }
    print(json.dumps(report, indent=2))
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
