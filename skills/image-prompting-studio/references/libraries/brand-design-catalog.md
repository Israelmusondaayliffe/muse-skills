# Brand Design Catalog

These are preserved prompt recipes from the source skill. Read the relevant example, then adapt its subject, count, references, format and requested change to the current brief. Concrete counts, aspect ratios, media and named model settings in examples are recipe values, never studio defaults. A prompt field such as `controlnet`, `recommended_weight`, `quality`, `system` or `search` is descriptive text unless the selected host exposes a matching real control. The current skill and shared prompt contract govern execution. Some historical examples contain pose shifts, fixed counts or search calls; use those only when the current request calls for them. Attribution remains source-recorded unless separately verified.


35+ brand design use cases with prompt templates. Primary source: Amir Music's Nano Banana prompt catalog (Feb 2026). Templates marked [VERBATIM] are extracted directly from source. Templates marked [RECONSTRUCTED] are inferred from visual output descriptions and shared patterns.

---

## Category 1: Branded Products

### UC 1.1: Creative Product Concepts [VERBATIM]

**What it does**: AI invents a novel utility product using a brand's design DNA, materials, and philosophy. The brand doesn't actually make this product.

**Input type**: Smart prompt (AI decides the object)

**Template**:
```
[BRAND NAME]:
A high-end, glossy concept art magazine editorial photograph of a unique, unexpected functional object conceptualized and designed by the brand.

1. The Concept & Object (AI Invention):
Based on the design philosophy, heritage, and material vocabulary of the specified brand, the AI must invent a novel utility product (NOT standard clothing, shoes, or bags). Examples could be home goods, tech accessories, tools, or sporting equipment, reinterpretated through the brand's lens. The object should feel sculptural yet functional.

2. Materials & Details (Hyper-Premium):
The object is constructed from ultra-premium, highly tactile materials characteristic of the brand (e.g., patinated exotic leathers, brushed aerospace-grade titanium, sculpted matte ceramics, molded carbon fiber, or technical high-fashion textiles). Every detail is hyper-realistic: visible stitching, microscopic material grain, precision engravings, and complex texture contrasts.

3. Photography & Lighting (Cinematic Studio):
Shot on a medium format Phase One camera with a 100mm macro lens. Extremely shallow depth of field, with sharp focus on the hero details of the object and a creamy, smooth bokeh background. The lighting is sophisticated studio softbox lighting: gentle, enveloping fill light with precise rim lighting to accentuate contours and material textures.

4. Environment:
A seamless, impeccably clean studio cyclorama background in a pure, ultra-light pastel tone (e.g., desaturated mint, pale blush, or off-white), free of shadows.

5. Layout & UI Elements (Strict Placement):
- Bottom Right Corner: A small, understated, monochrome gray logo of the brand.
- Bottom Left Corner: Small, minimalist monochrome gray text describing the invented product. The font style looks like Manrope Regular with very tight tracking (kerning) and balanced line spacing. Example format:
  "CONCEPT STUDY: [AI inserts invented product name]. MATERIAL: [AI inserts main materials]. SS25."
```

**Placeholders**: [BRAND NAME]
**Visual output**: Single hero product on pastel studio background with UI overlays.
**Brand adaptation**: Works for any brand. AI autonomously selects object type and materials based on brand DNA.

---

### UC 1.2: Premium Beverage [VERBATIM]

**What it does**: Non-beverage brands reimagined as wellness elixir bottles. AI auto-generates product name, flavor, form.

**Input type**: Auto prompt

**Template**:
```
[BRAND NAME] is launching a new functional wellness elixir (e.g., adaptogenic, nootropic, or natural energy drink). As the Creative Director, devise a product name and visualize a complete high-end promotional shot. The aesthetic is "Cosmic Premium", technological, clean, and sophisticated, like top-tier Apple product photography.

THE PRODUCT: Design a sculptural, multi-layered beverage bottle suspended in the center. The form is engineered and futuristic. The materials are hyper-tactile: bead-blasted titanium details, frosted borosilicate glass, and textured haptic polymer grips.
Crucial Color Instruction: The liquid inside must have a distinct, natural color relevant to its invented function (e.g., vibrant turmeric yellow, deep berry red, earthy matcha green, or pale calming blue). The liquid should look real with subtle natural sediment.
Crucial Graphic Detail: On the clear glass section of the bottle, apply a layer of subtle, minimalist, technical typography printed in matte white ink. This design should feel utilitarian and futuristic (e.g., small technical specs like 'SPACE GRADE FORMULA', 'BATCH: OZ-9', volume indicators, or coordinate markings), adding a functional aesthetic similar to aerospace labeling, without overwhelming the bottle's clean lines.

THE ENVIRONMENT & LIGHTING: The bottle is in a seamless studio.
Crucial Background Instruction: The background must be a solid, clean, very light pastel tone that is specifically chosen to complement the liquid color (e.g., a soft cool mint background for a warm orange liquid, or a pale blush background for a deep green liquid). No gradients. Ultra-soft, diffused studio lighting creates sleek highlights on metal and deep subsurface scattering in the glass and liquid.

PHOTOGRAPHY STYLE: High-resolution 100mm macro lens shot. Shallow depth of field, sharp focus on bottle textures and the printed graphics on the glass, smooth pastel background bokeh. 8k resolve, hyper-realistic textures.

GRAPHIC OVERLAYS: Include subtle dark gray UI elements.
Bottom Left Corner: Very small, minimalist text (like Manrope Regular font) describing the product's name and function in two sentences.
Bottom Right Corner: A small, minimalist dark gray logomark for [BRAND NAME].
```

**Placeholders**: [BRAND NAME]
**Visual output**: Sculptural beverage bottle on complementary pastel background.

---

### UC 1.3: Capsule Collection (Knolling) [VERBATIM]

**What it does**: Brand reimagined as a cohesive premium capsule collection. Multiple branded objects in knolling or isometric layout.

**Input type**: Auto prompt

