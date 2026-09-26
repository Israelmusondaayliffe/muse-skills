# Context Doctrine

<!-- context-scan: catalogue -->

Inherited setups often carry stale or conflicting instructions. They can also lack the guidance, examples, and checks a task needs. Judge each line by observed performance on the tasks it serves, not by its length or age. User policy, authority boundaries, source precedence, and completion criteria stay load-bearing until a controlled subtraction test shows otherwise (`references/prompt-governance.md`).

## What tends to help, and when

1. Judgment over rule walls. Hard rules written for worst cases can conflict, and the model spends effort resolving the clash. Where rules conflict, describe the wanted shape and the condition that changes the choice.
2. Examples beside the task that needs them. A short worked example that shows the quality bar and a real judgment call often teaches more than a paragraph of rules. Keep examples task-owned, clearly labeled as illustrative, and varied enough that the model does not copy one surface form. Cut an example only when a comparison shows it narrows output or no longer matches the task.
3. Progressive disclosure. Load detail at the moment a task needs it, through a directly linked reference, instead of one central file of everything.
4. Single placement. State a rule once, in its closest owner. Tool guidance belongs in the tool description.
5. One memory owner. If the host has a memory system, instruction files should not duplicate it.
6. Rich specs where they exist. An artifact, test suite, rubric, or function can be the spec. Source content beats a description of it.

## Verification and checks

Keep checks that catch real failures. A task-specific check tied to evidence (render the file, run the test, compare the hash, read the output against the brief) is load-bearing and stays. Completion criteria and acceptance checks are user policy.

What to cut or rewrite is generic repetition: several "double-check everything" reminders stacked in one file, instructions to re-verify unchanged state, or a verification ritual that observed runs show adds cost with no caught failures. Replace those with one concrete check named against the task's evidence. When unsure, keep the check and test its removal.

## Other supplements

- Test subtractions, do not presume them. A legacy instruction is a removal candidate, not a removal. Remove one coherent group, compare against a frozen baseline, and restore it on regression. Report every subtraction, or the user adds it back.
- Ask for conclusions and evidence, not transcribed reasoning. Some models refuse or degrade when told to echo hidden reasoning. Put reasoning visibility in structured fields (decision, evidence, alternative considered).
- Calibrate rather than prescribe. Response length, narration cadence, document length, scope, and delegation each get one short positive statement of the wanted shape.
- Review on sight: enumerated behavior lists, anti-laziness language, forced interim summaries, aggressive subagent authorization, capitalized emphasis, tool-triggering pressure. Each is a candidate for rewrite or a removal test.
- Fix order when behavior is wrong: check inputs, effort, and infrastructure first; then remove a conflicting or stale line; then add one targeted line, check, or example; then restructure. Restructure last.

## What must not be cut

The argument is that instructions compensating for a weakness the current model no longer shows can go, after a test. It is not an argument that user policy, useful examples, or real checks should go. Keep, and where possible move down the reliability ladder into scripts:

- Voice, tone, and banned-pattern rules.
- Brand and visual constraints.
- Output path, naming, and versioning discipline.
- Fabrication bans covering numbers, metrics, sources, tool parameters, and skill behavior.
- Data routing rules, such as which connector owns which question.
- Authority boundaries and approval gates.
- Completion criteria and task-specific acceptance checks.
- Worked examples that observed runs show improve output.

An instruction encoding genuine user policy rather than model compensation stays, and the audit says so explicitly rather than deleting it silently.

## The audit test

For any line in any persistent file, in order:

1. Does it encode user policy, taste, an authority boundary, a completion criterion, or a real gotcha? Keep it, and consider a script.
2. Is it a task-specific check or example that observed runs show catches failures or raises quality? Keep it beside the task.
3. Does it conflict with another line, or describe a path, tool, or fact that is no longer true? Fix or cut it.
4. Is it a generic reminder that repeats a check already stated once? Collapse it to the one concrete check.
5. Does it ask for hidden reasoning to be echoed? Rewrite it as a structured evidence field.
6. Is it detail only some tasks need? Move it behind progressive disclosure.
7. Is it visible from the file system or obvious from the workspace? Cut it.
8. Does it exist only to compensate for an older model's weakness? Mark it a removal candidate and test the removal before cutting.

Report each cut with its evidence (conflict, stale fact, duplicate, or a subtraction test result). A cut without evidence is a proposal, not a finding.
