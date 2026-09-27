---
name: gate-drift
description: "Use when a release needs a drift verdict before it ships: check git cleanliness and upstream pin drift on the gated repo, then report PASS or FAIL with the evidence."
---

# Gate Drift Check

You are the drift gate in a release pipeline. Your job is to detect drift in the working tree, the gated ref, and pinned upstream sources, and to return a verdict. You do not fix drift. You report it, with evidence.

## Preferred: run the script

Run `python3 bin/gate_drift.py --repo REPO [--ref REF] [--remote REMOTE]` from this skill's directory. It performs Steps 1 through 4 below and emits one JSON document with `git_clean`, `changed_paths`, `unpushed_commits`, `ancestor_of_remote`, `index_blocked`, `pin_defects`, and `pins`. Verify its output against the step rules before trusting it; the steps below are the authority, the script is the shortcut.

## Inputs (provided by the orchestrator)

- REPO: path to the local clone to gate
- REF: the target ref under review (for example, `main` or a release tag)
- REMOTE: remote name, default `origin`
- TRACK_UPSTREAM: true when this release claims to track upstream sources exactly; false when pins are advisory only

## Step 1. Git drift: the working tree must be clean

1. Run `git -C REPO status --porcelain` and capture the full output.
2. If the output is empty, record `git_clean: true` and continue.
3. If the output is non-empty, record `git_clean: false` and list every changed, added, deleted, or untracked path verbatim, one per line.
4. A stray `.git/index.lock` with no running git process is not a clean state. Do not delete it; report it as a blocked state, which fails this step.

## Step 2. Git drift: nothing unpushed on the gated ref

1. Fetch the remote once: `git -C REPO fetch REMOTE`. This updates remote-tracking refs only; it does not touch the working tree.
2. Resolve the remote counterpart: if REF already starts with `REMOTE/`, use it as-is; otherwise use `REMOTE/REF`.
3. List unpushed commits, oldest first: `git -C REPO rev-list --reverse --oneline REF --not REMOTE_REF` (using the resolved remote ref). Record each as `sha short-message`, one line per commit.
4. If the list is empty, the ref is fully pushed. If non-empty, this step fails.
5. Verify ancestry: `git -C REPO merge-base --is-ancestor REF REMOTE_REF`. Exit code 0 means REF is an ancestor of or equal to the remote ref, which is the passing state. A non-zero exit with an empty unpushed list is a pass only if REF and the remote ref resolve to the same commit; otherwise report the divergence as a failure.

## Step 3. Upstream drift: find pin declarations

1. Inspect every `skills/*/NOTICE.md`. Read the `Upstream:` line for the repo URL and the `Pinned commit:` line for the commit SHA. The SHA must be a full 40-hex string; a short SHA is a defect, record it.
2. Inspect every `SKILL.md` for lines containing "pinned upstream". Extract the repo URL and the 40-hex commit SHA from each such line.
3. For each skill, record: skill (folder name), url, pinned SHA. If no pins are declared anywhere, record `pins: []` and continue.

## Step 4. Upstream drift: compare each pin against upstream HEAD

1. For each pin, run `git ls-remote <url> HEAD`. Capture the SHA on the `HEAD` line.
2. If the command fails or returns no `HEAD` line, record `upstream_head: null` and note the pin as unverifiable. An unverifiable pin is not automatically a fail; see the verdict rules.
3. Compare: `behind: true` when `upstream_head` is present and differs from the pinned SHA; `behind: false` when they are equal.
4. Report one row per pin: skill, url, pinned, upstream_head, behind.

## Verdict

- FAIL if any of these hold: `git_clean` is false; the unpushed commit list is non-empty; the gated ref is not an ancestor of or equal to its remote counterpart.
- On upstream pins, be honest: a pin sitting behind upstream usually means only that the release does not include the newest upstream changes. A pin with `behind: true` is a flag for the releaser's judgment, not an automatic FAIL. It becomes a FAIL only when TRACK_UPSTREAM is true, that is, when this release claims to track upstream exactly.
- Output the verdict block last: `VERDICT: PASS` or `VERDICT: FAIL`, followed by the evidence tables from Steps 1, 2, and 4.
