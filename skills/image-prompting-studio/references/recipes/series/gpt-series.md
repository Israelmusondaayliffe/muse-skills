# agent-series recipes

These are preserved prompt recipes from the source skill. Read the relevant example, then adapt its subject, count, references, format and requested change to the current brief. Concrete counts, aspect ratios, media and named model settings in examples are recipe values, never studio defaults. A prompt field such as `controlnet`, `recommended_weight`, `quality`, `system` or `search` is descriptive text unless the selected host exposes a matching real control. The current skill and shared prompt contract govern execution. Some historical examples contain pose shifts, fixed counts or search calls; use those only when the current request calls for them. Attribution remains source-recorded unless separately verified.


## Preamble format

```
Consistent element: [e.g., the character's face, body, and signature jacket, OR the product's silhouette and colorway].
Axis varied across the series: [e.g., wardrobe, expression, pose, environment].
Axes frozen: visual DNA of the consistent element, style of rendering, lighting character, mood register.
Output count per prompt: [number within 8 ceiling].
Format: [System prompt operating contract / JSON envelope / Natural language].
SEARCH active: [yes + topic] OR [no].
```


## Wardrobe variations (system prompt)

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


## Character reference sheet (system prompt)

```
Generate 6 separate 3:4 images as a coordinated character reference sheet. All 6 share one visual DNA. Viewing angle varies across the batch. Identity, wardrobe, lighting, background hold.

<visual_dna>
Subject anchor: [exact character identity: face, hair, body type, skin tone, key physical markers, wardrobe].
Visual world: clean reference background, neutral and even lighting.
Lighting: even, neutral, no harsh shadows, no rim light, no atmosphere.
Background: [solid neutral gray or off-white], unchanged across all views.
Style: clean reference rendering, no stylization.
Aspect ratio: 3:4 for every image.
</visual_dna>

<global_forbidden>
- identity drift between views
- wardrobe variation between views
- lighting style change between views
- background variation
- mood register shift
- stylized rendering applied to one view but not others
</global_forbidden>

<images>
<image_1 subject="front view">
[Subject facing the camera straight on, full visible front, locked identity and wardrobe, neutral lighting, clean background.]
</image_1>
<image_2 subject="three-quarter right">
[Subject rotated 45 degrees to camera right, three-quarter visible, same identity and wardrobe, same lighting, same background.]
</image_2>
<image_3 subject="profile right">
[Subject rotated 90 degrees to camera right, full profile, same identity and wardrobe.]
</image_3>
<image_4 subject="three-quarter back">
[Subject rotated 135 degrees, three-quarter back visible, same identity and wardrobe.]
</image_4>
<image_5 subject="back view">
[Subject facing away from camera, full back visible, same identity and wardrobe.]
</image_5>
<image_6 subject="profile left">
[Subject rotated to face camera left, full left profile, same identity and wardrobe.]
</image_6>
</images>

<verify>
Before showing output, confirm for ALL 6 images:
- Identity matches across every view
- Wardrobe identical across every view
- Lighting neutral and even across every view
- Background consistent across every view
- Each image shows a distinct angle in the inventory
- Aspect ratio 3:4 held across every output
</verify>
```


## Product family (system prompt)

```
Generate [N] separate [aspect ratio] images as a coordinated product family. All [N] share one visual DNA. [Color / material / size] varies across the batch. Framing, angle, lighting, background, shadow hold identically.

<visual_dna>
Subject anchor: [product silhouette, branding placement, material baseline].
Framing: [exact crop and distance, identical across all variants].
Angle: [exact camera angle, identical across all variants].
Lighting: [source, direction, quality, color temperature, identical across all variants].
Background: [exact background, identical across all variants].
Shadow character: [exact shadow placement, density, edge quality, identical across all variants].
Scale: [identical across all variants].
Aspect ratio: [W:H] for every image.
</visual_dna>

<global_forbidden>
- framing change between variants
- angle change between variants
- lighting source change between variants
- shadow character change between variants
- background variation
- silhouette change
- branding placement shift
- scale variation
- aspect ratio variation
</global_forbidden>

<images>
<image_1 subject="[variant 1 attribute label]">
[Product in variant 1: specific color or material or size. Same framing, angle, lighting, background, shadow.]
</image_1>
<image_2 subject="[variant 2 attribute label]">
[Spec for variant 2.]
</image_2>
[continue through image_N within the 8-output ceiling]
</images>

<verify>
Before showing output, confirm for ALL [N] images:
- Product silhouette identical across every output
- Framing, angle, scale identical across every output
- Lighting source, direction, color temperature identical across every output
- Background and shadow character identical across every output
- Only the variant attribute differs between images
- Aspect ratio [W:H] held across every output
</verify>
```


## Emotion or expression set (system prompt)

