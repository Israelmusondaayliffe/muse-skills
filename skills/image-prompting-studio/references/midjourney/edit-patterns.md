# Midjourney edit prompt patterns
The original worked prompts are preserved, including their historical `--v 8.2` flags. These are craft examples, not a required model choice. Use only selected-model controls in a new prompt.


Use these patterns after the core skill has identified the base, delta, protected anchors, reference roles, and risk level.

Do not paste every category into every prompt. Select only what matters.

# Prompt anatomy

Priority order:

1. direct edit instruction;
2. target and reference relationship;
3. protected anchors;
4. spatial or compositional requirement;
5. integration cues;
6. style reinforcement;
7. exclusions;
8. parameters.

Compact formula:

```text
[DIRECTIVE]. Preserve [ANCHORS]. Match [INTEGRATION CUES]. Do not alter [PROTECTED AREAS] or add [UNWANTED CONTENT]. [PARAMETERS]
```

# Language rules

Prefer:

- concrete nouns;
- direct verbs;
- one major edit per sentence;
- visible identity or geometry anchors;
- frame-relative direction;
- exact counts and locations;
- concise preservation clauses;
- medium-specific cohesion cues.

Avoid:

- make it better;
- change the vibe;
- use the other one;
- keep everything the same;
- long style-tag piles;
- full scene descriptions for one small edit;
- conflicting instructions;
- claims of exact model control.

# Preservation anchors

## Character

Use only visible and relevant anchors:

- face shape;
- eye spacing;
- nose shape;
- skin tone;
- hairstyle;
- facial hair;
- distinctive jewelry;
- body proportions;
- garment construction;
- seams;
- accessories.

## Product or object

- silhouette;
- proportions;
- control layout;
- logo placement;
- material finish;
- edge treatment;
- surface details;
- mechanical relationships.

## Architecture

- massing;
- facade geometry;
- window rhythm;
- openings;
- material system;
- camera position;
- perspective lines;
- site relationship.

## Composition

- crop;
- camera distance;
- horizon;
- subject scale;
- subject position;
- foreground arrangement;
- negative space;
- depth order.

# Integration cues

## Inserted prop

Prioritize:

- size relationship;
- perspective;
- contact point;
- occlusion;
- cast shadow;
- reflections;
- material response.

## Character relocation

Prioritize:

- matching light direction;
- color temperature;
- reflected environment light;
- atmospheric depth;
- edge detail;
- lens behavior;
- grain.

## Illustration or graphic style

Prioritize:

- line weight;
- edge language;
- fill behavior;
- texture;
- palette;
- contrast;
- paper or surface character.

## Photographic style

Prioritize:

- camera distance;
- focal behavior;
- depth of field;
- light direction;
- contrast;
- grain;
- color response;
- motion or shutter character.

# Mode recipes

## 1. Direct delta

```text
Replace [existing element] with [new element] at [location]. Keep [protected elements] unchanged. Match [scale, perspective, contact, shadow, reflections, texture, light]. Do not alter [protected area] or add [unwanted content]. [parameters]
```

Example:

```text
Replace the white ceramic mug on the table with an antique brass hourglass in the same position. Keep the hand, table setting, camera angle, crop, and room unchanged. Match the hourglass scale, table contact, warm window light, soft cast shadow, brass reflections, shallow depth of field, and 35mm grain. Do not add any other objects. --raw --v 8.2
```

## 2. Removal and reconstruction

```text
Remove [specific element] completely and reconstruct the revealed [background or surface] seamlessly. Match the surrounding [texture, material, pattern, light, grain, perspective]. Do not add a replacement object or change [protected elements]. [parameters]
```

Example:

```text
Remove the framed poster from the concrete wall and reconstruct the exposed wall seamlessly. Match the raw concrete texture, pores, hairline cracks, soft side light, and shallow perspective. Do not replace it with art, text, hardware, or decoration. Keep the furniture, crop, and room lighting unchanged. --raw --v 8.2
```

## 3. Character or object consistency

```text
Use the [visually identified reference subject] as the same [person, character, object, vehicle, creature]. Place [subject] [new action or location]. Preserve [specific identity or geometry anchors]. Change only [named delta]. Match [camera, light, environment, material] without redesigning [protected feature]. [parameters]
```

Example:

```text
Use the woman with short black curls and a silver nose ring as the same person. Turn her approximately 45 degrees toward frame left into a three-quarter profile, looking toward the open window. Preserve her face shape, skin tone, hairstyle, nose ring, body proportions, outfit, crop, and camera distance. Change only her head, gaze, and upper-torso orientation. Keep the room and light unchanged. --raw --v 8.2
```

## 4. Perspective or viewpoint

```text
Show the same [subject or object] from [precise viewpoint]. Preserve [identity, silhouette, proportions, markings, wardrobe, geometry]. Reconstruct newly visible surfaces coherently. Keep [camera distance or framing requirement] and do not redesign [protected features]. [parameters]
```

Example:

```text
Show the same motorcycle directly from the rear at matching camera height and distance. Preserve its frame proportions, seat shape, exhaust geometry, tire width, paint finish, decals, and lighting. Reconstruct the rear assembly and unseen surfaces coherently without redesigning the vehicle. --raw --v 8.2
```

## 5. Background-only replacement

```text
Replace only the background with [environment]. Preserve the foreground subject, pose, crop, camera perspective, and existing subject lighting. Match edge detail and atmospheric depth without changing [identity or object]. [parameters]
```

