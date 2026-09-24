# Verification independence

Why the verifiers must be strangers to the build, what actually enforces that, and what to say when the platform cannot fully provide it.

## Why independence matters

Two invariants depend on it directly.

**INV-2, the builder never grades itself.** A verifier that has seen the builder's reasoning inherits the builder's framing: it knows what was attempted, what was hard, and what the builder believes is fine. That knowledge converts judgment into confirmation. The entire value of verification is that the verifier meets the artifact the way a stranger would, with only the goal, the criteria, the bar, the artifact, and the inspection output. If the verifier is downstream of the builder's context, the run has verified the builder's story, not the work.

**INV-4, quality and integrity are judged separately.** A beautiful document that invents a statistic passes a quality critic and fails the work. Quality and integrity verifiers carry different mandates and must not share context with each other either: an integrity verifier that has read a glowing quality verdict is primed to skim, and a quality verifier that has read an integrity pass treats honesty as settled and stops looking. Separate spawns, separate inputs, separate verdicts, and consensus computed afterward by script.

The same logic bans verifier-to-verifier contact within a type. Three quality verifiers who share context are one verifier with three signatures. The vote counts in `consensus.json` are only meaningful if each vote was formed alone.

## What the spawning layer enforces versus what is instructional

Enforcement is structural plus instructional, and the two must not be confused.

**Structural, enforced by the spawning layer and validated by script:**

- Each verifier is spawned as its own clean-context subagent. It has no conversational history, so builder reasoning, critic verdicts, and other verifiers' results are absent by construction, not by request.
- The input list is assembled by the lead before spawning: goal from `CONTEXT.md`, success criteria from `PLAN.md`, the bar, the acceptance criterion, the artifact, the inspection output. What is not passed does not exist for the verifier.
- No path into `.gauntlet/sealed/` appears anywhere in a verifier's inputs. The blind map is unreachable, not merely off-limits.
- The round-loop analogue is validated by `round_record.py`, which rejects any critic verdict where `critic_saw_builder_context` is true or `critic_context_source` is anything other than `files-only`. Those fields are asserted by the spawning code, never self-reported.
- Consensus is computed only by `consensus.py`. A model cannot rescue a failed integrity vote by arguing with the table.

**Instructional, real but weaker:**

- The agent instruction sets (`agents/quality-verifier.md`, `agents/integrity-verifier.md`) tell the verifier not to seek forbidden inputs and to stop and name any forbidden input that appears in context anyway.
- The critic instruction not to try to discover which artifact is ours is an instruction, not a wall.

When designing or repairing a run, prefer moving a guarantee from the instructional column to the structural column. Asking agents nicely is the fallback, not the mechanism.

## Honest limits

Blind enforcement is strong, not airtight. A determined agent could infer provenance from residual signals: writing tics that match the goal statement, file contents that reference project-specific names, formatting conventions, timestamps or ordering artifacts that survive the metadata strip, or simple familiarity between the candidate and the stated goal. `blind_pair.py` copies both artifacts to neutral paths with neutral filenames, strips metadata, and seals the map outside anything the judge receives, and that removes the cheap channels. It cannot remove every channel. State this plainly in any report or discussion of the method rather than overclaiming. The claim the plugin makes is "no path to the map exists in the judge's inputs and the cheap provenance signals are removed", not "the judge cannot possibly know".

## Degraded-mode isolation semantics

When the surface precheck cannot confirm clean-context subagent spawning, the run may proceed only in the documented degraded mode:

- Each verifier (and each judge generally) runs as a separate task invocation seeded only from files on disk, with no shared conversational context.
- This is weaker than a clean context window. Separate invocations on some surfaces may share caches, tool state, or ambient session context that a true clean spawn would not, and the spawning layer cannot assert `files-only` provenance with the same force.
- `run.json` records `"context_isolation": "degraded"`.
- Every handoff document and every evidence report from a degraded run carries a banner naming the degradation. The banner is mandatory, appears in section 1 of `EVIDENCE.md` and at the top of `HANDOFF.md`, and is never removed because the results look good.
- Never claim isolation the platform did not provide. If even file-seeded separate invocations are unavailable, verification cannot run: the outcome is `cannot-verify`, not a narrated stand-in verifier.
