# reference-deconstruction recipes

These are preserved prompt recipes from the source skill. Read the relevant example, then adapt its subject, count, references, format and requested change to the current brief. Concrete counts, aspect ratios, media and named model settings in examples are recipe values, never studio defaults. A prompt field such as `controlnet`, `recommended_weight`, `quality`, `system` or `search` is descriptive text unless the selected host exposes a matching real control. The current skill and shared prompt contract govern execution. Some historical examples contain pose shifts, fixed counts or search calls; use those only when the current request calls for them. Attribution remains source-recorded unless separately verified.


## Template prompt (NL, default)

```
PLAN: Reference deconstruction. Extract the underlying creative system from the uploaded image, do not reproduce it. Output a 4:3 visual brand board capturing seven systems: core idea and creative tension, color and material language, typography direction, image and composition logic, signature visual device, layout and grid system, multi-format campaign applications.

SEARCH: SKIP.

GENERATE: Acting as a senior Creative Director, study the attached reference image and rebuild its underlying creative system as a clean 4:3 visual brand board. Do not copy the reference directly. Extract and present: the core idea and creative tension, color and material palette named with roles, typography direction and hierarchy, image vocabulary and composition logic, the single signature visual device that defines the reference, layout and grid system, and a strip of multi-format campaign applications. Treat the board as a premium editorial agency slide. Modular grid, strong hero zone, large visual tiles, limited labels, minimal micro-copy, clean margins, no overlapping text on active backgrounds. The board should function as a portable system that another designer could pick up and apply to a different brand without ever seeing the original reference.

VERIFY: Before showing output, confirm all seven systems are visibly present on the board. Confirm no direct reproduction of the reference subject, scene, or figures. Confirm 4:3 ratio. Confirm micro-copy is minimal and readable.
```


## Template prompt (JSON envelope, anti-drift)

```json
{
  "plan": "Reference deconstruction. Extract the creative system from the attached image into a 4:3 brand board. Do not copy the reference. Seven extraction targets: core idea and tension, color and material language, typography direction, image and composition logic, signature visual device, layout and grid, multi-format applications.",
  "search": "skip",
  "format": "4:3 visual brand board, premium editorial agency layout",
  "extraction_targets": [
    "core idea and creative tension",
    "color and material language with named roles",
    "typography direction and hierarchy logic",
    "image vocabulary and composition logic",
    "signature visual device",
    "layout and grid system",
    "multi-format campaign applications strip"
  ],
  "design_rules": [
    "modular grid",
    "strong hero zone",
    "large visual tiles",
    "limited labels",
    "minimal micro-copy",
    "clean margins, consistent spacing",
    "no text overlap on active backgrounds"
  ],
  "forbidden": [
    "direct reproduction of the reference subject or scene",
    "copying any specific figure, product, or location from the reference",
    "pixel-level mimicry of textures or marks",
    "text overlap on active backgrounds",
    "overcrowding"
  ],
  "verify": [
    "all seven extraction targets present and labeled",
    "no direct copy of the reference",
    "4:3 ratio held",
    "micro-copy minimal and readable",
    "layout reads as a portable system"
  ]
}
```

## Applying the method

Extract seven useful systems: core idea and tension; color and material language; typography direction; image/composition logic; signature visual device; layout/grid; and application logic. Distinguish observation from interpretation. Use the analysis directly in the requested prompt. A 4:3 board is an available recipe, not a required intermediate image, brand workflow, or fixed aesthetic.
