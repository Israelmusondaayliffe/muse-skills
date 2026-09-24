# system-prompt-template recipes

These are preserved prompt recipes from the source skill. Read the relevant example, then adapt its subject, count, references, format and requested change to the current brief. Concrete counts, aspect ratios, media and named model settings in examples are recipe values, never studio defaults. A prompt field such as `controlnet`, `recommended_weight`, `quality`, `system` or `search` is descriptive text unless the selected host exposes a matching real control. The current skill and shared prompt contract govern execution. Some historical examples contain pose shifts, fixed counts or search calls; use those only when the current request calls for them. Attribution remains source-recorded unless separately verified.


## Canonical structure

```
Generate [N] separate [aspect ratio] images as a coordinated [task type]. All [N] share one visual DNA. [What varies across the batch]. [What holds across the batch].

<reference>
[OPTIONAL block. Include only when reference images are uploaded with the brief. State what aesthetic cues to pull. State what NOT to pull. Include negative usage constraints when the subject of the reference is NOT the subject of the outputs.]
</reference>

<visual_dna>
[What persists across every output. Style, palette, lighting philosophy, subject anchor, typographic treatment, surface vocabulary. State aspect ratio here as one DNA element among others.]
</visual_dna>

<global_forbidden>
[Category-level exclusions that apply to ALL outputs. Same construction rules as the JSON envelope's forbidden array. Cluster by category.]
</global_forbidden>

<images>
<image_1 subject="[brief subject label]">
[Full spec for image 1: composition, framing, subject specifics, per-image variations from the shared DNA.]
</image_1>
<image_2 subject="[brief subject label]">
[Full spec for image 2.]
</image_2>
[continue through image_N within the 8-output ceiling]
</images>

<verify>
Before showing output, confirm for ALL [N] images:
[Cross-image consistency checks. What must hold identically across the batch. What must vary distinctly.]
</verify>
```


## Variant A: SERIES (consistent multi-output along one axis)

```
Generate [N] separate [aspect ratio] images as a coordinated wardrobe variation series. All [N] share one visual DNA. Wardrobe varies across the batch. Identity, environment, lighting, framing hold.

<visual_dna>
Subject anchor: [exact character identity: face, hair, body type, skin tone, key physical markers].
Visual world: [environment, palette, treatment, mood register].
Pose anchor: [pose held across the set].
Lighting: [source, direction, quality, color temperature].
Style: [photographic standard or rendered medium].
Aspect ratio: [W:H] for every image.
</visual_dna>

<global_forbidden>
- subject identity drift across images
- facial feature change between images
- body proportion change
- hair color or length variation
- environment redress between images
- lighting source or color temperature shift
- style reinterpretation between images
- mood register shift
- aspect ratio variation
</global_forbidden>

<images>
<image_1 subject="[wardrobe variant 1 label]">
[Subject in [wardrobe 1: top, bottom, footwear, accessories]. Same pose anchor. Same environment. Same lighting.]
</image_1>
<image_2 subject="[wardrobe variant 2 label]">
[Spec for variant 2.]
</image_2>
[continue through image_N within the 8-output ceiling]
</images>

<verify>
Before showing output, confirm for ALL [N] images:
- Subject identity matches across every output
- Pose anchor held across every output
- Environment and lighting identical across every output
- Each image shows a distinct wardrobe with no repeats
- Aspect ratio [W:H] held across every output
</verify>
```


## Variant B: NARRATIVE (character bible across panels)

```
Generate [N] separate [aspect ratio] panels as a coordinated sequential narrative. All [N] share one visual DNA. Story beat varies across the panels. Character identities, art tradition, line work, palette hold.

<visual_dna>
Protagonist: [exact identity: name, age, hair, signature feature, wardrobe].
Supporting characters: [each with locked features].
Art tradition: [Seinen / Shonen / Shojo / specific tradition].
Visual style: [line work treatment, ink contrast, screentone usage, color treatment if any].
Visual world: [setting, era, palette logic, mood register].
Aspect ratio: [W:H] for every panel.
</visual_dna>

<global_forbidden>
- protagonist feature drift between panels
- supporting character feature drift
- art tradition shift between panels
- ink treatment or screentone style change
- color treatment shift
- panel-to-panel quality variance
- story beat repetition across panels
- dialogue paraphrasing
</global_forbidden>

<images>
<image_1 subject="[story beat 1 label]">
[Which characters appear, the action, the panel composition, dialogue in quotes if any.]
</image_1>
[continue through image_N]
</images>

<verify>
Before showing output, confirm for ALL [N] panels:
- Character identities consistent across every panel
- Visual style and ink treatment consistent
- Each panel renders a distinct story beat
- Dialogue spelled correctly where present
- Aspect ratio [W:H] held across every panel
</verify>
```


## Variant C: MULTI-OUTPUT (visual DNA backbone across distinct deliverables)

```
Generate [N] separate images as a coordinated multi-page system. All [N] share one visual DNA backbone. Each image is a distinct page type. Visual DNA, palette, treatment, mood hold.

<visual_dna>
Subject: [name and type: brand, event, product, character, IP].
Description: [what it is, what it stands for. 1 to 3 sentences.]
Key text: [exact name, tagline, or line that must appear verbatim in relevant pages].
Palette: [primary color, accent color, secondary tones, named].
Treatments: [textures, grain, glitch, compositional devices].
Subject matter: [imagery vocabulary that lives in this world].
Mood: [2 to 4 descriptors].
Aspect ratio defaults: [per page type, listed below].
</visual_dna>

<global_forbidden>
- palette drift across pages
- treatment loss between pages
- text spelling errors on key text
- page-type bleed (one page looking like another)
- system incoherence (pages that read like different brands)
- generic stock-image substitutes for brand-specific imagery
</global_forbidden>

<images>
<image_1 subject="[page type 1, e.g. brand identity sheet]">
[Page type, layout logic, exact text in quotes, aspect ratio for this page type, specific visual elements.]
</image_1>
<image_2 subject="[page type 2, e.g. campaign keyvisual]">
[Spec for page 2.]
</image_2>
[continue through image_N for each distinct page type]
</images>

<verify>
Before showing output, confirm for ALL [N] pages:
- Visual DNA palette and treatment present on every page
- Exact text rendered verbatim on each page where it appears
- Each page is a distinct deliverable type with no duplicates
- Aspect ratio matches the page type defaults stated in the visual DNA
- The set reads as one coherent system, not seven different brands
</verify>
```

## Applying the operating prompt

State the requested file count and task in the opening. Put only genuinely shared constraints in `<visual_dna>`. Give each numbered image enough subject, action, layout and content direction to stand on its own. Use per-image exceptions for constraints that change. Add current-data retrieval only where needed, and base the prompt on verified supplied facts when the host cannot search.

Before delivery, count image entries against the requested total; compare shared and local ratios; check that changing wardrobe, material, viewpoint or time has not also been accidentally frozen in the shared block. Keep exclusions relevant and checks observable. The whole requested batch belongs in one copyable prompt. A system-style prompt can be used in ordinary chat, but does not itself grant native batch capability. Actual outputs must be counted separately.
