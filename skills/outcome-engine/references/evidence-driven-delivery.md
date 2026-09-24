# Evidence-Driven Delivery

Build from proof instead of confidence. Complete one bounded behavior or outcome per cycle.

## The loop

1. Check: define one observable acceptance check through the real user or audience interface.
2. Confirm unmet state: run the check or show that the required artifact or behavior is absent. A check that already passes does not prove the new work.
3. Change: make the smallest useful change that can satisfy this one check.
4. Verify: rerun the same check and read the full result.
5. Improve: simplify structure only after the check passes. Rerun it after every structural change.
6. Repeat with the next acceptance check.

## Rules

- Work one slice at a time. Do not create all checks first and all outputs second.
- Test observable results, not the internal steps used to produce them.
- Derive expected results from the brief, an approved example, or an independent source.
- Prefer real interfaces over mocks, summaries, prompts, or proxy metrics.
- Keep evidence fresh. Run the proving check in the same phase where completion is claimed.
- Stop when the proof fails for an unknown reason. Diagnose before adding more changes.
- Parallelize independent slices by delegating them to subagents. Keep dependent work in this context.

## Domain adaptation

The loop stays fixed while the proof surface changes. Choose proof that observes the real result through the interface its user or audience will rely on:

- Research: claim-to-source table, primary-source citation check, reproduction of a calculation or extraction, explicit separation of fact, inference, and unknown. Avoid using the number of sources as proof of truth.
- Writing and documents: the reader can find the decision or next action; required sections and fields are present; claims trace to approved sources; the rendered file opens and preserves its structure. Avoid treating grammar checks as proof the document does its job.
- Creative work: the artifact matches the approved brief and reference set; required subjects, composition, duration, or dimensions are present; inspect the delivered file itself. Avoid using prompt quality as proof of output quality.
- Operations and workflows: one real or safe test request completes from intake to confirmation; owners and handoffs are observable; failure recovery works in a controlled test. Avoid treating a written procedure as proof the process works.
- Data and spreadsheets: known examples produce known results; totals reconcile to an independent source; formulas are inspected and recalculated. Avoid calculating expected values with the same formula being tested.
- Communications: recipient, intent, facts, tone, and requested action are correct; the draft is reviewed before sending. Draft approval is proof of readiness, not authorization to send.
- Personal plans: calendar, budget, energy, travel, or dependency constraints are checked against the user's real schedule. Avoid plans that prove only that a checklist was created.
- Software and systems: automated behavior tests through a public interface run from the terminal; user-visible behavior is checked via the live-browser task; build, lint, schema, security, or deployment checks run where they match the risk. Avoid tests tied only to internal calls or mocks of owned code.

## Completion contract

Report the outcome, the exact proof run, its fresh result, and any untested risk. Do not claim that a whole plan is complete because one slice passed.
