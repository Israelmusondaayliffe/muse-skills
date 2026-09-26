# Approved local file operations

Use this helper when an approved build creates or updates local text or binary files. It never authenticates, runs shell commands, changes accounts, or certifies a host. Only `create` and `update` are supported. A command-line approval flag records existing user authority; it cannot provide that authority itself.

Fill `assets/harness-plan.template.json` with concrete outcomes, a finite resource budget, exact absolute targets, approved roots, approval groups, and operations. Resolve filesystem aliases first (`Path(...).resolve()`); symlink paths are rejected. Every update needs the current SHA256. Supply exactly one of `content` (a text string) or `source` (a local file path). A create requires an absent target. Duplicate targets are rejected. A plan that still carries the template's `replace-me` values in `run_id` or `outcome` is rejected: fill them before dry-run.

Run from this skill's directory. On hosts where the temporary directory is a symlink (macOS `/var`, `/tmp`), pass resolved paths or the target is rejected as a symbolic-link path.

```sh
python3 scripts/harnessctl.py dry-run --plan /absolute/plan.json --approved-group local-files
python3 scripts/harnessctl.py apply --plan /absolute/plan.json --approved-group local-files --backup-dir /absolute/new-backup-directory
python3 scripts/harnessctl.py rollback --manifest /absolute/new-backup-directory/manifest.json
```

Inspect the dry-run target list and hashes before applying. Choose a new backup directory outside the replaceable skill package. The helper checks all selected files before writing, verifies backups, journals recovery data before mutation, then replaces files atomically. Preserve the backup directory and manifest. Apply is per-file, not a multi-file transaction: interruption may leave a partially applied group; report that and use the manifest.

Rollback first checks every file and backup. It refuses to overwrite work changed after apply, restores only matching updates, verifies each restored hash, and removes only unchanged files created by this run. Parent directories that apply created are left in place. It is safe to resume after interruption. A conflict needs a new reviewed plan; never force it. Run with one writer and no concurrent changes to the same targets. Hash preconditions are drift detection, not an operating-system security boundary.

A file update is not runtime acceptance. Reload/discover the changed skill and run the task-owned behavior check before calling the build complete.
