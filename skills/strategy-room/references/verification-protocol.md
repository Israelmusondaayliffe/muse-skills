# Verification Protocol

How the verifier agent should triple-verify findings against the research dossier and the analysis plan. The pipeline's quality depends on this being done rigorously.

## The Three Checks

Every finding from the challenger gets three checks. A finding cannot survive if it fails the evidence or reasoning check. A finding can survive a counter-evidence concern by being revised to incorporate it.

### Check 1: Evidence Check

Locate the dossier evidence the finding cites. Read it. Ask:

**Does the evidence actually support the claim?**

A common failure mode is that evidence supports a weaker version of the claim than the finding states. Example:

- Dossier evidence: "73% of B2B SaaS companies use email newsletters as a primary marketing channel."
- Challenger finding (overstated): "Email newsletters are essential for B2B SaaS marketing success."
- Verified version: "Most B2B SaaS companies (73%) use email newsletters as a primary channel. The dossier evidence supports prevalence, not necessity for success."

Always reduce the finding to what the evidence actually supports.

**Is the evidence current enough?**

For fast-moving subjects, evidence older than 12 to 18 months is often stale. The dossier should have flagged stale sources, but the verifier should re-check, especially for findings about technology, regulation, or market dynamics.

**Is the evidence from a strong source?**

Cross-reference the source tier from the dossier. Findings with High confidence should rest on Tier A sources or multiple Tier B sources. Findings resting only on Tier C sources should be downgraded to Low or Speculative.

**Are multiple cited evidence items consistent?**

If a finding cites multiple evidence items, do they actually agree, or is the finding combining items that point in different directions? A finding that draws on three sources where two agree and one dissents should reflect that disagreement, not pretend consensus.

### Check 2: Reasoning Check

Trace the reasoning chain step by step. Ask:

**Does each step follow from the previous one?**

Mark every transition. "Therefore", "thus", "given that", "implies". Each transition should be defensible. A reasoning chain with smooth language but a buried logical leap is the most dangerous kind of finding because it sounds rigorous.

**Are there hidden inferential leaps?**

Common patterns:

- The leap from "X correlates with Y in the dossier evidence" to "X causes Y in the user's case"
- The leap from "Most cases of X have property Y" to "The user's case will have property Y"
- The leap from "Similar plans have failed" to "This plan will fail" (without checking whether the failure modes apply)
- The leap from "Expert A says X" to "X is true" (without weighing expert disagreement)

If a leap is found, either repair it by surfacing the missing inferential step (and verifying that step) or downgrade the finding.

**Does the reasoning rely on framing that smuggles in the conclusion?**

Watch for findings where the framing of the question already implies the answer. A finding that asks "What are the risks of X?" and then lists risks is not surprising. A finding that asks "Is X actually risky compared to alternatives?" and then argues for risk is doing real work.

**Could the same evidence support a different conclusion?**

This is the hardest check. Hold the evidence and ask whether a different reasoner could reach a different conclusion from it. If yes, the finding is at minimum less confident than the challenger drafted, and should probably acknowledge the alternative.

### Check 3: Counter-Evidence Check

Search the dossier for evidence that contradicts or complicates the finding. The challenger may have selectively used the dossier. The verifier reads it more completely.

**Does the dossier contain expert disagreement that complicates this finding?**

If the dossier maps expert disagreement (per the research protocol), check whether the finding sits on one side of a disagreement without acknowledging the other. If so, revise to incorporate both sides or split the finding into two parallel considerations.

**Does the dossier contain temporal evidence that the challenger missed?**

A regulatory change in the last six months, a recent product launch, a recent failure pattern. Findings can become wrong fast in fast-moving subjects.

**Does the dossier contain a competing explanation?**

The challenger may have proposed cause X for observation Y, but the dossier may also support cause Z for the same observation. Surface the alternative.

If counter-evidence exists and is strong, the finding should be revised. If counter-evidence is weak, it can be noted as a complicating factor without overturning the finding.

