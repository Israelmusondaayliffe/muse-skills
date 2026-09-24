# General prompt recipes

Preserved recipe structures. The shared prompt contract governs count, format and current reference intent. Adapt example pose/ratio/search instructions to the actual request.


## Planning Block

```
DIVERSITY PLAN:
User intent: [what they asked for]
Diversity mode: [OPEN / DIRECTED / PARTIALLY DIRECTED]
Strategy: [which categories to span, or how to vary within the directed dimension]

1. [Concept] — SAFE
2. [Concept] — INVENTIVE
3. [Concept] — INVENTIVE
4. [Concept] — INVENTIVE
5. [Concept] — BOLD
6. [Concept] — BOLD
7. [Concept] — BOLD
8. [Concept] — EXPERIMENTAL
9. [Concept] — EXPERIMENTAL
10. [Concept] — EXPERIMENTAL

Anti-sameness check: No two prompts feel like the same shoot ✓
Anti-paste check (if editing): Style transforms include pose/angle shift (or are exempt) ✓
```


## Photorealistic Scenes

```
A photorealistic [shot type] of [subject], [action or expression], set in [environment]. The scene is illuminated by [lighting description], creating a [mood] atmosphere. Captured with a [camera/lens details], emphasizing [key textures and details]. The image should be in a [aspect ratio] format.
```


## Stylized Illustrations & Stickers

```
A [style] sticker of a [subject], featuring [key characteristics] and a [color palette]. The design should have [line style] and [shading style]. The background must be [transparent/white].
```


## Text in Images

```
Create a [image type] for [brand/concept] with the text "[EXACT TEXT TO RENDER]" in a [font style]. The design should be [style description], with a [color scheme].
```


## Product Mockups

```
A high-resolution, studio-lit product photograph of a [product description] on a [background surface/description]. The lighting is a [lighting setup] to [purpose]. The camera angle is a [angle type] to showcase [specific feature]. Ultra-realistic, with sharp focus on [key detail]. [AR].
```


## Minimalist & Negative Space

```
A minimalist composition featuring a single [subject] positioned in the [position] of the frame. The background is a vast, empty [color] canvas, creating significant negative space. Soft, subtle lighting. [AR].
```


## Sequential Art / Comic Panels

```
Make a [number] panel comic in a [art style]. Put the character in a [type of scene].
```


## Adding/Removing Elements

```
Using the provided image of [subject], please [add/remove/modify] [element] to/from the scene. Ensure the change is [integration description].
```


## Inpainting / Semantic Masking

```
Using the provided image, change only the [specific element] to [new element/description]. Keep everything else exactly the same, preserving original style, lighting, and composition.
```


## Style Transfer

Historical source recipe below combines a pose change with composition preservation. For a faithful conversion, omit the pose-change clause. For a creative re-shoot, describe the new composition instead of retaining the contradictory preservation clause.

```
Transform the provided photograph of [subject] into the artistic style of [artist/art style]. [ANTI-PASTE: recompose with new angle/pose]. Preserve the original composition but render it with [stylistic elements].
```


## Multi-Image Composition

```
Create a new image by combining elements from the provided images. Take the [element from image 1] and place it with/on the [element from image 2]. The final image should be a [scene description].
```


## Search-Grounded Generation

```
[Request for visualization] based on [real-time data topic]. Include [specific data points to look up].
```


## Faithful style-transfer variant

```
Transform the supplied photograph of [visible subject and recognition anchors] into [target illustration medium or supplied style reference]. Preserve the subject, action, framing, color relationships and world identity. Translate surfaces, edges, shading and detail into the target medium's visual language. Keep [specific distinctive feature] recognizable. [Requested aspect ratio].
```

## New-shot style-transfer variant

```
Use the supplied reference of [subject and recognition anchors] to create a new [target medium] image from [new viewpoint]. Develop the pose, gaze and visible lighting naturally for this shot while retaining [character/object/world anchors]. Compose the new frame around [purpose]. Render with [line, material, color and texture treatment]. [Requested aspect ratio].
```
