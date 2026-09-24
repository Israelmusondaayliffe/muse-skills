# Use Case Patterns

These are preserved prompt recipes from the source skill. Read the relevant example, then adapt its subject, count, references, format and requested change to the current brief. Concrete counts, aspect ratios, media and named model settings in examples are recipe values, never studio defaults. A prompt field such as `controlnet`, `recommended_weight`, `quality`, `system` or `search` is descriptive text unless the selected host exposes a matching real control. The current skill and shared prompt contract govern execution. Some historical examples contain pose shifts, fixed counts or search calls; use those only when the current request calls for them. Attribution remains source-recorded unless separately verified.


43 specialized workflows with example prompts and workflow guidance. **Scan this file during image analysis to identify applicable patterns.**

---

## CHARACTER & IDENTITY

### 1. Pixar/3D Animation Transformation

**Trigger**: "Make me Pixar", "cartoon version", "3D character"

**Pattern**:
```
Using the uploaded portrait of [explicit description], transform into a Pixar-style 3D animated character. [ANTI-PASTE: recompose as 3/4 view with slight head tilt]. Maintain [specific identifying features: face shape, distinctive hair, unique characteristics]. Apply characteristic [exaggerated proportions, stylized textures, warm render quality]. Eyes should be [color] with Pixar's signature catchlight reflections. Expression: [match original or specify]. Background: [simple gradient or story-appropriate setting]. Do not change aspect ratio.
```

**Key considerations**:
- Maintain recognizability through 2-3 anchoring features
- Exaggerate proportions stylistically but keep essence
- Eyes carry the Pixar magic. Describe them specifically.

### 2. Anime/Manga Transformation

**Trigger**: "Anime style", "manga version", "Japanese animation"

**Pattern**:
```
Using the uploaded portrait of [description], transform into [anime style: Studio Ghibli soft/shonen dynamic/seinen detailed]. [ANTI-PASTE: repose with wind-swept hair and turned shoulders]. Maintain [distinctive features]. [Hair should flow with characteristic anime physics]. Eyes: [enlarged, colored appropriately, with anime highlight patterns]. Line work: [clean cel-shaded/sketch/painterly]. Background: [gradient blur/environmental/abstract speed lines]. Do not change aspect ratio.
```

### 3. Multi-Character Consistency

**Trigger**: Multiple people in one scene, group shot from individual references

**Pattern**:
```
Using the uploaded references of [describe person 1: hair, face, build, clothing], [person 2: same detail], and [person 3: same detail], create a group scene where [scenario]. Position [person 1] at [location], [person 2] at [location], [person 3] at [location]. All looking [direction/at each other/camera]. Unified lighting: [describe]. Each person maintains their distinctive [list key features for each]. [AR]
```

**Limit**: 5 people maximum for reliable consistency

### 4. Character Sheet (4-Angle Reference)

**Trigger**: "Character sheet", "reference sheet", "multiple angles"

**Pattern**:
```
Using the uploaded portrait of [description], create a 4-panel character reference sheet showing: top-left: front view straight-on; top-right: 3/4 angle; bottom-left: profile; bottom-right: 3/4 back view. Consistent [lighting/outfit/expression] across all panels. Gray neutral background. Maintain exact [hair style, facial features, proportions]. Clear separation between panels. 1:1
```

---

## PRODUCT & COMMERCIAL

### 5. Apple-Style Product Hero

**Trigger**: "Product shot", "hero image", "e-commerce"

**Pattern**:
```
[Product description] photographed on [infinite white/gradient/contextual surface]. Studio lighting: three-point softbox setup creating soft, even illumination with controlled highlights on [reflective surfaces]. Camera: slightly elevated 45°, [lens choice for product type]. Sharp focus on [key feature], shallow depth fading background. Ultra-clean, no dust, no fingerprints. Professional retouching standard. [AR based on product proportions]
```

### 6. Lifestyle Product Context

**Trigger**: "Product in use", "lifestyle shot", "contextual"

**Pattern**:
```
[Product] naturally integrated into [specific lifestyle scenario]. [Who is using it/where it sits]. Natural lighting from [window/overhead/mixed practical]. Focus: product sharp, environment with pleasant bokeh. Tells story of [aspiration/use case]. Not staged—feels like real moment caught. [Person/hands if present] interact authentically with product. [AR]
```

