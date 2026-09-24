# agent-typography recipes

These are preserved prompt recipes from the source skill. Read the relevant example, then adapt its subject, count, references, format and requested change to the current brief. Concrete counts, aspect ratios, media and named model settings in examples are recipe values, never studio defaults. A prompt field such as `controlnet`, `recommended_weight`, `quality`, `system` or `search` is descriptive text unless the selected host exposes a matching real control. The current skill and shared prompt contract govern execution. Some historical examples contain pose shifts, fixed counts or search calls; use those only when the current request calls for them. Attribution remains source-recorded unless separately verified.


## Step 1: Declare the text content exactly

```
EXACT TEXT: [word or phrase or copy block, quoted]
SCRIPT(S): [Latin, Japanese, Korean, Chinese, Hindi, Bengali, mixed]
```


## Preamble format

```
Exact text: "[quoted text]"
Script(s): [list]
Axis varied: [e.g., typographic treatment, from Bauhaus to Memphis to Swiss International to Art Deco to Y2K to Pixel to Handwritten]
Axes frozen: text content, aspect ratio, mood register.
Format: [JSON envelope / Natural language fallback / System prompt for batch].
SEARCH active: [yes + topic] OR [no].
```


## Non-Latin script focus (JSON)

```json
{
  "plan": "Script-specific rendering. [Japanese: vertical flow, stroke authenticity. Korean: geometric vs brush character. Hindi Devanagari: conjuncts, matras. Arabic: connected forms, baseline character. Chinese: stroke order, radical structure.] Culturally appropriate design heritage.",
  "search": null,
  "subject": "[Poster, packaging, signage] featuring \"[EXACT TEXT]\" rendered in [Japanese calligraphy / Korean Hangul display / Chinese seal script / Hindi Devanagari / Bengali display / Arabic / Hebrew]. Exact text in correct script characters.",
  "pose": "Static typographic composition.",
  "environment": "[Supporting visual elements or clean field.]",
  "camera": "[Layout framing.]",
  "lighting": "[Lighting that supports legibility.]",
  "mood": "[Mood register tied to script's cultural design heritage.]",
  "style": "[Stroke and letterform character: traditional brush / modern geometric / vernacular hand-lettering / official type-set / engraved.]",
  "palette": "[Color palette tied to the language's cultural design heritage.]",
  "quality": "Rendered at full legibility. Authentic stroke character. No invented glyphs.",
  "aspect_ratio": "[W:H]",
  "verify": [
    "[EXACT TEXT] in correct script characters, no garbling",
    "stroke order and letterform conventions appropriate to script",
    "no invented characters or pseudo-script",
    "legibility at intended scale",
    "cultural design heritage respected"
  ],
  "negative_prompt": {
    "forbidden": [
      "character corruption",
      "invented glyphs",
      "pseudo-script (decorative shapes resembling but not being the script)",
      "latin substitution for non-latin characters",
      "wrong script (e.g., Chinese hanzi when Japanese kanji requested)",
      "stroke order errors that produce non-existent characters",
      "latinized typographic conventions applied to non-latin script",
      "missing diacritics, matras, or conjuncts",
      "decorative substitution where literal rendering was requested",
      "hybrid characters mixing scripts",
      "AI-style abstract typography in place of correct script"
    ]
  }
}
```


## Mixed-script layout (JSON)

