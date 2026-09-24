# agent-edit recipes

These are preserved prompt recipes from the source skill. Read the relevant example, then adapt its subject, count, references, format and requested change to the current brief. Concrete counts, aspect ratios, media and named model settings in examples are recipe values, never studio defaults. A prompt field such as `controlnet`, `recommended_weight`, `quality`, `system` or `search` is descriptive text unless the selected host exposes a matching real control. The current skill and shared prompt contract govern execution. Some historical examples contain pose shifts, fixed counts or search calls; use those only when the current request calls for them. Attribution remains source-recorded unless separately verified.


## Step 1: Describe the upload

```
UPLOADED IMAGE: [subject identity, pose, wardrobe, setting, lighting, framing, color palette, distinctive features, mood]
```


## Preamble format

```
Uploaded image: [one-line summary of what was uploaded].
Axis varied: [e.g., time of day, from dawn to noon to golden hour to night].
Axes frozen: [subject identity, wardrobe, pose, framing, composition].
Format: [JSON envelope / Natural language fallback / System prompt for batch].
SEARCH active: [yes + topic] OR [no].
```


## Element or object swap (JSON)

```json
{
  "plan": "Surgical element swap. Target: [current element] -> [new element]. Everything else preserved against drift.",
  "search": null,
  "subject": "Using the uploaded [description], replace [current element] with [new element]. Preserve identity markers, pose, framing, lighting, environment.",
  "pose": "Preserve original pose exactly.",
  "environment": "Preserve original environment, framing, and camera distance.",
  "camera": "Preserve original camera position and lens character.",
  "lighting": "Preserve original lighting source, direction, and quality. Match new element's material response to existing light.",
  "mood": "Preserve original mood register.",
  "style": "Preserve original photographic or rendered style.",
  "palette": "Preserve original palette except where the new element naturally introduces its own color.",
  "quality": "Preserve original capture quality. New element must integrate seamlessly.",
  "aspect_ratio": "[Match source.]",
  "verify": [
    "[new element] present and [current element] absent",
    "all preservation clauses held",
    "new element integrates with existing lighting and material logic",
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
      "regenerating untouched regions"
    ]
  }
}
```


## Color variant (JSON)

```json
{
  "plan": "Color shift on [element], from [current] to [new]. Form, reflections, shadows, environment, angle frozen.",
  "search": null,
  "subject": "Using the uploaded [description], change [element] from [current color] to [new color]. Maintain exact form, reflections, shadows, environment, and angle.",
  "pose": "Preserve original pose.",
  "environment": "Preserve original environment.",
  "camera": "Preserve original camera position and angle.",
  "lighting": "Preserve original lighting. New color must respond to existing light naturally.",
  "mood": "Preserve original mood.",
  "style": "Preserve original style.",
  "palette": "Update only the named element's color. Preserve all other palette tokens.",
  "quality": "Preserve original capture quality.",
  "aspect_ratio": "[Match source.]",
  "verify": [
    "[element] now reads as [new color]",
    "form, reflections, and shadows consistent with new color material response",
    "no spillover color shift on adjacent elements"
  ],
  "negative_prompt": {
    "forbidden": [
      "form change on [element]",
      "shadow direction change",
      "environment color cast shift",
      "lighting direction change",
      "color spillover to adjacent elements",
      "global palette regrade",
      "saturation shift on unrelated regions"
    ]
  }
}
```


## Background replacement (JSON)

```json
{
  "plan": "Replace background. Subject identity, pose, wardrobe, and lighting on body preserved. New environment must match perspective and provide environmentally consistent ambient light.",
  "search": null,
  "subject": "Using the uploaded [subject description], transport the subject into [new environment]. Preserve subject pose, wardrobe, identity, and lighting on body.",
  "pose": "Preserve original pose exactly.",
  "environment": "Replace with [new environment]. Match perspective to original subject capture angle. Provide environmentally consistent ambient light.",
  "camera": "Preserve original camera position and lens character.",
  "lighting": "Preserve direct lighting on body. Update environmental ambient to match new background.",
  "mood": "Update mood to match new environment. Preserve subject's expression.",
  "style": "Preserve original photographic style.",
  "palette": "Subject palette preserved. Environment palette per new setting.",
  "quality": "Preserve subject capture quality. Match environment fidelity to subject.",
  "aspect_ratio": "[Match source.]",
  "verify": [
    "subject identity, pose, wardrobe intact",
    "environmental lighting consistent with new background",
    "perspective matches subject capture angle",
    "no halo or cutout artifact at subject edges"
  ],
  "negative_prompt": {
    "forbidden": [
      "subject identity drift",
      "pose change",
      "wardrobe modification",
      "perspective mismatch between subject and background",
      "halo or cutout artifact",
      "subject lighting change inconsistent with new environment",
      "subject scale wrong for environment"
    ]
  }
}
```


## Style transfer (JSON)

