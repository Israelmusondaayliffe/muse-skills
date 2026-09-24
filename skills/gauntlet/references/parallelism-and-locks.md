# Parallelism and locks

How gauntlet work is shaped across sessions and threads, who owns what, and how the lock keeps two sessions from destroying each other's rounds. The shape is chosen at brief time, recorded in `run.json`, and can change at a wave boundary, never mid-wave.

## Execution shapes

**S1, single session.** Ten pieces or fewer, one wave, one lane. No handoff machinery beyond a final report. The lock still exists (it is cheap and it protects against an accidental second session), but there is no lane contention by design.

**S2, sequential multi-session.** Many pieces, one lane at a time, work spans sessions. Exactly one session holds the lock at any moment. A handoff is written at every session exit. Default for most mega projects.

**S3, parallel lanes.** Pieces partition cleanly by artifact path. Multiple concurrent sessions or threads run at once, one lane each, with lane-level locks and a merge plus smoothing pass at wave boundaries. `validate_pieces.py` refuses S3 when two lanes claim the same artifact path. Two lanes writing one file is the fastest way to lose a day of Max-effort compute.

## Lane ownership

- Every piece belongs to exactly one lane. Every lane owns a disjoint set of artifact paths, declared in `lanes.json` and validated at brief time.
- A lane may not touch a path it does not own, including to read-and-rewrite. Reading another lane's output to inform your own edit of your own file is fine; editing another lane's file, for any reason, is not.
- Cross-lane changes wait for the wave boundary merge. If a gap cannot be closed without touching a path the lane does not own, the builder says so and stops (that is the builder mandate), and the lead records the piece as `blocked` until the boundary.

## Lock lifecycle

All lock operations go through `~/workspace/skills/gauntlet/scripts/lock.py` with `--run-dir`. The lock file is `run.lock` in the run directory; in S3 each lane has its own lock entry.

**Acquire.** At session entry, after `gauntlet-handoff` read mode. Acquiring records the holder session and a fresh heartbeat timestamp, and writes the session entry in `sessions.json`. If the lock is held and live, do not proceed on that lane: wait, take a different unclaimed lane (S3), or tell the user.

**Heartbeat.** Every round, at step 5 of the round algorithm. The heartbeat timestamp is the liveness signal other sessions read.

**Release.** At session exit (wall clock, user stop, wave boundary, or explicit request): release the lock, write the `sessions.json` exit record, generate `HANDOFF.md` via `gauntlet-handoff` write mode.

**Stale reclaim.** A lock is stale when its heartbeat is older than two hours or its holder session is marked exited in `sessions.json`. A stale lock may be reclaimed: `lock.py` performs the check and the reclaim, a model does not eyeball timestamps and decide. Because state is written after every round, reclaiming a stale lock loses at most one round of work.

## Wave boundary protocol

From SPEC section 10, in order:

1. All lanes stop. No new rounds start once the boundary is reached.
2. Merge. Lane outputs come together into the whole artifact.
3. Run the smoother across the whole artifact (fresh context, `~/workspace/skills/gauntlet/agents/smoother.md`, no piece history). Its changes are recorded as a round of type `smooth`.
4. Write `waves/<n>/merge.md`.
5. Re-validate `pieces.json` with `validate_pieces.py`. The next wave's plan goes to `waves/<n+1>/PLAN.md` with the root `PLAN.md` pointing at it. The execution shape may change here, and only here.
6. Only then does the next wave open.

## Cross-surface handoff

A run can continue across sessions or machines if the run directory is reachable. The incoming surface runs the front door precheck and records its own result. If it comes back weaker than the previous session's, the run continues in degraded mode with the banner on every handoff and report, or waits. It never silently proceeds at lower isolation.