**Template**:
```
[BRAND NAME], conceptualized as a cohesive, premium "capsule collection" of branded merchandise and functional souvenirs. The image displays a curated set of various physical objects (such as tech accessories, utility gear, lifestyle items, or stationery) that are semantically relevant to the brand's specific industry and audience. Every item is designed using the brand's official signature color palette and features bold logo integration. The objects are arranged in a clean, organized group composition (knolling or isometric perspective) on a seamless, infinite studio white background. The lighting is soft and professional, creating subtle shadows. The framing is wide, ensuring significant negative space (air) surrounds the product grouping on all sides.
```

**Placeholders**: [BRAND NAME]
**Visual output**: Multiple branded items in organized flat-lay on white.

---

### UC 1.4: Creative Concepts (Everyday Objects) [VERBATIM]

**What it does**: Takes mundane everyday objects and elevates them into luxury artifacts using brand DNA. AI selects from diverse object categories.

**Input type**: Smart prompt

**Template**:
```
[BRAND NAME].
Act as a creative director curating a wide-ranging, eclectic collection of "recontextualized everyday objects."
DIVERSE OBJECT SELECTION (MANDATORY VARIETY):
Your goal is to surprise the viewer with the VARIETY of the object chosen.
Randomly select ONE object from these distinct categories to ensure diversity:
Analog Office & Desk:
Sport & Leisure:
Barware & Kitchen:
Utility & Tools:
Grooming:
Travel:
THE CONCEPT:
Take the chosen mundane object and elevate it into a luxury artifact using [BRAND NAME]'s signature materials and colors. The object must be immediately recognizable but look incredibly expensive.
MATERIALS & FINISH:
Use materials that contrast with the object's usual cheap nature. Think: marble, brushed titanium, matte rubber, carbon fiber, gold plating, or high-grade leather. The branding must be physically integrated (embossed/engraved), not just a sticker.
PRESENTATION (NO BOXES):
The object should stand alone on the pedestal or table, fully exposed. If it has parts (like a ping pong set), arrange them neatly ("knolling"). Avoid closed boxes that hide the shape.
PHOTOGRAPHY & LIGHTING:
Style: High-end product editorial (Wallpaper* / Dezeen style).
Lighting: Soft, studio high-key lighting. No harsh shadows.
Background: Clean, seamless light grey or white cyclorama.
GRAPHIC OVERLAYS (UI):
Bottom Left: A small, minimalist 2-line text block describing the object. Font: Manrope Regular. Color: #414141.
Bottom Right: A small, discreet, monochrome logomark of [BRAND NAME]. Color: #414141.
Do NOT visualize "Font name" and "Color code".
```

**Placeholders**: [BRAND NAME]
**Visual output**: Single elevated everyday object on clean background with UI overlays.

---

### UC 1.5: System Prompt Method (Viral Product Architect) [VERBATIM]

**What it does**: Two-step pipeline. Step 1: paste system prompt into any LLM. Step 2: provide brand name, LLM generates the image prompt.

**Input type**: System prompt (paste into LLM first)

**Template (System Prompt)**:
```
SYSTEM PROMPT: The Viral Product Architect
ROLE: You are a world-class Concept Art Director & Product Designer with 20+ years of experience at agencies like Pentagram, IDEO, and DONDA. Your specialty is "Speculative Design" and "Hype-culture artifacts". You create viral, thumb-stopping product concepts that mix High Fashion, Tech, and Utility in unexpected ways.

OBJECTIVE: The user will provide ONLY a [BRAND NAME]. Your task is to invent a hyper-realistic, unexpected, and visually stunning physical product concept for this brand. It must be something they don't sell, but could strictly hypothetically design if they went crazy.

CORE ALGORITHM (THE "FRESHNESS" FORMULA):
1. Analyze Brand DNA: Extract the brand's iconic materials, colors, and textures (e.g., Adidas = Primeknit/Boost foam; Rimowa = Aluminum grooves; Jacquemus = Tiny, leather).
2. Select Unexpected Object: Choose a mundane or tech object completely unrelated to the brand (e.g., Toothbrush, Inhaler, Drone, Smart Ring, VR Headset, Coffee Press).
3. Apply Texture Mapping: Wrap the "Unexpected Object" in the "Brand DNA". Crucial: Use materials typically reserved for fashion/furniture on tech items (like the silver puffer watch).
4. Viral Check: Ask yourself: "Would Highsnobiety or Hypebeast repost this?" If no, make it weirder.

VISUAL STYLE GUIDELINES (IMMUTABLE):
Vibe: Ultra Hi-End Product Design, Conceptual, Expensive, Tactile.
Environment: Minimalist light studio, infinity white/light grey background.
Lighting: Softbox studio lighting, clean reflections, high-key, ambient occlusion.
Camera: Telephoto lens (50mm-85mm), shallow depth of field, sharp focus on texture details.

OUTPUT FORMAT: You must output a SINGLE, OPTIMIZED IMAGE PROMPT (English) tailored for Google Imagen/Midjourney. Do not write an explanation. Just the prompt.

PROMPT STRUCTURE TO GENERATE:
[Subject Description with Brand Materials] + [Context/Action] + [Specific Brand Details/Logo placement] + [Lighting & Environment] + [Technical 3D Specs]
```

**Placeholders**: [BRAND NAME] (provided by user in step 2)

---

### UC 1.6: Dieline-to-3D Visualization [VERBATIM]

**What it does**: Upload a flat 2D dieline as reference image, prompt folds it into photorealistic 3D box render.

**Input type**: Image-to-image (requires uploaded dieline)

**Template**:
```
Assemble the dieline into a perfectly folded 3D box with accurate panel placement, clean edges, and undistorted typography. Preserve all artwork exactly as printed on the dieline. Render the box in a minimal, high-end studio setup on a soft neutral background with gentle diffused lighting, subtle shadows, and no extra props. Show the box upright in a refined 3/4 angle. Ultra-realistic detail, true colors, matte paperboard texture, crisp folds, premium editorial aesthetic.
```

**Placeholders**: None (image input provides context)

---

### UC 1.7: Boxing Gloves Reinterpretation [VERBATIM]