```json
{
  "plan": "Style reinterpretation. Composition and subject identity preserved. Rendering shifts to match [target style] characteristics.",
  "search": null,
  "subject": "Using the uploaded [description], reinterpret in [target style: oil painting, watercolor, charcoal, Studio Ghibli, 1960s French New Wave, Bauhaus]. Preserve composition and subject identity.",
  "pose": "Preserve original pose.",
  "environment": "Preserve original environment in style-appropriate rendering.",
  "camera": "Preserve original framing.",
  "lighting": "Preserve original light direction. Render lighting in style-appropriate manner.",
  "mood": "Preserve original mood register, expressed through style.",
  "style": "[Target style] with [key style characteristics: brushwork, palette, line quality, texture].",
  "palette": "[Style-appropriate palette derived from original].",
  "quality": "[Style-appropriate fidelity, not photorealism unless target style is photoreal].",
  "aspect_ratio": "[Match source.]",
  "verify": [
    "style-specific rendering characteristics present",
    "subject identity recognizable through the style",
    "composition preserved",
    "not a filter-on-top look"
  ],
  "negative_prompt": {
    "forbidden": [
      "filter-on-top appearance (style applied as overlay rather than reinterpretation)",
      "subject identity loss",
      "composition change",
      "pose change",
      "generic stylization not specific to [target style]",
      "photorealism leaking through stylization"
    ]
  }
}
```


## Era or period shift (JSON)

```json
{
  "plan": "Era shift to [decade or period]. Wardrobe, environment, and photographic quality updated to era. Facial identity preserved.",
  "search": "[Search the web, today is [date]: wardrobe conventions in [decade].] OR null",
  "subject": "Using the uploaded [description], re-render as if photographed in [decade]. Update wardrobe, environment, and photographic quality. Preserve facial identity and composition.",
  "pose": "Preserve original pose.",
  "environment": "Update to era-appropriate setting.",
  "camera": "Update lens and capture characteristics to era-appropriate.",
  "lighting": "Era-appropriate lighting.",
  "mood": "Era-appropriate mood register.",
  "style": "Era-appropriate photographic style and grain.",
  "palette": "Era-appropriate color science and grading.",
  "quality": "Era-appropriate capture authenticity.",
  "aspect_ratio": "[Match source.]",
  "verify": [
    "era-appropriate wardrobe present",
    "era-appropriate environment present",
    "facial identity preserved",
    "era-appropriate photographic texture present"
  ],
  "negative_prompt": {
    "forbidden": [
      "facial identity drift",
      "pose change",
      "modern wardrobe details leaking through",
      "modern photographic polish (HDR, sharpness) on era output",
      "era anachronism in props or environment",
      "style-transfer look instead of period authenticity"
    ]
  }
}
```


## Texture or material transformation (JSON)

```json
{
  "plan": "Material transformation on [element]. Form and silhouette frozen. Material properties of [target material] rendered realistically.",
  "search": null,
  "subject": "Using the uploaded [description], transform [element] from [current material] to [target material: marble, bronze, glass, ice, gold leaf]. Maintain form and silhouette.",
  "pose": "Preserve original pose.",
  "environment": "Preserve original environment.",
  "camera": "Preserve original camera position.",
  "lighting": "Preserve original lighting. New material responds to existing light realistically.",
  "mood": "Preserve original mood.",
  "style": "Preserve original style.",
  "palette": "Update [element] to [target material] color and tonal response. Preserve all other palette tokens.",
  "quality": "Preserve original capture quality. Render [target material] with realistic surface detail and light response.",
  "aspect_ratio": "[Match source.]",
  "verify": [
    "[target material] surface detail and light response present on [element]",
    "form and silhouette intact",
    "no material spillover to adjacent elements"
  ],
  "negative_prompt": {
    "forbidden": [
      "form distortion on [element]",
      "silhouette change",
      "material spillover to adjacent elements",
      "lighting direction change",
      "[target material] rendered incorrectly (e.g., marble without veining, gold without specular)",
      "background or environment material change"
    ]
  }
}
```


## Relighting (JSON)

```json
{
  "plan": "Lighting replacement. Subject and composition preserved. New lighting scheme defined: key direction, fill, rim, color temperature, shadow character.",
  "search": null,
  "subject": "Using the uploaded [description], replace existing lighting with [new scheme]. Preserve subject and composition.",
  "pose": "Preserve original pose.",
  "environment": "Preserve original environment, illuminated by new lighting.",
  "camera": "Preserve original camera position and framing.",
  "lighting": "[Key light direction and quality]. [Fill behavior]. [Rim behavior]. [Color temperature: e.g., 3200K tungsten, 5600K daylight, 7000K shade]. [Shadow character: hard, soft, multiple, single].",
  "mood": "[Mood implied by new lighting scheme].",
  "style": "Preserve original style.",
  "palette": "Update palette to reflect new color temperature and lighting mood.",
  "quality": "Preserve capture quality. New lighting must read as authentic to the scene.",
  "aspect_ratio": "[Match source.]",
  "verify": [
    "shadow direction consistent with stated key light position",
    "color temperature shift visible throughout image",
    "subject identity and composition intact",
    "fill and rim behavior matches stated scheme"
  ],
  "negative_prompt": {
    "forbidden": [
      "subject identity drift",
      "composition change",
      "pose change",
      "shadow direction inconsistent with stated key light",
      "color temperature only applied to subject, not environment",
      "filter-style relight (color overlay rather than light direction shift)"
    ]
  }
}
```


