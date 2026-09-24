---
name: "harness-engineering"
description: "Design, build, verify, or maintain Muse's personalized operating setup — memory and instruction files, workspace layout, skills, automations, and connectors — from a vague brief or an existing setup. Use when the user asks for an operating system for their AI, a setup overhaul or guided setup, instruction-file or memory work, workspace architecture, capability cleanup, or a scheduled review of the assistant's own configuration. Route focused requests to the phase that matches."
metadata: { "includeInPrompt": true }
---

# Harness Engineering

## Purpose
Turn a rough brief into Muse's smallest working operating harness: the persistent instruction files, workspace layout, skills, automations, and connectors that make everyday work consistent. Treat the user's existing files and live environment as implementation truth.

The default failure mode of an inherited setup is over-constraint, not absence. Read `references/context-doctrine.md` before writing or judging any persistent context, and prefer removing an instruction to adding one.

## Workflow
Phases run in order for end-to-end work: interview → audit → plan → approve → build → verify → hand off. Each phase's workflow lives in `references/phases.md`; resolve the details there, not here.

1. Vague or incomplete brief: run the interview phase. Do not build during it.
2. Existing setup or upgrade request: run the audit phase first — read-only, no changes.
3. Confirmed profile plus audit: run the plan phase; present approval groups and get explicit approval before touching files.
4. Instruction-file work only (SOUL.md, IDENTITY.md, USER.md, MEMORY.md, AGENTS.md, TOOLS.md, ~/docs): use the instruction-file phase.
5. Over-constrained or inherited context: run the context-doctor phase before rewriting anything.
6. Missing reusable skill: use the skill-engineering phase (follows the workspace skill-creator conventions).
7. Approved plan: run the build phase — dry-run, hash preconditions, backups, one approval group at a time.
8. Sustained approved build: run the runner phase with durable state, launch caps, and stop rules.
9. Completion claim: run the verify phase against fresh evidence from the installed environment.
10. Model update, recurring review, or drift: run the maintainer phase.

## Output Contract
- Interview → a confirmed, schema-versioned profile (`references/profile.schema.json`).
- Audit → findings grouped as verified facts, inferred risks, and user decisions. No changes.
- Plan → a decision-complete operations plan from `assets/harness-plan.template.json`: approval groups, expected hashes, rollback actions, resource budget.
- Build → per-group receipts: what changed, backup location, hash verification, rollback manifest.
- Verify → one compact completion receipt, one result per required check, plus `functional_result` and `qualitative_result` when human judgment is load-bearing.
- Maintain → drift classification and a reversible update plan.

## Operating Rules
- Investigate before asking factual questions: read the existing files and live state first.
- Audit and planning are read-only.
- Present the complete plan and approval groups before changing files. Approval for one group never approves another.
- Back up every existing file before an approved update; write atomically; keep a rollback manifest. Stop on hash drift.
- For build or change requests, execution against the target is the primary work. Audits, plans, and reports count as progress only when they enable or verify a requested change. Unresolved required work blocks completion.
- Verify with fresh evidence from the installed environment. A passing check never outweighs unresolved required work.
- Never install third-party code, trust hooks, authenticate accounts, send messages, or publish externally without separate approval. See `references/safety-and-approvals.md` for the never-implicit list.
- Record configuration keys and capability state in reports, never secret values.