**What it does**: Any brand reimagined as premium leather boxing gloves with brand's signature patterns and colors.

**Input type**: Direct prompt

**Template**:
```
[BRAND NAME], conceptualized as a pair of premium, professional-grade leather boxing gloves. The design is a complete luxury reinterpretation using the signature color palette, iconic patterns, and graphic language historically associated with the brand. The primary brand logo is prominent across the main dorsal striking area and repeated on the wrist cuffs. The gloves are crafted from high-quality, supple full-grain leather with precise reinforced stitching in contrasting brand colors. They are hanging against a clean, seamless studio white background. Professional studio lighting is arranged to create a subtle cinematic bloom and light halation around the contours of the gloves. The image is rendered with a 50mm prime lens aesthetic, featuring a shallow depth of field that gently blurs the rear parts of the gloves and cuffs, topped with a fine, subtle film grain texture throughout. 3D product render.
```

**Placeholders**: [BRAND NAME]

---

## Category 2: Brand Identity Systems

### UC 2.1: Brand Kit Bento Grid [VERBATIM]

**What it does**: Complete brand identity system in one bento-grid image. Hero image, social mockup, color palette with HEX codes, typography specimen, logo, brand DNA manifesto.

**Input type**: Auto prompt (AI makes autonomous creative decisions)

**Template**:
```
[BRAND NAME]
({INDUSTRY}).

Act as a Lead Brand Designer creating a comprehensive "Brand Identity System" presentation (Bento-Grid Layout).

THE TASK:
Generate a single, high-resolution bento-grid board containing 6 distinct modules that define the visual identity for [BRAND NAME].

PHASE 1: VISUAL STRATEGY (AUTONOMOUS)
1. Analyze the Brand: Determine the archetype and visual vibe.
2. Define the Palette: Select 4 distinct colors.
3. Select Typography: Choose ONE specific Google Font (Serif, Sans-Serif, or Display) relevant to the industry.

PHASE 2: THE LAYOUT (6-MODULE GRID)
The image must be a clean, gap-separated grid featuring these specific blocks:

Block 1 (The Hero): A high-end Key Visual photography showing the product/service in context. Cinematic lighting, photorealistic. Overlay the brand logo in white.
Block 2 (Social Media): A mockup of an Instagram Post. It features a bold headline using the brand font and a lifestyle image.
Block 3 (The Palette & HEX): A clean design block displaying 4 Vertical Color Swatches. Crucial Detail: Inside or below each color swatch, simulate distinct text looking like HEX Codes (e.g., "#1A2B3C").
Block 4 (Typography Spec): A minimalist block dedicated to the Brand Font. CRITICAL CONSTRAINT: Do NOT show the alphabet (Aa Bb Cc). The block must display ONLY the Name of the Font written in large, crisp characters using that specific font style. Subtext: Tiny text reading "Primary Typeface".
Block 5 (The Logo): A solid background block featuring the Final Logo (clean, vector style, NO construction lines/grids). Minimalist and iconic.
Block 6 (Brand DNA): A text-heavy "Manifesto Card" with three short paragraphs titled: ARCHETYPE, VOICE, VISUALS.

PHASE 3: AESTHETIC & FINISH
Style: Behance Trend / Awwwards Winner.
Quality: 8k resolution, razor-sharp vector graphics mixed with high-end photography.
Lighting: Soft studio lighting across the whole grid.
```

**Placeholders**: [BRAND NAME], {INDUSTRY}

---

### UC 2.2: Swiss Design Logos [RECONSTRUCTED]

**What it does**: Reimagines any brand logo in clean geometric Swiss/International Typographic Style.

**Input type**: Direct prompt

**Template**:
```
[BRAND NAME] logo reimagined in the Swiss International Typographic Style. The logo is reduced to pure geometric forms, clean lines, and mathematical proportions. Primary shapes only: circles, squares, triangles, and precise curves. Rendered in a strict two-color palette of the brand's primary color against an off-white or warm cream background. Below the geometric logo mark, the brand name is set in Helvetica Neue or Akzidenz-Grotesk, all caps, with generous letter-spacing. The overall composition follows a rigid grid system with ample negative space. Printed on heavyweight uncoated stock with a subtle paper texture visible. Flat lighting, no shadows, no gradients, no 3D effects. 1:1
```

**Placeholders**: [BRAND NAME]

---

### UC 2.3: Glass Logos [RECONSTRUCTED]

**What it does**: Brand logos rendered in transparent, glossy 3D glass material.

**Input type**: Direct prompt

**Template**:
```
[BRAND NAME] logo rendered as a three-dimensional transparent glass sculpture. The glass material is pristine, with accurate caustics, internal refractions, and subtle chromatic dispersion at the edges. The glass is tinted in the brand's primary color with high transparency, allowing light to pass through and create colored shadow patterns on the surface below. The logo sits on a clean, matte white surface. Soft studio lighting from above and slightly behind creates elegant specular highlights along the glass contours. Shallow depth of field with sharp focus on the logo's front face, rear edges softly diffused. No other objects in frame. Premium product photography aesthetic. 1:1
```

**Placeholders**: [BRAND NAME]

---

### UC 2.4: Crowd Logos [VERBATIM]

**What it does**: Aerial perspective of crowds/people forming brand logos. Drone-style overhead photography.

**Input type**: Direct prompt

**Template (Apple example)**:
```
Aerial nighttime photograph of a giant glowing [Apple logo (bitten apple silhouette)] formed by thousands of people on a dark city square, European architecture surroundings. Each person holding an iPhone with a flashlight creating bright white illumination. The entire logo radiating white light against a deep black background, bite area prominently lit. Directly overhead drone perspective, dramatic contrast, cinematic lighting, 4K quality.
```

**Placeholders**: [BRAND NAME and logo shape description]
**Adaptation note**: Replace Apple-specific details (iPhone flashlight, bitten apple) with brand-relevant elements. For Nike, people wearing reflective running gear forming a swoosh. For Mercedes, car headlights forming the three-pointed star.

