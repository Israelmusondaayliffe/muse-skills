# Use Case Catalog for Uni-1

These are preserved prompt recipes from the source skill. Read the relevant example, then adapt its subject, count, references, format and requested change to the current brief. Concrete counts, aspect ratios, media and named model settings in examples are recipe values, never studio defaults. A prompt field such as `controlnet`, `recommended_weight`, `quality`, `system` or `search` is descriptive text unless the selected host exposes a matching real control. The current skill and shared prompt contract govern execution. Some historical examples contain pose shifts, fixed counts or search calls; use those only when the current request calls for them. Attribution remains source-recorded unless separately verified.


30+ specialized use cases with triggers, recommended mode, template, and pattern notes. Scan this during Step 2 of every invocation to identify applicable patterns for the user's request.

---

## PORTRAITURE & PEOPLE

### UC 1: Documentary Portrait
**Trigger:** portrait, documentary, editorial portrait, real person, candid
**Mode:** CREATE or SHOW-ME
**Template:** Cinematic Control
**Pattern:** Subject + environment tell a story. Imperfect details (worn hands, messy workspace, natural skin) signal authenticity. Natural light, medium focal length (50mm-85mm). The person IS their context.

### UC 2: Fashion Editorial
**Trigger:** fashion, editorial, lookbook, campaign, outfit, styling
**Mode:** CREATE or SHOW-ME
**Template:** Cinematic Control
**Pattern:** Clothing is the subject. Every garment described with color, material, fit. Environment complements (not competes). Pose and body language serve the clothing. Multiple framings (wide for silhouette, close for texture).

### UC 3: Character Transformation (Pixar/Anime/Stylized)
**Trigger:** pixar, anime, cartoon, 3D character, manga, ghibli, stylized
**Mode:** STYLE-SHIFT
**Template:** Fast Start + anti-paste recomposition
**Pattern:** Maintain 2-3 anchoring identity features. Exaggerate proportions for target style. Eyes carry the style's magic. Background shifts to match aesthetic. Anti-paste mandatory: new pose native to the animation style.

### UC 4: Character Sheet / Reference Sheet
**Trigger:** character sheet, reference sheet, multiple angles, turnaround
**Mode:** LAYOUT
**Template:** Layout Control
**Pattern:** 4-panel grid (front, 3/4, profile, back). Consistent lighting, outfit, expression across all panels. Neutral background. Explicit panel labeling. Uni-1 excels here because reasoning plans consistency.

### UC 5: Age Progression / Regression
**Trigger:** aging, younger, older, age shift, de-age, time progression
**Mode:** TEMPORAL
**Template:** Cinematic Control
**Pattern:** Bone structure persists. Skin, hair, posture change. Each age has appropriate context (toys for child, workspace for adult, garden for elder). Recompose for each age, do not just filter.

### UC 6: Group / Multi-Person Scene
**Trigger:** group, team, couple, family, multiple people, together
**Mode:** CREATE or FUSE
**Template:** Cinematic Control or Fusion
**Pattern:** Max 5 people for reliable consistency. Each person needs distinct description. Position each explicitly. Interaction/body language between them matters more than individual poses. Avoid default side-by-side lineup.

---

## PRODUCTS & COMMERCIAL

### UC 7: Studio Product Hero
**Trigger:** product shot, hero image, e-commerce, product photography
**Mode:** CREATE
**Template:** Fast Start or Cinematic Control
**Pattern:** Three-point softbox, seamless background, slightly elevated camera angle. Sharp focus on key feature, shallow DOF. Ultra-clean. No dust, no fingerprints. Material properties described precisely (matte, glossy, metallic, textured).

### UC 8: Lifestyle Product in Context
**Trigger:** lifestyle, product in use, in context, in situ
**Mode:** CREATE
**Template:** Cinematic Control
**Pattern:** Product naturally integrated into scenario. Person interacting authentically (not posing with product). Natural lighting. Feels like real moment, not staged. Aspirational but believable.

### UC 9: Product Color Variant
**Trigger:** different color, color swap, color variant, show in blue/red/etc
**Mode:** MODIFY
**Template:** Direct Edit
**Pattern:** Change ONLY the color element. Maintain form, lighting, reflections, environment. New color must interact with light consistently (matte absorbs, glossy reflects, metallic shifts).

### UC 10: VFX Product Swap
**Trigger:** replace product, swap the bottle, put my product in this scene
**Mode:** MODIFY or FUSE
**Template:** Direct Edit or Fusion
**Pattern:** New product matches existing lighting angle, color temperature, shadow direction. Scale appropriate to context. Hand/interaction points adjusted naturally.

