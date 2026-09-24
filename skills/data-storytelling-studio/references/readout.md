# Executive readout workflow

## Answer-first sequence

1. Decision question.
2. Answer in one bounded sentence.
3. Evidence that changes the decision.
4. What remains uncertain or contradictory.
5. Decision or recommendation.
6. Risks and mitigation conditions.
7. Next actions, owners, and timing when known.

## Evidence discipline

Each evidence item must include a stable identifier, a claim, a source reference, and a confidence state. Use `measured`, `inferred`, or `judgment` inside the claim text when the distinction matters.

## Publish gate

Publish only when the route is valid, material visuals pass or have documented revisions, every load-bearing claim has a source, and limitations are visible to the decision-maker. If any of these fails, set `publish_ready` to `false` and return the required repair instead of writing around the gap.
