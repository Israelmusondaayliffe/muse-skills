# Dated V8.2 edit model baseline

Source baseline checked: September 1, 2026. Retained for historical examples; not reverified during extraction. Read `../../../references/model-profiles.md` for shared current guidance. Check current model support before including version-sensitive prompt parameters.

Use official Midjourney documentation and update posts as the authority for current capability. Use community tests as dated operational evidence, not permanent product truth.

## Officially documented baseline

At the last check:

- V8.2 is the current default model.
- V8.2 became the default on July 24, 2026.
- The Edit Model public test was announced on August 27, 2026.
- An Edit Model image-quality update was announced on August 29, 2026.
- The Edit Model works with V8.1 and V8.2.
- It can edit an existing image from written instructions.
- It can create new images from up to four Edit Model references.
- It replaces Omni Reference and Character Reference for V8.X.
- It supports inpainting and outpainting through the Editor.
- It can be combined with Image Prompts, Style References, Moodboards, Personalization, `--hd`, and `--raw`.
- The main Midjourney site and Alpha site both expose the new workflow.
- Raw can give prompt text more influence by reducing Midjourney's added creative interpretation.

## Field-tested observations supplied by the user

Treat these as provisional:

- `remove`, `replace`, `add`, `change`, `surrounded by`, profile, and directional instructions often work.
- Natural-language `no` statements often work without relying only on `--no`.
- A detail can often be removed without using the erase tool.
- The source aspect ratio is often retained unless another ratio is requested.
- Character consistency may fall when environment, pose, or action changes.
- Character style may drift during those same changes.
- Added objects may render in a different style.
- Using the source image again as a Style Reference may improve cohesion.
- Multiple selected regions may produce the wrong count or place objects outside the regions.
- Manual aspect-ratio changes can still stretch, crop, or deform the image.

Because the August 29 quality update came after the initial release, retest failure cases before treating them as stable limitations.

## Claims not established by official documentation

Do not state these as facts:

- that the model is a specific transformer or diffusion architecture;
- that it performs a literal internal semantic diff;
- that the first reference automatically receives more weight;
- that reference order is equivalent to a hidden `--ow`;
- that `--sref`, `--p`, or prompt order creates deterministic identity strength;
- that natural-language preservation words create a hard lock.

Use anchor, delta, and role order as prompting methods only.

# Reference and parameter matrix

## Edit Model reference

Web:

- Place one to four images in Attach to prompt.
- Use visible role descriptions in the text prompt.
- No URL syntax is needed in the prompt.

Discord:

```text
[instruction] [other parameters] --edit <url1> <url2> <url3> <url4>
```

Prompt text comes before `--edit`.

Do not use:

```text
--edit <urls> [instruction]
```

## Style Reference

Syntax:

```text
--sref <url or code>
```

Role:

- palette;
- medium;
- texture;
- light;
- grain;
- rendering character.

It does not provide identity control.

## Style Weight

Syntax:

```text
--sw <0-1000>
```

Role:

- strength of Style Reference only.

Default:

- 100.

Restrictions:

- not edit strength;
- not identity strength;
- not compatible with Moodboards.

## Personalization and Moodboards

Syntax:

```text
--p
--p <profile code>
--p <moodboard code>
```

Use only when the learned aesthetic should influence the edit.

The Stylize value affects the influence of Personalization and Moodboards.

Moodboards are not compatible with `--sw` or `--sv`.

## Raw

Syntax:

```text
--raw
```

Use for:

- precision;
- identity-sensitive work;
- geometry preservation;
- short direct instructions;
- recovery from over-interpretation.

Raw is not a fidelity guarantee.

## Aspect ratio

Syntax:

```text
--ar W:H
```

Use only when a new ratio is wanted.

When changing ratio:

- state which sides gain new content;
- ask to preserve the original subject scale and proportions;
- state no stretch, squeeze, crop, or recentering;
- prefer the web Editor's resize and canvas tools;
- make extreme changes in smaller steps.

## HD

Syntax:

```text
--hd
```

Use when higher-resolution V8.X output is requested or beneficial.

Inspect the current surface because editing, upscaling, and HD behavior may change.

## No

Syntax:

```text
--no <elements>
```

Use as a supplemental exclusion. Keep edit-specific exclusions in natural language.

Example:

```text
Remove the wall sign and reconstruct the brick behind it. Do not replace it with text or decoration. --no signage typography
```

## Seed

Syntax:

```text
--seed <number>
```

Use for controlled A/B tests where one wording or parameter changes.

Do not promise exact repetition.

## Stylize

Syntax:

```text
--s <0-1000>
```

Role:

- Midjourney stylization;
- Personalization or Moodboard influence.

It is not edit strength. Avoid fixed values for every task.

## Image Weight

Syntax:

```text
--iw <value>
```

Use only if a separate Image Prompt is intentionally present.

Do not apply it to Edit Model references.

## Optional creative controls

`--c`, `--w`, and experimental aesthetic controls should be omitted in precision edits.

Use them only for deliberate exploration or retexturing, and only after verifying current Edit Model compatibility on the target surface.

## Unsupported or obsolete for V8.2 Edit Model workflows

Do not generate:

- `--oref`;
- `--ow`;
- `--cref`;
- `--cw`;
- `--q`;
- `--draft`;
- text-concept multi-prompt weights using `::`;
- invented Edit Model weights.

Individual Style Reference weighting is a separate feature. Do not confuse it with text multi-prompting or Edit Model reference weighting.

# Surface-specific output

## Web default

When the platform is unspecified, default to the web workflow.

Output:

1. one short attachment-role line when multiple images are used;
2. prompt text without image URLs;
3. only purposeful parameters.

Example setup:

`Attach as Edit Model references in this order: base portrait, red jacket, alley environment. Use the portrait again as a Style Reference only if source-style drift appears.`

Example prompt:

```text
Place the woman with short black curls from the portrait reference in the rain-soaked alley, wearing the red leather jacket from the garment reference. Preserve her face shape, skin tone, hairstyle, body proportions, and earrings. Keep the alley geometry and wet-pavement reflections from the environment reference. Match perspective, scale, contact, cool neon light, and 35mm grain without exchanging features between references. --raw --ar 4:5 --v 8.2
```

## Discord

Example:

```text
Place the woman with short black curls from the portrait reference in the rain-soaked alley, wearing the red leather jacket from the garment reference. Preserve her face shape, skin tone, hairstyle, body proportions, and earrings. Match perspective, scale, wet-pavement reflections, cool neon light, and 35mm grain without exchanging features between references. --raw --ar 4:5 --v 8.2 --edit <portrait_url> <jacket_url> <alley_url>
```

# Refresh rule

Recheck official sources after:

- a V8.2 Edit Model update;
- a new default model;
- reference-system changes;
- parameter compatibility changes;
- changes to Personalization, Moodboards, or Style References;
- changes to HD, upscaling, inpainting, or outpainting.

Official source set:

- Edit Model;
- Version;
- Editor;
- Modifying Your Creations;
- Creating on Web;
- Style Reference;
- Moodboards;
- Personalization;
- Raw;
- Aspect Ratio;
- Parameter List;
- Edit Model for V8 announcement;
- Edit Image Quality Update.

When official documentation conflicts with field notes, follow the current official capability boundary and retain the field note only as a dated troubleshooting heuristic.
