# templates recipes

These are preserved prompt recipes from the source skill. Read the relevant example, then adapt its subject, count, references, format and requested change to the current brief. Concrete counts, aspect ratios, media and named model settings in examples are recipe values, never studio defaults. A prompt field such as `controlnet`, `recommended_weight`, `quality`, `system` or `search` is descriptive text unless the selected host exposes a matching real control. The current skill and shared prompt contract govern execution. Some historical examples contain pose shifts, fixed counts or search calls; use those only when the current request calls for them. Attribution remains source-recorded unless separately verified.


## Template 1: Fast Start

```
A [subject], in [style], with [lighting], [camera/composition], [environment/background], mood: [emotion], details: [key specifics]
```


## Template 1: Fast Start

```
A ceramic artist shaping a lopsided bowl, documentary photography style, soft window lighting, close-up shot, cluttered home studio background, mood: focused and quiet, details: clay-covered hands, imperfect texture, tools scattered on wooden table
```


## Template 2: Cinematic Control

```
Subject: [who/what]

Style: [editorial / documentary / fine art / etc.]

Scene:
- Environment: [where]
- Time of day: [lighting context]
- Mood: [emotional tone]

Camera:
- Shot type: [close-up / wide / overhead]
- Lens: [35mm / 85mm / etc.]
- Composition: [framing approach]

Details:
- Textures: [materials]
- Motion: [if any]
- Extra: [small details that matter]
```


## Template 2: Cinematic Control

```
Subject: A street tailor repairing a jacket

Style: documentary photography

Scene:
- Environment: sidewalk workshop with hanging fabrics
- Time of day: late afternoon natural light
- Mood: patient, intimate

Camera:
- Shot type: medium close-up
- Lens: 50mm
- Composition: slightly off-center, hands in focus

Details:
- Textures: worn fabric, frayed edges, thread spools
- Motion: subtle hand movement mid-stitch
- Extra: pins in mouth, chalk markings on fabric
```


## Template 3: Direct Edit (Modify Mode)

```
Edit instructions:
- Change: [what to modify]
- Keep: [what must stay the same]
- Style shift: [optional]
- Lighting: [optional]
- Details: [specific adjustments]
```


## Template 3: Direct Edit (Modify Mode)

```
Edit instructions:
- Change: replace background with a quiet bookstore interior
- Keep: subject posture, clothing, and facial expression
- Style shift: slightly more warm and nostalgic
- Lighting: soft golden indoor lighting
- Details: add bookshelves with uneven stacks and handwritten notes
```


## Template 4: Multi-Reference Fusion

```
Combine the following:

IMAGE 1: [what it provides]
IMAGE 2: [what it provides]
IMAGE 3: [optional]

Output:
- Subject: [final image goal]
- Style: [dominant style]
- Composition: [layout guidance]
- Details: [specific merges]
```


## Template 4: Multi-Reference Fusion

```
Combine the following:

IMAGE 1: a vintage portrait (use for pose and framing)
IMAGE 2: a modern fashion editorial (use for styling and lighting)
IMAGE 3: textured paper background (use for surface quality)

Output:
- Subject: a contemporary portrait with vintage posture
- Style: editorial with subtle retro influence
- Composition: centered subject, clean framing
- Details: blend modern clothing with aged texture finish
```


## Template 5: Layout Control

```
Layout instructions:

[LEFT]: [object + description]
[CENTER]: [object + description]
[RIGHT]: [object + description]
[BACKGROUND]: [environment]

Style: [style]
Lighting: [lighting]
```


## Template 5: Layout Control

```
Layout instructions:

LEFT: a stack of handwritten letters tied with string
CENTER: a wooden desk with an open notebook
RIGHT: a cup of tea with steam rising
BACKGROUND: softly lit room with a window

Style: still life photography
Lighting: soft morning natural light
```


## Template 6: Storyboard Generator

```
Create a storyboard with [X] frames.

Story:
[short narrative]

Frame details:
1. [scene]
2. [scene]
3. [scene]

Style: [style]
Consistency: same characters and setting
```


## Template 6: Storyboard Generator

```
Create a storyboard with 4 frames.

Story:
A baker wakes up early to prepare bread for the day.

Frame details:
1. Dim kitchen, flour being poured
2. Hands kneading dough on wooden surface
3. Oven light glowing with rising bread
4. Morning customers entering small bakery

Style: warm, documentary realism
Consistency: same space and character throughout
```


## Template 7: Loose / Creative Mode

```
[vibes, fragments, ideas, emotions]
```


## Template 7: Loose / Creative Mode

```
quiet morning, dust in sunlight, old apartment, slightly messy, books everywhere, slow life, soft textures, calm, lived-in feeling
```


## Template 8: Structured JSON

```json
{
  "subject": "",
  "style": "",
  "environment": "",
  "lighting": "",
  "camera": {
    "shot": "",
    "lens": "",
    "composition": ""
  },
  "details": []
}
```


## Template 8: Structured JSON

```json
{
  "subject": "elderly man repairing a watch",
  "style": "fine art photography",
  "environment": "small workshop filled with tools",
  "lighting": "soft directional window light",
  "camera": {
    "shot": "close-up",
    "lens": "85mm",
    "composition": "tight framing on hands"
  },
  "details": ["tiny screws", "dust particles", "aged skin texture"]
}
```
