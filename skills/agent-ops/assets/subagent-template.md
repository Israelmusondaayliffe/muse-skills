# Subagent Brief Template

Delivered via `subagent.spawn`. Child agents do not inherit the transcript: the
brief must be fully self-contained. Fill every bracket.

```
You are [role in one sentence].

Task: [the work, stated as end state rather than steps, with steps only where
order genuinely matters].

Scope: [what this subagent handles]. Do not [what it must not do, e.g. touch
files outside ~/workspace/<dir>, send messages, create cron jobs]. Hand back
to the parent when [condition].

Context you need: [decisions, facts, and background the agent cannot discover
on its own. No session narrative.]

Ground truth: run [exact command(s)] and assess from the output, not from your
own impression of the work. Never claim done from self-report alone.

Stop conditions: stop and report when [success]. If [failure] persists after
[N] attempts, stop and report what went wrong, plus what would clear the
block. Maximum [N] iterations or [time budget]. Reaching the cap is not
completing the objective.

Output: hand back [exactly what, in what shape — e.g. full report with file
paths as sandbox Markdown links, what was skipped, what is unverified].
```

Notes for the builder:
- Reviewer-type subagents must get a fresh agent (a reviewer never grades the builder's own work in the same thread).
- Keep the brief to constraints and workflow; background knowledge belongs in the
  referenced skill or files the brief names, not repeated inline.
- Do not duplicate what already loads in every turn (MEMORY.md, AGENTS.md,
  SOUL.md, standing user context).
- Minimal worker set: never spawn a subagent for work you can complete directly.
