# Harness Phases

Phases run in order for end-to-end work: interview → audit → plan → approve → build → verify → hand off. Focused requests enter at their phase.

## Interview
The confirmed profile is the deliverable. Do not build during this phase.

1. Follow `references/interview-tree.md` one branch at a time. Ask one to three linked questions; offer a recommended default and its main tradeoff when evidence supports one.
2. Inspect existing files and capability state before asking discoverable facts. Define key terms before dependent choices use them.
3. Record each answer as a fact, constraint, preference, assumption, or decision; keep only records that change the profile.
4. Pressure-test authority, failure modes, maintenance, portability, and proof.
5. Convergence check: every material branch is resolved, explicitly excluded, or deferred with an owner or revisit trigger. Present the complete working model and ask for corrections.
6. Save a schema-versioned profile (`references/profile.schema.json`) only after confirmation.

Profile requirements: user context, harness scope, workspace choice, goal pattern, data sources, capability needs, authority boundaries, verification expectations, maintenance ownership, exclusions, accepted assumptions, deferred decisions.

## Audit
Read current state before proposing changes. Read-only: no changes of any kind. Do not record secret values.

1. Inventory the surfaces the request touches: instruction files (`~/SOUL.md`, `~/IDENTITY.md`, `~/USER.md`, `~/MEMORY.md`, `~/AGENTS.md`, `~/TOOLS.md`, `~/docs/`), workspace layout and skills, memory notes, goals, cron jobs, hooks, feed prompt, ideas.
2. Run any deterministic check the harness already owns first; its failures enter findings as verified facts with the script output as evidence.
3. Check for conflicts, placeholders, stale paths, duplicated ownership, missing validators, untrusted hooks, unsupported settings, and absent evidence.
4. Run the over-constraint pass: `python3 scripts/context_scan.py <files>` and read `references/context-doctrine.md`. Reasoning-echo hits rank first (they cause refusals); verification instructions second.
5. Classify findings across information, execution, and feedback layers; separate verified facts, inferred risks, and user decisions.
6. Promote repeat finding classes into a deterministic check script instead of longer prose: if the harness lacks one, creating it is the first proposed fix.
7. Stop when the next safe target action is known. An audit is support work — it does not count as implementation progress.

## Plan
Plan the outcome, scopes, operations, approvals, evidence, and rollback. Leave no implementation decision unresolved. Requires a confirmed profile and current audit, or a recorded reason why one is not applicable.

1. Name the primary outcome metric, the before state, the target state, and the unresolved required-work count.
2. Set caps: expected primary outputs, a support-artifact cap, a total launch cap, and a one-low-yield-wave stop (one wave with no target-state delta ends the run for re-planning).
3. Design the information, execution, and feedback layers per `references/harness-architecture.md`.
4. Put each requirement in the narrowest durable scope.
5. Plan removals before additions. Instructions the audit marked as model compensation go in their own approval group, each with a stated reason.
6. Reuse installed capabilities before proposing a new skill.
7. Define separate approval groups per `references/safety-and-approvals.md`. Generate file previews, operations, expected hashes, the smallest proportional checks, failure stops, and rollback actions.
8. When the outcome depends on visual, editorial, or strategic human judgment, name the task-owned qualitative acceptance artifact: owner, evidence surface, threshold, failure stop — separate from functional proof.
9. Present the human plan and machine operations together. Start from `assets/harness-plan.template.json`. Do not begin implementation until the user accepts the plan or explicitly requests end-to-end execution.

## Build
Apply only the approved operation groups. Do not reinterpret the plan during execution.

Start gate: re-read current hashes and stop on drift; run a dry-run pass and review the receipt; confirm approved groups and allowed roots.

- Apply one approval group at a time. Run `tar -czf BACKUP-<group>-<date>.tgz <files>` before any update, write files atomically (write temp, rename), and record pre/post sha256 in the receipt.
- Preserve unrelated files. If reality invalidates the plan, log the deviation and return to planning.
- After every change that affects persistent context, re-run the behavior checks from the plan — not only after memory or instruction-file edits.
- Rollback: restore from the backup tarballs in reverse apply order and verify hashes before reporting recovery.

## Runner
Use for an explicitly requested sustained build. Ordinary approved builds stay in the current conversation with one compact run ledger; durable state (a ledger file under the run directory) only when the run must cross sessions or resume.

1. Require the approved profile, plan, allowed roots, caps, and stop rules. Confirm the outcome metric, before/target states, and unresolved count.
2. Observe fresh state, choose one bounded target action, apply only an approved operation group.
3. Record progress only when the requested target state changes. Tests, receipts, and reports are support work.
4. Stop and re-plan after one wave with no unresolved-work reduction, or when support artifacts outgrow primary outputs.
5. Terminal states only: waiting input, blocked, exhausted, failed, cancelled, or completed. Do not rename a failure as success.
6. Send the integrated completion candidate to the verify phase once.
7. The run never grants broader filesystem, authentication, publication, or external-action authority.

