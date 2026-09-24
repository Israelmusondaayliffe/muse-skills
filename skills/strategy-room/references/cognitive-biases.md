# Cognitive Biases

A taxonomy of biases the challenger and verifier should look for. Used by the challenger to identify biases in the user's input. Used by the verifier to identify biases in the challenger's own findings.

This is not an academic catalog. It's a working taxonomy organized by where the bias typically shows up in the inputs this skill handles (plans, prompts, strategies, ideas).

## Biases in How the User Frames the Problem

### Confirmation Bias

The user has framed the input around evidence that supports their preferred conclusion and excluded evidence against it.

**Detection patterns:**
- The input cites supporting examples but no failure cases
- The input draws on sources that are all from one viewpoint
- The input's framing presupposes the conclusion ("how do we ensure X works?" rather than "should we do X?")
- The input dismisses obvious counter-arguments in one sentence rather than engaging them

**Counter:** Note the biased framing. Ask what evidence would change the user's mind. If they cannot answer, the input is unfalsifiable as currently framed.

### Anchoring Bias

The user's input is anchored on a specific number, framework, or comparison that may not be appropriate.

**Detection patterns:**
- A specific number (price, timeline, target metric) that is not justified by the dossier
- A framework imported from a different domain that may not apply
- A comparison to one company or case that drives most of the strategy

**Counter:** Test the anchor. The dossier should reveal whether the number, framework, or comparison is reasonable for this context. If the anchor is arbitrary, surface that and suggest re-anchoring.

### Survivorship Bias

The user is reasoning from cases that survived without accounting for cases that did not.

**Detection patterns:**
- The input cites successful precedents without cited failures
- The strategy mimics famous successes ("we'll do what [X company] did")
- Selection logic (who gets hired, what gets shipped, what gets covered) is not factored in

**Counter:** The dossier should include failure cases. If it doesn't, return to the researcher. Findings that incorporate the survivor base rate are more honest than findings that only count winners.

### Availability Heuristic

The user has weighted recent or vivid information disproportionately.

**Detection patterns:**
- The input is heavily shaped by a recent industry event
- The input prioritizes a risk that is rare but emotionally salient (competitor entry, single bad customer experience)
- The input ignores high-frequency, low-vividness factors (e.g., compounding small operational issues)

**Counter:** The dossier should provide base rates. Reweight the user's framing toward statistical reality.

### Sunk Cost Fallacy

The user is continuing a path because of prior investment, not because the path is currently the right one.

**Detection patterns:**
- The input refers to "we've already done X" as a reason to continue X
- The input contains language about "doubling down" without re-examining premises
- The input frames pivots as failures rather than learning

**Counter:** Ask the falsifying question: "If you were starting today, would you choose this path?" The user's input may not engage this question, and the report should surface it.

### Planning Fallacy

The user underestimates time, cost, and difficulty of their plan, especially based on the inside view.

**Detection patterns:**
- Timelines that don't account for typical delays in the domain
- Cost estimates without contingency
- Resource estimates that assume best-case productivity
- No mention of what happens when things take longer than planned

**Counter:** The dossier should provide outside-view base rates. Findings should reference what comparable plans actually took.

### Optimism Bias

The user assumes positive outcomes in scenarios where the dossier suggests mixed or negative outcomes are more common.

**Detection patterns:**
- The input describes outcomes as "when this works" rather than "if this works"
- Failure modes get one paragraph at the end while success scenarios fill the bulk of the input
- Risk language is vague ("there are some risks") while opportunity language is specific

**Counter:** Findings should match the dossier's actual base rates. If the dossier shows comparable plans succeed 30% of the time, the report should not let the input assume 70%.

### Authority Bias

The user has uncritically adopted a framework, claim, or strategy from an authority figure.

**Detection patterns:**
- "[Famous person/company] does this, so we should too"
- A framework name used without engagement with its actual mechanics
- A guru-quote that does the work of an argument

**Counter:** The dossier should reveal whether the authority's actual context matches the user's. Most authority transplants fail because the context differs.

### Status Quo Bias

The user has framed any change from the current state as risky and the current state as default-safe.

**Detection patterns:**
- "If we don't do X, we'll be fine" as an unexamined assumption
- Risk analysis that only considers risks of action, not risks of inaction
- The input omits counterfactual: what happens if we don't do this?

**Counter:** Surface the risks of inaction. Often they are larger than the risks of action.

## Biases in How the User Reasons Through the Problem

### Narrative Fallacy

The user has constructed a clean causal story where the actual causal structure is messier.

**Detection patterns:**
- "X happened because of Y" without ruling out Z
- Linear chains of causation in domains where feedback loops dominate
- Hindsight reasoning that explains past outcomes too neatly

**Counter:** The dossier may surface alternative causal explanations. Findings should hold the user's narrative loosely.

### Conjunction Fallacy

The user has assigned higher probability to a specific scenario than to a more general scenario that includes it.

**Detection patterns:**
- The input depends on multiple specific conditions all holding
- "If A and B and C and D, then we win" without multiplying the probabilities

**Counter:** Multiply the conditional probabilities. A plan that needs five things to go right has lower probability than a plan that needs two.

### Base Rate Neglect

The user has reasoned from features of the specific case while ignoring how often cases like this actually succeed or fail.

**Detection patterns:**
- "Our team is special because X" as a reason to expect outsized results
- Reasoning that ignores the dossier's domain-wide success rates

**Counter:** Surface base rates from the dossier. Specifics matter, but base rates set the prior.

## Biases the Challenger Itself Can Have

The verifier should look for these in the challenge findings, not just in the user's input.

### Confirmation Bias in the Challenger

The challenger gravitates toward findings the dossier most easily supports, even when those aren't the most important.

**Counter (verifier):** Ask which dimensions of the user's input received the least challenge attention. Those may be where the most important findings hide.

### Generic Critique Pattern-Matching

The challenger produces findings that pattern-match across all subjects ("regulatory risk", "competition", "execution risk") rather than findings specific to this subject.

**Counter (verifier):** Ask of each finding "could this have been written without the dossier?" If yes, the finding is generic and should be either specified or removed.

### Adversarial Bias

The challenger over-weights risks because the role is adversarial. Findings tilt toward "this won't work" even when the dossier supports the plan.

**Counter (verifier):** Some inputs are well-grounded. The verifier should let the report say so. A report that manufactures concerns to justify the analysis is dishonest.

### Confidence Inflation

The challenger overstates confidence to make findings sound rigorous.

**Counter (verifier):** Recalibrate. Most findings rest on indirect evidence and should be Medium or Low. High confidence requires Tier A evidence and intact reasoning.

### Vivid Example Bias

Specific, vivid examples in the dossier produce more challenge findings than dry structural patterns, even when the structural patterns matter more.

**Counter (verifier):** Weight findings by impact and probability, not by how interesting they are to write.

## How to Surface Biases in the Final Report

In the Meta-Reflections section, the synthesizer should call out which biases were detected in the user's input and how the analysis tried to compensate. Format:

```
Biases detected in input framing:
- Confirmation bias: input cited five supporting cases but no failures. The analysis surfaced two notable failure cases in the alternate viewpoints section.
- Planning fallacy: timeline assumptions are 30% more aggressive than the dossier base rate for comparable projects. Recommendation 4 addresses this.
```

This is more useful than a generic "watch out for biases" warning. It tells the user exactly what was missing and where in the report it was addressed.
