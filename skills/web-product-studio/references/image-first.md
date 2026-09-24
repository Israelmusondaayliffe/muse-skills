# Image-first web design

For visually important web tasks — heroes, landing pages, marketing sites,
brand pages, portfolios — generate design comps first, analyze them deeply,
then implement. Do not start with freeform coding. The generated images are
the primary visual source of truth.

Required order: **generate comps → deep analysis → implementation.**

## Baseline configuration

Use these defaults unless the user clearly wants something else:

- **Design variance 8/10** (art-directed, asymmetric) — break centered-dark-hero defaults.
- **Visual density 3/10** (airy) — readability beats packing.
- **Art direction 8/10** — bold but codeable.
- **Implementation clarity 9/10** — every comp must be buildable UI, not mood art.
- **Image-led 9/10** when appropriate.
- **Spacing generosity 9/10** — breathe.
- **Analysis precision 10/10** — extract real design detail, not vibes.
- **Image count eagerness 10/10** — generate as many images as needed; never compress multiple sections into one.
- **Simplicity discipline 9/10** — aggressively cut clutter, tiny pills, fake chrome.

If the user says "clean", reduce density. "Premium SaaS" → controlled art direction, high clarity. "Editorial" → stronger type, more asymmetry.

## One image per section (hard rule)

- 1 section → 1 image. 4 sections → 4 images. 8 sections → 8 images.
- "Landing page" with no count → 6 sections → 6 images. "Full website template" → 8 sections → 8 images.
- Never combine multiple sections into one frame. Never return one tall image of the whole page.
- Prefer large, readable, section-specific images. Generate fresh images for detail views instead of cropping old ones.
- Announce each ("Section 1 of 6: Hero", "Section 2 of 6: Trust bar", ...).

Generate comps with your image generation capability (the `media` namespace).
Keep a shared narrative concept, second-read details, and one consistent
palette across all sections so the design can be recreated in code.

## Hero composition bias

The default left-text / right-image hero is the most overused AI pattern —
allowed, but not the first instinct. Consider first: centered over background
image, bottom-left or bottom-right over image, top-left lead, stacked center,
image-as-canvas, off-grid editorial, mini minimalist, or right-text /
left-image. Use left-text / right-image only when it is genuinely strongest.

Keep the hero clean, spacious, and readable on a small laptop viewport:
one clear headline, one supporting line, one or two actions, and room to
breathe. Too much information in the first screen is the classic failure.

## Default traps to break

Single giant compressed image for many sections · unreadably small text ·
centered dark hero clichés · generic card spam (especially cards inside cards
inside cards) · repeated left-text/right-image layouts · weak type hierarchy ·
vague spacing · giant rounded containers everywhere · tiny pills, labels, and
fake interface jargon · designs that look nice but can't be extracted into
code · generic coded reinterpretations after the image step.

## Analysis before building

For each comp, extract before writing any code:

1. **Layout** — grid, section rhythm, alignment, spacing scale.
2. **Typography** — families, sizes, weights, tracking, line-height, hierarchy.
3. **Color** — exact palette: surfaces, text, one accent (saturation under 80%).
4. **Imagery** — placement, treatment, crops, overlays.
5. **Components** — buttons, nav, cards, badges: shapes, radii, borders, shadows.
6. **Motion cues** — what implies movement or state change.
7. **Responsive spirit** — how the section should collapse on mobile.

Only then implement, matching the analyzed comps as closely as possible.
If the picture is load-bearing (likeness, realism, reference match), the
visual-fidelity gate applies — see the main SKILL.md workflow.
