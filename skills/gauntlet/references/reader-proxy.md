# Reader-proxy test

The knowledge-work equivalent of running the code, and the highest-value mechanism in this plugin. Prose, research, strategy, decks, and prompt systems do not compile or render, so the loop simulates the one event that matters: a reader trying to use the artifact.

## The mechanism

Spawn a fresh subagent from `~/workspace/skills/gauntlet/agents/reader-proxy.md`. Give it the artifact and a target reader profile, nothing else: no builder history, no brief, no bar, no explanation of what the artifact is trying to do. Ask it to do the thing the artifact exists to enable.

Every guess, every unanswerable question, every wrong answer, and every instruction it could not follow is a gap. The reader-proxy is instructed not to be charitable, not to fill gaps from its own knowledge, and not to assume the author meant something reasonable. The guesses are the finding.

Mandatory for `prose`, `research`, `strategy`, `deck`, and `prompt-system` pieces. On any knowledge-work piece, `read` alone is never sufficient inspection; it must pair with `reader-proxy` or `claim-audit`, and `validate_pieces.py` rejects pieces that break that rule.

## Artifact-to-task table

| Artifact | Reader-proxy task |
|---|---|
| Spec | Build the first component from it. Report every place you had to guess |
| Research brief | Answer the questions the brief was commissioned to answer |
| Decision memo | State the decision, the strongest counter-argument, and what would change it |
| Skill or system prompt | Execute it on three test inputs |
| Deck | State the ask, the evidence, the next step, and what would make you say no |
| Editorial | Say what it argues and why a reader continues past line three |

## Frozen question sets

Each piece's reader-proxy question set is declared at brief time in `pieces.json` and frozen with the plan hash. It cannot be softened once the answers start coming back wrong: swapping a question the artifact keeps failing for one it can pass is the same failure mode as editing a rubric mid-run, and the hash mismatch surfaces at verification as an integrity failure.

If the questions turn out to be genuinely wrong (not merely hard), that is a re-plan event at a wave boundary, recorded in `CONTEXT.md` with a date and a reason, never a quiet edit.

## Outputs become inspection evidence

The reader-proxy's report is written to `rounds/<piece>/<n>/inspection/` alongside any other declared inspection output. That file, not the artifact's own claims about itself and not the builder's summary, is what the critic and later the verifiers judge:

- The critic receives the neutral, blind-paired inspection outputs (ours and the reference's) and compares what the reader-proxy could actually do with each. An unanswered question in ours against an answered one in the reference is exactly the kind of gap it names.
- A reader-proxy report that is missing or empty means the round failed at inspection: no critic is spawned, and the failure itself goes back to the builder. Never judge an un-inspected artifact.
- At verification, unanswered or wrongly answered questions block convergence claims: a piece whose reader-proxy could not answer its frozen questions has open gaps by definition, and those gaps survive into the evidence report verbatim.
