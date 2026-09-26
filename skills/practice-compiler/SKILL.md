---
name: practice-compiler
description: Mine a bounded window of my own work sessions (or selected Codex/Claude Code session roots) for repeated tasks, recurring corrections, follow-up instructions, missed tools, and failed commands, then stage redacted, evidence-backed improvement proposals for review. Use when the user asks what their recent work reveals, what keeps going wrong, what should become a skill or workflow, or to review, decide on, or hand off practice proposals. Never scans implicitly and never applies a proposal. It stages proposals only, and approval produces a handoff record, not a change.
---

# Practice Compiler

Turn repeated work into reviewed improvement proposals. The finished result is a scan summary, staged proposals with redacted session-and-line evidence, recorded decisions, and a handoff record for each approval. The scanner never makes the destination change: approval authorizes a handoff record only, never a memory write, config edit, publication, or message.

## Start here

1. **Pin the scan inputs.** One source, an exact inclusive `--since`/`--until` window, a timezone, and the source classes. Take them from the request. If the user named sessions or a window, that is authority to preview; do not re-ask.
2. **Pick the source route:**

| What the user has | Route | Adapter |
|---|---|---|
| "My recent work" in Muse | Export the chosen chats to JSONL per `references/transcript-export.md` into `~/workspace/practice-compiler/session-exports/<since>_<until>/` | `--adapter muse` |
| A named Codex or Claude Code session folder | Scan that exact folder | `--adapter codex` or `--adapter claude` |
| A neutral design export file | `ingest-design-export --input <file>` with the same window | none |
| One lesson stated in the message, or a question about who owns learning | Answer from the message; no scan | none |

3. **Check state before the first persistent write:** `python3 scripts/practice_compiler.py state status` (see State below).
4. **Preview read-only**, from this skill folder:

```bash
python3 scripts/practice_compiler.py scan --adapter muse \
  --sessions-root ~/workspace/practice-compiler/session-exports/2026-09-16_2026-09-23 \
  --since 2026-09-16 --until 2026-09-23 --timezone America/New_York \
  --source-class user --min-occurrences 2 --stdout
```

Report files considered and processed, signal counts by class, source-class counts, proposal count, and input errors. Drop `--stdout` only when the user wants the results kept; that writes the cursor, signal registry, and proposals to the state root.

## Review and decide

1. `python3 scripts/practice_compiler.py report` lists staged proposals.
2. For each one, read the evidence citations (`session:line`). Reject one-offs, generic advice, and signals where a command was only mentioned, not run. Prefer updating an existing skill over proposing a new one. Class definitions: `references/signal-policy.md`.
3. When two proposals share one root cause (a failing flag and the correction about it), approve the one closest to the fix and defer the other with that reason.
4. Record each decision the user makes or has already stated: `decide pc-<id> approve|reject|defer --note "reason"`.
5. Approval writes `<state-root>/handoffs/<id>.json`. Owners in `references/ownership-and-routing.md` are preferred, not required: pass `--available-owner <skill>` only when the user confirms that skill is available; otherwise the handoff stays `generic`.

## Worked example (illustrative, runnable from this skill folder)

Two synthetic sessions fail on the same flag. State and inputs stay in a scratch folder:

```bash
SCRATCH=$(mktemp -d)
export PRACTICE_COMPILER_STATE="$SCRATCH/state"
mkdir "$SCRATCH/exports"
for n in 1 2; do
  printf '%s\n' \
    '{"type":"session_meta","payload":{"id":"demo-'$n'","thread_source":"synthetic","timestamp":"2026-09-1'$n'T10:00:00Z"}}' \
    '{"type":"response_item","payload":{"type":"function_call","name":"muse.exec","arguments":"{\"command\": \"reportgen export --csv weekly.json\"}"},"timestamp":"2026-09-1'$n'T10:01:00Z"}' \
    '{"type":"response_item","payload":{"type":"function_call_output","output":"exit_code: 2 unknown flag --csv"},"timestamp":"2026-09-1'$n'T10:01:02Z"}' \
    > "$SCRATCH/exports/demo-$n.jsonl"
done
python3 scripts/practice_compiler.py scan --adapter muse --sessions-root "$SCRATCH/exports" \
  --since 2026-09-10 --until 2026-09-20 --timezone UTC --source-class synthetic
python3 scripts/practice_compiler.py report
```

The scan processes 2 files and stages two proposals: `repeated-task` (the same export command in both sessions) and `command-failure` with destination `tool-cli`, each with 2 occurrences and citations like `demo-1:3`. Judgment: the failure is the useful signal, since the command repeats only because it keeps failing. Approve the `command-failure` proposal with a note naming the flag, reject or defer the `repeated-task` one as the same root cause, and report the handoff path. The handoff says it authorizes nothing beyond itself; the fix belongs to the tool's owner.

A wrong version would scan without a window, stage the one-off "make the title bold", call the approval a fix, or pass `--available-owner` on a guess.

## State

State lives at `~/workspace/practice-compiler/state/`, outside this replaceable skill folder. Override with `--state-root` or `PRACTICE_COMPILER_STATE`. Earlier versions kept it inside the package at `hidden_files/state/`. `state status` reports one of:

- `none`: use the state root.
- `migrate`: only legacy records exist. Reads use them; persistent writes are refused until you run `state migrate`, which copies them forward and keeps the legacy copy.
- `conflict`: both roots hold different records. Nothing is merged or overwritten; reads use the new root; ask the user which root to keep and pass it with `--state-root`.

## When something goes wrong

| Symptom | Likely cause | Next move | Stop and ask when |
|---|---|---|---|
| `scan requires an exact --since and --until window` | Window missing | Use the window from the request | no window was given; ask once for it |
| `files_processed` is 0 | Source-class filter excludes the files, wrong adapter, or window misses the timestamps | Check `source_class_counts` in the output and the adapter; rerun once | the counts show the files are outside the window |
| `errors` lists input lines | Export lines are not valid JSONL | Fix the export, not the scanner; rerun | the export cannot be regenerated |
| `state needs attention (migrate)` | Legacy in-package state | `state migrate` | never |
| `state needs attention (conflict)` | Two different state trees | Report both paths | always; the user picks the root |
| An email, secret, or private path appears in a record | Redaction miss | Do not share the record; report the field | before anything leaves this machine |

## Completion

Done means the user has: the scan id and mode, files processed and skipped, signal counts, staged proposals (id, class, destination, occurrences, confidence), decisions recorded, and handoff paths for approvals. A preview-only run is complete when the user asked for a preview. If persistence was refused by the state check, say so and give the command that clears it.

## Operating rules

- Exact window on every scan and export. No open-ended mining.
- Require repeated evidence (`--min-occurrences 2`). Stage a one-off only when the user asks.
- The scanner reads direct user-authored events only; injected instructions, tool output, and quoted transcripts are not user feedback.
- A scheduled scan may run `scan` and `report` only. Decisions stay with the user. If a proposal's destination is a hook or cron job, hand it to `harness-engineering` with a safety note; never build the hook here.
- Stale handoffs are re-checked against the current destination before anyone acts on them.