```json
{
  "plan": "Two-script hierarchy. Each script rendered in its native tradition. Unified palette across both. Neither script degrades to decorative noise.",
  "search": null,
  "subject": "[Layout type] combining \"[EXACT TEXT 1]\" in [script 1] with \"[EXACT TEXT 2]\" in [script 2]. Each script in its native typographic tradition.",
  "pose": "Static composition.",
  "environment": "[Supporting design field.]",
  "camera": "[Layout framing.]",
  "lighting": "[Lighting that supports legibility of both scripts.]",
  "mood": "[Unified mood across both scripts.]",
  "style": "[Editorial / luxury / street / minimalist] with both scripts in their native tradition.",
  "palette": "[Unified palette across both scripts.]",
  "quality": "Both scripts rendered authentically. Hierarchy clear. No script degrades.",
  "aspect_ratio": "[W:H]",
  "verify": [
    "EXACT TEXT 1 spelled correctly in script 1",
    "EXACT TEXT 2 spelled correctly in script 2",
    "neither script becomes decorative",
    "hierarchy and size relationship clear",
    "palette unified"
  ],
  "negative_prompt": {
    "forbidden": [
      "either script corrupted or invented",
      "decorative use of one script as ornament instead of legible text",
      "latinization of non-latin script",
      "palette breaking between scripts",
      "hierarchy inversion",
      "size accident causing one script to dominate when balance was specified"
    ]
  }
}
```


## Brand wordmark (JSON, fidelity-flagged)

```json
{
  "plan": "Wordmark for brand. Design direction defined. Letterform consistency required. Fidelity risk acknowledged.",
  "search": null,
  "subject": "Wordmark design for \"[EXACT BRAND NAME]\". [Design direction: geometric / organic / serif / script / stencil].",
  "pose": "Static logo composition.",
  "environment": "[Clear background: white, black, or specified field.]",
  "camera": "[Centered or specified layout.]",
  "lighting": "[Flat lighting for logo legibility.]",
  "mood": "[Mood implied by design direction.]",
  "style": "[Letterform relationships: tight spacing, generous tracking, ligatures.] Brand wordmark fidelity is a known limitation.",
  "palette": "[Color spec.]",
  "quality": "Letterform consistency required. Iteration may be needed for exact fidelity.",
  "aspect_ratio": "[W:H]",
  "verify": [
    "brand name spelled correctly",
    "letterform consistency across the wordmark",
    "design direction visible in execution",
    "no extra characters or repetition"
  ],
  "negative_prompt": {
    "forbidden": [
      "brand name misspelling",
      "extra letters appended",
      "letter substitution",
      "letterform inconsistency (some letters in one style, others in another)",
      "decorative ornament obscuring the wordmark",
      "spacing chaos",
      "imitation of an existing trademark not requested"
    ]
  }
}
```


## Single-word display typography

```
PLAN: Hierarchy: "[EXACT TEXT]" as the sole focal element. Medium and rendering tradition defined. Legibility required at full scale.
SEARCH: SKIP.
GENERATE: Typographic composition featuring the word "[EXACT TEXT]" rendered as [typeface voice: heavy geometric sans, hand-lettered script, Art Deco capitals, pixel bitmap]. [Color palette]. [Layout: centered, asymmetric, overlapping]. [Background and supporting elements]. [Texture or medium: letterpress, neon glow, carved stone, embroidered thread]. [Aspect ratio].
VERIFY: Before showing output, verify "[EXACT TEXT]" is spelled correctly and legible at full scale. Verify the medium-specific texture is present.
```


## Multilingual poster

```
PLAN: Text hierarchy: "[EXACT TEXT 1]" in [script 1] as primary headline, "[EXACT TEXT 2]" in [script 2] as supporting line. Each script rendered in its native typographic tradition.
SEARCH: SKIP. (Active if text content requires factual verification.)
GENERATE: Poster design with "[EXACT TEXT 1]" in [script 1] as primary headline and "[EXACT TEXT 2]" in [script 2] as supporting line. [Typographic hierarchy]. [Visual style: minimalist Japanese editorial, Korean luxury, French New Wave, Bauhaus]. [Palette]. [Optional image or texture backdrop]. [Aspect ratio].
VERIFY: Before showing output, verify both text strings are spelled correctly in their respective scripts. Verify typographic hierarchy is visually clear.
```


## Dense editorial layout

