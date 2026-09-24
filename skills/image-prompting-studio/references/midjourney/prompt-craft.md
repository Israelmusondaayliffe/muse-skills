# Durable Midjourney prompt craft

Use this reference for visual decisions that remain useful across Midjourney versions. Read only the sections that match the request.

## Contents

- Prompt order
- Medium and mode
- Composition and action
- Light, atmosphere, and color
- Prompt length
- Variation
- References and exact text
- Palette contracts
- Exclusions
- Common failure modes

## Prompt order

Build outward from the image's identity:

1. Primary subject
2. Medium or production format
3. Defining action, pose, or state
4. Essential setting
5. Composition and camera placement when relevant
6. Light, atmosphere, and palette
7. Essential technical treatment

Use concrete visual nouns and verbs. Remove a phrase if it does not change the likely image.

## Medium and mode

For photography, name the photographic context when useful: documentary, editorial, studio product, environmental portrait, architectural, street, analog snapshot, or cinematic production still. Add lens, depth of field, focus, shutter character, grain, or color treatment selectively.

For illustration, name the actual medium: gouache, pen and ink, risograph, woodblock, watercolor, graphic novel, pixel art, editorial illustration, or mixed media. Use medium-native details such as paper texture, pigment, brushwork, ink weight, halftone, registration, or line hierarchy.

For graphic design, specify the artifact and hierarchy: poster, album cover, package, title card, identity mark, layout, negative space, typography placement, and print or screen finish.

Do not add publication, studio, artist, camera, or material references merely to make a prompt sound sophisticated.

## Composition and action

Make pose and movement visible. Replace vague emotion with posture, gaze, expression, camera distance, weather, negative space, or surface condition.

Useful framing choices include extreme wide, wide, medium, close-up, profile, three-quarter, high angle, low angle, overhead, first-person, or framed through foreground. Choose one primary framing idea instead of stacking incompatible camera directions.

Translate moving-camera language into a still-image result. For example, turn a tracking shot into profile framing with directional space, or a crane shot into a high-angle composition.

## Light, atmosphere, and color

Choose light for the requested meaning: flat overcast daylight, hard side sun, soft window light, direct flash, golden backlight, blue-hour ambience, neon practicals, harsh overhead light, volumetric light, or controlled studio light.

Use a clear palette or color relationship only when it helps the concept. Avoid generic cinematic language that does not produce an observable choice.

## Prompt length

- **Concise, roughly 15 to 35 words:** simple concepts, mood studies, minimal compositions, or prompts carried by references.
- **Controlled, roughly 35 to 70 words:** the default for most work.
- **Complex, roughly 70 to 110 words:** use only for essential spatial relationships, multiple subjects, detailed production design, or strict lighting.

Prefer one coherent sentence or compact phrase sequence. Long instructions and keyword inventories weaken priority.

## Variation

Honor the requested count. For alternatives, vary only the dimensions that serve the task. A controlled comparison can change one variable; an open interpretation can change several. Useful dimensions include:

- moment before, during, or after an action;
- framing, angle, or subject placement;
- light and weather;
- palette or surface treatment;
- lens character or depth of field for photography;
- mark-making or print behavior for illustration;
- restraint versus expressive energy.

Do not vary locked details. Do not invent unrelated locations, wardrobe, demographics, objects, or narrative events to manufacture difference.

## References and exact text

Treat an Image Prompt as guidance for content, composition, or color, not exact copying. Describe the intended final image directly.

Treat a Style Reference as aesthetic guidance. Keep competing style language simple. Preserve supplied URLs, codes, order, and weights exactly.

Treat personalization and moodboard identifiers as user-owned values. Never invent or shorten them.

Include visible wording only when requested. Put the exact text in double quotation marks, state where it appears, and preserve spelling, accents, punctuation, and capitalization.

## Palette contracts

Treat an approved palette contract as visual authority, not a decorative list. Preserve named colors and exact values, then translate the contract's role relationships into observable choices such as dominant field, supporting surface, highlight, shadow, or small accent.

Use color names and material or lighting behavior in the prompt. Include exact hex values only when the contract or user requires them. Do not replace a locked palette merely to create variation. Vary the balance, placement, light, or material expression of approved colors instead.

Read `palette-contract.md` for intake, authority, and missing-source rules.

## Exclusions

Describe the desired state positively when possible. Use a supported exclusion parameter only for a small, essential exclusion. Avoid conversational instructions such as "please do not include" inside the image description.

## Common failure modes

- Repeating the same composition with cosmetic adjective changes
- Overwriting a user's locked detail to make a prompt more dramatic
- Adding camera language to an illustration without a photographic intent
- Treating a style reference as a content-copy command
- Inventing reference codes, personalization IDs, URLs, or visible text
- Forcing maximum parameter values into ordinary work
- Adding a model version or costly mode without a reason
- Relying on remembered compatibility instead of the current profile
- Producing a keyword pile instead of a coherent image
