# agent-create recipes

These are preserved prompt recipes from the source skill. Read the relevant example, then adapt its subject, count, references, format and requested change to the current brief. Concrete counts, aspect ratios, media and named model settings in examples are recipe values, never studio defaults. A prompt field such as `controlnet`, `recommended_weight`, `quality`, `system` or `search` is descriptive text unless the selected host exposes a matching real control. The current skill and shared prompt contract govern execution. Some historical examples contain pose shifts, fixed counts or search calls; use those only when the current request calls for them. Attribution remains source-recorded unless separately verified.


## Preamble format

```
Axis varied: [e.g., lighting, from harsh midday to blue hour to candlelit interior]
Axes frozen: [e.g., subject, composition, wardrobe, mood register, style]
Format chosen: [Natural language (default) / JSON envelope (photoreal preservation) / System prompt (creative session batch)].
SEARCH active: no.
```


## General text-to-image

```
PLAN: [Composition intent: subject placement, depth, spatial relationships, key constraints.]
SEARCH: SKIP.
GENERATE: [Shot type and framing] of [subject with specific identifying details]. [Action or state]. [Environment with atmospheric detail]. [Lighting quality and direction]. [Key textures and materials where relevant]. [Mood and emotional register]. [Camera or lens quality if photographic]. [Aspect ratio as natural phrase].
VERIFY: Before showing output, verify the axis has varied across all 7 outputs, frozen axes are consistent, and no keyword stacks appear in the prompt.
```


## Photoreal portrait

```
PLAN: Portrait framing with [close-up, medium, three-quarter, full] coverage. Priority: skin realism, lighting consistency, no AI sheen.
SEARCH: SKIP.
GENERATE: [Framing] of [subject: age, features, ethnicity if relevant, styling]. [Pose and expression]. [Environment]. [Lighting: source, direction, quality, color temperature]. [Skin and material notes: visible pores, natural specular highlights, fabric drape, no plastic skin, no over-sharpening]. [Authentic film grain or digital capture note]. [Aspect ratio].
VERIFY: Before showing output, verify no plastic skin, no over-sharpening, lighting logic is internally consistent.
```


## Minimalist negative space

```
PLAN: Negative space composition. Subject anchors [corner or edge]. Text overlay territory preserved.
SEARCH: SKIP.
GENERATE: Minimalist composition. Single [subject] positioned in [corner or edge]. Vast [color] empty space dominates. Subject occupies [percentage] of frame. [Lighting from direction]. Purpose: [text overlay space, artistic statement, calm aesthetic]. [Aspect ratio].
VERIFY: Before showing output, verify the empty space reads as intentional, not as an incomplete composition.
```


## Cinematic scene

```
PLAN: Cinematic [wide, medium, close-up]. Palette and blocking determined by mood. Lens character stated.
SEARCH: SKIP.
GENERATE: Cinematic [wide shot, medium shot, close-up] of [scene or character]. [Mood: tense, melancholic, triumphant]. [Time of day and lighting]. [Palette and color grade reference]. [Lens feel: anamorphic flare, 35mm film, shallow depth]. [Framing and blocking]. [Aspect ratio: 2.39:1 ultra-wide or 16:9].
VERIFY: Before showing output, verify palette is consistent with stated mood reference, not a generic cinematic default.
```


## Camera simulation

```
PLAN: [Camera type] authenticity. Distortion, artifacts, and grain appropriate to the specific device.
SEARCH: SKIP.
GENERATE: [Scene] as captured by [GoPro, body cam, CCTV, drone, Polaroid, disposable camera, vintage Super 8, iPhone RAW]. [Characteristic distortion or quality: fisheye edges, low-light noise, chromatic aberration, motion blur]. [Framing typical of that camera]. [Artifacts that sell authenticity]. [Aspect ratio].
VERIFY: Before showing output, verify device-specific artifacts are present and the image does not revert to a clean generic look.
```


## Anti-slop photoreal

```
PLAN: Amateur authenticity. Candid framing, mixed lighting, no AI polish. iPhone quality only.
SEARCH: SKIP.
GENERATE: Amateur photo of [subject]. [Casual framing, slight off-center]. [Natural imperfections: motion blur, mixed lighting, lens flare, no flash]. Shot on iPhone. [Setting with candid detail]. [Everyday texture and authenticity markers]. [Aspect ratio].
VERIFY: Before showing output, verify no AI sheen, no studio lighting, no perfectly centered composition.
```