```
PLAN: Article layout defined. Headline and subhead exact text specified. Body copy length and column structure determined before brief.
SEARCH: SKIP. (Active if article content requires factual accuracy.)
GENERATE: Magazine spread featuring a full article layout. Headline: "[EXACT HEADLINE]". Subhead: "[EXACT SUBHEAD]". Body copy: [specify exact paragraphs or describe topic]. Typographic style: [serif elegance, modernist sans, brutalist industrial]. Grid structure: [two-column, three-column, asymmetric]. [Image placement if relevant]. [Palette]. [Aspect ratio].
VERIFY: Before showing output, verify headline and subhead are spelled correctly and visually dominant. Verify body copy density is legible at the stated scale.
```


## Non-Latin script focus

```
PLAN: Script-specific rendering requirements. [Japanese: vertical flow, stroke authenticity]. [Korean: geometric vs brush character]. [Hindi Devanagari: conjuncts, matras]. Culturally appropriate design heritage.
SEARCH: SKIP.
GENERATE: [Poster, packaging, signage] featuring "[EXACT TEXT]" rendered in [Japanese calligraphy, Korean Hangul display, Chinese seal script, Hindi Devanagari, Bengali display]. [Stroke and letterform character: traditional brush, modern geometric, vernacular hand-lettering]. [Color palette tied to the language's cultural design heritage]. [Supporting visual elements]. [Aspect ratio].
VERIFY: Before showing output, verify "[EXACT TEXT]" is in the correct script and characters are not garbled or invented. Verify script-appropriate conventions are applied.
```


## Mixed-script layout

```
PLAN: Two-script hierarchy. Script 1 primary, Script 2 supporting. Each rendered in its native tradition. Unified palette across both.
SEARCH: SKIP.
GENERATE: [Layout type] combining "[EXACT TEXT 1]" in [script 1] with "[EXACT TEXT 2]" in [script 2]. Each script rendered in its native typographic tradition. [Hierarchy and size relationship]. [Unified palette]. [Overall design voice: editorial, luxury, street, minimalist]. [Aspect ratio].
VERIFY: Before showing output, verify both text strings are spelled correctly in their respective scripts. Verify neither script degrades or becomes decorative noise.
```


## Brand wordmark (flag fidelity)

```
PLAN: Brand name to render. Design direction: [geometric, organic, serif, script, stencil]. Fidelity risk acknowledged.
SEARCH: SKIP.
GENERATE: Design a wordmark for "[EXACT BRAND NAME]". [Design direction]. [Letterform relationships: tight spacing, generous tracking, ligatures]. [Color]. [Supporting mark or icon if desired]. Clear on [white or black] background. [Aspect ratio]. Note: brand mark fidelity is a known limitation; iteration may be required.
VERIFY: Before showing output, verify brand name spelling is correct. Flag any letterform drift for iteration.
```


## Sign or environmental typography

```
PLAN: Sign type and material defined. Environmental context stated. Script and fabrication technique determine rendering approach.
SEARCH: SKIP. (Active if sign content must reflect current accurate information.)
GENERATE: [Type of sign or surface: shopfront, restaurant facade, airport departure board, street banner, vintage enamel sign] displaying "[EXACT TEXT]" in [script]. [Material and fabrication: enamel, neon, backlit acrylic, painted plaster, engraved brass]. [Contextual environment: street scene, interior, weathered surface]. [Lighting and time of day]. [Aspect ratio].
VERIFY: Before showing output, verify "[EXACT TEXT]" is legible and correctly spelled. Verify material-specific aging or fabrication artifacts are present.
```


## Verbatim exemplars from the research

```
Bauhaus-inspired poster with bold typography that says "GPT IMAGE 2" and "DESIGN THE FUTURE".
```


## Verbatim exemplars from the research

```
以眼部特写图片为基础，生成3:4的四屏构图超写实眼部特写，四屏按春夏秋冬上下排序... 画面中央"SPRING"白色艺术字点缀... 下面用书法体写着春.
```


## Verbatim exemplars from the research

```
Luxury fashion book spread, premium hospitality campaign using Korean typography.
```
