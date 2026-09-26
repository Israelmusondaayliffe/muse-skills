# Visual direction guide

Choose exactly one visual direction for the build, or none. Multiple broad
style directions loaded at once produce conflicting defaults, so never mix
them — select one, record the rejected alternatives, and keep everything else
out of the implementation context.

## When to select none

Select none when a supplied screenshot, an established design system, or an
already-approved product reference controls the visual system. In that case
preserve its information hierarchy and derive tokens (type scale, spacing,
color, radius) from the source before adding anything new.

## Candidate directions

Describe the chosen direction as a short named statement plus the concrete
tokens it implies. Examples (not an exhaustive list — name whatever fits):

- **minimalist / content-first**: restrained hierarchy, generous whitespace, quiet typography. Fits dense operational tools and content sites.
- **premium editorial**: strong type contrast, asymmetric grids, serif display paired with a neutral sans. Fits brand pages and marketing.
- **brutalist / raw**: high contrast, exposed structure, mechanical details. Fits creative or technical audiences that want edge.
- **warm crafted**: soft radius, organic texture, human tone. Fits consumer products, community, food, wellness.
- **dark immersive**: deep surfaces, luminous accents, cinematic lighting. Fits media, gaming, AI products.

If the user explicitly names a style, honor it unless it conflicts with a
higher-priority project contract (supplied reference, locked visual contract).

If no direction fits, select none and derive tokens from the supplied brand
or product reference instead of inventing a mood.

## Record

Fill `assets/route-template.json`'s `design_constitution` field with the
selected direction name or `null`. Record `selected`, `evidence`, `rationale`
and `rejected` in a selection file shaped like `assets/selection-template.json`,
then run `python3 scripts/validate_selection.py selection.json`.

Recheck the rendered product against the selected direction and the source
brief before delivery.
