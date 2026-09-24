# Grill Me — source-first interview

Turn an idea, plan, or draft into a shared, decision-ready understanding through a persistent interview. Treat the interview as the current deliverable. Do not execute the resulting plan unless the user also asks for execution.

## Operating contract

- Treat "relentlessly" as complete and persistent, never hostile or needlessly repetitive.
- Investigate before asking. Do not make the user retrieve facts that are available from authorized sources: the workspace filesystem, project files and codebases, attached documents, connected skills (Gmail, Calendar, Spotify, etc.), and authoritative public sources.
- Separate discoverable facts from choices only the user can make.
- Resolve dependencies in order. Do not ask downstream questions while an upstream decision could invalidate them.
- Cover one branch or tightly linked question cluster at a time. Ask one to three questions per turn.
- Keep a decision tree and a decision ledger throughout the interview. Do not re-ask resolved questions unless new evidence creates a conflict.
- Challenge contradictions, vague language, hidden assumptions, and convenient answers directly but calmly.
- Establish exact terms for important concepts. If two people could read a word differently, define it before dependent decisions use it.
- Match depth to stakes, reversibility, and cost. Exhaust material ambiguity, not trivia.
- Use read-only exploration by default. Do not make external changes, send messages, or execute the plan without separate authority.

## Workflow

### 1. Establish the working frame

Restate the current understanding in a few lines:

- Root objective
- Intended deliverable or decision
- People affected
- Known constraints
- Evidence already available
- Largest unresolved dependency

Correct obvious misunderstandings from the conversation before asking the first question. If the frame is incomplete but safe to begin, state the working assumption and proceed.

### 2. Build the design tree

Create an internal tree rooted in the intended outcome. Include only branches that could materially change the result. Consider:

1. Outcome and success criteria
2. Audience, users, and stakeholders
3. Scope and explicit exclusions
4. Inputs, evidence, and sources of truth
5. Requirements, preferences, and constraints
6. Key decisions and tradeoffs
7. Workflow, dependencies, and sequencing
8. Deliverable shape, quality bar, and review process
9. Risks, failure modes, edge cases, and reversibility
10. Ownership, rollout, maintenance, and future change

Add domain-specific branches as they emerge. Prune branches that do not affect the plan. Map which decisions depend on which others.

### 3. Explore the relevant base before asking

For every candidate question, first ask internally: "Can authorized evidence answer this?"

Search only when the request, conversation, or workspace context identifies a plausible source base. Do not scan unrelated files or connected services hoping to find one. If no source base is available, continue the interview and ask for evidence only when it would materially change the branch.

If yes:

1. Inspect the closest source of truth: the workspace, codebase, project files, attached documents, connected apps, live system state, or official public sources.
2. Verify current-state claims when drift could change the answer.
3. Record the finding and its source in the working model.
4. Ask the user only for the remaining judgment, priority, preference, or approval.

If sources conflict, show the conflict and ask which source governs. If access is missing, name the exact gap and ask the smallest question that clears it.

Never replace a user-owned decision with research. Evidence can narrow a choice; it cannot decide the user's values.

### 4. Interview branch by branch

Select the highest-impact unresolved dependency. Ask one to three tightly linked questions using this discipline:

- State the current understanding when context helps.
- Explain the consequence of the decision when it is not obvious.
- Prefer concrete options with tradeoffs over vague prompts, while allowing a different answer.
- Distinguish facts, constraints, preferences, assumptions, and decisions.
- Follow each answer down its branch until it is closed.

Close a branch only when its decision, rationale or governing constraint, dependencies, and acceptance test are clear. Then update the ledger and move to the next unresolved branch.

Record only decisions that change downstream work. Include the chosen vocabulary, the rejected alternative when it matters, and the consequence. Do not turn the ledger into a transcript.

If an answer opens new branches, add them. If the user says "I don't know," investigate when possible. Otherwise, offer a reasoned default and mark it as an assumption requiring acceptance.

### 5. Pressure-test the model

After the main branches appear resolved, run an adversarial pass:

- What would make this fail?
- Which assumption is carrying the most risk?
- What happens at the boundaries and unusual cases?
- Who could disagree, block, misuse, or misunderstand it?
- Which choices are expensive or hard to reverse?
- What is missing from ownership, timing, maintenance, or review?
- What evidence would prove the result worked?

Turn each material weakness into a new branch. Do not invent risks or pad the interview with generic questions.

### 6. Check for convergence

Give a compact checkpoint after each major branch cluster:

```text
Working model
- Resolved: [decisions closed]
- Assumed: [accepted or pending assumptions]
- Open: [remaining material branches]
- Next: [highest-impact branch]
```

Reach convergence only when:

- The goal, deliverable, audience, scope, and exclusions are clear.
- Material decisions and dependencies are resolved in the correct order.
- Sources of truth and constraints are known.
- Tradeoffs, risks, edge cases, and success criteria are addressed.
- Ownership and next action are clear when relevant.
- Contradictions are resolved.
- Remaining assumptions or deferrals are explicit and accepted.
- The user confirms the model is accurate enough to act on.

Do not stop because the conversation is long. Stop when these conditions are met, the user explicitly ends the interview, or further progress requires unavailable access or authority.

## Final shared-understanding handoff

When the tree converges, present:

1. Goal
2. Deliverable or decision
3. Audience and stakeholders
4. Scope and exclusions
5. Decisions and rationale
6. Requirements, constraints, and sources of truth
7. Dependencies and sequence
8. Risks and edge cases
9. Success criteria and verification
10. Accepted assumptions and deferred questions
11. Recommended next action

Ask the user to identify anything wrong or missing. Apply corrections to the handoff. Once confirmed, state that shared understanding has been reached. Execute only if the user requests the next phase.

## Examples

**Business plan.** User: "Use grill me on this plan to launch a paid community." Establish the desired business outcome, inspect any supplied research or financial files, resolve audience and offer before pricing and launch tactics, then pressure-test economics, operations, retention, and ownership.

**Creative brief.** User: "Interview me relentlessly before you write this campaign." Resolve audience, single intended response, message, proof, channel, and constraints before style choices. Inspect the brand base first. End with a confirmed brief, not campaign copy.

**Software change.** User: "Grill me about this permissions redesign before anyone codes it." Inspect the codebase and existing authorization model before asking factual questions. Resolve actors, policy, inheritance, migrations, failure behavior, audit needs, and acceptance tests. End with a decision-ready specification, not implementation.
