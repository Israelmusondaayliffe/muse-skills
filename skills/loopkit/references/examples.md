# LoopKit examples (Hatch)

Adapted from the plugin's example tasks. Provide the stated inputs before each run.

## 1. Weekly local activity scout

Inputs: town, travel limit, interests, preferred reporting time.

```text
Use the loopkit skill to design a weekly research loop for local activities over the next seven days. Return a best plan, backup, shortlist, and source check. Include current dates, travel estimates, and costs or unknowns. No bookings, purchases, or messages. Complete and verify one manual run before proposing the schedule. If scheduling is unavailable, return the schedule specification and say it is inactive.
```

Expected: a bounded contract, a sourced report, a verification receipt; a cron job only when supported and explicitly authorized.

## 2. Workshop revision through review

Inputs: approved revision scope, draft pages, output folder, any existing verification command.

```text
Use the loopkit skill to design a contract for this approved workshop revision. Name the permitted files, required editorial and beginner reviews, completion checks, and stop conditions. Allow at most three iterations and stop after one iteration with no progress. Then execute the local revision. Do not publish until I explicitly approve the final pages and destinations.
```

Expected: a saved contract, bounded iterations, and a completion receipt supported by actual checks.

## 3. Compare two repository copies before synchronizing

Inputs: the two repository paths and the files that should match.

```text
Use the loopkit skill to compare the approved files in these two repositories. Record the expected relationship, actual differences, and permitted repairs in a contract. Begin read-only and show the proposed synchronization. After approval, apply only those repairs, verify the result, and save a checkpoint for resuming if interrupted. Do not push, merge, install, or change credentials.
```

Expected: a reproducible comparison and proposed repair scope, followed by approved local changes and a verified receipt.

## 4. Morning briefing loop (Hatch-native)

```text
Use the loopkit skill to design a daily briefing loop. Allowed paths: ~/workspace/briefings/. Machine checks: the briefing file exists for today's date and names its sources. No-op behavior: when no calendar items, messages, or news changed since yesterday, write nothing and record a receipt with status running and progressed=false. After one successful manual run, schedule it with a cron job.
```

Expected: a cron-owned daily loop whose quiet days are cheap, verifiable no-ops.
