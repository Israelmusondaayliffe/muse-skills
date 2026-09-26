# Routing Examples

## Decision grill (inside an Outcome Engine run)

- "Run Outcome Engine on this workshop idea; start by settling whether it is live or recorded."
- "Take the onboarding redesign from fuzzy to a first verified slice; ask me the hard questions first."

## Outcome brief

- "Turn everything we agreed into a campaign brief."
- "Write the research spec from this conversation."
- "Capture the decisions and scope in a plan another agent can use."

## Action slices

- "Break this approved brief into independent work packages."
- "Give me tickets with blockers and proof for each one."
- "Sequence this rollout so several people can pick up unblocked work."

## Evidence-driven delivery

- "Work through S1 and prove it before moving on."
- "Build this one acceptance check at a time."
- "Keep iterating until the rendered document passes review."

## Bounded test

- "Prototype the riskiest assumption before we commit to the full build."
- "Run the cheapest test that would tell us whether this idea is viable."

## Intake triage

- "I have research, a half-settled brief, and some implementation notes. Tell me what phase this is in."

## System architecture

- "Why is this workflow so hard for agents to follow?"
- "Audit the structure of this knowledge base."
- "Find where ownership and information are scattered across this process."

## Full flow

- "Take this idea from fuzzy concept to verified execution."
- "Run the whole Outcome Engine on this launch."
- "Help me think this through, brief it, break it down, and complete the first slice."

## Durable handoff

- "Prepare this action slice so another task can continue without this conversation."
- "Write a self-contained handoff for the next agent inside the approved output folder."

## Near misses

- A direct request to edit one sentence should use a writing skill.
- A direct request to look up one fact should use research or web tools.
- A direct request to fix a known software bug should use diagnosis and implementation, not a full decision grill.
- A request to send, publish, assign, purchase, or delete needs explicit authorization at that action boundary.
- A standalone "grill me", "challenge this hiring plan before I commit", or "pressure-test this decision" with no execution goal belongs to `strategy-room`. A request that names Matt belongs to `matt-partok-bundled-plugin-for-knowledge-work`.
- A request for a durable fresh-task handoff uses `continuity-vault` when that optional skill is installed. When it is absent, Outcome Engine writes a self-contained handoff inside the user-approved output root and does not rely on conversation history.
