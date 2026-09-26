# Multi-Thread Execution (Hatch)

Gauntlet parallelism on Hatch uses subagents spawned by the lead. A
spawned subagent is intended to start with no inherited transcript, so the
lead's brief is its entire context. Treat that as unverified until the lead
records evidence with `gauntletctl.py capabilities --fresh-isolation
--isolation-evidence "<observed check>"` (for example, the child could not
produce a canary string that exists only in the parent turn). A host or
model name is not proof. Without that record, `runtime-capabilities.json`
says `unknown`, and a verdict that depends on fresh judges carries the
isolation caveat (`verified_with_caveats` at best). Never resume an old
task as a substitute for a fresh critic.

Default parallelism: bounded subagents inside the current task. Creating
durable external channels instead (cron jobs, event hooks, separate chats,
or any user-owned task surface) requires explicit user approval, a named
thread plan, and is never a substitute for a fresh critic.

For every parallel unit:

- declare purpose, inputs, outputs, quality bar, dependencies, evidence, and integration owner;
- assign disjoint write targets, or serialize when targets overlap;
- preserve the lead's sandbox, authority, and approval limits;
- cap concurrency at what the runtime can actually run and at `budget.max_concurrency` (record the live limit in `runtime-capabilities.json`);
- before each dispatch, confirm `agent_launches` in `budget-ledger.json` plus the proposed launches stays within `budget.max_agent_launches`; record usage right after launching;
- batch verifier panels when subagent slots are limited.

The lead remains responsible for integration and cannot treat subagent
summaries as substitutes for real artifacts. The lead inspects the files
themselves; a builder's report is not evidence.

A critic, handoff reader, or verifier brief contains only: the approved
goal, the quality bar, artifact paths, constraints, evidence locations,
and the verdict schema. Never include builder discussion transcripts.
