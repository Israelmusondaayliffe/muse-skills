---
name: "knowledge-work-superpowers"
description: "Run substantial non-coding knowledge work end to end: framing, planning, systematic research, evidence-first analysis, sourced drafting, staged execution, parallel research strands, review, feedback handling, fresh verification, and delivery handoff. Use for research reports, memos, comparisons, recommendations, and decision briefs — anything multi-source, high-stakes, or expected to guide a decision. Skip for simple lookups or one-step answers."
metadata: { "includeInPrompt": true }
---

# Knowledge Work Superpowers

## Purpose

Route substantial knowledge work (research, analysis, planning, drafting, review, verification, handoff) through the smallest set of phases that protects quality. Full phase procedures live in `references/phases.md`; templates in `assets/`; the bundle checker in `bin/verify_research_bundle.py`.

## Trigger And First Decision

Use this skill when one or more apply:

- The work has several steps or sources.
- The output will guide a decision.
- The user wants deep research, an evidence-backed result, or a reusable artifact.
- Current or disputed facts matter.
- Errors would be costly or embarrassing.
- The task will produce a report, memo, brief, comparison, recommendation, or research package.

Use a fast path (one direct lookup or transformation, cited inline) when the task is a single lookup, a simple transformation, or a low-stakes answer that does not need an evidence trail. This skill is not a substitute for domain-specific legal, medical, financial, or compliance review.

## Phase Router

Read the full procedure for a phase in `references/phases.md` before executing it:

1. Unclear outcome, audience, scope, or success criteria → **Framing** (work brief)
2. Approved brief or clear multi-step requirements → **Planning** (executable plan)
3. Deep, current, disputed, or multi-source research → **Systematic research** (source ledger)
4. Important claims or recommendations need support → **Evidence-first analysis** (claim ledger)
5. A sourced draft must be written → **Drafting from evidence**
6. A written plan must be carried out → **Executing plans** (staged, checked)
7. Two or more independent research strands, and subagents are permitted → **Parallel research**
8. A draft or deliverable needs quality review → **Reviewing knowledge work**
9. Feedback has arrived → **Receiving work review**
10. About to call the work complete → **Verification before delivery** (fresh checks)
11. Verified work needs packaging → **Finishing a deliverable** (delivery note)

Default sequence for a new substantial task: frame → plan → research and build the evidence record → analyze claims → draft from evidence → review → verify with fresh checks → finish and hand off. Skip a phase only when its output already exists or the task does not need it; state the reason briefly.

## Host Capabilities Mapping

Translate "source of truth" and verification steps into what this host can actually run:

- Internal facts (email, calendar, messages, device galleries): the matching connected skill (`~/workspace/skills/` or `/opt/hatch/skills/`); load its `SKILL.md` first.
- Working documents in `~/workspace/`: file tools (`muse.read`, `muse.write`, `muse.edit`).
- Public current facts: `browser.search` and `browser.open`; never treat training memory as current.
- Logged-in sites, forms, purchases, multi-step web interactions: delegate a browser task to an eligible parent/agent (subagents cannot do this themselves).
- Calculations and data: rerun with a deterministic tool (shell, `python3`) and check units, denominators, date ranges.
- Repetition and monitoring: `cron` for scheduled checks; `hooks` for event-driven ones.
- Parallel research strands: spawn subagents when permitted, with separate artifact paths so they never write the same ledger concurrently.

## Operating Rules

1. Do not present inference as sourced fact.
2. Do not cite a source that does not support the nearby claim.
3. Do not claim completion without fresh verification.
4. Do not expand scope silently.
5. Do not use subagents when user or platform instructions prohibit it.
6. Preserve progress in files (brief, plan, source ledger, claim ledger, review, delivery note), not chat history. After a resumed session, inspect those artifacts before repeating work.
7. When you need personal input (writing samples, business details, audience facts, credentials, permissions), ask the user. Do not invent user-specific data.
8. External actions (sending, publishing, sharing, moving, deleting) need separate authority. Without it, prepare the artifact and stop at handoff.

## Workflow Durability

Long work should survive interruption: keep the brief, plan, ledgers, progress record, and delivery note beside the deliverable or in the user-approved output location. For long research, also write `research-handoff.md` in the output root containing the complete source ledger, open questions and unresolved conflicts, research boundaries and stop condition, the next action, and the current verification state.

## Output Contract

A finished engagement produces, at minimum: the verified deliverable at its agreed location, the evidence package preserved (brief, plan, source and claim ledgers, review, verification results), known limitations recorded, and a delivery note summarizing what was delivered, what was verified, the limits, and one recommended next action.

## File-Based Verification

For a standard research bundle, run from this skill directory:

```bash
python3 bin/verify_research_bundle.py /path/to/bundle --profile research    # or: --profile deliverable
python3 bin/verify_research_bundle.py --self-test
```

Expected filenames and table schemas are documented by the templates in `assets/`. Chat-only tasks can run the same checks manually. This structural check does not replace opening sources and inspecting claim support.
