# Preserved controlled-angle templates

Use these exact source forms for camera-only work. The active skill decides the format; JSON and forbidden arrays express intent, not guaranteed enforcement. PSGV labels and preambles are optional craft. Ratio, count and search statements are example values. VERIFY clauses ask for checks; only observed outputs can establish visual fidelity. The panoramic example is unverified on the selected model until tested.

## Step 1: Describe the upload (source block 1)

```
UPLOADED SUBJECT: [identity, wardrobe, pose, style of the original image, lighting logic, color palette, mood, distinctive features]
```

## Preamble format (source block 2)

```
Uploaded subject: [one-line summary].
Axis varied: camera angle and framing only.
Axes frozen: subject identity, wardrobe, pose integrity (where compatible with angle), style, lighting logic, mood, color palette.
Format: [JSON envelope / Natural language fallback].
SEARCH active: no.
```

## Prompt template: JSON envelope (default) (source block 3)

```json
{
  "plan": "Angle variation only. Visual DNA: subject identity, wardrobe, style, lighting logic, mood, color palette. Variation axis: camera position. Physical lighting shift (if any) must follow from the new angle, not introduce a new style.",
  "search": null,
  "subject": "Show the uploaded [subject identity, wardrobe, distinctive features] from [new angle name]. Subject identity locked.",
  "pose": "[Pose anchor adapted to be visible from the new angle without re-staging.]",
  "environment": "Preserve original environment.",
  "camera": "[Specific angle name: close-up, three-quarter front, profile, low angle, high angle, etc.]. [Framing distance.] [Lens character if relevant.]",
  "lighting": "Preserve original lighting source, direction, and quality. New angle reveals existing lighting from a different vantage, does not introduce new lighting style.",
  "mood": "Preserve original mood register.",
  "style": "Preserve original style exactly.",
  "palette": "Preserve original palette.",
  "quality": "Preserve original capture quality and material rendering.",
  "aspect_ratio": "[Match source unless angle requires reframing.]",
  "verify": [
    "camera position has changed",
    "subject identity, wardrobe, distinctive features intact",
    "style, lighting logic, mood, color palette preserved",
    "lighting shift (if any) follows from new angle physically, not stylistically"
  ],
  "negative_prompt": {
    "forbidden": [
      "wardrobe variation",
      "subject identity drift",
      "facial feature change",
      "body proportion change",
      "lighting style change (color, intensity, mood)",
      "color temperature shift",
      "environment redress",
      "style reinterpretation",
      "mood register shift",
      "palette substitution",
      "rendered medium change",
      "filter overlay applied to new angle",
      "era shift",
      "stylistic flourish introduced for the angle"
    ]
  }
}
```

## Prompt template: NL fallback (exploratory) (source block 4)

```
PLAN: Freeze set: [subject identity, wardrobe, style, lighting logic, color palette, mood]. New camera position: [angle name and description]. Physical lighting shift (if any) must follow from the new angle, not introduce a new style.
SEARCH: SKIP.
GENERATE: Show the uploaded [subject description] from [new angle or framing]. [Compositional specifics: what fills the frame, what's now revealed, how the subject is oriented]. Keep [identity markers: face, wardrobe, distinctive features] consistent. Match the original's style, lighting logic, color palette, and mood. [Optional: new spatial context the angle reveals].
VERIFY: Before showing output, verify the camera position has changed. Verify style, mood, wardrobe, and identity markers are intact. Verify no stylistic drift has occurred beyond what the new angle physically implies.
```

## Verbatim exemplar (source block 5)

```
360 equirectangular panoramic image of a cozy mountain cabin in winter, photorealistic, 2:1 aspect ratio, seamless
```

