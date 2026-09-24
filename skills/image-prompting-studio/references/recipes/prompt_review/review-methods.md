# Review methods

## Establish the actual contract

Use the brief's requested count, formats, aspect ratio, reference roles and intended changes. Distinguish one prompt for multiple separate images, separate submitted prompts, one composite grid, sequential stills and a controlled study. An optional shot plan is evidence of intent, not a mandatory prerequisite.

## Structure

For JSON, check parsing and the fields required by the chosen prompt form. Reject unresolved placeholders in a finished prompt where values are needed. Do not assume every image needs human subjects, clothing, skin, micro-expression, a negative list or a mode field. A source prompt skeleton is not a native API schema.

Keep quoted copy, code and structured literals unchanged unless the requested correction concerns them. Do not lint image prompt content for broad prose banned words or rewrite an intentional title. A malformed code block must be reported even if other blocks parse.

The bundled checker can verify these narrow properties:

```sh
python scripts/validate_prompt_payload.py prompts.md --expect-count 4
python scripts/validate_prompt_payload.py prompts.json --require-path generation_request.input.mode --require-path generation_request.camera.angle
python scripts/validate_prompt_payload.py prompts.json --equal-path generation_request.styling.subject_1 --equal-path generation_request.styling.subject_2
```

Only supply paths appropriate to the selected form and brief. Exact equal-path checks are for deliberately repeated fields, not a synonym-aware visual identity judgment. Check each intended subject, object or world anchor rather than only the first subject. The checker does not interpret photographed outputs or infer semantic equivalence.

## Coverage and variation

Compare each frame to its purpose. A full editorial shoot may benefit from close detail, full body/context, side/rear, candid and direct engagement; an all-close-up request should remain all close-ups. Product and world coverage follow their own functions. Repetition can be purposeful in a turnaround or matched comparison.

Check framing/angle/action together. A new label on the same composition is not necessarily a new useful shot. Conversely, similar framing can reveal a meaningfully different action. Do not use keyword matches or arbitrary lexical similarity thresholds as artistic pass/fail tests.

## Continuity

For a coherent shoot, inspect identity, styling, grade, location family, physical light sources and material treatment. For narrative or time progression, distinguish intended state changes from accidental drift. For controlled viewpoints, keep the same moment unless requested otherwise. A natural new shot may change pose, gaze or expression.

Inspect every relevant subject, object and landmark. A small textual change can invert a defining color or direction; high string similarity would miss it. Differently worded descriptions can still preserve the same thing.

## Semantic checks

- Do change and preserve instructions agree?
- Are reference roles specific enough to avoid swapping subject and style?
- Does the output format match separate files versus a composite?
- Are exact text and important labels correct and readable where outputs exist?
- Does the prompt require a feature the selected surface does not expose? Consult the model profile only as needed.
- Are style/realism constraints appropriate to the source and target medium?
- Are assumptions about hidden details, future states or facts identified when material?

When expressions matter, specific eye, mouth, brow, jaw or gesture cues can help. They are unnecessary for many objects/worlds and need not vary in a controlled study. Avoid adding mandatory negative items just to meet a minimum length. Text, logos, symmetry, polished skin or studio light may be the user's actual goal.

## Repair and delivery

For an obvious syntax defect, repair it when revisions are authorized. For creative contradictions, name the issue and propose the smallest change that fits the user's intent. When an ambiguity can be resolved reasonably, do so and state the choice. Ask only when materially incompatible requirements remain.

If the same issue affects a set, repair the shared instruction once and apply it consistently. Return the findings and any requested complete revised prompts. Passing syntax and consistency checks supports review but does not confer final creative acceptance.
