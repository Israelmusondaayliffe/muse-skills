# Palette contract intake

Use this adapter only when the user supplies a palette contract, a contract file, or a canonical pointer owned by the relevant project.

## Accepted input

Read JSON, YAML, Markdown, or structured text that identifies some or all of:

- palette or collection name;
- named colors and exact values;
- roles such as dominant, support, highlight, shadow, neutral, or accent;
- approved pairings, proportions, contrast rules, materials, or lighting behavior;
- forbidden substitutions or combinations;
- provenance and the contract's authority level.

Treat explicitly approved fields as locked. Preserve exact color names and values. If the contract has no role mapping, use the colors without inventing a hierarchy and state the assumption outside the prompt only when consequential.

## Prompt mapping

Translate the contract into observable color behavior:

- name the dominant field or material;
- assign supporting colors to surfaces, wardrobe, environment, or light;
- reserve accents at the stated scale;
- preserve approved contrast and temperature relationships;
- vary placement, balance, atmosphere, or material response without leaving the palette.

Prefer meaningful color language over dumping a sequence of hex codes. Include exact values only when the user or contract requires them.

## User-selected palette sources

Use a palette library (for example a Sanzo Wada combination set) only when the user or project selects it. Obtain its exact palette data and reference image from that source; do not invent URLs, combination numbers, or a publisher-owned palette by default. Preserve the contract's color names, values, roles and proportions.

For an image-reference recipe, when explicitly selected:

1. Read the palette data and preserve its exact identifier, color names, hex values, and any supplied prompt recipe.
2. Put the corresponding reference image URL before the Midjourney text prompt as an Image Prompt when the source supplies one.
3. Translate the named colors into observable materials, surfaces, atmosphere, and light without adding unrelated hues.
4. Keep the same palette across prompt variations unless the user explicitly chooses palette as the variation axis.
5. Validate that the palette data and reference image identify the same combination.

This is an optional resource alongside current supplied brand colors and free color exploration. State a selected combination identifier only after it is verified against the source.

If the selected source cannot be read, use any exact supplied palette data and identify unverified fields. A prompt that does not need that specific combination can continue with its supplied or openly proposed color direction. Never invent a combination or URL.