### UC 11: Luxury Campaign Float
**Trigger:** floating product, levitation, campaign style, luxury
**Mode:** CREATE
**Template:** Fast Start
**Pattern:** Product suspended against minimal background. Soft shadows beneath implying hover. High contrast lighting, cinematic quality. The product IS the hero. Environment is negative space.

---

## TEXT & TYPOGRAPHY

### UC 12: Logo Design
**Trigger:** logo, brand mark, wordmark, identity, icon design
**Mode:** CREATE
**Template:** Fast Start or Structured JSON
**Pattern:** Text in quotes: 'EXACT TEXT'. Specify font feel (bold sans-serif, elegant serif, hand-drawn). Design direction (geometric, organic, typographic). Works-at-all-sizes consideration. Clean background.

### UC 13: Infographic
**Trigger:** infographic, data visualization, explain visually, visual data
**Mode:** CREATE or LAYOUT
**Template:** Layout Control or Structured JSON
**Pattern:** Uni-1's reasoning sweet spot. Clear hierarchy: headline, sections, data callouts. Exact text in quotes. Specify flow direction (top-down, left-right, radial). Color scheme matching topic. Uni-1 plans layout before rendering, so labels are readable.

### UC 14: Text Effect / Typographic Art
**Trigger:** text effect, typography art, lettering, glass text, 3D text
**Mode:** CREATE
**Template:** Fast Start
**Pattern:** Exact text in quotes. Describe the effect precisely (refracted through glass, carved in stone, growing from moss). Light source and how it interacts with the text treatment. Background that contrasts.

### UC 15: Menu / Recipe Card
**Trigger:** menu, recipe card, restaurant, food menu
**Mode:** CREATE or LAYOUT
**Template:** Layout Control
**Pattern:** Exact text for all items and prices. Layout style (single page, sections). Typography hierarchy (dish names vs descriptions vs prices). Visual elements (illustrations, borders). Paper texture.

---

## STRUCTURED CONTENT

### UC 16: Spritesheet / Icon Grid
**Trigger:** spritesheet, icon set, icon grid, emoji set, sticker pack
**Mode:** CREATE or LAYOUT
**Template:** Layout Control
**Pattern:** Grid arrangement with consistent size, style, and spacing. Each element labeled or self-explanatory. Neutral background. Consistent line weight and color treatment across all icons.

### UC 17: Technical Diagram
**Trigger:** diagram, exploded view, technical illustration, how it works, schematic
**Mode:** CREATE or LAYOUT
**Template:** Structured JSON or Layout Control
**Pattern:** Exploded isometric or orthographic view. Components separated along axis. Labels with leader lines (non-overlapping). Style: technical illustration or clean 3D render. Uni-1 reasons through spatial relationships, making this reliable.

### UC 18: Flowchart / Process Diagram
**Trigger:** flowchart, process flow, decision tree, workflow, pipeline
**Mode:** CREATE or LAYOUT
**Template:** Layout Control
**Pattern:** Nodes and connections. Clear directional flow. Decision points labeled. Color coding for different path types. Keep it readable, not dense. Uni-1 plans hierarchy before rendering.

### UC 19: Comparison Layout
**Trigger:** before/after, comparison, side by side, vs, versus
**Mode:** CREATE or LAYOUT
**Template:** Layout Control
**Pattern:** Split frame or adjacent panels. Clear visual distinction between states. Labels for each side. Consistent scale and framing across comparison. Vertical split for portraits, horizontal for landscapes.

---

## NARRATIVE & SEQUENTIAL

### UC 20: Comic Panels
**Trigger:** comic, manga panels, comic strip, panel layout
**Mode:** STORYBOARD
**Template:** Storyboard Generator
**Pattern:** "Make a [N] panel comic in [style]." Panel borders visible. Character consistent across panels. Story beats clear. Art style locked (gritty noir, manga, cartoon, realistic).

### UC 21: Step-by-Step Guide
**Trigger:** step by step, tutorial, how to, instructions, guide
**Mode:** STORYBOARD
**Template:** Storyboard Generator
**Pattern:** Each frame is one step. Numbered. Consistent environment and hands/tools. Instructional clarity over artistic flair. Key action highlighted in each frame.

### UC 22: Storyboard for Video/Film
**Trigger:** storyboard, shot list, film planning, scene breakdown
**Mode:** STORYBOARD
**Template:** Storyboard Generator + Cinematic Control hybrid
**Pattern:** Each frame specifies camera angle, shot type, character action. Consistent aspect ratio (typically 16:9). Notes for movement/transition between frames. Director's tool, not final output.

### UC 23: Day-in-the-Life Sequence
**Trigger:** day in the life, daily routine, morning to night, timeline
**Mode:** STORYBOARD
**Template:** Storyboard Generator
**Pattern:** Time progression is the narrative spine. Lighting evolves (morning to night). Character consistent but activities change. Environment shifts with routine.

