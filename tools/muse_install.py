#!/usr/bin/env python3
"""Plan, apply, or roll back a replacement of the 30 public Muse skill packages.

Dry-run by default. The file writes, pre-write journal, backups, atomic replace and
conflict-aware rollback come from harness-engineering/scripts/harnessctl.py; this
tool only decides which files may change.

Rules:
- Only the 30 allowlisted skill folders are considered. Anything else in the
  installed skills directory (local skills, extra files) is never read or written.
- An installed file may be replaced only when its hash equals the baseline (the
  release it came from). A local edit, deletion, or unknown file at a release path
  blocks the plan instead of being overwritten.
- Protected paths (personal voice and in-package legacy state) are never written.
- Files the new release no longer ships are reported and left in place.
- Staged files must match the staged manifest hash, so the release cannot drift
  between review and apply.

A recorded approval reference is required for apply. It records an approval the
user already gave; the tool cannot grant one. No network, no host probes.
"""
from __future__ import annotations

import argparse
import fnmatch
import importlib.util
import json
import re
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
POLICY = Path(__file__).with_name("install-policy.json")


def _harnessctl():
    path = ROOT / "skills/harness-engineering/scripts/harnessctl.py"
    spec = importlib.util.spec_from_file_location("harnessctl", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


h = _harnessctl()


class InstallError(RuntimeError):
    pass


def load_policy(path=POLICY):
    policy = json.loads(Path(path).read_text())
    if len(policy["skills"]) != 30 or len(set(policy["skills"])) != 30:
        raise InstallError("install policy must list exactly 30 unique skills")
    if any(not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name)
           for name in policy["skills"]):
        raise InstallError("skill names must be plain lowercase folder names")
    return policy


def protected(relative, policy):
    return any(fnmatch.fnmatchcase(relative, pattern) for pattern in policy["protected"])


def ignored(relative):
    parts = relative.split("/")
    return any(p in {"__pycache__", ".git", ".DS_Store"} or p.endswith(".pyc") for p in parts)


def tree_manifest(skills_dir, policy):
    """Hash every regular file under the allowlisted folders of a skills directory."""
    skills_dir = Path(skills_dir)
    files = {}
    for skill in policy["skills"]:
        folder = skills_dir / skill
        if folder.is_symlink():
            raise InstallError(f"symbolic link at package root: {skill}")
        if not folder.is_dir():
            continue
        for path in sorted(folder.rglob("*")):
            relative = path.relative_to(skills_dir).as_posix()
            if path.is_symlink():
                raise InstallError(f"symbolic link in package tree: {relative}")
            if path.is_file() and not ignored(relative):
                files[relative] = h.sha256_file(path)
    return files


def git_manifest(repo, ref, policy):
    """Hash the allowlisted files of skills/ at a git ref (for the installed baseline)."""
    listing = subprocess.run(["git", "-C", str(repo), "ls-tree", "-r", ref, "skills/"],
                             check=True, capture_output=True, text=True).stdout
    files = {}
    for line in listing.splitlines():
        meta, path = line.split("\t", 1)
        relative = path[len("skills/"):]
        if relative.split("/", 1)[0] not in policy["skills"] or ignored(relative):
            continue
        if meta.split()[0] == "120000":
            raise InstallError(f"symbolic link in baseline: {relative}")
        blob = subprocess.run(["git", "-C", str(repo), "cat-file", "blob", meta.split()[2]],
                              check=True, capture_output=True).stdout
        files[relative] = h.sha256_bytes(blob)
    return files


def plan(staged_dir, installed_dir, baseline, policy, staged_manifest=None, exclude=(), only=()):
    """Classify every release path. Pure read; returns the decision record."""
    staged_dir, installed_dir = Path(staged_dir).resolve(), Path(installed_dir).resolve()
    selected = set(only) or set(policy["skills"])
    if selected - set(policy["skills"]):
        raise InstallError("unknown --only-skill selection")
    staged = tree_manifest(staged_dir, policy)
    if staged_manifest is not None and staged != staged_manifest:
        drift = sorted(set(staged) ^ set(staged_manifest) |
                       {k for k in staged.keys() & staged_manifest.keys() if staged[k] != staged_manifest[k]})
        raise InstallError(f"staged tree differs from its reviewed manifest: {drift[:10]}")
    missing = [s for s in policy["skills"] if not (staged_dir / s / "SKILL.md").is_file()]
    if missing:
        raise InstallError(f"staged release lacks SKILL.md for: {missing}")
    rows = {"create": [], "update": [], "unchanged": [], "blocked": [], "protected": [],
            "excluded": [], "retired_left_in_place": []}
    for relative, new_hash in sorted(staged.items()):
        target = installed_dir / relative
        if relative in exclude or relative.split("/", 1)[0] not in selected:
            rows["excluded"].append(relative)
            continue
        if protected(relative, policy):
            rows["protected"].append(relative)
            continue
        if any(a.is_symlink() for a in (target, *target.parents) if a != installed_dir and h.is_within(a, installed_dir)):
            rows["blocked"].append({"path": relative, "reason": "symbolic link on installed path"})
        else:
            current = h.sha256_file(target) if target.is_file() else None
            base = baseline.get(relative)
            if target.exists() and not target.is_file():
                rows["blocked"].append({"path": relative, "reason": "installed path is not a regular file"})
            elif current == new_hash:
                rows["unchanged"].append(relative)
            elif current is None and base is None:
                rows["create"].append({"path": relative, "after": new_hash})
            elif current is None:
                rows["blocked"].append({"path": relative, "reason": "baseline file deleted locally"})
            elif base is None:
                rows["blocked"].append({"path": relative, "reason": "unknown installed file at a new release path"})
            elif current != base:
                rows["blocked"].append({"path": relative, "reason": "installed file modified locally"})
            else:
                rows["update"].append({"path": relative, "before": current, "after": new_hash})
    for relative in sorted(set(baseline) - set(staged)):
        if (installed_dir / relative).exists():
            rows["retired_left_in_place"].append(relative)
    status = "blocked" if rows["blocked"] else ("noop" if not rows["create"] and not rows["update"] else "ready")
    return {"status": status, "staged": str(staged_dir), "installed": str(installed_dir),
            "selected_skills": sorted(selected), "reviewed_manifest_verified": staged_manifest is not None,
            "counts": {k: len(v) for k, v in rows.items()}, **rows}


