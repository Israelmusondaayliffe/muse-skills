# agent-search recipes

These are preserved prompt recipes from the source skill. Read the relevant example, then adapt its subject, count, references, format and requested change to the current brief. Concrete counts, aspect ratios, media and named model settings in examples are recipe values, never studio defaults. A prompt field such as `controlnet`, `recommended_weight`, `quality`, `system` or `search` is descriptive text unless the selected host exposes a matching real control. The current skill and shared prompt contract govern execution. Some historical examples contain pose shifts, fixed counts or search calls; use those only when the current request calls for them. Attribution remains source-recorded unless separately verified.


## Preamble format

```
Axis varied: [e.g., seven current NBA team home arenas].
Axes frozen: photographic style, time of day, compositional approach, mood.
SEARCH active: yes: [topic + date anchor].
Known risks: [mode-specific warnings: geographic hallucination, brand fidelity, stale data, safety blocks on named figures].
```


## Current event illustration

```
PLAN: [Visual format and what facts must appear: team, score, key players, date, location. Define design container before search populates it.]
SEARCH: Search the web, today is [date]: [specific current event or topic]. Retrieve [key facts needed].
GENERATE: Create a [photorealistic image, illustration, infographic] of [subject] incorporating the retrieved facts. Include [key factual elements]. [Style specification]. [Aspect ratio].
VERIFY: Before showing output, verify all named entities, scores, dates, and facts are retrieved from search and not sourced from training memory. Flag any geographic labels.
```


## Real-entity rendering

```
PLAN: [Entity type and visual context. Define which identity markers must match current reality.]
SEARCH: Search the web, today is [date]: current [entity: team, company, product, public figure]. Retrieve current [uniform, logo, appearance, lineup].
GENERATE: Generate a [image type] showing [entity] in [context]. [Style]. [Aspect ratio].
VERIFY: Before showing output, verify current-state markers (uniform, logo, appearance) match retrieved information, not training-memory defaults.
```


## Live-data infographic

```
PLAN: Infographic container defined first. [Layout: grid, modular, poster]. [Metrics and labels that will be populated by live data.] Title: "[EXACT TITLE]".
SEARCH: Search the web, today is [date]: [current data source: weather, stock data, news, standings]. Retrieve [specific data points].
GENERATE: Create an infographic titled "[EXACT TITLE]" incorporating the retrieved data. Design style: [clean, editorial, newsroom]. [Layout notes]. [Aspect ratio]. Include source attribution in the design.
VERIFY: Before showing output, verify all data points are search-retrieved, not hallucinated. Verify labels match the data.
```


## Geographic or cartographic

```
PLAN: [Map type and scope. Define which geographic elements must be accurate: country borders, capitals, rivers, regional features.]
SEARCH: Search the web, today is [date]: current borders and capitals of [specific region]. Source: Wikipedia or [specified reference].
GENERATE: Generate a [map type] of [specific region] with accurate current borders and labels. Include [specific features]. Legible legend. [Style]. [Aspect ratio].
VERIFY: Before showing output, verify all country names and capital cities against the retrieved source. Flag any invented place names ("Ciger" / "Mharee" type failures).
```


## Current product or brand state

```
PLAN: [Brand visual state: current logo, color scheme, packaging. Define which brand marks must be accurate.]
SEARCH: Search the web, today is [date]: current official [brand] logo and visual identity.
GENERATE: Generate a [product image, lifestyle shot, brand visualization] for [brand] as it currently appears. Reproduce the current official logo, current color scheme, and current packaging accurately. [Scene or context]. [Style]. [Aspect ratio].
VERIFY: Before showing output, verify logo reproduction against retrieved reference. Flag if logo fidelity is low and recommend iteration.
```


## Scientific or taxonomic accuracy

```
PLAN: [Species or concept. Define which anatomical or structural features must be accurate and labeled.]
SEARCH: Search the web, today is [date]: current taxonomy and reference images of [species or scientific concept].
GENERATE: Create an [illustration or diagram] of [specific species or scientific concept] with taxonomically accurate features based on retrieved references. Label [key anatomical or structural elements] accurately. [Style: scientific illustration, encyclopedia plate, modern infographic]. [Aspect ratio].
VERIFY: Before showing output, verify all anatomical labels are accurate and structurally coherent. Flag any missing attachments or invented features.
```


## Verbatim exemplars from the research

```
Generate an infographic about activities I should do with tomorrow's weather in San Francisco in mind.
```


## Verbatim exemplars from the research

```
generate an image of today's IPL match with the current playing XI.
```


## Verbatim exemplars from the research

```
Search the web: Create a concept character sheet for Leon Kennedy set in the world of Grand Theft Auto V. Aim for accuracy when mixing his character with a different universe.
```
