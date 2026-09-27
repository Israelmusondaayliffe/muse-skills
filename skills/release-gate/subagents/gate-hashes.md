---
name: gate-hashes
description: "Use when a release gate needs hash verification. Repo mode proves the pushed branch tree is byte-identical to the locally reviewed tree; install mode proves every installed file matches the repo blob at the target commit."
---

Invocation: gate step. Run repo mode before install mode. This repo has no versioning scheme, so commit and tree SHAs are the identity of the release; record both SHAs in every report.

## Inputs

- Repo mode: `LOCAL_REPO` (the reviewed working copy), `BRANCH` (the pushed branch name).
- Install mode: `CLONE` (a local clone of the repo), `TARGET_COMMIT` (the exact commit SHA under review), `INSTALLED_DIR` (the installed skill directory, for example `$HOME/.claude/skills/<skill-name>`).

## Mode: repo

Goal: prove the pushed branch tree is byte-identical to the locally reviewed tree. This is the same guard used in the real rebuilds.

Procedure:

1. In the local repo, record the reviewed state.

   ```
   git -C "$LOCAL_REPO" rev-parse HEAD          # LOCAL_COMMIT, for the record
   git -C "$LOCAL_REPO" rev-parse HEAD^{tree}   # LOCAL_TREE, the reviewed tree
   git -C "$LOCAL_REPO" status --porcelain
   ```

   The status output must be empty. If the working copy is dirty, stop and report: an uncommitted tree cannot be compared.

2. Fetch the branch and resolve its tree.

   ```
   git -C "$LOCAL_REPO" fetch origin "$BRANCH"
   git -C "$LOCAL_REPO" rev-parse "origin/$BRANCH"          # REMOTE_COMMIT
   git -C "$LOCAL_REPO" rev-parse "origin/$BRANCH^{tree}"   # REMOTE_TREE
   ```

3. Compare, either by string equality of the two tree SHAs or:

   ```
   git -C "$LOCAL_REPO" diff-tree --quiet "$LOCAL_TREE" "origin/$BRANCH^{tree}" && echo IDENTICAL || echo MISMATCH
   ```

   Preferred: run the script, which emits the comparison as JSON.

   ```
   bin/gate_hashes.py --mode repo --repo "$LOCAL_REPO" --ref "origin/$BRANCH" --local-tree "$LOCAL_TREE"
   ```

4. Verdict:
   - PASS: the tree SHAs are identical. Record `LOCAL_TREE`, `REMOTE_TREE`, `REMOTE_COMMIT`.
   - FAIL: any mismatch. Abort the gate here. Do not proceed to install mode. A mismatch means the pushed branch is not the reviewed tree; the release cannot continue until the branch is rebuilt from the reviewed tree.

## Mode: install

Goal: prove every file under the installed skill directory is byte-identical to the blob of the same path at the target commit.

Procedure:

1. Confirm the clone is at the exact target commit before reading any blob.

   ```
   git -C "$CLONE" rev-parse HEAD
   ```

   This must equal `TARGET_COMMIT`. If it does not, check out the commit first; never compare against a different commit.

2. Preferred: run the script, which reads each blob with local git (`git cat-file -p <commit>:<path>`) and emits JSON.

   ```
   bin/gate_hashes.py --mode install --repo "$CLONE" --commit "$TARGET_COMMIT" --skill "$INSTALLED_DIR"
   ```

3. Manual fallback if the script is unavailable. For each regular file `F` under the installed dir:

   ```
   REL=${F#"$INSTALLED_DIR"/}
   EXPECTED=$(git -C "$CLONE" cat-file -p "$TARGET_COMMIT:skills/<skill-name>/$REL" | sha256sum | cut -d' ' -f1)
   GOT=$(sha256sum "$F" | cut -d' ' -f1)
   [ "$EXPECTED" = "$GOT" ] && echo "OK $REL" || echo "MISMATCH $REL"
   ```

   `git cat-file -p` exits nonzero when the path is not a blob at that commit. Treat that as unverifiable, which is a FAIL, not a skip. Also enumerate the repo side (`git -C "$CLONE" ls-tree -r "$TARGET_COMMIT" -- "skills/<skill-name>/"`) and fail on any repo file missing from the installed dir.

4. Parse the script JSON: `files_checked` (integer), `mismatches` (array of `{path, expected, got}`), `ok` (boolean). Record the total and list every mismatch with its expected and got SHA256.

5. Verdict:
   - PASS: `ok` is true and `mismatches` is empty.
   - FAIL: any mismatch, or any file that cannot be verified: missing from the repo at the target commit, extra on disk with no repo counterpart, unreadable, or a symlink. List each one.

## Rules for both modes

- Never modify the local repo, the clone, or the installed dir during the check.
- The check is read-only. Any failure to read (missing ref, missing commit, missing path) is a gate failure, never a skip.
- Keep the script JSON output in the gate report as the evidence record.

## Report format

```
Gate: hashes
Mode: repo | install
Ref: <branch or commit>
Tree SHA: <local> vs <remote>        # repo mode
Files checked: <n>                   # install mode
Mismatches: <path: expected -> got, or "none">
Verdict: PASS | FAIL
```
