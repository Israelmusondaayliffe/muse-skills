# json-envelope-template recipes

These are preserved prompt recipes from the source skill. Read the relevant example, then adapt its subject, count, references, format and requested change to the current brief. Concrete counts, aspect ratios, media and named model settings in examples are recipe values, never studio defaults. A prompt field such as `controlnet`, `recommended_weight`, `quality`, `system` or `search` is descriptive text unless the selected host exposes a matching real control. The current skill and shared prompt contract govern execution. Some historical examples contain pose shifts, fixed counts or search calls; use those only when the current request calls for them. Attribution remains source-recorded unless separately verified.


## Canonical schema

```json
{
  "plan": "[Composition intent. Spatial relationships. What the model reasons about before generating. State the visual DNA anchor if relevant. State the variation axis frozen vs. varied.]",
  "search": "[Search trigger string with date anchor IF current data needed. Otherwise null.]",
  "subject": "[WHO/WHAT: appearance, clothing, key identifiers, preserved features.]",
  "pose": "[Body position. Hand placement. Crop point. Camera-relative orientation.]",
  "environment": "[Setting. Surfaces. Props. Negative space.]",
  "camera": "[Lens type. Height. Angle. Framing logic. Distortion notes.]",
  "lighting": "[Source. Direction. Quality. Bounce surface. Contrast level. Color temperature.]",
  "mood": "[3 to 5 words. Emotional register.]",
  "style": "[Photographic or rendered style. Realism standard. Reference frame.]",
  "palette": "[5 to 7 color and tone tokens.]",
  "quality": "[Material specifics. Texture standard. Output fidelity. Capture method authenticity.]",
  "aspect_ratio": "[W:H, e.g. 3:4]",
  "verify": [
    "[checklist item 1]",
    "[checklist item 2]",
    "[checklist item 3]"
  ],
  "negative_prompt": {
    "forbidden": [
      "[category-level exclusion 1]",
      "[category-level exclusion 2]"
    ]
  }
}
```


## Construction pattern

Instructional fragment from the source. Wrap the selected fields in a complete JSON object and remove comments before delivering JSON.

```text
"forbidden": [
  // Anatomy correction cluster
  "anatomy normalization",
  "body proportion averaging",
  "aesthetic proportion correction",
  "dataset-average anatomy",

  // Skin and texture artifacts cluster
  "plastic skin",
  "airbrushed texture",
  "skin smoothing",
  "beautification filters",

  // Lens and framing cluster
  "wide-angle distortion not in reference",
  "lens compression not in reference",
  "cropping that removes intent"

  // Style drift cluster
  "stylized realism",
  "editorial fashion proportions",
  "more realistic reinterpretation"
]
```


## ControlNet block: instructional, not literal

Instructional fragment from the source. Wrap the selected fields in a complete JSON object and remove comments before delivering JSON.

```text
"controlnet": {
  "pose_control": {
    "model_type": "OpenPose",
    "purpose": "Exact skeletal and pose lock",
    "constraints": [
      "preserve shoulder width",
      "preserve hip angle",
      "preserve spine curvature",
      "preserve limb placement"
    ],
    "recommended_weight": 0.95
  },
  "depth_control": {
    "model_type": "ZoeDepth",
    "purpose": "Depth, volume, and camera-to-body spatial lock",
    "constraints": [
      "preserve foreground volume",
      "prevent flat or compressed depth",
      "maintain torso-to-background separation"
    ],
    "recommended_weight": 0.8
  }
}
```


## Exemplar 1: Photoreal preservation with mirror-selfie authenticity

