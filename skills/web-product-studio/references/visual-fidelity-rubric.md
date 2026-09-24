# Visual fidelity rubric

Judge the fresh rendered hero against the locked references at the same intended viewport. Do not score from telemetry, source code, labels, feature count, or builder explanation.

## Score

- 9 to 10: the first-glance identity, composition, form, material, light, atmosphere, and motion cues are convincing. Remaining differences are P3 polish only.
- 7 to 8: the target is clearly recognizable and the three non-negotiable traits hold. Remaining differences are P3 only.
- 5 to 6: the idea is recognizable, but one load-bearing trait or the first-glance read is weak. Repair or switch method before feature expansion.
- 3 to 4: the runtime works but the picture communicates the wrong object, medium, mood, scale, or motion. Switch method unless a small, observable repair can close the gap.
- 0 to 2: the reference is not meaningfully represented or evidence is not viewable.

Seven is the minimum pass. A score of seven or more still fails if any P0, P1, or P2 visual gap remains.

## Required comparisons

Inspect the desktop hero and the mobile crop when framing changes materially. For stateful experiences, inspect default and extreme states without relying on labels to identify them. Compare:

1. first-glance identity and silhouette;
2. composition, framing, scale, and depth;
3. material, lighting, color, and atmosphere;
4. motion or state behavior when load-bearing;
5. visible artifacts, placeholders, faceting, banding, stretching, clipping, and fake detail.

## Severity

- P0: unsafe, deceptive, unusable, or no viewable comparison.
- P1: wrong first-glance identity, object, medium, or composition.
- P2: a required trait is visibly weak, broken, or absent.
- P3: polish issue that does not change recognition or the locked traits.

## Method switch

Use the contract's observable switch condition. Examples include a shader technique that cannot reproduce the reference silhouette, geometry whose sampling visibly facets the nearest surface, a procedural system that cannot produce the required state, or a generated asset that cannot maintain the locked crop. Record the failed method and selected replacement before continuing.

The reviewer must be independent of the builder and must name concrete differences. The review binds the validated contract, current source, references, and rendered artifacts. The validator recomputes those bindings and reports the review file hash. It does not replace visual judgment.