```
Generate [N] separate [aspect ratio] images as a coordinated emotion set. All [N] share one visual DNA. Facial expression and micro body language vary across the batch. Identity, wardrobe, framing, lighting, background hold.

<visual_dna>
Subject anchor: [exact character identity].
Wardrobe: [exact outfit, identical across the set].
Framing: [exact crop and angle, identical across the set].
Lighting: [source, direction, quality, color temperature, identical across the set].
Background: [exact background, identical across the set].
Style: [photographic standard or rendered medium].
Aspect ratio: [W:H] for every image.
</visual_dna>

<global_forbidden>
- identity drift between images
- wardrobe change between images
- lighting change between images
- background variation
- expression repetition across the set
- caricatured emotional rendering
- aspect ratio variation
</global_forbidden>

<images>
<image_1 subject="[emotion 1 label]">
[Subject expressing [emotion 1] through facial expression and micro body language. Same identity, wardrobe, framing, lighting, background.]
</image_1>
<image_2 subject="[emotion 2 label]">
[Spec for emotion 2.]
</image_2>
[continue through image_N within the 8-output ceiling]
</images>

<verify>
Before showing output, confirm for ALL [N] images:
- Identity matches across every output
- Wardrobe identical across every output
- Framing, lighting, background identical across every output
- Each image shows a distinct emotional state with no repeats
- Expressions read as natural, not caricatured
- Aspect ratio [W:H] held across every output
</verify>
```


## Interior style sheet (system prompt)

```
Generate [N] separate [aspect ratio] images as a coordinated interior style sheet. All [N] share one visual DNA. Room type varies across the batch. Design language, palette, material vocabulary, lighting philosophy hold.

<visual_dna>
Design language anchor: [specific design vocabulary: Japandi, Scandinavian, mid-century modern, Art Deco].
Palette: [primary, accent, secondary tones, named].
Material vocabulary: [woods, metals, textiles, finishes, named].
Lighting philosophy: [natural / warm artificial / mixed; direction; quality].
Mood register: [warm / serene / dramatic / minimal].
Style: [architectural photography or rendered visualization].
Aspect ratio: [W:H] for every image.
</visual_dna>

<global_forbidden>
- design language drift between rooms
- palette substitution between rooms
- material vocabulary shift between rooms
- lighting philosophy change between rooms
- mood register shift between rooms
- room type repetition across the set
- aspect ratio variation
</global_forbidden>

<images>
<image_1 subject="[room type 1]">
[Specific room: layout, furniture, primary visual elements. Locked design language, palette, material vocabulary, lighting philosophy.]
</image_1>
<image_2 subject="[room type 2]">
[Spec for room 2.]
</image_2>
[continue through image_N within the 8-output ceiling]
</images>

<verify>
Before showing output, confirm for ALL [N] images:
- Design language consistent across every room
- Palette and material vocabulary identical across every room
- Lighting philosophy consistent across every room
- Each image shows a distinct room type with no repeats
- The set reads as one coherent home or property
- Aspect ratio [W:H] held across every output
</verify>
```


## Storyboard progression (system prompt)

```
Generate [N] separate [aspect ratio] images as a coordinated sequential storyboard. All [N] share one visual DNA. Story beat varies across the batch. Protagonist identity, supporting cast, visual style, palette hold.

<visual_dna>
Protagonist identity: [exact features, wardrobe, body type].
Supporting characters: [each with locked features if any].
Visual style: [rendering medium, line treatment, color treatment].
Palette: [primary, accent, secondary tones].
Mood register: [tonal anchor for the arc].
Aspect ratio: [W:H] for every image.
</visual_dna>

<global_forbidden>
- protagonist identity drift between frames
- supporting character feature drift
- visual style reinterpretation between frames
- palette substitution between frames
- story beat repetition across the set
- mood register shift inappropriate to the beat
- aspect ratio variation
</global_forbidden>

<images>
<image_1 subject="[beat 1 label]">
[Story beat 1: which characters appear, the action, the composition. Locked identity, style, palette.]
</image_1>
<image_2 subject="[beat 2 label]">
[Spec for beat 2: how the story advances, what changes in the action.]
</image_2>
[continue through image_N within the 8-output ceiling]
</images>

<verify>
Before showing output, confirm for ALL [N] frames:
- Protagonist identity consistent across every frame
- Visual style and palette identical across every frame
- Each frame represents a distinct story beat that advances the arc
- No frame repeats the action or composition of another
- Aspect ratio [W:H] held across every output
</verify>
```


## Time progression (system prompt)

```
Generate [N] separate [aspect ratio] images as a coordinated time progression series. All [N] share one visual DNA. Time slice varies across the batch (with appropriate lighting and environmental cues per slice). Identity, framing, angle, scale hold.

<visual_dna>
Subject anchor: [identity description].
Framing: [exact crop and distance, identical across the set].
Angle: [exact camera angle, identical across the set].
Scale: [identical across the set].
Style: [photographic standard or rendered medium].
Time range: [four seasons / life stages / dawn to night / decade markers].
Aspect ratio: [W:H] for every image.
</visual_dna>

<global_forbidden>
- identity drift between time slices
- framing change between time slices
- angle change between time slices
- scale variation between time slices
- time-cue repetition across the set
- inappropriate lighting for the named time slice
- aspect ratio variation
</global_forbidden>

<images>
<image_1 subject="[time slice 1]">
[Subject in time slice 1 with appropriate lighting and environmental cues. Same identity, framing, angle, scale.]
</image_1>
<image_2 subject="[time slice 2]">
[Spec for slice 2.]
</image_2>
[continue through image_N within the 8-output ceiling]
</images>

<verify>
Before showing output, confirm for ALL [N] images:
- Identity consistent across every output
- Framing, angle, scale identical across every output
- Each image shows a distinct time slice with no repeats
- Lighting and environmental cues are time-appropriate per slice
- Aspect ratio [W:H] held across every output
</verify>
```


