#!/usr/bin/env python3
"""Release gate drift check for the muse-skills repo.

Dependency-free (stdlib only). Runs two drift checks against a local clone:

1. Git drift: the working tree must be clean (``git status --porcelain``
   empty) and the target ref must have no commits unpushed to its remote
   counterpart, and must be an ancestor of (or equal to) it.
2. Upstream drift: skills that declare a pinned upstream source (a
   ``skills/<skill>/NOTICE.md`` with an ``Upstream:`` URL and a
   ``Pinned commit:`` SHA, or a "pinned upstream" line in a ``SKILL.md``)
   are compared against upstream HEAD via ``git ls-remote``. A pin is
   ``behind`` when upstream HEAD differs from the pinned SHA.

This repo has no versioning scheme (no version fields, no CHANGELOG, no
manifest), so pinned upstream commits are the only version-like signal.

Usage:
    gate_drift.py --repo /path/to/clone [--ref main] [--remote origin]

Output is a single JSON document:
    {
      "git_clean": true,
      "changed_paths": ["<porcelain line>", ...],
      "index_blocked": false,
      "unpushed_commits": ["<sha> <subject>", ...],
      "ancestor_of_remote": true,
      "pin_defects": [{"skill": "<skill>", "issue": "<description>"}],
      "pins": [
        {
          "skill": "<skill folder>",
          "url": "<upstream repo url>",
          "pinned": "<pinned 40-hex sha>",
          "upstream_head": "<sha at upstream HEAD, or null>",
          "behind": true | false | null
        }
      ]
    }

``behind`` is null when upstream HEAD could not be resolved (network or
repo error); that is unverifiable, not proof of drift. ``pin_defects``
records pins whose SHA is missing or not a full 40-hex string.

Exit code is 0 on success. Any fatal git error (bad repo, unknown ref)
exits nonzero with a message on stderr. Verdict logic (PASS/FAIL) is left
to the caller; see subagents/gate-drift.md.
"""

import argparse
import json
import os
import re
import subprocess
import sys

SHA_RE = re.compile(r"\b([0-9a-f]{40})\b")
SHORT_SHA_RE = re.compile(r"\b([0-9a-f]{7,39})\b")
URL_RE = re.compile(r"(https?://\S+|git@\S+|\S+\.git)")


def run_git(args, cwd):
    """Run a git command, returning the CompletedProcess."""
    return subprocess.run(
        ["git"] + args, cwd=cwd, capture_output=True, text=True, timeout=120
    )


def find_pins(skills_dir):
    """Return ({skill: (url, pinned_sha)}, [defects]) from NOTICE.md and SKILL.md pins.

    A pin with a URL but no full 40-hex SHA (missing or short) is recorded
    as a defect instead of being silently dropped.
    """
    pins = {}
    defects = []
    if not os.path.isdir(skills_dir):
        return pins, defects
    for skill in sorted(os.listdir(skills_dir)):
        skill_dir = os.path.join(skills_dir, skill)
        if not os.path.isdir(skill_dir):
            continue
        notice = os.path.join(skill_dir, "NOTICE.md")
        if os.path.isfile(notice):
            text = open(notice, encoding="utf-8").read()
            m_url = re.search(r"^[*-]?\s*[Uu]pstream\s*:\s*(\S+)", text, re.M)
            m_sha = SHA_RE.search(text)
            if m_url and m_sha:
                pins[skill] = (m_url.group(1).rstrip(".,;"), m_sha.group(1))
            elif m_url:
                m_short = SHORT_SHA_RE.search(text)
                defects.append({
                    "skill": skill,
                    "issue": "Upstream URL declared but pinned SHA is %s" % (
                        "short (%s), not a full 40-hex commit" % m_short.group(1)
                        if m_short else "missing"),
                })
        for root, _dirs, files in os.walk(skill_dir):
            if "SKILL.md" not in files:
                continue
            path = os.path.join(root, "SKILL.md")
            for line in open(path, encoding="utf-8"):
                if "pinned upstream" not in line.lower():
                    continue
                m_url = URL_RE.search(line)
                m_sha = SHA_RE.search(line)
                if m_url and m_sha:
                    pins.setdefault(
                        skill, (m_url.group(1).rstrip(".,;)"), m_sha.group(1))
                    )
                elif m_url and skill not in pins:
                    defects.append({
                        "skill": skill,
                        "issue": "pinned-upstream line in SKILL.md has no full 40-hex SHA",
                    })
    return pins, defects


