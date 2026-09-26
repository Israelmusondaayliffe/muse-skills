# Hatch mechanics for gauntlet runs

How the gauntlet method's platform assumptions map onto Hatch. The method's rules
are unchanged; this file says how to satisfy them here.

## Fresh-context spawning

On Hatch, `subagent.spawn` is intended to create a child that does not inherit the
lead's transcript. Treat that as unverified until the lead records evidence (for
example, a child asked for a canary string that exists only in the parent turn cannot
produce it). `precheck.py` reports `subagents: "unknown"` for every host label, so a
Muse run records `context_isolation: "degraded"` unless that evidence exists. Either
way, the lead disciplines what goes into the brief:

- The brief is the child's entire context. Write it self-contained: goal, bar refs
  (as file paths it can read), piece definition, current artifact path, and the
  agent instruction file (`agents/<role>.md`). Never paste in builder reasoning,
  prior verdicts, gaps, or other pieces' state.
- For critics, hand over only the neutral A/B inspection outputs under `runs/`,
  never any path into `.gauntlet/sealed/`.
- A child cannot see the lead's memory files, transcript, or other spawned
  children's output unless the lead copies it into the brief. Keep that one-way:
  builders and critics never receive each other's context.
- The lead asserts `critic_saw_builder_context: false` and
  `critic_context_source: "files-only"` when recording verdicts. That assertion
  is made by the spawning code (the lead), never self-reported by the child.
  `round_record.py` rejects anything else.

## Tooling available to the lead

- **Shell**: `muse.exec` runs the `scripts/` gates and inspection commands.
- **Browser**: the live Chromium browser is a delegated task from the main agent,
  not a subagent tool. For `screenshot`/`render`/`source-reach` inspection, the
  lead asks the user (or the parent task) to run the browser capture and store the
  result under the round's `inspection/` directory before judgment. Never judge a
  screenshot from a description — if no capture exists, the round fails.
- **Cron**: creating a scheduled job is outside the run's authority and needs its
  own explicit user approval. If approved, the job re-invokes the lead with
  "continue the gauntlet" on the run directory; the round loop owns iteration and
  each tick runs precheck, lock heartbeat, and `check_stops.py` first. Without an
  approved job, a multi-day run resumes when the user invokes it.
- **Files**: run state lives under `.gauntlet/` in the target project root
  (default: the current working directory). The lead never edits a sealed map,
  a verdict file that a script rejected, or consensus output by hand.

## What does not transfer

- There is no effort ladder and no multi-agent opt-in token on Hatch. The prompt
  clause is "use subagents freely and work at the highest effort setting" — the
  linter checks for the words "subagent" and "effort", nothing more.
- There is no built-in `/loop` surface. An approved cron job or the user's own
  re-invocation paces a multi-session run.
- Budgets are cooperative. `check_stops.py` reads `run.json` and `cost.json`; it
  cannot see or block launches the lead does not record. Record every launch and
  metered cost in `cost.json` as it happens, and run
  `check_stops.py --next-launches N --next-cost C` before each dispatch.
- Lane locks (`lock.py`) matter only when two sessions touch the same run
  concurrently (S3 or a resumed session). Single-lead runs may acquire the lock
  once and heartbeat it; they must still release it at handoff.