## 6. Fully integrated relocation

```text
Place the same [subject] inside [environment]. Preserve [identity and wardrobe anchors], then relight the subject to match [new light source, color temperature, direction, reflections, atmosphere]. Keep [pose and framing] unchanged. [parameters]
```

Do not mix `preserve the original lighting` with `fully relight for the new environment` unless a hybrid composite look is intentional.

## 7. Multi-reference composite

```text
Create a new composition using [subject with visible descriptor] from the [subject reference], [garment, prop, or second subject] from the [content reference], and [environment] from the [environment reference]. Preserve [named attributes] from each source and do not exchange features between them. Arrange them [precise spatial relationship]. Unify the result through [light, perspective, scale, contact, material, grain, palette]. [parameters]
```

Example:

```text
Create a new composition using the woman with the close-cropped hair from the portrait reference, the sculptural black coat from the garment reference, and the brutalist stairwell from the environment reference. Preserve her face, skin tone, hair, proportions, and earrings. Preserve the coat's high collar, asymmetric closure, seam map, and hem shape. Place her centered on the lower landing, facing camera. Match scale, stair perspective, concrete bounce light, contact shadow, cool gray palette, and fine film grain. Do not exchange facial, garment, or architectural features between references. --raw --ar 4:5 --v 8.2
```

## 8. Retexture

```text
Retexture the entire image as [target medium or visual treatment]. Preserve the original composition, subject silhouettes, proportions, spatial relationships, and camera position. Render every surface consistently with [line, texture, palette, light, grain, material cues]. [optional style control] [parameters]
```

Describe the target style in words even when a Style Reference or Moodboard is attached.

Example:

```text
Retexture the entire image as a hand-rendered architectural gouache study on warm cotton paper. Preserve the building massing, window rhythm, people, landscaping, camera position, and perspective. Use opaque mineral pigments, dry-brush concrete texture, fine graphite construction lines, soft sky washes, and restrained warm-gray shadows across every surface. --raw --v 8.2
```

## 9. Aspect-ratio expansion

```text
Expand the canvas to [target ratio] by generating new scene content on [left, right, top, bottom, or all sides]. Preserve the original image at its existing proportions and camera scale. Continue [environment, lighting, perspective lines, texture] naturally into the new area. Do not stretch, squeeze, crop, enlarge, recenter, or reposition [protected subject]. --ar [ratio] [parameters]
```

Example:

```text
Expand the canvas to 16:9 by generating additional street and architecture on frame left and frame right. Preserve the original subject at the same size, position, proportions, pose, and camera perspective. Continue the wet pavement, storefront rhythm, vanishing lines, evening light, and reflections naturally into the new areas. Do not stretch, squeeze, crop, enlarge, or recenter the subject. --ar 16:9 --raw --v 8.2
```

## 10. Targeted inpainting

Use the full web Editor.

Workflow:

1. Select or erase the target region.
2. Include enough surrounding edge context for blending.
3. Protect unrelated regions.
4. State one local change.
5. Match the surrounding material, light, perspective, and texture.

Prompt:

```text
Inside the selected area, [local change]. Match the surrounding [material, light, edge, texture, perspective]. Keep everything outside the selected area unchanged. Do not add [unwanted content]. [parameters]
```

When several selected regions need an exact count, edit one region or object per pass.

## 11. Layer-assisted composite

Use Editor layers when a specific external object or plate must be placed with more exact scale and position.

Workflow:

1. Add and position the layer.
2. Erase unwanted edges or background.
3. Submit an edit to flatten and integrate.
4. Run a second style-cohesion pass only if necessary.

Integration prompt:

```text
Integrate the placed [object or subject] into the scene. Preserve its shape and design. Match the scene's scale, perspective, edge softness, contact, occlusion, shadow, reflected light, color response, and grain. Do not redesign the source element or change the surrounding composition. --raw --v 8.2
```

# Staged chains

## Identity plus action plus environment

```text
PASS 1, submit alone:
Change only the subject's pose, gaze, or viewpoint. Preserve visible identity, body proportions, wardrobe, crop, camera distance, and source style. --raw --v 8.2

PASS 2, use the chosen Pass 1 result as the new base:
Place the same subject inside [environment]. Preserve identity, pose, wardrobe, crop, and camera distance from the new base. Build and light the environment around the subject. --raw --v 8.2

PASS 3, only if needed:
Unify the subject and environment through [specific palette, grain, light, texture, or Style Reference]. Preserve identity, pose, composition, and object geometry. --raw --v 8.2
```

## Geometry plus style

```text
PASS 1:
Correct or transfer the exact object or architectural geometry. Keep the source style simple and neutral. --raw --v 8.2

PASS 2:
Retexture the approved geometry using [target style]. Preserve silhouette, proportions, layout, and camera position. [style controls] --raw --v 8.2
```

# Four-route output calibration

For simple edits:

1. Precision Delta: minimal wording.
2. Anchor-Rich: explicit protected features.
3. Cohesion-Controlled: stronger integration language.
4. Editor Fallback: local mask or layer route.

For high-risk edits:

1. Best one-pass attempt.
2. Preservation-heavy one-pass attempt.
3. Reference-role optimized attempt.
4. Recommended staged chain.

Each chosen route must pursue the same requested outcome. Four is a calibration example, not an output quota.
