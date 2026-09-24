# agent-editorial recipes

These are preserved prompt recipes from the source skill. Read the relevant example, then adapt its subject, count, references, format and requested change to the current brief. Concrete counts, aspect ratios, media and named model settings in examples are recipe values, never studio defaults. A prompt field such as `controlnet`, `recommended_weight`, `quality`, `system` or `search` is descriptive text unless the selected host exposes a matching real control. The current skill and shared prompt contract govern execution. Some historical examples contain pose shifts, fixed counts or search calls; use those only when the current request calls for them. Attribution remains source-recorded unless separately verified.


## Step 1: Declare the design brief

```
DESIGN BRIEF:
Format: [poster, magazine cover, slide, ad, brand system, book cover]
Subject or product: [what the design is for]
Exact text: [headline, subhead, date, secondary copy, all in quotes]
Design tradition or reference: [Bauhaus, French New Wave, Korean luxury, brutalist, vernacular]
Palette direction: [specified or open]
Aspect ratio or format: [letter, tabloid, billboard, 1:1, 2:3]
```


## Preamble format

```
Format: [poster, spread, slide, brand system].
Exact text: [key text in quotes].
Axis varied: [e.g., design tradition, from Bauhaus to Swiss International to Memphis to French New Wave to Art Deco to vernacular hand-painted to Y2K techno].
Axes frozen: text content, subject, aspect ratio, message.
Format chosen: [Natural language (default) / JSON envelope (hero shot escalation) / System prompt (campaign series)].
SEARCH active: [yes + topic] OR [no].
```


## Film or concert poster

```
PLAN: Format: [film, theater, concert] poster, [aspect ratio: 2:3]. Key text: title "[EXACT TITLE]", tagline "[EXACT TEXT]". Hero image direction and typographic voice defined.
SEARCH: SKIP.
GENERATE: [Film, theater, concert] poster for "[EXACT TITLE]". [Tagline: "EXACT TEXT"]. [Hero image direction: protagonist portrait, symbolic object, atmospheric scene]. [Typographic voice: elegant serif, brutalist sans, hand-lettered, French New Wave vernacular]. [Palette]. [Layout: centered, asymmetric, split, full-bleed image with text band]. [Mood]. [Aspect ratio: 2:3].
VERIFY: Before showing output, verify title and tagline are spelled correctly and visually dominant. Verify typographic voice matches the stated tradition.
```


## Magazine cover

```
PLAN: Cover hierarchy: masthead dominant, cover line secondary, image as backdrop. All exact text defined before brief.
SEARCH: SKIP.
GENERATE: Magazine cover for [title or concept magazine]. Masthead: "[EXACT TITLE]". Cover line: "[EXACT HEADLINE]". Secondary lines: [list in quotes]. [Cover image direction]. [Typographic system: serif luxury, modernist sans, editorial elegance]. [Palette]. [Aspect ratio: 3:4 or similar].
VERIFY: Before showing output, verify masthead and cover line are correctly spelled and in correct hierarchy. Verify the cover image does not obscure masthead.
```


## Campaign keyvisual

```
PLAN: Campaign intent: [brand, product, tone]. Headline and supporting copy exact. Compositional approach defined.
SEARCH: SKIP. (Active if campaign must reference current stats or live data.)
GENERATE: Campaign keyvisual for [brand or product]. Hero element: [image direction]. Headline: "[EXACT TEXT]". Supporting copy: "[EXACT TEXT]". [Brand tone: luxury, everyday, aspirational, utilitarian]. [Compositional approach: symmetrical, diagonal, rule-of-thirds, full-bleed]. [Palette]. [Aspect ratio].
VERIFY: Before showing output, verify headline and copy are present and correctly spelled. Verify brand tone is consistent across image and typography.
```


## Brand identity system (from a name)

```
PLAN: Brand name to render. Personality keywords: [bold/angular/industrial, OR soft/organic, OR editorial]. Deliverable set: wordmark, symbol mark, palette swatches, typography sample, one application mockup.
SEARCH: SKIP.
GENERATE: Full brand identity system for "[EXACT BRAND NAME]". Include: primary wordmark, symbol mark, palette swatches, supporting typography sample, one application mockup. [Brand personality]. [Aspect ratio appropriate for identity sheet].
VERIFY: Before showing output, verify brand name is spelled correctly in the wordmark. Verify aesthetic is consistent across all system components.
```


## Slide deck page

```
PLAN: Slide headline and content exact text defined. Visual anchor type determined. Design system stated.
SEARCH: SKIP. (Active if slide must contain current data or verified statistics.)
GENERATE: Single slide titled "[EXACT HEADLINE]". Content: [bullet points or message as exact text]. [Visual anchor: chart, photo, diagram, illustration]. [Design system: corporate modern, editorial, startup bold, consulting conservative]. [Palette: two or three colors]. [Aspect ratio: 16:9].
VERIFY: Before showing output, verify headline is spelled correctly. Verify all content text is legible at slide scale.
```


## UI mockup

```
PLAN: UI type and product category. All UI element labels exact. Design tradition and color palette defined.
SEARCH: SKIP.
GENERATE: [Mobile app or web] screen mockup for [product type]. Layout includes: [specify UI elements: search bar at top, featured cards, bottom navigation with labeled icons: "Home", "Explore", "Bookings", "Profile"]. [Design tradition: Material, Apple HIG, neobrutalist, glassy, skeuomorphic]. [Color palette]. [Typography]. [Aspect ratio: 9:19.5 for mobile, 16:10 for web].
VERIFY: Before showing output, verify all UI labels are spelled correctly and semantically consistent. Verify the layout reads as a functional UI, not decorative.
```


## Book or album cover

```
PLAN: Title and creator exact text. Genre or category determines visual direction and typographic voice.
SEARCH: SKIP.
GENERATE: [Book, album] cover for "[EXACT TITLE]" by "[EXACT CREATOR]". [Genre or category]. [Visual direction: single strong image, typographic-first, abstract composition, illustrated]. [Typographic voice]. [Palette]. [Aspect ratio: 2:3 for books, 1:1 for albums].
VERIFY: Before showing output, verify title and creator name are spelled correctly. Verify genre conventions are present in the visual treatment.
```


## Event flyer

```
PLAN: Event details exact: name, date, location. Design voice appropriate to event type.
SEARCH: SKIP.
GENERATE: [Event type] flyer. Event: "[EXACT NAME]". Date: "[EXACT DATE]". Location: "[EXACT LOCATION]". [Design voice: hand-painted vernacular, punk cut-and-paste, modernist grid, luxury minimal]. [Color palette]. [Supporting imagery or texture]. [Aspect ratio: 2:3 or 1:1].
VERIFY: Before showing output, verify event name, date, and location are spelled correctly. Verify all critical information is legible.
```


## Verbatim exemplars from the research

```
French New Wave–inspired poster for a film titled "L'Amour à Paris".
```


## Verbatim exemplars from the research

```
Luxury fashion book spread, premium hospitality campaign using Korean typography.
```


## Verbatim exemplars from the research

```
Generate a clean and modern mobile app UI design for a travel booking platform. The layout should include a search bar at the top, featured destination cards with high-quality imagery, a bottom navigation bar with icons for 'Home', 'Explore', 'Bookings', and 'Profile', and a minimalist typography style. Use a color palette of soft blues, whites, and light grays.
```


## Verbatim exemplars from the research

```
Generate a full stamp-and-badge identity system from one product name. Bold, angular, industrial.
```