### 7. Product Color Variant Swap

**Trigger**: "Show in different colors", "color variants"

**Pattern**:
```
Using the uploaded product shot of [description], change the [specific color element] from [current color] to [new color]. Maintain exact [design, form, lighting, reflections, environment, camera angle]. The [new color] should interact with light consistently—[specify if matte/glossy/metallic affects how color appears]. All other elements unchanged. Do not change aspect ratio.
```

### 8. VFX Product Swap

**Trigger**: "Replace product in scene", "swap the bottle"

**Pattern**:
```
Using the uploaded lifestyle scene showing [describe scene and current product], replace the [current product] with [new product description]. New product should match existing [lighting angle, color temperature, shadow direction, reflection quality]. Scale appropriately to [context]. Maintain all other scene elements exactly. Hand/interaction points naturally adjusted. Do not change aspect ratio.
```

---

## TEXT & TYPOGRAPHY

### 9. Logo Design Iteration

**Trigger**: "Create logo", "logo for", "brand mark"

**Pattern**:
```
Modern minimalist logo for [brand name: 'EXACT TEXT']. [Design direction: geometric/organic/typographic/abstract]. Incorporates [visual element that represents brand cleverly]. Typography: [describe font feel—bold sans-serif for tech, elegant serif for luxury, hand-drawn for artisan]. Color: [specific palette]. Works at [sizes: favicon to billboard]. Clear [symbol mark/wordmark/combination]. White or black background for versatility. 1:1
```

### 10. Infographic with Complex Text

**Trigger**: "Create infographic", "data visualization", "explain visually"

**Pattern**:
```
Infographic titled '[EXACT HEADLINE TEXT]'. [Topic/data to visualize]. Structure: [top-to-bottom flow/left-right comparison/radial/timeline]. Key data points: [list 3-5 specific facts or figures with exact text]. Typography: headline in [style], body in [style], data callouts in [style]. Color scheme: [palette matching topic]. Icons: [style—flat/outlined/illustrated]. [AR: typically 9:16 for social or 16:9 for presentation]
```

### 11. Menu/Recipe Card

**Trigger**: "Design menu", "recipe card"

**Pattern**:
```
[Restaurant style] menu featuring '[EXACT MENU TEXT]'. Layout: [single page/trifold/sections]. Items: [list dishes with exact names and prices]. Typography: dish names in [elegant script/bold caps/handwritten], descriptions in [readable body style], prices aligned [right/inline]. Visual elements: [illustrations/photos/borders/icons]. Paper texture: [cream/white/textured]. [AR matching format]
```

### 12. Glass Refraction Text Effect

**Trigger**: "Text through glass", "refracted text"

**Pattern**:
```
The text '[EXACT TEXT]' appearing [behind/through] [glass type: frosted/water-droplet-covered/beveled crystal]. Text [distorted/fragmented/prismatic] by refraction. Light source from [direction] creating [caustics/rainbows/shadows]. Background: [color/gradient/scene]. Text readable but artistically transformed. [AR]
```

---

## EDUCATIONAL & INFORMATIONAL

### 13. Exploded Technical Diagram

**Trigger**: "Exploded view", "technical breakdown", "how it works"

**Pattern**:
```
Exploded isometric view of [subject]. Components separated along [axis] showing internal structure. Each part labeled: '[LABEL 1]' pointing to [component], '[LABEL 2]' pointing to [component]. Leader lines clean and non-overlapping. Style: [technical illustration/sketch/3D render]. Background: [neutral gray/blueprint blue/white]. Reveal [specific internal mechanisms or parts]. [AR]
```

### 14. Flowchart/Process Diagram

**Trigger**: "Process flow", "decision tree", "workflow diagram"

**Pattern**:
```
Flowchart showing [process name]. Steps: [list in order with exact text]. Decision points at [where]. [Start/end shapes], [process rectangles], [decision diamonds]. Arrows flowing [left-to-right/top-to-bottom]. Style: [minimal/colorful/corporate]. Text: legible [font size description]. Color-coded by [category if applicable]. [AR matching flow direction]
```

