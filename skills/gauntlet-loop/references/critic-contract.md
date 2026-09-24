# Critic Contract

An authoritative critic:

1. starts as a new agent with no inherited conversation turns;
2. receives only the approved goal, applicable bar, artifact paths, constraints, evidence locations, and verdict schema;
3. inspects the real artifact;
4. separates factual failure from judgment differences;
5. identifies the largest meaningful remaining gap;
6. cites inspectable evidence and states uncertainty;
7. does not praise effort, accept builder narrative as evidence, or repair the artifact;
8. returns `bar_wins`, `artifact_wins`, `tie`, or `unable_to_evaluate`;
9. may inspect several integrated low-risk workstreams in one bounded pass, then ends after the verdict and is never reused as the next authoritative critic.

If the host cannot provide isolated context, return `unable_to_evaluate`.