---

### UC 2.5: 3D Embossed Glossy Contour [VERBATIM]

**What it does**: Monochromatic 3D embossed logo with blind emboss effect. Raised, smooth, liquid-like glass bezel.

**Input type**: Direct prompt

**Template**:
```
3D embossed glossy contour render of center-aligned [BRAND] on a flat surface, perfectly centered composition with ample negative space surrounding the object for a premium minimalist aesthetic. Monochromatic [COLOR] palette with soft tonal gradients. The object is defined by a raised, smooth, liquid-like glass bezel or chrome rim, creating a blind emboss effect where the interior matches the background. Matte surface finish with fine film grain or noise texture overlay. Soft diffuse lighting, strong specular highlights on the rounded edges, top-down view.
```

**Placeholders**: [BRAND], [COLOR]

---

### UC 2.6: Dark Metallic Logos [RECONSTRUCTED]

**What it does**: 3D metallic logo renders with dramatic dark studio lighting. Heavy contrast, chrome/dark metal materials.

**Input type**: Direct prompt

**Template**:
```
[BRAND NAME] logo rendered as a three-dimensional dark metallic sculpture. The material is brushed dark chrome with subtle anisotropic reflections catching controlled studio light. Deep shadows surround the logo, creating dramatic contrast. The lighting is a single, precise key light from upper right with a subtle rim light from behind, emphasizing the metallic edges while keeping the background in near-darkness. The surface shows micro-scratches and machining marks consistent with CNC-milled metal. Background: deep charcoal to black gradient. The logo floats slightly above the surface, casting a soft, diffused shadow. Shot with a 85mm lens, shallow depth of field. 1:1
```

**Placeholders**: [BRAND NAME]

---

### UC 2.7: Wax Seal Logos [RECONSTRUCTED]

**What it does**: Brand logos rendered as realistic wax seals with dripping wax. Rich texture and color.

**Input type**: Direct prompt

**Template**:
```
[BRAND NAME] logo pressed into a thick, luxurious wax seal. The wax color matches the brand's primary color with rich saturation and depth. The seal shows precise embossed detail of the logo with crisp edges and readable text. Drips and overflow of warm, still-cooling wax extend naturally below the circular seal, with visible texture of cooling and solidification. The wax sits on heavyweight cream-colored laid paper with visible fiber texture. Soft, warm directional lighting from upper left creates deep shadows in the embossed details and highlights on the raised edges. Macro photography, 100mm lens, extremely shallow depth of field focused on the center of the seal. 1:1
```

**Placeholders**: [BRAND NAME]

---

### UC 2.8: Logo Retexturing Workflow [VERBATIM - workflow description]

**What it does**: Two-tool pipeline. Nano Banana generates retextured logo, MidJourney refines.

**Input type**: Workflow (Nano Banana + MidJourney pipeline)

**Workflow**:
1. In Nano Banana: Generate brand logo with desired texture applied (candy, metal, fabric, nature, etc.)
2. In MidJourney: Refine and enhance the output

**Template (Step 1, Nano Banana)**:
```
[BRAND NAME] logo constructed entirely from [TEXTURE MATERIAL, e.g., colorful candy and sprinkles / moss and tiny flowers / crumpled aluminum foil / woven fabric threads / circuit boards and microchips]. The logo shape is filled densely with the material, maintaining the exact silhouette of the original logo. The material has realistic depth, shadows, and micro-detail. Background: solid black for maximum contrast. Overhead studio lighting creating even illumination across the textured surface. 1:1
```

**Placeholders**: [BRAND NAME], [TEXTURE MATERIAL]

---

### UC 2.9: Branded Grillz [RECONSTRUCTED]

**What it does**: Brand logos rendered as luxury dental grillz (gold/silver teeth jewelry).

**Input type**: Direct prompt

**Template**:
```
A pair of luxury dental grillz designed for [BRAND NAME]. The grillz are crafted from polished [gold/silver/platinum] with the brand's logo prominently featured across the front teeth. Intricate detailing includes micro-pave diamond accents, engraved brand patterns, and custom tooth-shaped metalwork. The grillz are displayed on a black velvet jewelry display form shaped like a dental arch. Dramatic studio lighting creates sharp specular highlights on the metal surfaces while deep shadows emphasize the three-dimensional detailing. Macro photography, extremely sharp focus on the metalwork and gemstone details. Premium jewelry editorial aesthetic. 1:1
```

**Placeholders**: [BRAND NAME], [gold/silver/platinum]

---

### UC 2.10: Sticker-Bombed 3D Logos [VERBATIM - partial]

**What it does**: 3D physical object shaped like brand logo, covered in chaotic collage of colorful vibrant stickers. Y2K aesthetic.

**Input type**: Direct prompt

**Template**:
```
A hyper-realistic 3D physical object shaped like the [BRAND NAME] logo, soft studio lighting. The logo is sticker-bombed, covered in a chaotic collage of colorful vibrant stickers. Sticker style: Y2K aesthetic, mix of cartoon characters, retro tech icons, Japanese kawaii elements, skateboard brand logos, band stickers, and pop-culture references. The stickers overlap, peel at edges, and show wear. The underlying 3D form has the brand's primary color visible in gaps between stickers. Clean white studio background. The object has physical depth and casts a soft shadow. 1:1
```

**Placeholders**: [BRAND NAME]

---

## Category 3: 3D Objects / Logo Treatments

### UC 3.1: Metallic Logo Sculpture [RECONSTRUCTED]

**What it does**: Brand logo as free-standing 3D metallic art sculpture in gallery/museum context.

**Input type**: Direct prompt

**Template**:
```
[BRAND NAME] logo as a monumental, free-standing polished metal sculpture displayed in a minimalist white gallery space. The sculpture is fabricated from mirror-finish stainless steel, standing approximately 2 meters tall. The metal surface reflects the gallery environment with subtle distortions. Museum-quality track lighting from above creates defined highlights and shadow patterns on the floor beneath. The gallery floor is polished concrete. A single viewer stands at distance for scale reference. Shot with a wide-angle architectural lens, deep depth of field, the logo sculpture commanding the center of frame. 16:9
```