### 15. Academic Paper Visualization

**Trigger**: "Visualize this paper", "explain this research"

**Pattern**:
```
Research visualization summarizing [topic]. Key finding headline: '[EXACT TEXT]'. Methodology: [visual representation of process]. Data: [chart type showing key result]. Implications: [icon-driven key points]. Source citation: '[AUTHOR, YEAR]'. Academic but accessible style. Color palette: [professional/subdued]. [AR]
```

---

## DESIGN & BRANDING

### 16. Brand Package Generation

**Trigger**: "Create brand identity", "brand package"

**Pattern**:
```
Complete brand identity for '[BRAND NAME]'. Logo: [symbol + wordmark description]. Color palette: primary [HEX/description], secondary [HEX/description], accent [HEX/description]. Typography: headlines in [style], body in [style]. Applied to: [list touchpoints—business card, letterhead, social profile]. Consistent visual language expressing [brand personality]. Layout: brand board showing all elements unified. 16:9
```

### 17. Recursive Brand Application

**Trigger**: Using previous output as style reference for next deliverable

**Pattern**:
```
Using the uploaded [previous brand element—logo/business card/etc.] as the style reference, create [next deliverable—website mockup/packaging/signage]. Maintain exact [color palette, typography, visual language, spacing rhythm]. Apply brand identity to [new context with specific details]. Expand visual language naturally while staying true to established style. [AR appropriate for deliverable]
```

### 18. Instagram Grid Layout

**Trigger**: "Instagram feed", "grid layout", "feed aesthetic"

**Pattern**:
```
Create a 9-image grid layout for [brand/concept]. Each image: 1:1 square. Visual coherence through [consistent filter/color palette/composition style]. Grid narrative: [describe how images flow—color rhythm/alternating types/row themes]. Individual images: [describe each or describe variety approach]. When viewed as grid, creates [overall effect—pattern/gradient/mosaic]. 1:1 per image
```

---

## PHOTO MANIPULATION

### 19. Background Removal/Replacement

**Trigger**: "Remove background", "change background"

**Pattern**:
```
Using the uploaded image of [subject description], [remove background leaving subject isolated on transparent/replace background with [new environment]]. Subject edges: [clean cut/natural hair detail/subtle feathering]. If new background: [lighting that matches subject—direction, temperature, intensity]. [Shadow underneath if grounded]. Do not change aspect ratio.
```

### 20. Relighting Existing Photo

**Trigger**: "Change lighting", "relight this", "different time of day"

**Pattern**:
```
Using the uploaded photo of [description], transform lighting from [current: flat/harsh/natural] to [target: dramatic side light/golden hour warmth/blue hour cool/studio three-point]. Shadows now fall [direction]. Highlights appear on [surfaces]. Color temperature shifts to [warm/cool/neutral]. Subject's [skin/surface] reflects new light naturally. Atmosphere: [resulting mood]. Do not change aspect ratio.
```

### 21. Photo Restoration/Colorization

**Trigger**: "Restore this photo", "colorize", "fix old photo"

**Pattern**:
```
Using the uploaded [damaged/faded/black-and-white] photograph of [description], [restore damage—scratches, tears, fading/colorize with historically accurate colors]. Maintain [original composition, subjects, setting]. [Time period for color accuracy]. Skin tones: [natural for ethnicity]. Clothing: [era-appropriate colors]. Environment: [logical colors for setting]. Quality: modern clarity while respecting vintage character. Do not change aspect ratio.
```

### 22. Historical Photo Modernization

**Trigger**: "What would they look like today", "modern version"

**Pattern**:
```
Using the uploaded historical photograph of [description from era], recreate the same [person/scene] as if photographed today with [modern camera—iPhone/DSLR/professional]. Maintain [pose, composition, mood] but update [fashion to contemporary, photography technology, color processing]. [Person] appears same age but styled for [current year]. Modern clothing appropriate for [context/personality]. Do not change aspect ratio.
```

---

## SEARCH-INTEGRATED

### 23. Real-Time Data Visualization

**Trigger**: "Current weather", "stock price chart", "live data"

