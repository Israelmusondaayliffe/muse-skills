# To Outcome Brief

Convert known context into a durable brief that another person or agent can execute without reopening settled decisions.

## Use and limits

Use this after the main questions have been resolved. If material choices are still open, route to `references/decision-grill.md` first unless the user explicitly asks for a draft with named unknowns.

Do not publish, submit, email, or create tracker items without separate authorization. The default output is a Markdown brief in chat or at a user-approved file path.

## Workflow

1. Read the current conversation and the closest source of truth.
2. Choose the brief type that matches the work. Keep the common Outcome Brief sections even when the title changes.
3. Separate facts, decisions, assumptions, risks, unresolved questions, and blockers. Never bury a blocker inside prose or silently convert it into an assumption.
4. State the outcome from the audience or user's point of view.
5. Name observable success evidence. Avoid vague goals such as "better" unless a concrete check defines them.
6. Record constraints, requirements, decisions, risks, scope limits, and the next action.
7. Use `assets/outcome-brief-template.md`. Remove all instructional placeholders from the finished brief.
8. For a local Markdown file, run from this skill's directory:

```bash
python3 scripts/validate_outcome_brief.py PATH
```

9. If validation fails, fix the brief and rerun it. Do not hand off an invalid brief.

## Source handling

- Inspect files, memory, or current public sources when the fact is discoverable.
- Cite source-dependent claims when the brief will be used for research, policy, finance, legal work, medicine, or other high-stakes decisions.
- Mark unverified claims as assumptions.
- Preserve the project's own terms when a glossary or reference set exists.

## Completion contract

A complete brief has a clear outcome, named user or audience, proof of success, explicit constraints, settled decisions, visible blockers, scope limits, and one next action. It does not hide material unknowns, invent a choice for an unresolved dependency, or imply authorization for external actions.
