# agent-multi-output recipes

These are preserved prompt recipes from the source skill. Read the relevant example, then adapt its subject, count, references, format and requested change to the current brief. Concrete counts, aspect ratios, media and named model settings in examples are recipe values, never studio defaults. A prompt field such as `controlnet`, `recommended_weight`, `quality`, `system` or `search` is descriptive text unless the selected host exposes a matching real control. The current skill and shared prompt contract govern execution. Some historical examples contain pose shifts, fixed counts or search calls; use those only when the current request calls for them. Attribution remains source-recorded unless separately verified.


## Template

```
MULTI-OUTPUT SYSTEM BRIEF

[SUBJECT & CONTEXT]
Subject: [Name and type: brand, product, event, IP, character]
Description: [What it is, what it does, what it stands for. 1-3 sentences.]
Key text: [Exact name, tagline, or line that must appear verbatim in relevant pages]

[VISUAL DNA]
Reference: [Attached images described / or stated visual world if no uploads]
Palette: [Primary color, accent color, secondary tones, name each]
Treatments: [Textures, grain, glitch, compositional devices, be specific]
Subject matter: [What imagery lives in this world: botanical, architectural, portrait, product, etc.]
Mood: [2-4 descriptors]

[PAGE INVENTORY]
Deliver each of the following as a separate image:
1. [Page type]: [specific content: exact text in quotes, key elements, layout intent]
2. [Page type]: [specific content: exact text in quotes, key elements, layout intent]
3. [Page type]: [specific content: exact text in quotes, key elements, layout intent]
4. [Page type]: [specific content: exact text in quotes, key elements, layout intent]
5. [Page type]: [specific content: exact text in quotes, key elements, layout intent]
6. [Page type]: [specific content: exact text in quotes, key elements, layout intent]
7. [Page type]: [specific content: exact text in quotes, key elements, layout intent]

[CONSISTENCY BACKBONE]
Visual DNA held across all pages: [which elements must appear in every image]
Color rules: [which colors are permitted and their roles]
Background default: [base surface across all pages]
Treatment rule: [which texture or effect is mandatory on every page]

[VERIFY]
Verify all text is correctly spelled before output.
Verify [key name or text] appears correctly in every page that includes it.
Verify visual DNA is consistent across all pages before output.
```


## System prompt (single batch submission)

```
Generate [N up to 8] separate images as a coordinated multi-page system for [SUBJECT NAME, type]. All [N] share one visual DNA backbone. Each image is a distinct page type. Visual DNA, palette, treatment, mood hold across the set.

<visual_dna>
Subject: [name and type: brand, event, product, character, IP].
Description: [what it is, what it stands for. 1 to 3 sentences.]
Key text: [exact name, tagline, or line that must appear verbatim in relevant pages].
Palette: [primary color, accent color, secondary tones, named].
Treatments: [textures, grain, glitch, compositional devices].
Subject matter: [imagery vocabulary that lives in this world].
Mood: [2 to 4 descriptors].
Aspect ratio defaults: [per page type, listed by page].
</visual_dna>

<global_forbidden>
- palette drift across pages
- treatment loss between pages
- text spelling errors on key text
- page-type bleed (one page looking like another)
- system incoherence (pages that read like different brands)
- generic stock-image substitutes for brand-specific imagery
- legible text in placeholder language not requested
- [SUBJECT NAME] misspelled
</global_forbidden>

<images>
<image_1 subject="[page type 1, e.g. brand identity sheet]">
[Page type, layout logic, exact text in quotes, aspect ratio for this page type, specific visual elements.]
</image_1>
<image_2 subject="[page type 2, e.g. campaign keyvisual]">
[Spec for page 2.]
</image_2>
<image_3 subject="[page type 3]">
[Spec for page 3.]
</image_3>
<image_4 subject="[page type 4]">
[Spec for page 4.]
</image_4>
<image_5 subject="[page type 5]">
[Spec for page 5.]
</image_5>
<image_6 subject="[page type 6]">
[Spec for page 6.]
</image_6>
<image_7 subject="[page type 7]">
[Spec for page 7.]
</image_7>
</images>

<verify>
Before showing output, confirm for ALL [N] pages:
- Visual DNA palette and treatment present on every page
- Exact text rendered verbatim on each page where it appears
- Each page is a distinct deliverable type with no duplicates
- Aspect ratio matches the page type defaults stated in the visual DNA
- The set reads as one coherent system, not seven different brands
- [SUBJECT NAME] spelled correctly throughout
</verify>
```


## PSGV Template per Prompt (NL fallback, when system prompt is overkill)

```
PLAN: [Page type] for [subject name]. Visual DNA backbone: [palette names], [treatment names], [mood]. Specific deliverables for this page: [elements]. Layout logic: [compositional approach]. Aspect ratio: [ratio].
SEARCH: SKIP. [Or: Search the web, today is [date]: [specific data needed].]
GENERATE: [The full creative brief for this page. Exact text in quotes. Visual DNA applied. Layout described. All key elements named. Connection to the broader system noted where relevant.]
VERIFY: Before showing output, verify [exact text] is spelled correctly. Verify [treatment] is present as specified. Verify this page shares palette and texture with the system DNA. Verify aspect ratio is [ratio].
```


## Preamble format

```
Mode: MULTI-OUTPUT.
Subject: [name and type].
Page inventory: [list the 7 page types, numbered].
Axis varied: page type (each prompt is a different deliverable).
Axes frozen: visual DNA (palette, treatments, mood, subject vocabulary, held across all 7 pages).
Format: [System prompt operating contract / NL fallback].
SEARCH active: [yes + which pages] OR [no].
```


## Consistency enforcement

```
PLAN: Typography specimen page for "BRAND NAME". Visual DNA backbone: slate navy background, hot coral red accent, halftone grain overlay, analog-digital editorial mood. Specific deliverables: ...
```