**Pattern**:
```
Look up [specific data request—weather in X city/stock price of X/current stats for X] and create [visualization type]. Include: [specific metrics to find]. Present as [chart type: line/bar/gauge/map]. Style: [clean minimal/infographic/dashboard widget]. Show [timeframe if applicable]. Verify from [credible sources]. [AR]
```

### 24. Fact-Checked Infographic

**Trigger**: "Research and visualize", "fact-based graphic"

**Pattern**:
```
Look up [topic] from [source type: news/research/official data] and create infographic showing [key facts to find]. Title: '[RELEVANT HEADLINE]'. Include: [number of data points] verified facts. Sources visible [as footnotes/integrated/separate]. Style: [news/academic/social]. [AR]
```

---

## FINANCIAL & BUSINESS

### 25. Earnings Dashboard from PDF

**Trigger**: "Visualize this earnings report", "create dashboard from PDF"

**Pattern**:
```
Analyze the uploaded [earnings report/financial document] for [company] and create executive dashboard showing: [key metrics—revenue, profit, growth, segments]. Charts: [bar for comparison/line for trends/pie for composition]. Highlight: [notable findings]. Time comparison: [QoQ/YoY if data available]. Style: professional financial, [dark/light mode]. 16:9
```

### 26. Meeting Notes Visualization

**Trigger**: "Visualize meeting notes", "make this visual"

**Pattern**:
```
Transform meeting notes into visual summary. Key decisions: [bullet visuals]. Action items: [assignee + task + deadline format]. Discussion highlights: [mind map/flow]. Participants: [icon representations]. Date/project header. Style: [corporate clean/startup casual/creative agency]. Quick-scan optimized. [AR]
```

---

## ARCHITECTURAL & ENGINEERING

### 27. Blueprint from Photo

**Trigger**: "Create blueprint", "floor plan from photo"

**Pattern**:
```
Using the uploaded [room/building/space] photo, create architectural blueprint view. Top-down perspective. Include: [walls, doors, windows, fixed furniture]. Measurements: [estimated based on visible reference points]. Line weight hierarchy: [thick for walls/medium for fixtures/thin for details]. Standard architectural symbols. Scale indicator. Blue-line or black-on-white style. [AR matching space proportions]
```

### 28. Lighting Diagram

**Trigger**: "Show the lighting setup", "lighting diagram"

**Pattern**:
```
Using the uploaded photograph, create behind-the-scenes lighting diagram showing how this shot was lit. Bird's eye view of set. Show: [key light position/fill/rim/background]. Light icons: [softbox/umbrella/bare bulb/reflector]. Camera position. Subject position. Directional arrows for light spread. Standard lighting diagram symbols. 1:1
```

---

## VIDEO INTEGRATION

### 29. Keyframe for Video

**Trigger**: "Keyframe for Veo", "frame for video", "start frame"

**Pattern**:
```
[Scene description] composed as video keyframe. Camera suggests [movement to follow: pan left/dolly in/crane up/static]. Subject positioned to [allow motion/action/transformation]. Lighting consistent for [video continuity]. Aspect ratio: 16:9 for video. Frame leaves room for [where action will go]. Atmosphere supports [video mood]. 16:9
```

### 30. Transformation Sequence Midpoint

**Trigger**: "Show the transformation between", "midpoint frame"

**Pattern**:
```
Create midpoint frame showing transformation from [state A] to [state B]. Subject caught [percentage: 30%/50%/70%] through change. [Describe hybrid state—part A, part B, blending elements]. Maintains [continuous elements that anchor identity]. Motion/energy implied in [direction of transformation]. 16:9
```

---

## CAMERA SIMULATIONS

### 31. GoPro Action Shot

**Trigger**: "GoPro perspective", "action cam"

**Pattern**:
```
[Action scene] captured by GoPro mounted on [chest/helmet/stick/ground]. Wide-angle distortion: curved horizon, bulging center. First-person immersion. Motion blur appropriate to [action speed]. Colors: GoPro saturated processing. Slight [fisheye/barrel distortion]. POV of [athlete/adventurer/participant]. 16:9
```

### 32. CCTV/Security Camera

**Trigger**: "Security camera view", "CCTV perspective"

