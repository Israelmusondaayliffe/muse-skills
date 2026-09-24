# Texture Library

These are preserved prompt recipes from the source skill. Read the relevant example, then adapt its subject, count, references, format and requested change to the current brief. Concrete counts, aspect ratios, media and named model settings in examples are recipe values, never studio defaults. A prompt field such as `controlnet`, `recommended_weight`, `quality`, `system` or `search` is descriptive text unless the selected host exposes a matching real control. The current skill and shared prompt contract govern execution. Some historical examples contain pose shifts, fixed counts or search calls; use those only when the current request calls for them. Attribution remains source-recorded unless separately verified.


Complete token library for skin, materials, and environmental textures. Use these for specificity in prompts.

---

## Skin Texture Tokens

### Primary Face Tokens (ECU/Macro use)

| Token | Effect | Best Lighting |
|-------|--------|---------------|
| `visible pores` | Skin pore detail on nose, cheeks, forehead | Side light |
| `natural skin sheen` | Subtle oil/moisture highlight | Any front |
| `fine peach fuzz` | Vellus hair on face | Backlight/rim |
| `constellation of freckles` | Natural freckling pattern | Direct |
| `fine lines` | Micro-wrinkles, expression lines | Side/hard |
| `natural redness` | Flush zones at cheeks, nose tip | Any |
| `skin imperfections` | Moles, small scars, blemishes | Even |
| `visible capillaries` | Thin skin areas (temples, eyelids) | Very close macro |

### Secondary Face Tokens

| Token | Effect | When to Use |
|-------|--------|-------------|
| `micro-wrinkles around eyes` | Crow's feet, laugh lines | Expressions, mature subjects |
| `natural undereye texture` | Realistic under-eye skin | Close portraits |
| `authentic lip texture` | Lip grain, moisture, cracks | Lip focus shots |
| `natural eyebrow hairs` | Individual brow detail | ECU on eyes |
| `ear lobe detail` | Realistic ear texture | Profile shots |
| `neck skin texture` | Natural neck lines, cords | Below-chin framing |
| `hairline detail` | Baby hairs, natural edge | Forehead visible |

### Body Texture Tokens

| Token | Effect | When to Use |
|-------|--------|-------------|
| `visible goosebumps` | Cold or emotional reaction | Shoulders, arms visible |
| `natural body hair` | Light arm/leg hair | Non-shaved realism |
| `knuckle creases` | Hand detail | Hand close-ups |
| `collarbone definition` | Bone structure visible | Décolletage shots |
| `shoulder freckles` | Sun exposure pattern | Bare shoulders |
| `elbow texture` | Realistic joint skin | Arms visible |
| `knee texture` | Realistic joint skin | Legs visible |

### Shot Distance Guide

**Extreme Close-Up (ECU)**: 3-5 primary tokens
```
visible pores, fine peach fuzz, natural skin sheen, micro-wrinkles around eyes, constellation of freckles
```

**Close-Up (CU)**: 2-3 tokens
```
visible pores, natural skin sheen, fine lines
```

**Medium Close-Up (MCU)**: 1-2 tokens
```
natural skin texture, visible pores
```

**Medium Shot (MS)+**: 0-1 tokens
```
natural skin texture OR none
```

---

## Material Texture Tokens

### Fabrics

| Token | Description |
|-------|-------------|
| `raw silk texture` | Slight sheen, natural slubs |
| `crushed velvet nap` | Direction-sensitive pile |
| `linen weave visible` | Open weave, natural creasing |
| `cashmere softness` | Ultra-fine, matte, luxurious |
| `denim twill pattern` | Diagonal weave, indigo depth |
| `leather grain` | Natural animal texture |
| `patent leather shine` | High gloss, mirror-like |
| `suede nap` | Soft, brushed texture |
| `wool cable knit` | Dimensional, chunky pattern |
| `chiffon transparency` | Sheer, floating, layered |
| `sequin reflection` | Multiple point highlights |
| `lace pattern detail` | Intricate negative space |
| `tulle layers` | Stiff net, volume |
| `satin drape` | Smooth, reflective folds |
| `tweed texture` | Multicolor woven, wool |

### Metals

| Token | Description |
|-------|-------------|
| `brushed aluminum` | Linear scratches, matte |
| `polished chrome` | Mirror finish, hard reflections |
| `aged bronze patina` | Green oxidation, warmth |
| `hammered copper` | Irregular surface, warm glow |
| `matte black anodized` | No reflection, absorbing |
| `gold leaf texture` | Thin, irregular, precious |
| `oxidized silver` | Darkened, tarnished character |
| `surgical steel precision` | Clean, cold, exact |
| `cast iron texture` | Rough, porous, industrial |
| `brass antiqued` | Warm, worn, heritage |

### Natural Materials

| Token | Description |
|-------|-------------|
| `weathered wood grain` | Aged, silvered, character |
| `polished walnut` | Deep, warm, refined |
| `raw oak texture` | Open grain, blonde |
| `bamboo segments` | Node pattern, sustainable |
| `cork granular surface` | Compressed bark texture |
| `marble veining` | Natural mineral patterns |
| `granite speckle` | Mixed crystals, durability |
| `terrazzo aggregate` | Embedded chips, retro |
| `concrete raw pour` | Industrial, minimal |
| `quartzite shimmer` | Crystalline reflection |
| `slate layered` | Flat, natural cleaving |
| `brick weathered face` | Fired clay, mortar lines |

### Glass & Transparency

