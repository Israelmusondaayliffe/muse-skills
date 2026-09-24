# Verification Standard

Completion requires fresh evidence from the installed environment. Verification is required by risk, not universally: verify changed or task-relevant surfaces, and do not re-prove unchanged state. Progress is an observable target-state delta plus a falling unresolved-work count. A passing validator never outweighs required items still marked needs-review, deferred, or otherwise unfinished; unresolved required work blocks completion.

When the requested outcome depends on visual, editorial, strategic, experiential, or other human judgment, the task owner must supply a named qualitative acceptance artifact with an owner, threshold, and evidence surface. Report `functional_result` and `qualitative_result` separately. Structural proof cannot substitute for a missing, failed, blocked, stale, or below-threshold qualitative result.

## Structural checks
- Required files exist at the approved paths.
- JSON, YAML, and Markdown parse or validate where a validator exists.
- Skill frontmatter carries `name` and a third-person `description` with trigger phrases.
- The instruction chain resolves in the intended order (persona → user → memory → workspace conventions).
- Generated files contain no secrets or user-specific sample data.
- Support artifacts stay within the approved cap.

## Behavioral checks
- A new request routes to the intended skill or front door.
- Changed automations are listed by the scheduler with the intended schedule and instructions.
- Required items have terminal states. Deferred, audit-only, and backfill-only remain incomplete unless approved as final.
- Command policy allows safe examples and blocks forbidden examples.
- A required task-owned qualitative result has current evidence and meets its declared threshold.

## Completion receipt
List every required check once in one compact receipt. Include the command or inspection, fresh result, evidence path, and pass or fail status. A required missing or stale check is a failure, not a clean no-op. Do not create checks for unchanged surfaces.

Evidence is risk-tiered. Summarize ordinary low-risk commands inline: command, exit code, one-line result. Reserve separate evidence files for destructive, security, installation, or similarly high-risk operations. Do not require repeated unchanged-state proofs or duplicated receipts.

The completion receipt must keep `functional_result` and `qualitative_result` as separate fields when judgment is load-bearing.
