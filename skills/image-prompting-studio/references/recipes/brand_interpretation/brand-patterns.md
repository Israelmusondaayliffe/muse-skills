# Brand interpretation patterns

These are preserved prompt recipes from the source skill. Read the relevant example, then adapt its subject, count, references, format and requested change to the current brief. Concrete counts, aspect ratios, media and named model settings in examples are recipe values, never studio defaults. A prompt field such as `controlnet`, `recommended_weight`, `quality`, `system` or `search` is descriptive text unless the selected host exposes a matching real control. The current skill and shared prompt contract govern execution. Some historical examples contain pose shifts, fixed counts or search calls; use those only when the current request calls for them. Attribution remains source-recorded unless separately verified.

## Recurring Visual Specifications

These are optional product-card treatments. Select them when they fit the brief; they are not universal defaults.

**Studio Environment**:
- Seamless cyclorama (white, light gray, or brand-complementary pastel)
- Infinite background, free of shadows (or with subtle, controlled shadows)
- Alternative: colored cyclorama flooded with brand's primary color (UC 9.2)

**Lighting**:
- Softbox studio, high-key, diffused
- No harsh shadows
- Rim lighting to accentuate contours and material textures
- Subtle cinematic bloom and halation for premium feel
- Alternative: dramatic single-source for dark/moody treatments (UC 2.6)

**Camera Simulation**:
- 50mm-100mm lens (telephoto/portrait range)
- Shallow depth of field with sharp focus on hero detail
- Creamy, smooth bokeh on background
- Medium format Phase One simulation for highest-end work
- 3/4 angle as default viewing position for products

**Material Emphasis**:
- Hyper-tactile: every surface has named material properties
- Visible micro-detail: stitching, grain, engravings, texture contrasts
- Premium materials: leather, titanium, ceramic, carbon fiber, brushed metal, borosilicate glass
- Material contrast is a key creative lever (cheap object + luxury material = brand recontextualization)

**Quality Target**:
- 8K resolution, hyper-realistic textures
- Optional fine film grain for editorial feel
- Ultra-clean, no dust, no fingerprints (product shots)

---


## Recurring UI/Graphic Overlay Conventions

Many brand design prompts include standardized UI elements in the final image. These create a consistent "editorial product card" aesthetic.

**Bottom Left Corner**:
- Small, minimalist text block (1-2 lines)
- Content: Product name, material description, collection code
- Font style: Manrope Regular with very tight tracking and balanced line spacing
- Color: #414141 (dark gray, monochrome)
- Example format: "CONCEPT STUDY: [product name]. MATERIAL: [materials]. SS25."

**Bottom Right Corner**:
- Small, discreet monochrome logomark of the brand
- Color: #414141 (matching the text)
- Size: understated, not competing with the product

**Critical Anti-Rule**:
- "Do NOT visualize font name and color code" means don't render the words "Manrope Regular" or "#414141" as visible text in the image. These are instructions for the AI, not content to display.

**When to use UI overlays**:
- Product concept prompts (UC 1.1, 1.2, 1.4)
- Editorial product photography
- "Magazine editorial photograph" framings

**When to skip UI overlays**:
- Logo treatments (UC 2.2-2.10)
- Posters (UC 4.1-4.5)
- Icons (UC 5.1-5.4)
- Typography experiments (UC 8.1-8.3)
- Any output that has its own internal graphic design

---


## The 5 Prompt Architecture Patterns

### Pattern A: Direct Prompt

The simplest form. One prompt with brand name placeholder, generates one output. No autonomous decisions by the AI beyond interpreting the description.

Used by: Boxing gloves (1.7), Capsule collection (1.3), Embossed contour (2.5), Crowd logo (2.4), Glass logos (2.3), Dark metallic (2.6), Wax seal (2.7), Sticker-bombed (2.10), all mockups (6.x), typography (8.x)

Structure: `[BRAND NAME] + [detailed visual description] + [lighting/camera] + [background]`

### Pattern B: Smart/Auto Prompt

