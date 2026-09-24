# Agent Design Spec

Filled by ARCHITECT before any artifact is written. Every field, no blanks.

```
TASK: [what the user wants done, one sentence]

PATTERN: [single call / chaining / routing / parallelization / orchestrator-workers / evaluator-optimizer / autonomous agent]
REJECTED SIMPLER RUNG: [the rung below and the concrete reason it fails this task]
TRADE ACCEPTED: [what this costs in latency and dollars, what it buys]

TARGET: [Hatch subagent brief / cron-scheduled run / workflow checklist / skill]

AUGMENTATIONS:
- Retrieval: [what, or none]
- Tools: [list, minimal grant]
- Memory: [what persists between steps or runs, or none]

GROUND TRUTH: [the exact commands or environmental checks that verify progress, e.g. pytest, npm run build, a curl check, diff review]

SUCCESS CRITERIA: [checkable by a stranger without asking questions]

STOP CONDITIONS:
- Success: [condition]
- Failure: [after N attempts, report what went wrong]
- Blocked: [stop and report when no defensible path remains, plus what would clear the block]
- Cap: [max N iterations / time budget]

ITERATION POLICY: [how the agent chooses the next action between attempts, e.g. expand axes if outputs cluster, tighten constraint if X appears, rerun check]

PAUSE POINTS: [where a human checks in, placed before steps that poison downstream work; for cron work, where the report should flag for user review]

SCOPE: [what it may read, what it may write, what it must never touch. Write scope defaults to ~/workspace/ with a named subdirectory, versioned naming, announce the path when done]

ENVIRONMENT: [what is already in context every turn and must not be duplicated in the brief: MEMORY.md, AGENTS.md, SOUL.md, standing user context, goal workspaces]
```