## Confidence Calibration

After the three checks, set verified confidence using these criteria:

### Verified High

- Evidence is from Tier A or multiple Tier B sources
- Evidence directly supports the claim (not just a weaker version)
- Reasoning chain has no inferential leaps
- No significant counter-evidence in the dossier
- A domain expert reading the finding would likely agree

### Verified Medium

- Evidence is from Tier B sources or a single Tier A source
- Evidence supports the claim with caveats
- Reasoning chain has minor gaps that have been surfaced
- Some counter-evidence exists but does not overturn the finding
- A domain expert would consider the finding plausible but might push back

### Verified Low

- Evidence is from Tier C sources or weak Tier B
- Evidence supports the general direction of the claim but not the specifics
- Reasoning chain has notable gaps
- The finding is worth surfacing as a hypothesis to test

### Speculative

- No direct dossier evidence
- Pure reasoning from principles or analogy
- Useful as a what-if for the user to consider
- Should be flagged in the synthesizer's report as the analyst's hypothesis, not a researched finding

### Removed

- Failed the evidence or reasoning check badly enough that surfacing it would mislead
- Counter-evidence overturns the finding entirely
- The finding is generic and could have been written for any input in the domain

## Calibration Drift Detection

Track the difference between the challenger's draft confidence and your verified confidence. Patterns:

- **If most findings get downgraded**: The challenger may be inflating confidence. Note this in the verifier notes. The orchestrator might want to re-prompt the challenger with stricter calibration guidance.
- **If most findings stay the same**: Either the challenger is well-calibrated or the verifier is rubber-stamping. Spot-check by trying to invalidate three random findings. If you cannot, calibration is fine.
- **If most findings get upgraded**: Rare. Could indicate the challenger is being too conservative, or the verifier is being too generous. Spot-check.

## Bias Detection in the Challenge

The challenger can be biased too. Common patterns:

### Confirmation Bias

The challenger gravitates toward findings the dossier most easily supports, even when those are not the most important findings. Counter: ask which dimensions in the user's input received the least challenge attention. Those may be where the most important findings hide.

### Availability Bias

Vivid, specific examples in the dossier produce more challenge findings than dry, structural patterns, even when the structural patterns matter more. Counter: weight findings by impact and probability, not by how interesting they are to write.

### Survivorship Bias in Evidence

If the dossier's case studies skew toward successes, findings will skew optimistic. If toward failures, pessimistic. Counter: check whether the dossier's case study set is balanced. If not, flag the bias in the verified findings.

### Generic Critique Patterns

The challenger may produce findings that pattern-match across all subjects ("regulatory risk", "competition", "execution risk") rather than findings specific to this subject. Counter: ask of each finding "could this have been written without the dossier?" If yes, the finding is generic and should be either specified or removed.

## Cross-Lens Verification

The challenger's cross-lens convergent findings, where the same root issue surfaces in multiple lenses, have the broadest effect on the report. Verify them with extra rigor:

- Do they really converge, or did the challenger force-match findings that aren't actually about the same root issue?
- Do they survive the three checks under each lens they appear in?
- Is the convergence strong enough to justify surfacing it as a single high-priority item?

A convergent finding that survives extra rigor is gold. A convergent finding that doesn't is worse than a single-lens finding because its apparent multi-angle support inflates its claim.

## When the Whole Challenge is Wrong

Sometimes verification reveals that the challenger's direction was misguided. The user's input is more well-grounded than the challenger assumed, and most challenge findings fail verification.

This is fine. Note it prominently. The synthesizer's report should lead with: "The plan is well-grounded. The few concerns are X, Y, Z." A report that manufactures concerns when the analysis didn't find them is dishonest.

## When Verification Itself Hits Limits

The verifier is not infallible. Some findings cannot be cleanly verified or refuted by the available dossier. Mark these Speculative with explicit reasoning. The user benefits from knowing what is open. Pretending false certainty in either direction is worse than acknowledging limits.
