#!/usr/bin/env python3
"""Hash gate for skill releases. Dependency free: stdlib only. Read only: makes no writes.

Two modes.

repo: compare the tree SHA of a ref in a local clone against an expected
(locally reviewed) tree SHA. Any mismatch aborts the gate.

install: compare every file under an installed skill directory against the
blob bytes of the same path at a target commit, using local git
(`git cat-file -p <commit>:<path>` per file). Both directions are checked:
a file on disk with no repo counterpart, and a repo blob with no file on
disk, are both mismatches.

Output is a single JSON object on stdout:
{"files_checked": int, "mismatches": [{"path", "expected", "got"}], "ok": bool}
On a fatal error (bad repo, unresolvable ref, unmappable skill dir) the JSON
carries ok:false plus an "error" field, and the process exits 2.
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys


def git(repo, *args):
    return subprocess.run(
        ["git", "-C", repo, *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def fatal(msg):
    print(json.dumps({"files_checked": 0, "mismatches": [], "ok": False, "error": msg}))
    sys.exit(2)


def tree_sha(repo, ref):
    p = git(repo, "rev-parse", ref + "^{tree}")
    if p.returncode != 0:
        return None, p.stderr.decode().strip()
    return p.stdout.decode().strip(), None


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def run_repo_mode(repo, ref, local_tree):
    if git(repo, "rev-parse", "--is-inside-work-tree").returncode != 0:
        fatal("not a git repository: %s" % repo)
    got, err = tree_sha(repo, ref)
    if got is None:
        fatal("cannot resolve ref %r: %s" % (ref, err))
    ok = got == local_tree
    mismatches = [] if ok else [{"path": "tree", "expected": local_tree, "got": got}]
    return {"files_checked": 1, "mismatches": mismatches, "ok": ok}


def run_install_mode(repo, commit, skill):
    if git(repo, "rev-parse", "--is-inside-work-tree").returncode != 0:
        fatal("not a git repository: %s" % repo)
    p = git(repo, "rev-parse", "--verify", commit + "^{commit}")
    if p.returncode != 0:
        fatal("cannot resolve commit %r: %s" % (commit, p.stderr.decode().strip()))
    if not os.path.isdir(skill):
        fatal("skill dir not found: %s" % skill)

    skill_name = os.path.basename(os.path.normpath(skill))
    prefix = "skills/%s/" % skill_name

    p = git(repo, "ls-tree", "-r", "-z", commit, "--", prefix)
    if p.returncode != 0:
        fatal("ls-tree failed: %s" % p.stderr.decode().strip())
    repo_blobs = {}
    for entry in p.stdout.decode().split("\0"):
        if not entry or "\t" not in entry:
            continue
        meta, path = entry.split("\t", 1)
        mode, objtype, _ = meta.split(" ", 2)
        if objtype != "blob":
            continue
        repo_blobs[path[len(prefix):]] = path

    mismatches = []
    seen = set()
    checked = 0
    for dirpath, dirnames, filenames in os.walk(skill):
        dirnames[:] = [d for d in dirnames if d != ".git"]
        dirnames.sort()
        for name in sorted(filenames):
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, skill).replace(os.sep, "/")
            checked += 1
            seen.add(rel)
            if os.path.islink(full):
                mismatches.append({"path": rel, "expected": "regular-file-blob", "got": "symlink"})
                continue
            if not os.path.isfile(full):
                mismatches.append({"path": rel, "expected": "readable-file", "got": "unreadable"})
                continue
            cat = git(repo, "cat-file", "-p", "%s:%s%s" % (commit, prefix, rel))
            if cat.returncode != 0:
                mismatches.append(
                    {"path": rel, "expected": "missing-from-repo", "got": sha256_file(full)}
                )
                continue
            expected = sha256_bytes(cat.stdout)
            got = sha256_file(full)
            if expected != got:
                mismatches.append({"path": rel, "expected": expected, "got": got})

    for rel in sorted(repo_blobs):
        if rel not in seen:
            checked += 1
            cat = git(repo, "cat-file", "-p", "%s:%s" % (commit, repo_blobs[rel]))
            if cat.returncode != 0:
                fatal("cannot read repo blob for %r" % rel)
            mismatches.append(
                {"path": rel, "expected": sha256_bytes(cat.stdout), "got": "missing-on-disk"}
            )

    mismatches.sort(key=lambda m: m["path"])
    return {"files_checked": checked, "mismatches": mismatches, "ok": not mismatches}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("repo", "install"), required=True)
    parser.add_argument("--repo", required=True, help="local clone path")
    parser.add_argument("--ref", help="ref for tree SHA (repo mode)")
    parser.add_argument("--local-tree", help="expected tree SHA (repo mode)")
    parser.add_argument("--skill", help="installed skill dir (install mode)")
    parser.add_argument("--commit", help="target commit (install mode)")
    args = parser.parse_args()

    if args.mode == "repo":
        if not args.ref or not args.local_tree:
            fatal("--mode repo requires --ref and --local-tree")
        result = run_repo_mode(args.repo, args.ref, args.local_tree)
    else:
        if not args.skill or not args.commit:
            fatal("--mode install requires --skill and --commit")
        result = run_install_mode(args.repo, args.commit, args.skill)

    print(json.dumps(result, indent=2))
    sys.exit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