| Token | Description |
|-------|-------------|
| `crystal clarity` | Perfect transparency, sharp |
| `frosted glass diffusion` | Soft blur, privacy |
| `beveled glass prismatic` | Rainbow edge refraction |
| `textured privacy glass` | Pattern obscuring |
| `water droplets on glass` | Condensation, lensing |
| `cracked glass web` | Shattered but holding |
| `seeded glass bubbles` | Vintage, imperfect |
| `dichroic color shift` | Angle-dependent color |
| `etched glass matte` | Sandblasted pattern |
| `molten glass drip` | Hot, flowing, dangerous |

### Ceramics & Stone

| Token | Description |
|-------|-------------|
| `matte ceramic finish` | Soft, touchable, refined |
| `high-gloss porcelain` | Mirror-like, delicate |
| `raku crackle glaze` | Intentional crazing pattern |
| `terracotta warmth` | Porous, earthen, rustic |
| `bone china translucency` | Light passing through |
| `stoneware rustic` | Thick, sturdy, handmade |
| `majolica painted` | Traditional decorated |
| `unglazed bisque` | Raw fired clay, porous |

---

## Environmental Texture Tokens

### Water States

| Token | Description |
|-------|-------------|
| `mirror-still water` | Perfect reflection, calm |
| `rippling distortion` | Moving, warping reflections |
| `ocean spray mist` | Salt, suspended droplets |
| `rain-streaked surface` | Vertical running drops |
| `puddle reflection` | Inverted world, ground level |
| `waterfall curtain` | Solid-seeming water sheet |
| `steam rising` | Heat, moisture, obscuring |
| `dew drops spherical` | Perfect morning beads |
| `ice crystalline structure` | Frozen, angular, clear |
| `frost pattern` | Delicate frozen lacework |

### Atmospheric

| Token | Description |
|-------|-------------|
| `dust motes in light` | Floating particles, beam |
| `fog density gradient` | Near clear, far obscured |
| `smoke wisps curling` | Lighter than air, flowing |
| `haze softening distant` | Aerial perspective |
| `rain sheets falling` | Visible precipitation |
| `snow flurries` | Scattered flakes, movement |
| `sandstorm particles` | Gritty, obscuring |
| `pollen suspended` | Spring, yellow, allergic |
| `fire embers floating` | Glowing particles rising |

### Ground/Surface

| Token | Description |
|-------|-------------|
| `cracked earth drought` | Desiccated, pattern |
| `fresh soil turned` | Rich, dark, gardening |
| `sand ripples wind-formed` | Desert pattern |
| `gravel scatter loose` | Multiple sizes, uneven |
| `moss carpet soft` | Green, damp, forest floor |
| `fallen leaves layer` | Autumn, decay, color |
| `grass blades individual` | Close meadow detail |
| `mud wet reflective` | Recent rain, tracks |
| `snow pristine undisturbed` | Perfect white, fresh |
| `asphalt oil rainbow` | Urban, wet, iridescent |

### Architectural

| Token | Description |
|-------|-------------|
| `exposed brick character` | Industrial, warm |
| `plaster weathered` | Peeling, revealing layers |
| `concrete brutalist` | Raw, massive, intentional |
| `stucco Mediterranean` | Textured, warm, bright |
| `wooden beam aged` | Structural, historic |
| `tile geometric pattern` | Repeated, precise |
| `wallpaper vintage` | Pattern, period, domestic |
| `crown molding detail` | Architectural ornament |
| `window mullion shadow` | Light pattern, grid |

---

## Texture Combination Patterns

### Contrast Pairings

```
Soft organic + Hard industrial
natural skin texture + brushed aluminum background

Warm natural + Cool synthetic
weathered wood grain + polished chrome accents

Rough weathered + Smooth pristine
cracked earth drought + mirror-still water

Transparent + Opaque
crystal clarity glass + matte black anodized metal
```

### Harmony Pairings

```
Luxe natural stack
cashmere softness + polished walnut + aged bronze patina

Industrial cohesion
raw concrete pour + surgical steel + matte ceramic finish

Organic forest
moss carpet soft + weathered wood grain + dew drops spherical

Urban night
asphalt oil rainbow + neon reflection + rain-streaked glass
```

### Shot-Specific Texture Bundles

**Beauty Portrait (ECU)**:
```
visible pores, fine peach fuzz, natural skin sheen, constellation of freckles
```

**Fashion Editorial**:
```
crushed velvet nap, gold leaf texture, satin drape, patent leather shine
```

**Product Luxury**:
```
brushed aluminum, polished walnut, matte ceramic finish, cashmere softness
```

**Environmental Moody**:
```
fog density gradient, rain-streaked surface, weathered wood grain, moss carpet
```

---

## Platform-Specific Texture Considerations

### Instagram
- Visible textures even at phone resolution
- Strong contrast for scroll-stopping
- Skin texture: moderate (readable on small screen)

### Print
- Maximum texture detail (4K output)
- Subtle variations visible
- Skin texture: full ECU range if shot type supports

### Video Keyframe
- Consistent textures across frames
- Avoid extreme detail that flickers
- Material textures stable across movement

---

## Anti-Pattern Warnings

**Don't stack incompatible textures**:
❌ `visible pores, matte skin, no texture`: contradictory
❌ `mirror polish, brushed finish`: opposite finishes

**Don't over-texture for distance**:
❌ ECU tokens on wide shot: invisible, wasted tokens
❌ Material detail when product is small element: viewer won't see

**Don't forget lighting affects texture visibility**:
❌ `visible pores` with flat front lighting: won't show
✅ `visible pores` with side/raking light: reveals depth