**Placeholders**: [BRAND NAME]

---

### UC 3.2: Neon Logo Sign [RECONSTRUCTED]

**What it does**: Brand logo as glowing neon sign installation.

**Input type**: Direct prompt

**Template**:
```
[BRAND NAME] logo as a hand-bent neon sign glowing in the brand's primary color. The neon tubes follow the exact contours of the logo with visible glass tube connections and transformer wires. The sign is mounted on a dark exposed brick wall. The neon casts a soft, colored ambient glow on the surrounding wall and creates a subtle reflection on a wet concrete floor below. The atmosphere is moody and intimate. Some tubes glow brighter than others, creating natural luminance variation. Shot at night with the neon as the primary light source. 35mm lens, slight wide-angle distortion. 16:9
```

**Placeholders**: [BRAND NAME]

---

### UC 3.3: Inflatable Logo [RECONSTRUCTED]

**What it does**: Brand logo as oversized inflatable sculpture, parade float or art installation style.

**Input type**: Direct prompt

**Template**:
```
[BRAND NAME] logo as an enormous inflatable sculpture, approximately 10 meters tall, displayed outdoors in an urban plaza. The inflatable material is glossy PVC vinyl in the brand's primary color with visible seam lines and air valve details. The surface catches daylight with broad, smooth highlights characteristic of inflated plastic. Slight wrinkles and tension points where the form curves add realism. People walk around the base, providing scale. Blue sky with scattered clouds. The inflatable sways very slightly as if in gentle wind. Wide-angle photography from a low vantage point looking up at the installation. 4:5
```

**Placeholders**: [BRAND NAME]

---

### UC 3.4: Ice/Frozen Logo [RECONSTRUCTED]

**What it does**: Brand logo carved or frozen in solid ice block.

**Input type**: Direct prompt

**Template**:
```
[BRAND NAME] logo carved from a single block of crystal-clear ice, displayed on a reflective black surface. The ice has realistic internal fracture patterns, micro-bubbles, and varying transparency. The logo's edges are sharp and precisely cut where freshly carved, with subtle melting beginning at the base where water pools on the surface. Cool blue-white backlighting passes through the ice, creating a luminous glow. The surrounding environment is dark, making the ice sculpture the sole focal point. Condensation droplets form on the outer surface. Macro-level detail on the ice texture. 1:1
```

**Placeholders**: [BRAND NAME]

---

### UC 3.5: Moss/Nature Logo [RECONSTRUCTED]

**What it does**: Brand logo grown from living moss, plants, and natural materials.

**Input type**: Direct prompt

**Template**:
```
[BRAND NAME] logo formed from living moss, small ferns, and delicate wildflowers growing on a weathered stone wall. The moss is dense, vibrant green, perfectly filling the logo's silhouette with natural texture variation. Tiny mushrooms and lichen grow at the edges. Small water droplets cling to the moss surface. The surrounding stone wall is aged gray with natural patina. Soft, overcast natural daylight creates even, shadowless illumination that makes the green tones rich and saturated. A few fallen leaves rest at the base of the wall. Shot with a 50mm lens at comfortable distance, moderate depth of field. 4:5
```

**Placeholders**: [BRAND NAME]

---

### UC 3.6: Liquid Metal Logo [RECONSTRUCTED]

**What it does**: Brand logo in mercury/liquid chrome, captured mid-pour or mid-formation.

**Input type**: Direct prompt

**Template**:
```
[BRAND NAME] logo forming from liquid mercury or liquid chrome, captured at the exact moment the metallic fluid coalesces into the recognizable logo shape. Some portions are already solidified and sharp while other areas are still flowing, with tendrils of liquid metal reaching toward their final position. The liquid metal surface is mirror-reflective with visible environment reflections distorted by the fluid motion. Droplets and splashes surround the forming logo. Black background with dramatic single-source lighting from above creating intense specular highlights on the liquid surface. High-speed photography freeze-frame aesthetic. 1:1
```

**Placeholders**: [BRAND NAME]

---

## Category 4: Posters and Illustrations

### UC 4.1: Photo-Grid Tribute Poster [RECONSTRUCTED]

**What it does**: Celebrity/athlete tribute poster where a large silhouette portrait is composed of smaller photo tiles, creating a mosaic effect.

**Input type**: Smart prompt

**Template**:
```
A tribute poster for [PERSON/ATHLETE NAME]. A large silhouette portrait composed entirely of a grid of small, square photograph tiles. Each tile contains a different photograph related to the person's career: game moments, celebrations, candid shots, iconic poses. The tiles are arranged so their combined tones form the recognizable silhouette of the subject's face and shoulders in profile or 3/4 view. The overall color palette leans toward [TEAM/BRAND COLORS]. The background outside the silhouette is solid black or the team's secondary color. The name is set in large, bold sans-serif typography along the bottom edge. 9:16
```

**Placeholders**: [PERSON/ATHLETE NAME], [TEAM/BRAND COLORS]

---

### UC 4.2: Modern Sport Poster [RECONSTRUCTED]

**What it does**: Clean, modern sports poster with large name typography, portrait photo, brand/team logo.

**Input type**: Direct prompt

**Template**:
```
A modern, minimalist sport poster design for [ATHLETE NAME]. The layout is dominated by an oversized, cropped portrait photograph of the athlete in dramatic side lighting, occupying roughly 60% of the frame. The athlete's last name is set in massive, ultra-bold condensed sans-serif typography (think Druk Wide or Impact) running vertically along the right edge or horizontally across the top. A small, clean team or brand logo mark sits in one corner. The color palette is restricted to two colors: the team's primary color and either black or white. Clean geometric shapes or lines create subtle structure. No texture, no noise, pure graphic design. 9:16
```

**Placeholders**: [ATHLETE NAME]

---

### UC 4.3: Mixed Media Collage [RECONSTRUCTED]

**What it does**: Mixed media collage composition combining photography, illustration, torn paper, and typography.