## Verify
Verify without repairing during the verification pass. Verification is required by risk, not universally: verify changed or task-relevant surfaces, do not re-prove unchanged state.

1. Read the profile and plan; do not rely on the builder's summary.
2. Inspect current files, hashes, and backup evidence. Confirm the target-state delta and unresolved required-work count first — a passing check cannot override unresolved required work.
3. When judgment is load-bearing, inspect the task-owned qualitative acceptance artifact and report `functional_result` and `qualitative_result` separately.
4. Run the smallest safe deterministic check set approved for the changed surfaces (markdown parses, frontmatter valid, cron jobs listed, skills discoverable).
5. Evaluate each judgment criterion with file, line, command, or live-surface evidence.
6. Emit one compact receipt with one result per required check. A required missing, skipped, stale, stubbed, or renamed check fails verification. See `references/verification-standard.md`.

## Maintain
Treat maintenance as a new audit and plan. Do not assume the previous state is current.

Cadence:
- Weekly: review outputs, run stops, automation and scheduled-task results, failed checks, repeated corrections.
- Monthly: review instruction files, memory staleness, skill use, automations, output hygiene.
- Quarterly or after a major model or platform change: re-verify platform behavior against `references/platform-notes.md`, model-specific prompt blocks, connectors, discovery, and security boundaries.

Workflow:
1. Run the harness's deterministic checks first; failures are the first work items. Then audit against fresh state.
2. Compare current behavior with the last verified receipt. Classify drift as user change, product change, broken dependency, stale policy, or missing enforcement.
3. Remove dead weight before adding new instructions. After a model generation change, run `context-doctor` across the whole chain and treat instructions written for the previous generation as removable until a regression proves otherwise.
4. Promote any correction seen twice into the deterministic check script when it is deterministically checkable.
5. Produce a reversible update plan and approval groups; run the standard build and verification phases.
6. Follow `references/model-change-policy.md` after every major model change.

## Instruction-file engineering
Keep instruction files short, accurate, durable, and scoped. Most of the value is in what comes out: cut anything visible from the file system or already true of the model's default behavior. Distinguish model compensation (removable) from user policy and taste (kept).

1. Inspect the applicable chain: `~/SOUL.md` and `~/IDENTITY.md` (persona), `~/USER.md` (the person), `~/MEMORY.md` plus `~/memory/` notes (curated memory), `~/AGENTS.md` (workspace conventions), `~/docs/`.
2. Run the context-doctor phase over the chain and remove what it finds before adding anything new.
3. Move detailed workflows into skills or references, and exact checks into scripts.
4. Separate global personal policy from workspace layout and goal-specific rules.
5. Preserve load-bearing rules and show a diff for updates. Name every removal and its reason; an unexplained cut gets reverted.
6. Verify closer files refine rather than silently contradict broader guidance.

## Context doctor
Read-only over-constraint audit. Produces findings and a proposed removal set; never edits the source.

1. Resolve the scope: one file, one skill directory, or the whole instruction chain. Name every file to be judged.
2. Run `python3 scripts/context_scan.py PATH [--json OUT.json]` for deterministic findings.
3. Apply `references/context-doctrine.md` to what the scanner cannot see: judgment calls, examples that could be interface design, upfront detail that could load on demand, content that only restates what the file system shows.
4. Keep model compensation (removable) separate from user policy, taste, gotchas, authority boundaries, and data routing (not removable).
5. Rank: reasoning-echo first, verification instructions second, everything else by token weight.
6. Report the removal set with a reason per line and the keep set with justification. Application belongs to instruction-file engineering (files) or skill-engineer (skills).

## Skill engineering
Create a skill only for a repeated, named failure or workflow. Reuse an existing capability when one already owns the task.

1. Define concrete trigger examples and the failure the skill prevents.
2. Search installed skills for an existing owner first.
3. Author to the workspace format: a directory with `SKILL.md`, frontmatter carrying `name` and a third-person `description` with specific trigger phrases, depth moved into linked `references/`. Author persistent context to `references/context-doctrine.md`.
4. Add deterministic scripts only when exact behavior warrants them; compile Python helpers before reporting success.
5. Validate: structural check (frontmatter, paths, links), plus realistic positive and near-miss trigger tests.
6. Do not create a broad everything-skill or load an entire library by default. Add the skill to the harness plan and discovery checks.
7. When upgrading an existing skill, run context-doctor first and treat its findings as the starting removal set.
