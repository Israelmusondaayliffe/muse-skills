# Decision Grill

Resolve the decision tree before turning the idea into a plan or artifact.

## Operating rules

- Ask one question at a time.
- Ask about the highest-impact unresolved choice whose answer affects later choices.
- Give a recommended answer and one short reason before asking for the user's decision.
- Inspect available files, memory, connected sources, and the workspace before asking the user to restate discoverable facts.
- Push back when an answer conflicts with the goal, constraints, evidence, or an earlier decision.
- Define important domain terms before dependent choices use them. Preserve the user's established vocabulary when it is precise.
- Do not start implementation, publish anything, or create external state during the interview.

## Workflow

1. State the likely objective in one sentence.
2. Name the current source of truth and inspect it when available.
3. Map the first decision branches. Typical branches: audience, outcome, scope, proof, constraints, format, ownership, timing, risk, permissions.
4. Choose the next unresolved branch based on dependency, not convenience.
5. Ask one focused question. Offer the recommended answer and the main tradeoff.
6. Record the answer, its consequences, and any branch it resolves or creates. Keep only decisions that change downstream work; do not produce an interview transcript.
7. Every four to six decisions, give a compact state recap so drift is visible.
8. Test the emerging design against edge cases, conflicting constraints, failure modes, and the person who bears the cost when it fails.
9. Continue until the completion test passes.

## Completion test

Stop when all material branches are one of:

- resolved,
- discoverable from an identified source,
- explicitly out of scope,
- deliberately deferred with an owner or trigger for revisiting.

End with: objective, decisions made, evidence used, open risks, deferred questions, out-of-scope items, and a recommended next step. Recommend `references/to-outcome-brief.md` when shared understanding is ready to be written down.

## User control

The user can say `stop`, `summarize`, `skip this branch`, or `decide for me` at any time. When asked to decide, choose the safest option consistent with the stated outcome and label the choice as an assumption.