## Element or object swap

```
PLAN: Target element to swap: [current element] → [new element]. All other elements frozen: identity markers, pose, framing, lighting, environment.
SEARCH: SKIP.
GENERATE: Using the uploaded [description], replace [current element] with [new element]. Keep [identity markers, pose, framing, lighting, environment] exactly as they are.
VERIFY: Before showing output, verify [new element] is present and [current element] is gone. Verify all frozen elements are intact.
```


## Color variant

```
PLAN: Element to recolor: [element], from [current color] to [new color]. Form, reflections, shadows, environment, angle: frozen.
SEARCH: SKIP.
GENERATE: Using the uploaded [description], change [element] from [current color] to [new color]. Maintain exact form, reflections, shadows, environment, and angle. Match the existing lighting and material response.
VERIFY: Before showing output, verify color has changed. Verify form, reflections, and shadows are consistent with the new color's material response.
```


## Lighting shift

```
PLAN: Current lighting state described. Target lighting state defined. Shadow direction and color temperature changes mapped.
SEARCH: SKIP.
GENERATE: Using the uploaded [description], transform the lighting from [current] to [target]. Shadows now fall [direction]. Highlights appear on [surfaces]. Color temperature shifts to [value]. Atmosphere: [mood]. Preserve subject pose and framing.
VERIFY: Before showing output, verify lighting character has shifted. Verify shadows are consistent with the new light source direction. Verify subject pose and framing are intact.
```


## Background replacement

```
PLAN: Subject to preserve: [identity, pose, wardrobe, lighting on body]. New environment defined. Perspective and environmental lighting must match.
SEARCH: SKIP.
GENERATE: Using the uploaded [subject description], transport the subject into [new environment]. Keep the subject's pose, wardrobe, and lighting on the body consistent. Generate matching environmental lighting on the new background. Match the perspective the subject is captured at.
VERIFY: Before showing output, verify subject identity, pose, and wardrobe are intact. Verify environmental lighting is consistent with the new background, not the original.
```


## Style transfer

```
PLAN: Style target: [oil painting, watercolor, charcoal, Studio Ghibli, 1960s French New Wave, Bauhaus]. Identity markers to preserve stated. Rendering shift defined.
SEARCH: SKIP.
GENERATE: Using the uploaded [description], reinterpret in [style]. Preserve the composition and subject identity. Shift rendering to match [key style characteristics: brushwork, palette, line quality, texture]. [Optional: shift pose slightly to prevent a filter-on-top look.]
VERIFY: Before showing output, verify style-specific rendering characteristics are present. Verify subject identity is recognizable through the style shift.
```


## Era or period shift

```
PLAN: Target era: [decade]. Wardrobe, environment, and photographic quality changes implied by era. Facial identity frozen.
SEARCH: SKIP. (Active if historically accurate costume details require verification: "Search the web, today is [date]: wardrobe conventions in [decade].")
GENERATE: Using the uploaded [description], re-render as if photographed in [decade or era]. Update wardrobe, environment, and photographic quality to match that era. Preserve facial identity and overall composition. [Era-specific texture and color-grading notes].
VERIFY: Before showing output, verify era-appropriate wardrobe and environmental details are present. Verify facial identity is preserved.
```


## Texture or material transformation

```
PLAN: Element to transform: [element]. Current material: [material]. Target material: [marble, bronze, glass, ice, gold leaf]. Form and silhouette frozen.
SEARCH: SKIP.
GENERATE: Using the uploaded [description], transform [element] from [current material] to [new material]. Maintain the form and silhouette. Render realistic material properties: [surface detail, light response, edge quality].
VERIFY: Before showing output, verify material-specific surface detail and light response are present. Verify form and silhouette are intact.
```


## Relighting

```
PLAN: New lighting scheme defined. Key light direction, fill, rim behavior, color temperature, shadow character all stated before brief.
SEARCH: SKIP.
GENERATE: Using the uploaded [description], replace the existing lighting with [new scheme]. [Key light direction and quality]. [Fill and rim behavior]. [Color temperature]. [Shadow character]. Preserve subject and composition.
VERIFY: Before showing output, verify shadow direction is consistent with stated key light position. Verify color temperature shift is visible throughout the image.
```