---

## STYLE & TRANSFORMATION

### UC 24: Medium Transfer (Photo to Painting/Drawing/Etc)
**Trigger:** make it a painting, watercolor, sketch, illustration, render
**Mode:** STYLE-SHIFT
**Template:** Fast Start + anti-paste
**Pattern:** Name the medium precisely. Describe medium-specific properties (brushwork for painting, line weight for drawing, render quality for 3D). Recompose for the target medium. The result should look like it was CREATED in that medium.

### UC 25: Era Relocation
**Trigger:** 1920s, victorian, retro, vintage, futuristic, cyberpunk, period
**Mode:** STYLE-SHIFT or TEMPORAL
**Template:** Cinematic Control + anti-paste
**Pattern:** Everything shifts: wardrobe, technology, architecture, lighting technology, color palette, body language norms. Not just costume change. Full environmental and contextual transformation.

### UC 26: Camera Era Simulation
**Trigger:** polaroid, film, daguerreotype, disposable camera, vintage camera
**Mode:** STYLE-SHIFT
**Template:** Fast Start + anti-paste
**Pattern:** Camera-specific artifacts (flash quality, grain structure, color science, border style, exposure characteristics). Each camera era has physical properties that affect the image. Describe the camera, not just "vintage."

---

## ENVIRONMENTS & SCENES

### UC 27: Cinematic Wide Shot
**Trigger:** landscape, establishing shot, wide shot, scenic, environment
**Mode:** CREATE
**Template:** Fast Start or Cinematic Control
**Pattern:** Environment IS the subject. Human figure small if present. Lighting and atmosphere define mood. Depth layers (foreground interest, midground subject, background depth). Time of day critical.

### UC 28: Interior Scene
**Trigger:** room, interior, home, office, kitchen, studio, indoor
**Mode:** CREATE
**Template:** Cinematic Control
**Pattern:** Every surface tells a story. Lived-in details (wear patterns, personal items, imperfect organization). Lighting source visible or implied. Depth from layered objects. Scale from known objects.

### UC 29: Weather/Atmosphere Scene
**Trigger:** rain, fog, storm, snow, mist, dust, atmospheric
**Mode:** CREATE or MODIFY
**Template:** Fast Start or Direct Edit
**Pattern:** Weather affects everything: light diffusion, surface reflections, subject behavior, color saturation. Describe how elements interact with weather (wet surfaces reflect, fog softens edges, snow muffles texture).

---

## EXPERIMENTAL & CONCEPTUAL

### UC 30: Surreal Composition
**Trigger:** surreal, impossible, dream, fantasy, conceptual
**Mode:** CREATE
**Template:** Fast Start or Loose/Creative
**Pattern:** State the impossible element clearly. Uni-1 reasons through the visual logic of impossibility (if gravity is reversed, what falls up? if scale is wrong, what casts what shadow?). Ground the surreal in otherwise realistic execution.

### UC 31: Humor / Absurd Scene
**Trigger:** funny, absurd, meme, comedic, ridiculous, silly
**Mode:** CREATE
**Template:** Fast Start
**Pattern:** The comedy is in the contrast. Describe the setup with deadpan seriousness. Uni-1 understands humor, so describe WHAT is funny (a knight at Starbucks), not that it SHOULD be funny. Specific props and details sell the joke.

### UC 32: Miniature / Tilt-Shift
**Trigger:** miniature, tiny, small world, tilt shift, diorama
**Mode:** CREATE
**Template:** Fast Start
**Pattern:** Subject at toy scale. Shallow DOF blur at top and bottom of frame. Saturated colors. Real environment treated as if miniaturized. The scale relationship is the creative statement.

### UC 33: Self-Insert (User as Character)
**Trigger:** user uploads their photo + wants to be in a new scene
**Mode:** FUSE or STORYBOARD
**Template:** Fusion or Storyboard Generator
**Pattern:** User's photo is CHARACTER reference. New scene is ENVIRONMENT. Label roles explicitly. Maintain identity features. "This image is of [description]. Use as CHARACTER reference. Generate a new scene where they are [scenario]."

---

## SCANNING GUIDE

When analyzing a request, score applicable use cases:

**For people/portraits:** UC 1, 2, 3, 4, 5, 6
**For products:** UC 7, 8, 9, 10, 11
**For text/design:** UC 12, 13, 14, 15
**For structured content:** UC 16, 17, 18, 19
**For narrative/sequential:** UC 20, 21, 22, 23
**For style changes:** UC 24, 25, 26
**For environments:** UC 27, 28, 29
**For experimental:** UC 30, 31, 32, 33

List 3-5 applicable use cases in your analysis to inform creative direction generation.