def upstream_head(url, cwd):
    """Return the SHA at <url> HEAD, or None if it cannot be resolved."""
    proc = run_git(["ls-remote", url, "HEAD"], cwd)
    if proc.returncode != 0:
        return None
    for line in proc.stdout.splitlines():
        parts = line.split()
        if len(parts) >= 2 and parts[1] == "HEAD" and SHA_RE.match(parts[0]):
            return parts[0]
    return None


def main():
    parser = argparse.ArgumentParser(
        description="Release gate drift check: git cleanliness plus upstream pin drift."
    )
    parser.add_argument("--repo", required=True, help="Path to the local clone.")
    parser.add_argument("--ref", default="main", help="Target ref to gate.")
    parser.add_argument(
        "--remote", default="origin", help="Remote name (default: origin)."
    )
    args = parser.parse_args()

    repo = os.path.abspath(args.repo)
    ref = args.ref
    remote = args.remote

    if not os.path.isdir(os.path.join(repo, ".git")):
        sys.stderr.write("error: %s is not a git repository\n" % repo)
        sys.exit(2)

    # The ref must exist locally.
    rv = run_git(["rev-parse", "--verify", "--quiet", ref], repo)
    if rv.returncode != 0:
        sys.stderr.write("error: ref %r not found in %s\n" % (ref, repo))
        sys.exit(2)

    # 1. Git drift: working tree cleanliness.
    st = run_git(["status", "--porcelain"], repo)
    index_blocked = False
    if st.returncode != 0:
        # A stray index.lock with no running git process is a blocked state.
        if os.path.isfile(os.path.join(repo, ".git", "index.lock")):
            index_blocked = True
            changed_paths = []
            git_clean = False
        else:
            sys.stderr.write("error: git status failed: %s\n" % st.stderr.strip())
            sys.exit(2)
    else:
        changed_paths = [line for line in st.stdout.splitlines() if line.strip()]
        git_clean = not changed_paths

    # 2. Git drift: commits on the ref that are not on the remote ref.
    remote_ref = ref if ref.startswith(remote + "/") else "%s/%s" % (remote, ref)
    run_git(["fetch", remote], repo)  # best effort; updates remote-tracking refs
    rl = run_git(["rev-list", "--reverse", "--oneline", ref, "--not", remote_ref], repo)
    if rl.returncode != 0:
        sys.stderr.write(
            "error: could not compare %s against %s: %s\n"
            % (ref, remote_ref, rl.stderr.strip())
        )
        sys.exit(2)
    unpushed_commits = [line for line in rl.stdout.splitlines() if line.strip()]

    # 2b. Ancestry: the ref must be an ancestor of (or equal to) its remote ref.
    mb = run_git(["merge-base", "--is-ancestor", ref, remote_ref], repo)
    if mb.returncode == 0:
        ancestor_of_remote = True
    else:
        same = run_git(["rev-parse", ref], repo).stdout.strip() == run_git(
            ["rev-parse", remote_ref], repo
        ).stdout.strip()
        ancestor_of_remote = same

    # 3. Upstream drift: declared pins vs upstream HEAD.
    pins_found, pin_defects = find_pins(os.path.join(repo, "skills"))
    pins_out = []
    for skill, (url, pinned) in pins_found.items():
        head = upstream_head(url, repo)
        pins_out.append(
            {
                "skill": skill,
                "url": url,
                "pinned": pinned,
                "upstream_head": head,
                "behind": (head != pinned) if head is not None else None,
            }
        )

    print(
        json.dumps(
            {
                "git_clean": git_clean,
                "changed_paths": changed_paths,
                "index_blocked": index_blocked,
                "unpushed_commits": unpushed_commits,
                "ancestor_of_remote": ancestor_of_remote,
                "pin_defects": pin_defects,
                "pins": pins_out,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
