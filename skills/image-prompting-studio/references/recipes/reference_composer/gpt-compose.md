# agent-compose recipes

These are preserved prompt recipes from the source skill. Read the relevant example, then adapt its subject, count, references, format and requested change to the current brief. Concrete counts, aspect ratios, media and named model settings in examples are recipe values, never studio defaults. A prompt field such as `controlnet`, `recommended_weight`, `quality`, `system` or `search` is descriptive text unless the selected host exposes a matching real control. The current skill and shared prompt contract govern execution. Some historical examples contain pose shifts, fixed counts or search calls; use those only when the current request calls for them. Attribution remains source-recorded unless separately verified.


## Step 1: Describe each upload

```
UPLOADED REFERENCES:
Reference 1: [full description: subject, identity markers, style, lighting, pose]
Reference 2: [full description]
Reference 3: [if present]
...
```


## Preamble format

```
Uploaded references: [Ref 1 summary, Ref 2 summary, Ref 3 summary, ...].
Axis varied: [e.g., narrative context, from formal boardroom to casual cafe to outdoor hike].
Axes frozen: identity of each reference subject, style anchor, lighting quality, interaction relationship.
Format: [JSON envelope / System prompt operating contract / Natural language fallback].
SEARCH active: [yes + topic] OR [no].
```


## Two-subject scene (JSON)

```json
{
  "plan": "Two-subject composition. Ref 1 and Ref 2 identities preserved. Lighting unified across both subjects, not patchworked from source images. Spatial relationship defined.",
  "search": null,
  "subject": "Composition of [Ref 1 identity: face, hair, wardrobe, markers] and [Ref 2 identity: face, hair, wardrobe, markers]. [Spatial relationship: who is where, what they are doing].",
  "pose": "[Pose for each subject in the composition.]",
  "environment": "[Environment for the scene, unified across both subjects.]",
  "camera": "[Camera angle and framing for the composition.]",
  "lighting": "[Unified lighting source, direction, quality, color temperature applied to both subjects.]",
  "mood": "[Mood register for the scene.]",
  "style": "[Photographic or rendered style, applied uniformly.]",
  "palette": "[Unified palette derived from the scene.]",
  "quality": "[Capture quality applied uniformly to both subjects.]",
  "aspect_ratio": "[W:H]",
  "verify": [
    "Ref 1 identity markers intact",
    "Ref 2 identity markers intact",
    "lighting unified across both subjects",
    "spatial relationship correct",
    "no wardrobe or feature cross-bleed between subjects"
  ],
  "negative_prompt": {
    "forbidden": [
      "wardrobe transfer between subjects",
      "facial feature blending between subjects",
      "hair color or style transfer between subjects",
      "patchwork lighting (each subject lit as in source image)",
      "scale mismatch between subjects",
      "perspective inconsistency between subjects",
      "Ref 1 absorbing Ref 2 features or vice versa",
      "generic group-photo composition replacing requested spatial relationship"
    ]
  }
}
```


## Subject in referenced environment (JSON)

```json
{
  "plan": "Subject from Ref 1 placed into environment from Ref 2. Subject identity locked. Environment locked. Lighting unified.",
  "search": null,
  "subject": "[Ref 1 identity: face, hair, wardrobe, markers] placed in [Ref 2 environment].",
  "pose": "[Pose appropriate to the new environment context.]",
  "environment": "[Ref 2 environment described in detail. Preserve its character.]",
  "camera": "[Camera angle that respects both subject and environment.]",
  "lighting": "[Unified lighting derived from environment, applied to subject.]",
  "mood": "[Mood derived from environment.]",
  "style": "[Style unified across subject and environment.]",
  "palette": "[Palette derived from environment, applied to subject.]",
  "quality": "[Capture quality unified.]",
  "aspect_ratio": "[W:H]",
  "verify": [
    "subject identity intact",
    "environment character preserved",
    "lighting on subject consistent with environment lighting",
    "subject scale appropriate for environment"
  ],
  "negative_prompt": {
    "forbidden": [
      "subject identity drift",
      "environment character drift",
      "subject lit as in original source rather than environment",
      "subject scale wrong for environment",
      "environment redress to match subject's original context",
      "halo or compositing artifact at subject edges",
      "perspective mismatch between subject and environment"
    ]
  }
}
```