```json
{
  "plan": "Preserve subject identity and feature specificity against beautification drift. Single high-fidelity output. Visual DNA anchor: amateur smartphone capture authenticity.",
  "search": null,
  "subject": "[WHO: detailed appearance preserving specific features the user wants held against normalization. Clothing described materially, not aesthetically.]",
  "pose": "[Body angle. Hand placement. Crop point. Camera-relative orientation.]",
  "environment": "[Restrained interior with named surfaces and minimal props.]",
  "camera": "Believable mirror selfie perspective. Visible smartphone reflection. Chest-height lens. Realistic amateur framing and accurate proportions.",
  "lighting": "[Soft natural source. Bounce surface named. Low contrast.]",
  "mood": "[3 to 5 words.]",
  "style": "High-fidelity, ultra-realistic amateur mirror selfie photography. Strict adherence to physical reality. Preserving skin pores, micro-details, natural lighting, material realism, unretouched proportions.",
  "palette": "[5 to 7 color and tone tokens.]",
  "quality": "[Material specifics. Capture method realism. Premium amateur smartphone capture without beauty corrections.]",
  "aspect_ratio": "3:4",
  "controlnet": {
    "pose_control": {
      "model_type": "OpenPose",
      "purpose": "Exact skeletal and pose lock",
      "constraints": ["preserve shoulder width", "preserve hip angle", "preserve spine curvature", "preserve limb placement"],
      "recommended_weight": 0.95
    },
    "depth_control": {
      "model_type": "ZoeDepth",
      "purpose": "Depth and volume lock",
      "constraints": ["preserve foreground volume", "prevent depth flattening", "maintain subject-to-background separation"],
      "recommended_weight": 0.8
    }
  },
  "verify": [
    "subject features preserved as described",
    "amateur smartphone authenticity not lost to studio polish",
    "lighting consistent with stated source",
    "no items in forbidden array present"
  ],
  "negative_prompt": {
    "forbidden": [
      "anatomy normalization",
      "body proportion averaging",
      "aesthetic proportion correction",
      "beauty standard enforcement",
      "dataset-average anatomy",
      "camera angles that reduce intended volume",
      "wide-angle distortion not in reference",
      "lens compression not in reference",
      "cropping that removes intent",
      "depth flattening",
      "beautification filters",
      "skin smoothing",
      "plastic skin",
      "airbrushed texture",
      "stylized realism",
      "editorial fashion proportions",
      "more realistic reinterpretation",
      "naturalization of distinct features"
    ]
  }
}
```


## Exemplar 2: Surgical EDIT with preservation

```json
{
  "plan": "Targeted modification of one element. Everything else held against drift.",
  "search": null,
  "subject": "[Subject as visible in source image. Modification target named explicitly: change X to Y.]",
  "pose": "Preserve original pose exactly.",
  "environment": "Preserve original environment, lighting setup, framing, and camera distance.",
  "camera": "Preserve original camera position and lens character.",
  "lighting": "Preserve original lighting source, direction, and quality.",
  "mood": "Preserve original mood register.",
  "style": "Preserve original photographic or rendered style.",
  "palette": "Preserve original palette except where the target modification requires color shift.",
  "quality": "Preserve original capture quality and material rendering. Modification must integrate seamlessly.",
  "aspect_ratio": "[Match source.]",
  "verify": [
    "only the named target element has changed",
    "all preservation clauses held",
    "modification integrates with original lighting and material logic",
    "no items in forbidden array present"
  ],
  "negative_prompt": {
    "forbidden": [
      "changing pose",
      "changing framing",
      "changing camera angle",
      "changing lighting direction",
      "changing background",
      "restyling unaltered subject elements",
      "color grading shift not requested",
      "skin tone adjustment not requested",
      "sharpening or smoothing not requested",
      "regenerating untouched regions"
    ]
  }
}
```


## Exemplar 3: SHOW-ME with style lock

```json
{
  "plan": "Identical subject and style across angle variations. Vary only camera angle and framing distance. Visual DNA: subject identity, wardrobe, lighting, environment, mood.",
  "search": null,
  "subject": "[Subject identity locked. Wardrobe locked. Identifying features preserved.]",
  "pose": "[Pose anchor. Body orientation that allows the requested angle without re-staging.]",
  "environment": "[Environment locked. No re-dressing.]",
  "camera": "[Specific angle for this output. The variation axis. Framing distance named.]",
  "lighting": "[Lighting locked. Same source, direction, quality across all outputs.]",
  "mood": "[Mood locked.]",
  "style": "[Style locked.]",
  "palette": "[Palette locked.]",
  "quality": "[Quality and capture method locked.]",
  "aspect_ratio": "[Locked.]",
  "verify": [
    "only camera angle has varied",
    "subject identity unchanged",
    "wardrobe unchanged",
    "lighting unchanged",
    "environment unchanged",
    "no style drift toward different aesthetic"
  ],
  "negative_prompt": {
    "forbidden": [
      "wardrobe variation",
      "subject identity drift",
      "facial feature change",
      "body proportion change",
      "lighting change",
      "color temperature shift",
      "environment redress",
      "style reinterpretation",
      "mood register shift",
      "palette substitution",
      "rendered medium change",
      "framing intent loss"
    ]
  }
}
```

## Applying the envelope

Use `plan` for intent, `search` only for a genuine retrieval need, descriptive keys for the visual brief, `preserve`/`changes` where useful, and `verify` for observable checks. A `forbidden` list can name related unwanted changes, such as smoothing, airbrushing or beautification when preserving real facial texture. Avoid arbitrary item counts or claims that a list guarantees fidelity. Strong positive direction remains necessary.

For precision, distinguish the subject's actual features from artistic translation. Remove contradictory constraints and irrelevant fields. Keep explicit reference roles and priority. If an example uses ControlNet names or weights, preserve them only as descriptive instruction when requested, never claim the provider ran that pipeline. When constraints flatten the result, simplify the least relevant ones and retain the reference-defining features.