**Input type**: Auto prompt

**Template**:
```
A mixed media collage composition for [BRAND NAME / SUBJECT]. The image combines multiple visual layers: torn magazine photographs, hand-drawn ink illustrations, paint splatters, vintage typography cutouts, and textured paper fragments. The composition is deliberately imperfect, with visible tape, staple marks, and adhesive residue where elements overlap. The overall color story uses the brand's palette but filtered through a raw, editorial aesthetic. Some photographic elements are in color while others are black and white. Handwritten annotations and doodles appear in margins. The collage sits on a cork board or studio wall background with pin holes visible. 4:5
```

**Placeholders**: [BRAND NAME / SUBJECT]

---

### UC 4.4: Fragmented Portrait Poster [VERBATIM]

**What it does**: Minimalist cinematic poster with portrait reconstructed from large square-cut paper fragments in a grid. Sticky notes with quotes around perimeter.

**Input type**: Direct prompt

**Template**:
```
A minimalist cinematic colored poster featuring a [Character Name]'s portrait from shoulders to the top of the head. The face is reconstructed using a small number of large, square-cut paper fragments arranged in a simple grid [around 4x5 or 5x6 pieces]. Each paper fragment contains a disjointed part of the face which together reconstruct the portrait. The internal paper fragments constituting the face are not perfectly flat; many have slightly curled edges and lifted corners, casting tiny, realistic shadows that give them a three-dimensional, tacked-down appearance. 4 of these squares have subtle black handwritten [text1, text2, text3, text4] directly on the skin/image. Scattered irregularly around the outer perimeter of this central grid in various randomly placed positions (not confined to the corners), several [Sticky Note Color] sticky notes are attached to the [Color] wall, containing handwritten [External Text Content, e.g., iconic quotes]. The overall layout is slightly irregular with visible gaps between the pieces showing [Color] concrete wall background. Realistic paper texture throughout, high-end studio lighting emphasizing the lifted edges, sharp focus on ink and paper grain.
```

**Placeholders**: [Character Name], [text1-4], [Sticky Note Color], [Color], [External Text Content]

---

### UC 4.5: Asymmetric Grid Campaign Poster [VERBATIM]

**What it does**: Campaign visual identity grid with strict 2-column layout. Three block types: logo, slogan, campaign photography. Distressed screen-print and halftone effects.

**Input type**: Direct prompt

**Template**:
```
[BRAND NAME].
Act as a graphic design creative director constructing a highly structured "Campaign Visual Identity Grid."

COMPOSITION (SPECIFIC 2-COLUMN ASYMMETRICAL LAYOUT):
The image must follow a strict 2-column grid structure.
LAYOUT STRUCTURE (TOP TO BOTTOM):
ROW 1: One single, full-width rectangular block (e.g., a wide photo).
ROW 2: Two equal-sized square blocks side-by-side.
ROW 3: One single, full-width rectangular block
ROW 4: Two equal-sized square blocks side-by-side.
ROW 5: One single, full-width rectangular block at the bottom.

CRITICAL CONSTRAINTS:
FULL BLEED (100% COVERAGE): No margins, no borders, no background space.
ZERO SPACING (NO GAPS): No gutters, white lines, or spacing between blocks.

GLOBAL RULES:
Typography: Use ONLY ONE font.
Uniqueness: Every photo cell must be UNIQUE. No duplicates.

THE GRID CONTENT (3 TYPES):
TYPE A: THE LOGO BLOCK (PRINT GRUNGE): Solid block in brand's primary color with ONLY the official logomark centered. Texture: Distressed screen-print with ink bleed and grunge noise.
TYPE B: THE SLOGAN BLOCK (PRINT GRUNGE): Solid block in contrasting brand color with ONLY the slogan. Texture: Heavy distressed ink texture.
TYPE C: CAMPAIGN PHOTOGRAPHY (HALFTONE): High-contrast B&W action shots. Texture: Strong halftone dot patterns, heavy film grain. "Multiply" color blending to wash photos in brand palette (duotone effect).
```

**Placeholders**: [BRAND NAME]

---

## Category 5: Icons

### UC 5.1: Notion-Styled Icons (Clean Line) [RECONSTRUCTED]

**What it does**: Minimalist Notion-styled line-art portraits. Clean black outlines on white background.

**Input type**: Smart prompt

**Template**:
```
A Notion-styled minimalist line illustration portrait of [PERSON NAME]. Clean, confident black outlines on a pure white background. The style is simplified but recognizable: key facial features (distinctive hair, glasses, facial hair, expression) are captured with minimal strokes. No shading, no gradients, no fill colors. The line weight is consistent throughout, approximately 2-3pt equivalent. The portrait shows head and upper shoulders only. The expression is neutral to slightly friendly. Below the portrait, the person's name in clean sans-serif type. The overall feel is professional, approachable, and immediately recognizable as a Notion/tech-aesthetic icon. 1:1
```

**Placeholders**: [PERSON NAME]

---

### UC 5.2: Notion-Styled Icons (Halftoned) [RECONSTRUCTED]

**What it does**: Same as 5.1 but with halftone dot texture overlay for comic-book shading effect.

**Input type**: Smart prompt

**Template**:
```
A Notion-styled portrait of [PERSON NAME] with halftone dot shading. Clean black outlines define the face and features on a white background. Shadows and tonal variation are rendered exclusively through halftone dots of varying density, no smooth gradients. Darker areas (under chin, side of nose, hair) use dense, tightly packed dots. Lighter areas use sparse, widely spaced dots. The halftone pattern is visible and deliberate, referencing 1960s pop art printing technique. Portrait shows head and upper shoulders. Below: name in clean sans-serif type. 1:1
```

**Placeholders**: [PERSON NAME]

---

### UC 5.3: Custom Branded Sticker Pack [RECONSTRUCTED]

**What it does**: Set of brand-themed stickers in various shapes and styles.

**Input type**: Direct prompt