## Style reference applied to subject (JSON)

```json
{
  "plan": "Subject from Ref 1 reinterpreted in style from Ref 2. Subject identity preserved. Style applied as full reinterpretation, not filter overlay.",
  "search": null,
  "subject": "[Ref 1 identity] rendered in style of [Ref 2 style anchor].",
  "pose": "[Preserve Ref 1 pose.]",
  "environment": "[Environment in Ref 2 style.]",
  "camera": "[Framing.]",
  "lighting": "[Lighting per Ref 2 style logic, applied to subject.]",
  "mood": "[Mood per Ref 2 style.]",
  "style": "[Ref 2 style: brushwork, palette, line quality, texture, rendering medium.]",
  "palette": "[Ref 2 palette applied throughout.]",
  "quality": "[Style-appropriate fidelity.]",
  "aspect_ratio": "[W:H]",
  "verify": [
    "Ref 1 subject identity recognizable",
    "Ref 2 style fully applied (not filter overlay)",
    "composition coherent under the new style"
  ],
  "negative_prompt": {
    "forbidden": [
      "filter-on-top appearance",
      "subject identity loss",
      "Ref 2 subject features bleeding into Ref 1 subject",
      "incomplete style application (some regions in style, others photoreal)",
      "generic stylization not specific to Ref 2"
    ]
  }
}
```


## Prompt templates: system prompt format (for compose batches)

```
Generate [N up to 8] separate [aspect ratio] images as a coordinated multi-composition batch using the uploaded references. All [N] share one visual DNA. Composition and narrative context vary across the batch. Reference identities, role assignments, lighting unification hold.

<reference>
Reference 1: [full identity description: face, hair, wardrobe, markers, style anchor].
Reference 2: [full identity description].
Reference 3 (if present): [full identity description].
Reference 4 (if present): [full identity description].

Reference roles:
- Subject reference(s): [Ref X, Ref Y].
- Environment reference: [Ref Z, if present].
- Style reference: [Ref W, if present].

Negative usage: do not pull subject features from style reference, do not pull lighting from subject reference's source image, do not swap roles.
</reference>

<visual_dna>
Composition style: [photographic / rendered medium].
Lighting unification: [single source, direction, quality, color temperature applied to all references in every output].
Mood register: [for the batch].
Aspect ratio: [W:H] for every image.
</visual_dna>

<global_forbidden>
- reference identity drift across the batch
- role swap between references (subject becoming style, style becoming subject)
- wardrobe or feature transfer between subject references
- patchwork lighting (each reference lit as in its source image)
- style reference subject features leaking into subject reference
- environment reference character loss
- composition collapse to generic group photo
- aspect ratio variation
</global_forbidden>

<images>
<image_1 subject="[composition 1 label]">
[Spatial arrangement, interaction, environment, mood for composition 1. Reference identities and roles preserved.]
</image_1>
<image_2 subject="[composition 2 label]">
[Spec for composition 2.]
</image_2>
[continue through image_N within the 8-output ceiling]
</images>

<verify>
Before showing output, confirm for ALL [N] images:
- Each reference identity preserved across every composition
- Reference roles never swap between images
- Lighting unified per composition, not patchworked from source images
- No cross-bleed between subject references
- Each composition is distinct, no duplicates
- Aspect ratio [W:H] held across every output
</verify>
```


## Two-subject scene