Prompt contains a role assignment and decision framework. The AI makes autonomous creative decisions within defined constraints (selects the object, invents the product name, chooses materials).

Used by: Creative product concepts (1.1), Everyday objects (1.4), Premium beverage (1.2), Brand kit bento grid (2.1), Photo-grid tribute (4.1), Character icons (5.4)

Structure: `[BRAND NAME] + [Role/task] + [Decision framework] + [Constraints] + [Visual specs]`

Key phrase: "Act as a..." or "Based on the design philosophy of..."

### Pattern C: System Prompt Method (Two-Step LLM Pipeline)

Step 1: Paste system prompt into any LLM (Claude, ChatGPT, Gemini). Step 2: User provides brand name. Step 3: LLM generates optimized image prompt. Step 4: Generated prompt goes into image gen tool.

Used by: Viral Product Architect (1.5)

Structure: System prompt defines role, objective, algorithm, style guidelines, output format. User input is brand name only.

### Pattern D: Image-to-Image

Requires uploaded reference image. Prompt describes transformation, not creation from zero.

Used by: Dieline-to-3D (1.6), Fashion model editorial (7.1), 3D character avatar (9.1)

Structure: `"Using the uploaded [explicit description]..." + [transformation instructions] + "Do not change aspect ratio."`

### Pattern E: JSON Structured Prompt

Structured prompt text with individually addressable fields. Use as a native API payload only if the provider documents that exact schema.

Used by: 3D Character Avatar (9.1) only

Structure: JSON object with nested parameters for task, input, style, character design, lighting, background, camera, render quality.

---


## The Brand Recontextualization Mechanism

This is the fundamental creative engine that ties the entire catalog together. Nearly every use case follows this pattern:

1. **User provides [BRAND NAME]** (and optionally [INDUSTRY] or specific direction)
2. **AI extracts brand's visual DNA**: signature colors, iconic materials and textures, logo and graphic language, design philosophy and heritage
3. **AI applies that DNA to an unexpected context/object**: The brand doesn't actually make this product or exist in this format, but the output feels authentic because it faithfully uses the brand's design vocabulary
4. **Output includes brand-accurate details**: Logo placement, colors, materials, all consistent with the real brand

The creative tension comes from the gap between "what the brand actually makes" and "what the brand could theoretically design." The further that gap, the more interesting the output.

**Low gap** (safe): Nike boxing gloves. Nike is already in sports.
**Medium gap** (inventive): Tesla kitchen appliances. Tech precision applied to domestic.
**High gap** (bold): Chanel fire extinguisher. Haute couture meets utility.
**Maximum gap** (experimental): IKEA haute couture. Democratic pricing meets fashion excess.

---


## Object Category Taxonomy

The prompts collectively can produce outputs in these categories. Use this to explore appropriate output types when the brief calls for range.

**Physical Products**:
- Functional utility objects (home goods, tech accessories, tools, sporting equipment)
- Beverage bottles (wellness elixirs, ceramic luxury bottles)
- Fashion accessories (boxing gloves, duffle bags, grillz)
- Food packaging (fast food leather bags)
- Capsule collections (multi-item knolling layouts)

**Brand Identity**:
- Logo transformations (glass, metallic, wax seal, sticker-bombed, embossed, crowd-formed, retextured, neon, inflatable, ice, moss, liquid metal)
- Brand systems (bento grids, campaign grids)
- Swiss design reimagining

**Print/Visual Communication**:
- Posters (fragmented portrait, sport poster, photo-grid tribute, Swiss typographic)
- Campaign grids (asymmetric layout, halftone)
- Mixed media collage

**Small Assets**:
- Icons (Notion-style, halftoned, duotone vector)
- Sticker packs (branded, crumpled)

**Fashion**:
- Full outfit editorial visualization
- Apparel mockups

**Typography**:
- Retro lettering treatments
- Frame-by-frame animation
- Swiss typographic posters

**Packaging**:
- Dieline-to-3D box rendering
- Ceramic bottle packaging

**Character/Avatar**:
- 3D character style transfer with brand context