**Pattern**:
```
[Scene] as seen on CCTV security camera. High angle, corner-mounted perspective. Slight wide-angle. [Black and white or desaturated color]. Timestamp overlay: '[DATE TIME]' in corner. Slight [compression artifacts/scan lines/noise]. Night vision green if [low light]. Static composition, no artistic framing. 4:3 or 16:9
```

### 33. Vintage Film Camera

**Trigger**: "Shot on film", "vintage camera"

**Pattern**:
```
[Scene] captured on [specific: Kodak Portra 400/Fuji Superia/Ilford HP5]. Film characteristics: [grain pattern, color rendering, contrast curve]. [Light leaks if applicable]. Analog imperfections: [dust/scratches/frame edges visible]. [Color cast typical of stock]. Composition: [era-appropriate aesthetic]. [AR matching camera format]
```

---

## SPECIALIZED CATEGORIES

### 34. Puzzle/Activity Book Page

**Trigger**: "Create maze", "spot the difference", "coloring page"

**Pattern**:
```
[Activity type] for [age group]. Theme: [subject]. If maze: clear path with [difficulty level] dead ends. If spot the difference: [number] differences between two versions. If coloring page: [outline style—bold/detailed/simple] with [subject]. Line art [thickness]. Print-ready [resolution consideration]. [AR matching page format]
```

### 35. Book Cover

**Trigger**: "Book cover for", "novel cover"

**Pattern**:
```
Book cover for [genre] novel titled '[EXACT TITLE]'. Author: '[AUTHOR NAME]'. Cover image: [concept that captures theme without literal illustration]. Title typography: [style matching genre—thriller bold, romance elegant, literary refined]. Author name: [size/placement convention for genre]. Spine and back if [full wrap]. [AR: 2:3 or 5:8 for standard book proportions]
```

### 36. Tongue Twister Typography

**Trigger**: "Visualize this tongue twister", "typography art"

**Pattern**:
```
Typographic illustration of '[EXACT TONGUE TWISTER TEXT]'. Each word styled to [reflect its meaning/sound]. Layout: [flowing/structured/chaotic matching difficulty]. [Alliterative letters emphasized]. Color: [palette matching mood]. Style: [playful/elegant/graffiti]. Readable despite artistic treatment. [AR]
```

---

## PLATFORM-SPECIFIC

### 37. YouTube Thumbnail

**Trigger**: "YouTube thumbnail", "video thumbnail"

**Pattern**:
```
YouTube thumbnail for [video topic]. [Main visual—face with expression/action shot/product]. Large text: '[2-4 WORDS MAX]' in [contrasting color, heavy weight, outline if needed for readability]. [Emotion/reaction if face shown]. Saturated colors for scroll-stop. Clear at small sizes. Avoid small text. 16:9
```

### 38. LinkedIn Post Image

**Trigger**: "LinkedIn graphic", "professional post image"

**Pattern**:
```
Professional graphic for LinkedIn post about [topic]. Style: [corporate clean/thought leader/data-driven]. Text if any: '[SHORT HEADLINE]'. Visual: [relevant imagery/abstract concept/headshot with context]. Colors: [professional palette—avoid neon/playful]. Readable on mobile. 1:1 or 4:5
```

### 39. Pinterest Pin

**Trigger**: "Pinterest image", "pin graphic"

**Pattern**:
```
Pinterest-optimized image for [topic/product/tutorial]. Tall format emphasizing [scroll-stopping visual]. Text overlay: '[EXACT TEXT—keep short]' in [readable font against image]. Rich, saturated colors. Strong visual hierarchy. Style: [lifestyle/infographic/product]. 2:3
```

### 40. Stories/Reels Frame

**Trigger**: "Instagram story", "reel frame", "vertical video frame"

**Pattern**:
```
Vertical frame for [Stories/Reels]. [Scene/subject positioned for vertical viewing]. Text safe zone respected [not in top/bottom extremes]. Thumb zone clear [bottom third for UI]. Engaging for [3-second hook]. Works as [static or video thumbnail]. 9:16
```

---

## COMBINING PATTERNS

Complex requests often combine patterns:

**Character + Product**:
```
Using the uploaded portrait of [person description], place them in [lifestyle context] holding/wearing/using [product description]. Natural interaction. Lighting unifies both elements. [AR]
```

**Data + Brand**:
```
Create infographic showing [data] in the visual style of [brand reference]. Maintain [brand colors, typography, visual language]. Data visualization follows brand aesthetic. [AR]
```

**Historical + Modern**:
```
Recreate [historical photo description] but [in modern context/with modern technology/contemporary styling]. Keep [compositional elements, pose, mood]. Update [fashion, technology, color grading]. [AR]
```

---

## ADVANCED PROMPTING TECHNIQUES

These techniques emerged from power-user experimentation and were highlighted by Google as effective strategies for getting more from Nano Banana Pro.

### 41. Variable-Defined Composition (Pseudo-Code Prompting)

**Trigger**: Complex multi-element scenes, technical diagrams, product sequences, anything requiring internal consistency across multiple objects

**Why it works**: Gemini 3 Pro's reasoning engine treats labeled variables as stable containers. Defining elements upfront prevents attribute drift, accidental merging, or illogical resizing. Works especially well for spatial relationships and material consistency.

**Pattern (Text-to-Image)**:
```
Define [VARIABLE_A] as [detailed object description with form, scale, material].
Define [VARIABLE_B] as [texture, finish, or surface quality].
Define [VARIABLE_C] as [lighting condition or color palette].

Create [scene type] where [VARIABLE_A] incorporates [VARIABLE_B] across [specific application]. Environment lit by [VARIABLE_C]. [Spatial relationship between elements]. [AR]
```

**Example**:
```
Define VESSEL as a tall cylindrical tower with ribbed vertical ridges and tapered base.
Define SURFACE as frosted glass with subtle internal luminescence.
Define LIGHT as cool directional studio lighting from upper left.

Create a minimalist product visualization where VESSEL incorporates SURFACE across its full exterior. Environment lit by LIGHT with soft gradient background fading from charcoal to white. VESSEL centered, slight 15° rotation. 4:5
```

**Pattern (Image Editing)**:
```
Using the uploaded [explicit description], define the following transformations:
CHANGE_A: [specific element] becomes [new state].
CHANGE_B: [specific element] becomes [new state].

Apply CHANGE_A to [location]. Apply CHANGE_B to [location]. Maintain [unchanged elements]. Do not change aspect ratio.
```

**Key considerations**:
- Use ALL_CAPS for variable names (mimics code convention, increases model attention)
- Define 2-4 variables maximum. More creates confusion
- Reference variables by exact name throughout prompt
- Best for: technical illustrations, multi-object still life, product catalogs, architectural concepts

---

### 42. Intentional Imperfection (Analog Realism Injection)

**Trigger**: Documentary style, vintage photography, lived-in realism, editorial authenticity. When output looks "too clean" or "AI sterile"

**Why it works**: Nano Banana Pro defaults to clinical perfection. Real cameras create incidental artifacts: lens dust, shake blur, light leaks, uneven exposure. These imperfections signal authenticity. The key is specificity. Not "make it imperfect" but naming the exact type, cause, and intensity.

**Pattern (Text-to-Image)**:
```
[Scene description with subject, action, environment]. Captured with [camera type/era] characteristics: [specific imperfection 1: lens artifact, motion quality, or exposure issue], [specific imperfection 2: film/sensor quality]. [Mood enhanced by imperfection]. [AR]
```

**Imperfection library** (pick 1-2 per prompt):

| Category | Specific tokens |
|----------|-----------------|
| Lens artifacts | subtle dust particles catching stray light, minor chromatic aberration at frame edges, soft corner vignette from aging optics, slight barrel distortion |
| Motion quality | handheld shake consistent with hurried capture, subject motion blur suggesting movement, micro-vibration from mirror slap |
| Exposure | minor overexposure in bright areas, crushed shadows from limited dynamic range, uneven development across frame |
| Film/sensor | fine grain structure of pushed film, color cast from expired stock, hot pixels in shadows, compression artifacts |
| Environmental | raindrops on lens surface, condensation fog at edges, sand/dust on sensor |