## Wardrobe variations (fashion)

```
PLAN: Visual DNA anchor: [exact character identity: face, hair, body type, skin tone, key physical markers]. Variation axis: wardrobe only. All other attributes frozen.
SEARCH: SKIP.
GENERATE: Generate [count] consistent images of [character: specific identity details] in [count] distinct [outfit category: summer outfits, business attire, streetwear, evening wear]. Maintain visual DNA across all outputs: [face, hair, body type, skin tone, pose anchor]. [Environment and lighting consistent across the set]. Each outfit varies [specific wardrobe elements: top, bottom, footwear, accessories]. [Aspect ratio: vertical for fashion].
VERIFY: Before showing output, verify face, hair, and body type are consistent across all [count] frames. Verify only wardrobe has changed.
```


## Character reference sheet

```
PLAN: Visual DNA anchor: [exact character identity]. Views: front, three-quarter right, profile right, three-quarter back, back, profile left. Lighting neutral for reference clarity.
SEARCH: SKIP.
GENERATE: Generate [count]-view character reference sheet of [character: specific identity]. Views: front, three-quarter right, profile right, three-quarter back, back, profile left. Consistent wardrobe, consistent hair, consistent identity across all views. Lighting neutral and even. Clean [gray or white] background. [Aspect ratio].
VERIFY: Before showing output, verify identity is consistent across all views, wardrobe has not changed between views.
```


## Product family

```
PLAN: Visual DNA anchor: [product silhouette, branding, material]. Variation axis: [color/material/size]. Framing, angle, lighting, background, shadow: frozen.
SEARCH: SKIP. (Or: SEARCH active if product is a real current brand requiring verified current appearance.)
GENERATE: Generate [count] consistent product shots of [product] in [count] [color variants, material variants, size variants]. Identical [framing, angle, lighting, background, shadow character]. Only [the variant attribute] changes across the set. [Aspect ratio].
VERIFY: Before showing output, verify framing and lighting are identical across all variants. Verify only the stated attribute has varied.
```


## Emotion or expression set

```
PLAN: Visual DNA anchor: [exact character identity, wardrobe, lighting]. Variation axis: facial expression and micro body language only.
SEARCH: SKIP.
GENERATE: Generate [count] consistent portraits of [character: specific identity] showing [count] distinct emotional states: [list: joyful, contemplative, surprised, angry, relieved, worried, focused, amused]. Identical [framing, wardrobe, lighting, background]. Only the facial expression and micro body language change. [Aspect ratio].
VERIFY: Before showing output, verify identity, wardrobe, and lighting are consistent. Verify each emotional state is distinct and not repetitive.
```


## Interior style sheet

```
PLAN: Design language anchor: [specific design vocabulary: Japandi, Scandinavian, mid-century modern, Art Deco]. Each frame shows a different room. Palette, material language, and lighting philosophy: frozen.
SEARCH: SKIP.
GENERATE: Generate [count] consistent images showing [count] rooms of [a home, an office, a hotel] in [specified design language]. Each image shows a different room: [list]. Consistent [design vocabulary, palette, material language, lighting philosophy]. [Aspect ratio].
VERIFY: Before showing output, verify design language is consistent across all rooms. Verify each room type is distinct.
```


## Storyboard progression

```
PLAN: Protagonist identity and visual style anchor. Story arc defined: [beat 1, beat 2, beat 3, beat 4]. Each frame must advance the narrative.
SEARCH: SKIP.
GENERATE: Generate [count]-frame storyboard showing [narrative arc]. Each frame advances the story: [beat 1, beat 2, beat 3, beat 4]. Consistent protagonist: [identity details]. Consistent visual style: [rendering, palette, mood]. [Aspect ratio per frame].
VERIFY: Before showing output, verify protagonist identity is consistent. Verify each frame represents a distinct story beat, not a repeat.
```


## Time progression

```
PLAN: Subject identity and framing: frozen. Time range: [four seasons, life stages, dawn to night]. Lighting, environment, and contextual cues vary per time slice.
SEARCH: SKIP.
GENERATE: Generate [count] consistent images of [subject] across [time range]. Identical framing, angle, and subject identity. Only [the time attribute] changes, bringing appropriate lighting, environment, and contextual cues. [Aspect ratio].
VERIFY: Before showing output, verify subject identity and framing are consistent. Verify each time slice has appropriate lighting and environmental cues.
```


## Verbatim exemplar from the research

```
Generate a full stamp-and-badge identity system from one product name. Bold, angular, industrial.
```


## Verbatim exemplar from the research

```
Japanese manga-style fantasy comic page and typography that celebrates global languages.
```