def to_harness_plan(record, run_id):
    changes = record["create"] + record["update"]
    staged, installed = Path(record["staged"]), Path(record["installed"])
    operations = []
    for index, row in enumerate(changes):
        op = {"id": f"f{index}", "action": "update" if "before" in row else "create",
              "target": str(installed / row["path"]), "approval_group": "packages",
              "source": str(staged / row["path"]), "expected_payload_sha256": row["after"]}
        if "before" in row:
            op["expected_sha256"] = row["before"]
        operations.append(op)
    return {
        "schema_version": 1, "run_id": run_id, "allowed_roots": [str(installed)],
        "approval_groups": ["packages"],
        "outcome": {"primary_metric": "package files replaced", "before_state": "baseline release",
                    "target_state": "staged release", "unresolved_before": len(changes),
                    "unresolved_target": 0, "expected_primary_outputs": max(1, len(changes))},
        "resource_budget": {"max_task_launches": 0, "max_support_artifacts": 0,
                            "max_verification_passes": 1, "max_low_yield_waves": 1,
                            "high_cost_approved": False, "cost_warning": None},
        "support_artifacts": [], "operations": operations,
    }


def apply(record, backup_dir, approval_ref, run_id="muse-install"):
    if not approval_ref or not approval_ref.strip():
        raise InstallError("apply needs --approval-ref naming the user's recorded approval")
    if record.get("reviewed_manifest_verified") is not True:
        raise InstallError("apply requires a reviewed staged manifest")
    if record["status"] != "ready":
        raise InstallError(f"plan status is {record['status']}; nothing applied")
    harness_plan = to_harness_plan(record, run_id)
    receipt = h.apply(harness_plan, {"packages"}, Path(backup_dir))
    staged = Path(record["staged"])
    for row in record["create"]:  # harnessctl creates files 0600; keep the release's mode
        mode = (staged / row["path"]).stat().st_mode & 0o755
        (Path(record["installed"]) / row["path"]).chmod(mode | 0o600)
    receipt["approval_ref"] = approval_ref
    return receipt


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--policy", type=Path, default=POLICY)
    commands = parser.add_subparsers(dest="command", required=True)
    m = commands.add_parser("manifest", help="hash the allowlisted packages of a tree or git ref")
    m.add_argument("--tree", type=Path, help="skills directory")
    m.add_argument("--git-ref", help="git ref of this repository")
    for name in ("plan", "apply"):
        c = commands.add_parser(name)
        c.add_argument("--staged", type=Path, required=True, help="staged release skills directory")
        c.add_argument("--installed", type=Path, required=True, help="installed skills directory")
        c.add_argument("--baseline", type=Path, required=True, help="baseline manifest JSON")
        c.add_argument("--staged-manifest", type=Path, required=(name == "apply"), help="reviewed manifest of the staged tree")
        c.add_argument("--exclude", action="append", default=[], help="release path to leave untouched")
        c.add_argument("--only-skill", action="append", default=[], help="limit this wave to named public skills")
        if name == "apply":
            c.add_argument("--backup-dir", type=Path, required=True, help="new directory, never reused")
            c.add_argument("--approval-ref", required=True)
    r = commands.add_parser("rollback")
    r.add_argument("--manifest", type=Path, required=True, help="journal written by apply")
    args = parser.parse_args(argv)
    try:
        policy = load_policy(args.policy)
        if args.command == "manifest":
            if bool(args.tree) == bool(args.git_ref):
                raise InstallError("give exactly one of --tree or --git-ref")
            files = tree_manifest(args.tree, policy) if args.tree else git_manifest(ROOT, args.git_ref, policy)
            result = {"source": str(args.tree or args.git_ref), "files": files}
        elif args.command == "rollback":
            result = h.rollback(args.manifest)
        else:
            baseline = json.loads(args.baseline.read_text())["files"]
            reviewed = json.loads(args.staged_manifest.read_text())["files"] if args.staged_manifest else None
            record = plan(args.staged, args.installed, baseline, policy, reviewed, set(args.exclude), args.only_skill)
            result = record if args.command == "plan" else apply(record, args.backup_dir, args.approval_ref)
        print(json.dumps(result, indent=2))
        return 1 if result.get("status") == "blocked" else 0
    except (InstallError, h.HarnessError, OSError, KeyError, ValueError, subprocess.CalledProcessError) as exc:
        print(json.dumps({"status": "error", "reason": str(exc)}))
        return 2


if __name__ == "__main__":
    sys.exit(main())
