# Two-way translation methods

## Read content and treatment together

The reference may depict a person, creature, product, sculpture, vehicle, room, landscape or an invented world. Recognize its design language before choosing a treatment. Several supplied images may show the intended correspondence; study the relationship, not just isolated traits. A reference pair is guidance for judgment, not a requirement that every later subject use the same coat, palette, pose or background.

A content reference supplies what is depicted. A target-style reference supplies how the new image is drawn, painted or photographed. If their roles are unclear but compatible, make a sensible interpretation. Ask only when a material conflict cannot be resolved from context.

## Illustration to photo

Translate flat color into suitable material response; drawn contours into edges, seams, folds, shadows or occlusion; simplified planes into coherent light and depth. The image should read as the same depicted thing photographed within its world. Avoid a photographic background with the original drawing pasted on it unless that hybrid is requested.

Retain meaningful exaggeration: an oversized silhouette stays oversized, a miniature world stays miniature, a long-limbed creature keeps its defining proportions. Do not automatically replace stylization with an averaged human, product or environment. Add construction or surface detail where it helps the treatment, without redesigning the subject.

A blank background can become a studio field, a simple real surface or an understated location whose tone/space fits the source. Several faithful interpretations may be useful. Do not fill quiet space with new narrative clutter. Infer photographic treatment from the source and request, not a mandatory documentary or glossy-fashion default.

## Photo to illustration

First inspect a supplied target illustration reference for contour, shape simplification, proportions, palette, mark-making, texture, edge treatment and spatial depth. Flat vector, textured thick-outline drawing, watercolor, woodcut and painterly work preserve likeness through different means.

Simplify rather than merely posterize when the target calls for simplification. Preserve recognizable silhouettes, relationships, important details and mood. Convert textures into medium-appropriate marks; use color relationships rather than mechanically sampling every photographic tone. Keep scene/world identity through landmarks and spatial logic even when perspective becomes flattened or expressive.

A style change does not require a new pose. Recomposition is appropriate when requested or when the user has opened the interpretation, not a default proof that illustration is authentic.

## Character, object and world judgment

**Character:** retain defining facial/design cues, hair or facial hair, headwear, distinctive body shape, silhouette, gesture and important accessories where visible. Preserve meaningful age/design cues without identifying a real person. An unclear eye or hidden garment may require a plausible choice; do not claim it is observed.

**Object:** retain overall form, dimensions relative to visible parts, component placement, markings, material distinctions, color blocking and functional features. Translate outlined glass, metal or fabric through appropriate surface behavior. Do not turn an unusual designed object into a conventional product.

**World:** retain landmarks, geography, architecture, scale relationships, atmosphere, palette and fictional rules. Reconstruct only the depth or hidden space needed for the view. Do not normalize fantasy architecture or add unrelated scenic spectacle.

## Natural-language working form

```text
Using the supplied [reference description] as the content source, translate this [character, object or world] into [photography / the requested illustration treatment]. Preserve its recognizable [forms, proportions, defining details, color relationships, mood and scene identity]. Use [supplied style-reference description / chosen treatment] for [material or mark-making, edges, depth and light]. Keep [composition or action that matters]; interpret [open or ambiguous detail] in a way that fits the source. The result should feel native to the target medium while remaining the same depicted subject or world. [Requested ratio and output form].
```

## JSON working form

Use JSON when requested or helpful to organize complex correspondence. These are prompt fields, not assumed provider API parameters. Keep only relevant fields when adapting.

```json
{
  "plan": "Translate the reference into the target medium while retaining its recognizable character, object or world.",
  "source": "[Concrete description of the supplied content reference]",
  "target_medium": "[Photography or specific illustration treatment]",
  "style_reference": "[Supplied style reference and its assigned role, or the chosen interpretation]",
  "preserve": "[Defining shapes, proportions, details, color relationships, mood and world identity]",
  "translate": "[How source edges, textures, materials, depth and light become native to the target medium]",
  "composition": "[Source composition retained or requested change]",
  "interpretation": "[Only the ambiguous or unspecified details that need a creative choice]",
  "output": "[Requested ratio, count and separate-images or composite form]",
  "review_intent": "Compare recognizability and the medium translation to the source; identify material drift when outputs are available."
}
```

## System-style working form

Use for a reusable session when requested. Fill project-specific anchors before delivering it; this template does not require another skill or hidden file.

```text
You translate reference imagery between illustration and photography. For each request, inspect the supplied content and style references and follow their assigned roles. Preserve the recognizable character, object or world, including meaningful stylized proportions and fictional premises. Translate materials, edges, mark-making, light and depth into the requested medium. Follow explicit count, format and composition choices. Use the target-style reference first; when treatment is open, make a sensible faithful interpretation or offer useful alternatives. Do not force a pose change, a human subject, a fashion treatment or numerical fidelity scoring. Return complete copyable prompts. When outputs are supplied, describe observed correspondence and drift; the user makes the final creative selection.
```

## Review without a score

Does the same subject/world remain recognizable? Does the target treatment carry the reference's mood and design language? Has the conversion silently replaced a defining form, color relationship, prop or landmark? Are photographic surfaces or illustrative marks coherent for the intended treatment? Explain the meaningful difference and suggest a focused prompt repair. A check cannot guarantee a perfect output.
