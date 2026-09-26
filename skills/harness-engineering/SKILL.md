---
name: "harness-engineering"
description: "Design, build, verify, or maintain Muse's personalized operating setup (memory and instruction files, workspace layout, skills, automations, and connectors) from a vague brief or an existing setup. Use when the user asks for an operating system for their AI, a setup overhaul or guided setup, instruction-file or memory work, workspace architecture, capability cleanup, or a scheduled review of the assistant's own configuration. Route focused requests to the phase that matches."
metadata: { "includeInPrompt": true }
---

# Harness Engineering

Turn a brief into Muse's smallest working operating harness: the persistent instruction files, workspace layout, skills, automations, and connectors that make everyday work consistent. The user's existing files and live environment are implementation truth.

A change request is finished when the target files changed as approved, the backup manifest exists, and the task-owned behavior check ran against the changed setup. An audit or plan is finished work only when that is what the user asked for.

## Start here

1. **Read the live state first.** Open the files the request touches before asking anything discoverable.
2. **Pick the entry by what the user already decided:**

| The user has | Enter at | First action |
|---|---|---|
| A vague goal ("set up my assistant") | Interview | `references/interview-tree.md`, one branch at a time |
| An existing setup to improve, no specific change | Audit (read-only) | `python3 scripts/context_scan.py <files>` plus reading them |
| Findings, wants options | Plan | fill `assets/harness-plan.template.json` |
| A specific, approved change ("replace X with Y in AGENTS.md") | Build | write the plan JSON, `python3 scripts/harnessctl.py dry-run ...` |
| A finished build, "is it working" | Verify | run the plan's behavior check on the changed files |
| A model update or periodic review | Maintain | re-audit against fresh state |

A clear, approved change is authorization to build. Do not re-interview or re-plan decisions the user already made; ask only for a fact that changes the operation (a missing path, conflicting instructions).

3. **Judge context by evidence.** Read `references/context-doctrine.md` before writing or trimming any persistent context. Keep guidance, examples, and checks that observed performance supports; cut what is stale, conflicting, duplicated, or shown unused. A task-specific check tied to evidence stays; stacked generic "double-check" reminders collapse into it.

Full phase workflows: `references/phases.md`.

## Build with the helper

Local file creates and updates go through `scripts/harnessctl.py` (`references/file-operations.md`):

1. Plan JSON from `assets/harness-plan.template.json`: concrete `run_id` and `outcome` (the helper rejects the template's `replace-me` values), resolved absolute `allowed_roots` and targets (a symlinked path such as macOS `/var` is rejected), one approval group per user approval, each update with the current `expected_sha256`, each operation with exactly one of `content` or `source`.
2. `python3 scripts/harnessctl.py dry-run --plan /abs/plan.json --approved-group <group>`; review targets and hashes.
3. `python3 scripts/harnessctl.py apply --plan /abs/plan.json --approved-group <group> --backup-dir /abs/new-dir`. A reused backup directory is refused.
4. Re-run the plan's behavior check. Rollback when needed: `python3 scripts/harnessctl.py rollback --manifest /abs/new-dir/manifest.json`.

The helper supports create and update only; it never deletes, authenticates, runs shell commands, or probes the host. Apply is per file, not one transaction; report partial application from the manifest.

## Worked example (illustrative, synthetic)

Request: "Approved: in AGENTS.md, replace the retired `old-notes/` line with `drafts/`, collapse the three generic reminder lines, and create docs/README.md with one line. Prove rollback works."

- Read `AGENTS.md`: three generic "double-check" lines, plus one task-specific line that runs the workspace's link-check script on `outputs/` before a link-list task is called done. Judgment: the link check names a command and a condition, so it is the one concrete check the generic lines were gesturing at. Keep it word for word and remove the three generic lines. The approval line is user policy; keep it.
- Plan: group `workspace-files`, one `update` with `expected_sha256` from `shasum -a 256 AGENTS.md`, one `create` for `docs/README.md`.
- `dry-run` lists both (`before` null for the create). `apply --backup-dir .../backup-1` prints `applied`. `rollback` prints `restored`; `AGENTS.md` hash matches the original; `docs/README.md` is gone (the empty `docs/` folder stays). Re-apply needs `backup-2`.
- Report: files changed, backup and manifest paths, the hash before and after, and that the link-check line survived.

A wrong version would delete the link-check line along with the reminders, edit the file directly, or report recovery without the helper's `restored` output.

## When something goes wrong

| Symptom | Likely cause | Next move | Stop when |
|---|---|---|---|
| `hash drift: <file>` | File changed since the plan was written | Re-read it, show the change, rebuild that operation | the change conflicts with the approval: ask |
| `symbolic-link path is not allowed` | Path passes through a symlink | Use the resolved path (`realpath`) in roots and targets | the real target is outside approved roots: stop |
| `run_id must be ... without template placeholders` | Template values left in the plan | Fill `run_id` and `outcome` | valid |
| `File exists: <backup dir>` | Backup directory reused | Choose a new directory | always new |
| `rollback conflict; new user work preserved` | File changed after apply | Leave it; report the file and ask | never force |
| Behavior check fails after apply | Change broke the setup | Roll back, report the failure, re-plan | second failure: report and stop |

## Completion

- **Applied and verified**: approved operations applied, manifest path given, behavior check passed on the changed files.
- **Applied, check pending**: the change landed but the behavior check could not run (for example the skill must reload first). Say what is unverified.
- **Partial**: some operations applied; list which from the manifest, and the rollback command.
- **Blocked**: name the conflict or missing approval and the smallest next action.
- Audit, plan, or interview requests end with their artifact: findings (verified facts, inferred risks, user decisions), a decision-complete plan, or a confirmed profile (`references/profile.schema.json`).

## Operating rules

- Audit and planning are read-only. Approval for one group never approves another.
- Verify with fresh evidence from the changed environment. A passing check never outweighs unresolved required work.
- Never install third-party code, trust hooks, authenticate accounts, send messages, or publish without separate approval (`references/safety-and-approvals.md`).
- Record configuration keys and capability state, never secret values.

## Resources

- `scripts/harnessctl.py` (dry-run, apply, rollback), `scripts/context_scan.py` (read-only context scan).
- `references/`: `phases.md`, `context-doctrine.md`, `file-operations.md`, `operations.schema.json`, `harness-architecture.md`, `interview-tree.md`, `profile.schema.json`, `prompt-governance.md`, `model-change-policy.md`, `safety-and-approvals.md`, `verification-standard.md`, `platform-notes.md`.
- `assets/harness-plan.template.json`.
