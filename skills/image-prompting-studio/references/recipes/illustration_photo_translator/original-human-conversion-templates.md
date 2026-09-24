# Original human illustration-to-photo forms

Load this detailed historical form only for a human-centered conversion where it helps. All fenced text is preserved verbatim. Its seven-prompt context, human-only fields, fixed scene/camera locks and prohibitions on impossible anatomy, fantasy light, CGI or other treatments do not override the active two-way method or the source design. Preserve defining stylized proportions and fictional premises. Adapt fields to the actual character, object or world; retain the reference-first craft rather than blindly applying every negative item.

## Required analysis before prompting (source block 1)

```
REFERENCE LOCK: [subject, pose, wardrobe, accessories, palette, framing, scene logic]
REALITY TRANSLATION: [anatomy, materials, garment construction, environment, light, lens, photographic texture]
```

## JSON envelope template (source block 2)

```json
{
  "plan": "Faithful illustration-to-photo conversion. Preserve the depicted subject and composition by visual equivalence while replacing all drawn abstraction with plausible photographic reality.",
  "search": null,
  "reference_lock": "Using the uploaded illustration of [specific subject description], preserve [identity cues], [pose and action], [body orientation], [wardrobe and exact color relationships], [accessories and props], [framing and negative space], and [scene logic].",
  "subject": "Render the same depicted subject as a believable real person. Translate simplified facial and anatomical cues into plausible human detail without changing apparent age range, presentation, complexion cues, hair, facial hair, eyewear, build, or character read.",
  "pose": "Preserve the illustrated stance or gait phase, head direction, gaze, hand placement, held objects, and direction of travel. Resolve impossible drawn geometry only as much as physical plausibility requires.",
  "wardrobe": "Reconstruct every visible garment and accessory as a real, wearable object. Preserve garment category, layering, silhouette, length, fit, dominant color, color blocking, and visual role. Add only construction details required by reality, such as seams, folds, closures, fabric thickness, and material response.",
  "environment": "Translate the illustrated setting into the simplest believable real location that preserves the original background tone, spatial simplicity, ground plane, and negative space. Do not add narrative clutter.",
  "camera": "[Photographic treatment for this variation]. Preserve source aspect ratio, subject scale, placement, direction, crop, and approximate camera height.",
  "lighting": "Use coherent real-world light with dimensional form, contact shadows, and material-specific highlights. Preserve the source's overall tonal hierarchy and mood.",
  "style": "A genuine photograph, not an illustration and not a 3D render. Natural skin, hair, fabric, leather, rubber, metal, wall, and pavement detail as applicable. [Named documentary, editorial, filmic, or other photographic treatment].",
  "palette": "Preserve the source's dominant color relationships and garment color blocking. Translate flat fills into plausible real materials without unnecessary recoloring.",
  "quality": "Photographically credible anatomy, garment construction, texture, optical depth, edge behavior, and environmental integration. Retain natural irregularity. Avoid synthetic polish.",
  "aspect_ratio": "Match the uploaded illustration.",
  "verify": [
    "the output reads immediately as a real photograph",
    "the depicted subject remains recognizable through identity cues, silhouette, pose, wardrobe, accessories, and color relationships",
    "the source composition, direction, crop, and negative space remain intact",
    "all drawn marks and flat graphic surfaces have become plausible real-world forms and materials",
    "no unrequested redesign, beautification, prop, or narrative detail has been introduced",
    "none of the forbidden failure classes are present"
  ],
  "negative_prompt": {
    "forbidden": [
      "remaining illustration, line art, drawn outlines, flat vector fills, halftone, paper grain, or sketch texture",
      "cartoon-photo hybrid or illustrated face on a photographic body",
      "3D render, CGI, game character, plastic skin, wax figure, doll, figurine, or mannequin appearance",
      "cosplay interpretation instead of the same depicted subject translated into reality",
      "generic fashion model or unrelated person replacing the illustrated subject",
      "identity normalization, beautification, age shift, complexion shift, facial hair loss, hairstyle change, or body-type averaging",
      "literal tracing of impossible illustrated anatomy or garment geometry",
      "pose restaging, gait change, gaze change, hand-position change, or direction-of-travel reversal",
      "wardrobe redesign, changed layering, changed hem lengths, color substitution, or accessory loss",
      "dropped, replaced, or invented held objects and props",
      "changed framing, subject scale, camera height, crop, aspect ratio, or negative-space structure",
      "busy set dressing or added story elements absent from the reference",
      "photo textures pasted inside illustrated shapes without full three-dimensional reconstruction",
      "glossy commercial retouching, HDR, excessive sharpness, cinematic spectacle, or fantasy lighting unless requested",
      "before-and-after split screen, diptych, captions, labels, watermark, or explanatory text unless requested"
    ]
  }
}
```

