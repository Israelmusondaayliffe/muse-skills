# To Action Slices

Turn a destination into small results that can be completed, checked, and handed off independently.

## Core rule

Slice by observable outcome, not by internal layer. A slice should cross every part needed to produce one narrow, usable result. A completed slice must be demonstrable or verifiable on its own.

Examples:

- Research: source one claim, assess it, and add the cited finding to the report.
- Writing: complete one reader action path from section purpose through review.
- Campaign: produce one approved message for one audience and one channel.
- Operations: run one real request through intake, decision, execution, and confirmation.
- Software: deliver one behavior through storage, logic, interface, and test.

## Workflow

1. Read the approved brief or source plan in full.
2. Identify the first thin path that exposes important unknowns early.
3. Draft slices in dependency order. Give each slice a unique ID.
4. For each slice, state its outcome, proof surface, acceptance checks, blockers, and boundaries.
5. Size each slice so a fresh context can understand, execute, and prove it from the brief plus the slice alone. If it cannot, split it or prepare the durable handoff (see the skill's handoff template).
6. Add enabling work only when it is required for a complete slice. Prefer small preparation inside the slice that needs it.
7. Present the proposed breakdown for a granularity and dependency check before assigning work to other people or creating external tickets. When the user already asked you to slice and execute locally, show the breakdown in the same reply and continue.
8. Use `assets/action-slices-template.json` for a machine-checkable local plan.
9. Validate a local plan from this skill's directory:

```bash
python3 scripts/validate_action_slices.py PATH
```

10. Fix every validation failure before handoff. The validator checks required fields, unique IDs, unknown blocker references, and dependency cycles.

## Durable slice handoff

If the optional `continuity-vault` skill is installed, it can own a durable cross-task or delegated-slice handoff. Otherwise write a self-contained handoff artifact using `assets/handoff-template.md` inside the user-approved output root. Include the outcome, source artifact paths, settled decisions, open questions, scope boundaries, slice ID and acceptance checks, blockers and dependencies, proof and verification state, and exact next action. Do not rely on conversation history. If the user has not approved an output root, ask for one before writing the handoff.

## Wide-change exception

When one broad mechanical change cannot remain valid in small outcome slices, use three stages:

1. Expand: add the new form beside the old form.
2. Migrate: move bounded groups while both forms remain supported.
3. Contract: remove the old form only after every migration is proven.

Use an integration slice when no migration group can be verified alone. State clearly where the final proof occurs.

## Authorization boundary

Creating local plan files is allowed when the task authorizes file output. Publishing issues, assigning people, changing tracker state, or sending messages requires separate user authorization.
