# Multi-Thread Execution (Hatch)

Gauntlet parallelism on Hatch uses subagents spawned by the lead. Every
subagent starts a fresh session with no inherited transcript: the lead's
brief is its entire context. That is what makes it "fresh" for critic,
reader, and verifier roles — there is no fork-turns control to set and no
old task to accidentally resume.

Default parallelism: bounded subagents inside the current task. Creating
durable external channels instead (cron jobs, event hooks, separate chats,
or any user-owned task surface) requires explicit user approval, a named
thread plan, and is never a substitute for a fresh critic.

For every parallel unit:

- declare purpose, inputs, outputs, quality bar, dependencies, evidence, and integration owner;
- assign disjoint write targets, or serialize when targets overlap;
- preserve the lead's sandbox, authority, and approval limits;
- cap concurrency at what the runtime can actually run (record the live limit in `runtime-capabilities.json`);
- batch verifier panels when subagent slots are limited.

The lead remains responsible for integration and cannot treat subagent
summaries as substitutes for real artifacts. The lead inspects the files
themselves; a builder's report is not evidence.

A critic, handoff reader, or verifier brief contains only: the approved
goal, the quality bar, artifact paths, constraints, evidence locations,
and the verdict schema. Never include builder discussion transcripts.
