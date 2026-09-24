# agent-edit recipes

These are preserved prompt recipes from the source skill. Read the relevant example, then adapt its subject, count, references, format and requested change to the current brief. Concrete counts, aspect ratios, media and named model settings in examples are recipe values, never studio defaults. A prompt field such as `controlnet`, `recommended_weight`, `quality`, `system` or `search` is descriptive text unless the selected host exposes a matching real control. The current skill and shared prompt contract govern execution. Some historical examples contain pose shifts, fixed counts or search calls; use those only when the current request calls for them. Attribution remains source-recorded unless separately verified.


## Step 1: Image Analysis & Use Case Scanning

```
UPLOADED IMAGE ANALYSIS:
Image 1: [Detailed: subject, clothing, hair, setting, lighting, pose, colors, expression, distinctive features]
Image 2: [If present, same detail level]
```


## Step 1: Image Analysis & Use Case Scanning

```
APPLICABLE USE CASES (from references/use-case-patterns.md):
- [Pattern #X: Name]: Why it applies
- [Pattern #Y: Name]: Why it applies

Mode detected: [editing / show-me / multi-reference / image-only]
Request interpretation: [What user wants]
```


## Image Editing

```
Using the uploaded [explicit description], [transformation action]. [ANTI-PASTE: angle/pose shift]. [Specific changes]. Match existing [lighting/style/perspective]. Maintain [what stays constant]. Do not change aspect ratio.
```


## Multi-Reference Composition

```
Using the uploaded references of [describe each: person 1 details, person 2 details, product details, style reference details], create [scene description]. Maintain [each element's traits]. [Composition and spatial relationships]. [Lighting that unifies all elements]. [AR or "Do not change aspect ratio."]
```


## Background Change

```
Using the uploaded [subject description], transport to [new environment]. Keep [subject details] identical. Create [new lighting for environment]. [Environmental details interacting with subject]. Do not change aspect ratio.
```


## Color Variant Swap

```
Using the uploaded product shot of [description], change [specific color element] from [current] to [new]. Maintain exact [design, form, lighting, reflections, environment, angle]. Do not change aspect ratio.
```


## VFX Product Swap

```
Using the uploaded scene showing [scene and current product], replace [current product] with [new product]. Match existing [lighting, color temperature, shadow direction, reflection quality]. Scale appropriately. Do not change aspect ratio.
```


## Relighting

```
Using the uploaded photo of [description], transform lighting from [current] to [target]. Shadows now fall [direction]. Highlights on [surfaces]. Color temperature shifts to [value]. Atmosphere: [mood]. Do not change aspect ratio.
```
