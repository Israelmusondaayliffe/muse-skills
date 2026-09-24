# Writing Agent Briefs

An agent brief is the authoritative, durable specification a delegated agent
(subagent, or a fresh session) works from. The original discussion is context;
the brief is the contract. It must stay useful for days or weeks as the
codebase changes.

## Principles

### Durability over precision

- **Do** describe interfaces, types, and behavioral contracts.
- **Do** name specific types, function signatures, or config shapes to look
  for or modify.
- **Don't** reference file paths or line numbers — they go stale.
- **Don't** assume the current implementation structure will remain.

### Behavioral, not procedural

Describe **what** the system should do, not how to implement it.

- **Good:** "The `SkillConfig` type should accept an optional `schedule`
  field of type `CronExpression`."
- **Bad:** "Open src/types/skill.ts and add a schedule field on line 42."

### Complete acceptance criteria

Every brief needs concrete, testable criteria, each independently verifiable.

- **Good:** "Running `gh issue list --label needs-triage` returns issues that
  have been through initial classification."
- **Bad:** "Triage should work correctly."

### Explicit scope boundaries

State what is out of scope to prevent gold-plating and adjacent-feature
assumptions.

## Template

```markdown
## Agent Brief

**Category:** bug / enhancement
**Summary:** one-line description of what needs to happen

**Current behavior:**
What happens now. For bugs: the broken behavior. For enhancements: the
status quo the feature builds on.

**Desired behavior:**
What should happen when the work is complete. Be specific about edge cases
and error conditions.

**Key interfaces:**
- `TypeName` : what needs to change and why
- `functionName()` return type : current vs expected
- Config shape : any new configuration options needed

**Acceptance criteria:**
- [ ] Specific, testable criterion 1
- [ ] Specific, testable criterion 2
- [ ] Specific, testable criterion 3

**Out of scope:**
- Thing that should NOT be changed or addressed
- Adjacent feature that might seem related but is separate
```

For work handed to a delegated agent that is *finishing existing work* rather
than building from nothing, the "Current behavior" section describes the
state of what's already there, and the brief asks for what's left to do:
finish it, close gaps, address review points.