**Example**:
```
A crowded flea market at midday, stalls overflowing with vintage kitchenware and worn textiles, shoppers browsing with canvas bags. Captured with aging compact camera characteristics: minor overexposure in bright sky areas bleeding into awning edges, subtle warm vignette from worn lens coating. Feels like found photograph from a shoebox. 3:2
```

**Pattern (Image Editing)**:
```
Using the uploaded [explicit description], add [specific imperfection type] as if photographed with [camera/condition]. Apply [imperfection] to [specific areas: highlights/edges/overall]. Maintain subject clarity while adding [environmental/technical artifact]. Do not change aspect ratio.
```

**Key considerations**:
- Match imperfection to era/camera type for coherence (iPhone = lens flare, not film grain)
- Subtlety beats heavy-handedness. "Minor" and "subtle" are useful modifiers
- Best for: documentary, editorial, vintage recreation, photojournalism aesthetic, archival simulation

---

### 43. Perspective Blending (Doubling the Instructions)

**Trigger**: Layered storytelling, spatial depth, conceptual photography, when single viewpoint feels flat

**Why it works**: Instead of two separate views, you fold a secondary perspective into the scene's conceptual fabric. Gemini 3 Pro's reasoning harmonizes both constraints, reshaping composition, lighting, and spatial cues to incorporate both simultaneously. Creates depth and narrative tension impossible from single vantage.

**Pattern (Text-to-Image)**:
```
[Primary scene description with subject, environment, lighting]. Subtly recomposed with spatial cues suggesting [secondary perspective: different viewer position, scale, or interpretive angle]. [How the two perspectives interact: what's revealed, emphasized, or distorted]. [AR]
```

**Secondary perspective options**:

| Type | Example tokens |
|------|----------------|
| Scale shift | ...as if viewed from floor at mouse height / ...from bird's eye revealing hidden patterns / ...from child's eye level looking up |
| Temporal | ...with traces of how it appeared 50 years ago bleeding through / ...showing the moment just before and just after simultaneously |
| Emotional | ...recomposed as the subject themselves would remember it / ...with the distortions of fading memory |
| Functional | ...revealing the hidden infrastructure beneath the surface / ...showing heat signatures overlaid on visible light |

**Example**:
```
Interior of a classical library, tall mahogany shelves reaching toward vaulted ceiling, warm lamplight pooling on leather reading chairs. Subtly recomposed with spatial cues suggesting how the same room would appear when viewed from the floor at mouse height, emphasizing the monumental scale of chair legs as columns, dust motes becoming boulders in lamplight shafts. 16:9
```

**Pattern (Image Editing)**:
```
Using the uploaded [explicit description], reinterpret the composition by integrating spatial cues from [secondary perspective]. Maintain [primary subject and lighting] while [specific adjustment: exaggerating scale relationships, adding reveals, shifting emotional weight]. Do not change aspect ratio.
```

**Key considerations**:
- The secondary perspective should *inform* composition, not split the image
- Works best when perspectives share subject but differ in relationship to it
- Avoid literal split-screen. The blend should be conceptual, not mechanical
- Best for: editorial photography, architectural visualization, narrative illustration, conceptual art, children's book illustration

---

## TECHNIQUE QUICK REFERENCE

| Technique | Best for | Avoid when |
|-----------|----------|------------|
| Variable-defined (#41) | Multi-element consistency, technical diagrams | Simple single-subject portraits |
| Intentional imperfection (#42) | Documentary, vintage, editorial realism | Clean product shots, infographics |
| Perspective blending (#43) | Narrative depth, conceptual work | Straightforward documentation |

---

## USE CASE SCANNING GUIDE

When an image is uploaded, scan this list to identify 3-8 applicable patterns:

**For portraits**: #1, #2, #3, #4, #22, #35, #37, #38
**For products**: #5, #6, #7, #8, #41
**For scenes/locations**: #19, #20, #27, #28, #29, #42, #43
**For documents/data**: #10, #13, #14, #15, #23, #24, #25, #26
**For brands/design**: #9, #16, #17, #18
**For social content**: #37, #38, #39, #40
**For creative/experimental**: #12, #30, #31, #32, #33, #36, #41, #42, #43

List applicable patterns in image analysis to inform creative exploration beyond the obvious directions.