**Template**:
```
A set of 9 custom sticker designs arranged in a 3x3 grid for [BRAND NAME]. Each sticker has a different shape (circle, rectangle with rounded corners, shield, star, banner, diamond, oval, hexagon, speech bubble). All stickers use the brand's color palette and incorporate the logo, taglines, or brand-associated imagery. The sticker style mixes: typographic stickers (bold text only), icon stickers (simple illustrations), and badge stickers (logo-centric with decorative borders). Each sticker has a white cut-line border and subtle drop shadow suggesting they could be peeled off. Background: light gray with subtle grid pattern. 1:1
```

**Placeholders**: [BRAND NAME]

---

### UC 5.4: Minimalist Character Icons (Duotone) [VERBATIM - partial]

**What it does**: Strict duotone flat vector icon of any character's face. Bold color background.

**Input type**: Smart prompt

**Template**:
```
A single, isolated, strict duotone flat vector icon representing the face of [CHARACTER NAME]. The design uses ONLY two colors: one bold, saturated background color and one contrasting tone for the facial features. No gradients, no shadows, no outlines. The face is extremely simplified: geometric shapes represent hair, eyes, nose, and mouth. Distinctive features of the person (signature hairstyle, facial hair, glasses, expression) are captured with minimal shapes. The icon is centered on a square canvas with generous padding. The person's name appears in small, clean sans-serif type below the face. Designed to work at 64x64px and 512x512px equally. 1:1
```

**Placeholders**: [CHARACTER NAME]

---

## Category 6: Mockups

### UC 6.1: Duffle Mockup [RECONSTRUCTED]

**What it does**: Any brand reimagined as a premium duffle bag design.

**Input type**: Direct prompt

**Template**:
```
A premium leather and nylon duffle bag designed by [BRAND NAME]. The bag features the brand's signature color palette as the dominant colorway with contrasting accent trim. The brand's logo is prominently displayed on the side panel, embossed into leather or woven into a patch. Materials include full-grain leather handles and base, ripstop nylon body, and brushed metal hardware (zippers, clasps, D-rings) in gunmetal finish. The bag sits on a clean white surface in a studio environment. Soft, even lighting creates gentle highlights on the metal hardware and leather. The bag is partially unzipped to show the interior lining in a brand-accent color. 3/4 view. 16:9
```

**Placeholders**: [BRAND NAME]

---

### UC 6.2: Fast Food Leather Bag [RECONSTRUCTED]

**What it does**: Luxury leather lunch/takeaway bags branded with any brand. Absurd luxury meets casual utility.

**Input type**: Auto prompt

**Template**:
```
A luxury, structured leather lunch bag designed by [BRAND NAME]. The bag is crafted from supple, premium full-grain leather in the brand's signature color. It resembles an elevated version of a classic paper lunch bag but in permanent, luxurious materials. The brand's logo is hot-stamped or embossed into the leather on the front. Details include a magnetic snap closure, leather-wrapped carry handle, and stitching in a contrasting brand-accent color. The interior is lined with suede. The bag sits on a marble surface with soft directional lighting from upper left. The leather shows natural grain and a slight sheen. 4:5
```

**Placeholders**: [BRAND NAME]

---

### UC 6.3: Branded Crumpled Stickers [RECONSTRUCTED]

**What it does**: Realistic crumpled and peeling sticker textures with brand logos applied.

**Input type**: Direct prompt

**Template**:
```
A collection of branded stickers for [BRAND NAME] in various states of wear and application. Some are freshly applied and smooth, others are crumpled with visible wrinkles and air bubbles, and several are partially peeled with curling edges revealing the white backing paper. The stickers feature the brand's logo, wordmark, and tagline in various sizes and color variants. They are applied to a weathered urban surface (metal mailbox, street pole, or laptop lid). The stickers overlap each other and show realistic adhesive residue, scratches, and sun-fading on older ones. Natural daylight. Close-up photography with shallow depth of field. 1:1
```

**Placeholders**: [BRAND NAME]

---

## Category 7: Apparel and Fashion

### UC 7.1: Fashion Model Editorial [VERBATIM]

**What it does**: Full outfit visualization on a model. Requires image input for face accuracy.

**Input type**: Image-to-image (requires uploaded face reference)

**Template**:
```
Main model (use image input with the face 100% accurate).

Wearing:
[detailed clothing description, pieces, color scheme, style, layers, fabrics].

Paired with footwear:
[type and details of shoes; include relevant accessories like socks, hats, bags, jewelry, etc.].

Setting:
studio backdrop in soft [describe color/tone/texture, e.g., pastel, urban, concrete, natural, saturated].

Lighting:
soft cinematic studio lighting

Style:
[define style, for example: fashion editorial, streetwear, minimalism, preppy, futuristic, luxury, sporty, etc.].

Composition:
model [describe pose, seated/standing/reclined, relaxed/confident/youthful] on [describe object if relevant, bench, chair, wall], with [accessories/pose details, e.g., accessories visible, hands in pocket, dramatic posture].
```

**Placeholders**: [clothing description], [footwear], [setting color/tone], [style], [pose/composition]

---

## Category 8: Custom Typography

### UC 8.1: American Retro-Lettering [RECONSTRUCTED]

**What it does**: Brand names rendered in American retro baseball/varsity lettering style. Swooping script, drop shadows.

**Input type**: Smart prompt

**Template**:
```
[BRAND NAME] rendered in classic American retro script lettering, reminiscent of 1950s baseball team logos and varsity sports typography. The letters are hand-drawn with confident, swooping curves, thick-to-thin stroke variation, and decorative swashes on capital letters and descenders. A subtle drop shadow in a darker tone adds depth. The color palette is a warm retro combination: cream, red, and navy blue, or the brand's own colors applied to this vintage framework. The lettering sits centered on a slightly off-white, textured canvas background with subtle aging and foxing marks. Below the script, a small banner or ribbon element contains a secondary tagline in block caps. 16:9
```

**Placeholders**: [BRAND NAME]

---

### UC 8.2: Frame by Frame Text Animation [RECONSTRUCTED]

**What it does**: Brand name shown as sequential animation frames, each frame showing the text in a different state of formation or movement.

