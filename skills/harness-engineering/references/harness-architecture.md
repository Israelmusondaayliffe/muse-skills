# Harness Architecture

## Three operating layers
1. Information: instructions, context, skills, tools, connectors, memory, and project references.
2. Execution: workspace boundaries, plans, autonomous runs, scripts, schedules, approvals, and recovery.
3. Feedback: checks, receipts, reviews, failure records, maintenance, and model-change audits.

A useful harness is balanced across all three. Do not compensate for missing verification by adding more instructions.

For change requests, the target-state delta is the primary output. Information and feedback work support execution and stay smaller than it. Reports, plans, receipts, and critics are not progress by themselves.

## Scope hierarchy
- Thread prompt: one task.
- Global instruction layer: `~/SOUL.md`, `~/IDENTITY.md`, `~/USER.md`, `~/MEMORY.md`, `~/AGENTS.md`, `~/TOOLS.md` — personal defaults that apply everywhere.
- Workspace layer: `~/workspace/` layout, skills, docs — shared routing and output rules.
- Goal or project layer: `~/workspace/goals/<slug>/` — goal-specific files and deliverables.
- Skill: a repeatable workflow under `~/workspace/skills/`.
- Connector: a connected external service (email, calendar, music, shopping).
- Scheduled work: cron jobs and hooks with explicit scopes and instructions.
- Script or check: deterministic enforcement (preferred whenever behavior must be exact).

Put a requirement in the narrowest scope that must always see it.

## Reliability order
Prefer the least-free mechanism that fits:
1. Script (deterministic check or helper)
2. Cron/hook configuration and scopes
3. Workspace template or convention
4. Instruction file
5. Skill guidance
6. Inference

Repeated corrections should move toward deterministic enforcement.

## Work-first controls
- One budget covers exploration, audit, implementation, review, repair, and final verification for the full request.
- Use the smallest sufficient topology. More available subagents do not imply more launches.
- One integrated critic may cover several low-risk workstreams.
- Stop after one low-yield wave when unresolved work does not fall.
- Completion requires terminal results for required items. Deferred, audit-only, and backfill-only are incomplete unless the user approved that outcome.

## Context architecture
Model-visible instructions are a compact context kernel plus delta-only overlays. The front-door skill stays in default context; specialists, detailed workflows, examples, and recovery guidance load from their task-owned files. Exact behavior belongs in deterministic mechanisms whenever possible.

Prompt size is a diagnostic, not an acceptance criterion. Freeze behavior before subtracting instructions and keep only reductions that preserve authority, routing, stopping, formatting, and verification. See `references/prompt-governance.md` for the evidence and rollout contract.
