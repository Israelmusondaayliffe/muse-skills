# Multi-session and multi-thread protocol

The full protocol for runs that span sessions, threads, and surfaces. A run must be resumable by an agent that has never seen the conversation, on a different surface, possibly a different model. Everything below assumes durable state on disk is the single source of truth.

## Session entry

Run read mode of `gauntlet-handoff`: `CONTEXT.md` first, then the newest `HANDOFF.md`, then `run.json`, `PLAN.md`, `pieces.json`, `lanes.json`.

Check the lock before claiming anything. A lock is stale when its heartbeat is older than two hours or its holder session is marked exited in `sessions.json`. A stale lock may be reclaimed via `lock.py`; a live lock may not be overridden, ever. Two sessions in one lane is the fastest way to lose a day of Max-effort compute.

Then claim the lane, write a `sessions.json` entry (index, surface, model, effort, lane, entry time), and restate the contract in one line before doing any work: the goal, the bar, and the lane claimed. If disk state and anything remembered from conversation disagree, disk wins and the discrepancy is surfaced to the user.

## During a session

- Heartbeat the lock every round.
- Write state after every round, not at the end. A session that dies mid-wave must lose at most one round of work.
- All durable facts go to files as they happen: verdicts to `rounds/`, gaps to `gap.md`, piece status to `pieces.json`. Nothing important lives only in the conversation.

## Session exit

Triggered by wall clock, user stop, wave boundary, or explicit request. In order:

1. Release the lane lock.
2. Write the `sessions.json` exit record (exit time, rounds completed, subagents spawned, exit reason, handoff path).
3. Generate `HANDOFF.md` via `write_handoff.py`. The departing agent may append only the `## Judgment notes (unverified)` section (INV-6).

Caps that end a session pause the run, they never certify it (INV-7). A piece interrupted at exit stays `looping` or becomes `capped`; it never becomes `done` because the session ended.

## Parallel lanes, S3 only

- Each lane holds its own lock and its own `sessions.json` entries.
- Lanes own disjoint artifact paths, validated at brief time by `validate_pieces.py`, which refuses S3 when two lanes claim the same path.
- A lane may not touch a path it does not own, including to read-and-rewrite. Reading a foreign path to inform work is allowed; writing it is not, in any form.
- Cross-lane changes wait for the wave boundary merge. A fix that spans lanes is recorded as a proposed merge item, not applied unilaterally.

## Wave boundary

1. All lanes stop.
2. Merge.
3. Run the smoother across the whole artifact: fresh context, sees the whole artifact and the goal, resolves conflicts between independently improved pieces, may not redesign or add. Its changes are recorded as a round of type `smooth`.
4. Write `waves/<n>/merge.md`.
5. Re-validate `pieces.json` with `validate_pieces.py`.
6. Only then does the next wave open. Execution shape may change at this point and only at this point, never mid-wave.

## Cross-surface handoff

A run can continue across sessions or machines if the run directory is reachable.

- The incoming surface runs the section 2 surface precheck (`precheck.py`) and records its own result. It never inherits the previous session's precheck.
- If the new result is equal to or stronger than the previous session's, proceed normally.
- If it comes back weaker (for example, clean-context isolation cannot be confirmed where it previously was), the run either continues in degraded mode, with `run.json` updated and the degradation banner on every handoff and report from that point, or it waits for a stronger surface. The user chooses, with the cost named.
- It never silently proceeds at lower isolation. Claiming the previous session's isolation level on a weaker surface is an integrity failure, not a convenience.
- Handoff documents make this survivable: section 11 of every `HANDOFF.md` records the platform, model, effort, and tools of the writing session, and what the next agent may lack.