**Input type**: Direct prompt

**Template**:
```
A horizontal strip showing 6 sequential animation frames of the text "[BRAND NAME]" in a bold sans-serif font. Frame 1: Letters are scattered randomly across the canvas in the brand's primary color. Frame 2: Letters begin drifting toward their correct positions. Frame 3: Letters are nearly assembled but slightly offset and overlapping. Frame 4: Letters lock into place with a subtle motion blur. Frame 5: The text is assembled, with a burst of small particles radiating outward from the letters. Frame 6: Clean, final state, letters perfectly spaced with a subtle glow. Each frame is separated by thin vertical lines. White background. The strip reads left to right like a film timeline. 16:9
```

**Placeholders**: [BRAND NAME]

---

### UC 8.3: Swiss Design Typographic Poster [RECONSTRUCTED]

**What it does**: Grid-based typographic poster in International Typographic Style. Minimal color, strong type hierarchy.

**Input type**: Direct prompt

**Template**:
```
A Swiss International Typographic Style poster for [BRAND NAME]. The design follows a strict grid system with asymmetric balance. The brand name is set in Helvetica Bold or Akzidenz-Grotesk Medium at a large scale, positioned in the upper third. Below, supporting text elements (tagline, date, location, or brand descriptors) are set in lighter weights with generous line spacing. The color palette is limited to two tones: black text on white, or the brand's primary color as a single accent element (a bold geometric shape, bar, or circle intersecting the grid). No images, no illustrations, purely typographic. Visible baseline grid and column structure inform the layout. The poster has a matte, uncoated paper texture. 9:16
```

**Placeholders**: [BRAND NAME]

---

## Category 9: Experimental

### UC 9.1: 3D Character Avatar Edition [VERBATIM]

**What it does**: Converts uploaded photo into stylized 3D character. Pixar-like but more minimal, toy figure render.

**Input type**: JSON structured prompt / Image-to-image

**Template**:
```json
{
 "task": "image_style_transfer_3d_character",
 "input": {
 "source_image": "USER_UPLOADED_IMAGE",
 "preserve_identity": true,
 "preserve_pose": true,
 "preserve_composition": true
 },
 "style_reference": {
 "render_style": "stylized_3d_character",
 "aesthetic": "soft_minimal_cartoon_3d",
 "inspiration": [
 "pixar_like_but_more_minimal",
 "toy_figure_render",
 "clean_product_character_design"
 ]
 },
 "character_design": {
 "skin": {
 "material": "smooth_matte_plastic",
 "texture": "soft_uniform",
 "subsurface_scattering": "gentle"
 },
 "facial_features": {
 "eyes": "half_closed_bored_expression",
 "eyelids": "heavy",
 "nose": "rounded_simplified",
 "mouth": "flat_neutral",
 "ears": "simplified_rounded"
 },
 "emotion": "unimpressed_calm_bored"
 },
 "clothing": {
 "style": "minimal_streetwear",
 "details": "no_logos_no_patterns",
 "fabric": "soft_matte"
 },
 "lighting": {
 "setup": "studio_softbox",
 "shadows": "very_soft",
 "contrast": "low",
 "highlights": "subtle"
 },
 "background": {
 "type": "solid_color",
 "color_palette": ["muted_green", "pastel_tone"],
 "gradient": "none"
 },
 "camera": {
 "angle": "front_facing",
 "framing": "medium_close_up",
 "lens": "50mm_equivalent",
 "distortion": "none"
 },
 "render_quality": {
 "resolution": "high",
 "edges": "clean",
 "noise": "none",
 "realism_balance": "stylized_over_realistic"
 }
}
```

**Placeholders**: USER_UPLOADED_IMAGE
**Note**: This JSON format is unusual for image gen. It's designed for structured API input and works well with Gemini's reasoning.

---

### UC 9.2: Luxury Ceramic Beverage Bottle [VERBATIM]

**What it does**: Ultra-high-end editorial of a luxury ceramic beverage bottle. Matte white ceramic body, brand-colored cap, brand-colored studio background.

**Input type**: Direct prompt

**Template**:
```
[BRAND NAME].
Act as a world-class product photographer creating an ultra-high-end editorial shot of a luxury beverage bottle.

COMPOSITION (FULL VIEW):
A full-body studio photograph showing the entire bottle from base to cap, centered in the frame. The bottle stands on a seamless surface.

THE VESSEL & COLORS (MATERIALITY):
Bottle Body: Premium, opaque matte white ceramic with a fine, powdery texture.
Bottle Cap: A premium matte or satin-finish cap colored exactly in [BRAND NAME]'s primary brand color.

LIGHTING & BACKGROUND (COLORED STUDIO):
The background is a seamless, smooth studio cyclorama flooded with [BRAND NAME]'s primary brand color.
Lighting: Sophisticated, high-end white studio lighting (large softboxes). Soft and wrapping, creating elegant highlights along ceramic edges.

CENTRAL BRANDING (ULTRA-PRECISION MICRO-EMBOSSING):
The main Gothic/Blackletter [BRAND NAME] text is centered on the bottle.
CRITICAL TEXTURE FIX: ultra-subtle, shallow precision micro-embossing (maximum 0.2mm to 0.3mm depth). Must NOT look like applied clay or heavy badge. Crisp, shallow tooling mark integrated into ceramic surface.
Color: Embossed text colored in brand's primary color, slight semi-gloss.

TYPOGRAPHIC HIERARCHY (AUXILIARY DETAILS):
All auxiliary text printed in neutral dark grey/black (monochrome):
Top Micro-Blocks: Two small lines (e.g., "LIMITED EDITION // BATCH 001").
Flavor Name: Below main text, smaller unobtrusive font.
Volume/Specs: Technical info (e.g., "500ML").
Ingredients Block: Dense micro-print at bottom edge.

CORNER ELEMENTS:
Top Right: Small, discrete monochrome Gothic brand name.
Bottom Right: Small monochrome original brand logo.
```

**Placeholders**: [BRAND NAME]
