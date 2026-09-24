# Task: Illustration ↔ photo translator (faithful conversion)

Scope: illustration-to-photo or photo-to-illustration prompts that preserve a reference character, object or world. Support both directions equally; the reference takes priority over a generic realism recipe.

Read first: `../prompt-contract.md`. When a model is named, consult only its entry in `../model-profiles.md`.

## Translate the visual idea

1. Inspect every reference used. Identify what gives the subject its visual identity: defining shapes and proportions, expression or attitude, materials, color relationships, props, composition, mood, the world's rules. Use a supplied illustration-style reference for its assigned treatment; keep content and style roles clear.
2. Illustration → photo: translate edges, marks, flat fills and simplified depth into a coherent photographic treatment. Preserve stylized proportions and fictional premises when they define the subject — a strange character or impossible world can still have believable materials and light.
3. Photo → illustration: translate observed form and atmosphere into the target's mark-making, shape language, palette, texture and depth. Preserve the content's identity without demanding every pore or photographic shadow survive unchanged.
4. Use judgment for ambiguous details and backgrounds: make the smallest useful interpretation, or offer a few faithful treatments when the direction is open. Do not require an intake taxonomy, score fidelity numerically, default every conversion to fashion, or force pose changes. Obey requested count and format.

## Recipes

Read `../recipes/illustration_photo_translator/two-way-methods.md` for character, object and world handling in NL, JSON and system-style forms. `original-human-conversion-templates.md` preserves a detailed one-way source for cases where it fits; its human fields and restrictive realism choices are not a universal contract.

Return complete copyable prompts, with concise interpretation notes only when they help. If outputs are supplied, compare recognizability and medium translation to the actual reference and describe meaningful drift. Do not declare a preferred recipe or creative acceptance for the user.
