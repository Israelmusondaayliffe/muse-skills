# Chart message audit workflow

## Required checks

1. Claim scope: the caption does not exceed the measured population, period, or metric.
2. Denominator and baseline: rates, shares, and changes have a clear base.
3. Encoding integrity: scale, axis, area, color, order, and aggregation do not distort the relationship.
4. Comparison validity: groups and periods are comparable, or the limitation is visible.
5. Uncertainty: small samples, missing data, intervals, and observational limits are stated when material.
6. Accessibility: labels, contrast, reading order, and non-color cues support the audience.
7. Action fit: the chart supports the decision it is presented to inform.

## Verdict rules

- `pass`: no material issue changes interpretation.
- `revise`: evidence supports the claim, but the encoding, wording, or accessibility needs correction.
- `block`: the evidence is absent, contradictory, incomparable, or materially weaker than the claim.

Record what was observed for every check. Do not write a pass or fail without evidence.

## Boundaries

Do not repair the underlying analysis. Route calculation, sampling, or data-quality failures to the analysis owner. Audit the message and evidence contract only.

## Complete the repair loop

For a build or revision request, repair authorized wording, scale, labels, or layout from the checked evidence, then audit the revised artifact once. Retain the original verdict and identify the revised file. A supported, narrower claim can replace an unsupported claim; missing analysis cannot be invented. Update the delivery status from the new audit. For audit-only work, give corrections without changing the artifact.