```
PLAN: Ref 1 identity anchor: [face, hair, wardrobe, key markers]. Ref 2 identity anchor: [same]. Spatial relationship: [who is where]. Lighting unification: [source, direction, temperature].
SEARCH: SKIP.
GENERATE: Using the uploaded references of [Ref 1: specific identity details] and [Ref 2: specific identity details], create a scene showing both subjects [in the specified situation]. [Spatial relationship]. [Interaction: what they are doing]. [Environment and unified lighting]. Preserve each subject's identity markers.
VERIFY: Before showing output, verify Ref 1 identity markers are intact. Verify Ref 2 identity markers are intact. Verify lighting is unified across both subjects, not sourced from their separate reference images.
```


## Subject + environment

```
PLAN: Subject identity anchor: [markers]. Environment anchor: [mood, lighting direction, color palette]. Lighting on subject must match environment logic.
SEARCH: SKIP.
GENERATE: Using the uploaded reference of [subject details] and the uploaded reference of [environment details], place the subject into the environment. [Position in frame]. [Lighting on subject matches environment: direction, color temperature, quality]. [Environmental details around the subject]. Preserve the subject's identity and the environment's mood.
VERIFY: Before showing output, verify subject identity is intact. Verify lighting on subject is consistent with the environment's light source direction.
```


## Subject + product

```
PLAN: Subject identity anchor. Product identity anchor: form, color, branding. Interaction type defined. Environment consistent with product category.
SEARCH: SKIP.
GENERATE: Using the uploaded reference of [subject details] and the uploaded reference of [product details], compose a lifestyle scene where the subject [interacts with, uses, holds, wears] the product. [Natural body language]. [Environment consistent with product category]. [Lighting that flatters both]. Preserve product form, color, and branding exactly. Preserve subject identity.
VERIFY: Before showing output, verify product form and branding are exact. Verify subject identity is intact. Verify the interaction looks physically plausible.
```


## Style reference + subject

```
PLAN: Style transfer attributes: [palette, lighting quality, mood, rendering technique]. Subject identity markers that must survive the transfer. Not a filter. A reinterpretation.
SEARCH: SKIP.
GENERATE: Using the uploaded style reference [palette, mood, rendering, composition] applied to the uploaded subject [identity details], generate a new image. Preserve the subject's identity. Transfer only the style reference's [color palette, lighting quality, mood, rendering technique], not its subject or composition. [Optional: shift pose slightly to prevent a filter-on-top look.]
VERIFY: Before showing output, verify subject identity is recognizable. Verify style-specific characteristics are present. Verify the output is not a pixel-level copy of the style reference.
```


## Wardrobe or attribute transfer

```
PLAN: Subject identity anchor. Wardrobe or attribute to transfer: [fit, color, material]. Source reference for wardrobe defined. Pose and framing frozen.
SEARCH: SKIP.
GENERATE: Using the uploaded reference of [subject] and the uploaded reference of [wardrobe or attribute], dress or equip the subject with the referenced wardrobe. [Fit and fall on the body]. Preserve the subject's facial identity, pose, and framing. Match the original subject's lighting and environment unless specified.
VERIFY: Before showing output, verify wardrobe details match the reference. Verify subject facial identity is intact.
```


## Multi-character ensemble

```
PLAN: Each character's identity anchor stated. Ensemble maximum: 4 references for fidelity. Spatial arrangement and unified lighting defined.
SEARCH: SKIP.
GENERATE: Using the uploaded references of [Ref 1 details, Ref 2 details, Ref 3 details, Ref 4 details], create an ensemble scene. [Spatial arrangement]. [Interaction or unified activity]. [Environment]. [Unified lighting]. Preserve each character's identity. Note: limiting to 4 references maintains highest identity fidelity.
VERIFY: Before showing output, verify each character's identity markers are intact. Verify lighting is unified across all four. Verify spatial positions match the stated arrangement.
```


## Verbatim exemplar from research

```
In the game Zelda totk link is in a e531 series train made by him
```
