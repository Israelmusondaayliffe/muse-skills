# Domain adapter: visual

SPEC 4.1 row: a piece is a component, section, or asset. The bar is screenshots of best-in-class work. Inspection is `screenshot` and `render`. Blind comparison is strong. Integrity checks: builds and renders at every target viewport, no placeholder assets.

## What counts as a piece

A piece is a component, a section, or an asset: one hero section, one pricing table, one navigation system, one dashboard card class, one OG image set, one icon family. The unit is what a viewer can judge in one look against one reference image. Bad pieces: "the whole site" (split by section), "make it feel premium" (adjective, not a piece), "the design system" (split into token classes and component families that each render independently). Each piece declares the target viewports it must survive, and those viewports are fixed at brief time in `pieces.json`. A visual piece that cannot be rendered to pixels by a command is not a valid piece.

## What a valid bar looks like here

The bar is screenshots, not descriptions of screenshots. Fetch and store real reference images in `bar/refs/` at brief time, either directly or via a checked-in `bar/refs/fetch_refs.sh`. A missing reference file fails bar validation: `validate_bar.py` rejects any bar whose reference paths do not resolve, so "look at Linear's landing page" is not a bar until `bar/refs/` contains the actual pixels at the actual target viewports. Record in `bar/bar.md` where each reference came from, at what viewport it was captured, and which pieces it applies to. Prose like "modern, clean, minimal" fails validation on its own. Hard brand constraints (palette, typography, spacing rules) go in `bar/bar.md` as pass or fail statements the integrity verifier can check.

## Three worked bar examples

Example 1, marketing hero section. Bar: three best-in-class hero screenshots stored as `bar/refs/hero-a-1440x900.png`, `bar/refs/hero-b-1440x900.png`, `bar/refs/hero-a-390x844.png`, fetched by `bar/refs/fetch_refs.sh` at brief time. Inspection: `render` with `inspection_command: npm run build` (exit 0 required), then `screenshot` with `inspection_command: npx playwright screenshot --viewport-size=1440,900 http://localhost:4321/ rounds/hero/003/inspection/hero-1440x900.png` and a second capture at 390x844. Acceptance: blind critic picks our screenshot over the weakest reference in 2 consecutive rounds at both viewports.

Example 2, analytics dashboard card class. Bar: reference dashboard screenshots at `bar/refs/dash-ref-1440.png`, `bar/refs/dash-ref-1024.png`, `bar/refs/dash-ref-390.png`. Inspection: `render` with `inspection_command: npm run build`, then `screenshot` at each of the three declared viewports into `rounds/cards/005/inspection/`. Acceptance: blind win at 1440 and 390, and every card renders with real seeded data, no empty states shown as finished work.

Example 3, OG image asset set. Bar: four reference social cards stored under `bar/refs/og/`, each 1200x630. Inspection: `render` with `inspection_command: python3 tools/render_og.py --all --out rounds/og-set/002/inspection/` producing one PNG per template at exactly 1200x630. Acceptance: blind critic picks each of our cards over the matched reference in 2 consecutive rounds, and the monochrome constraint in `bar/bar.md` holds on every card.

## Inspection methods, in priority order

1. `screenshot`. Capture the rendered artifact at every declared viewport with a command, and store the images in `rounds/<piece>/<n>/inspection/`. This is what critics and verifiers judge.
2. `render`. Prove the artifact builds and produces output: a build command exiting 0, or an asset generation script producing files at the declared dimensions.

Both methods declare an `inspection_command`. Judgment inspects pixels, never source, never a description of the layout. A round where the build fails, a viewport is skipped, or a screenshot command produces nothing is a failed round: record the failure and return it to the builder without judging.

## Blind comparison feasibility and how to set it up

Strong. Screenshots are naturally anonymous once filenames and metadata stop leaking provenance. Setup: `blind_pair.py` copies our capture and the reference to neutral paths with neutral filenames, strips metadata, and seals the label map outside `runs/`. Compare like against like: same viewport, same content category, comparable crop. The critic receives both images, the goal, and the acceptance criterion, picks the stronger one, and names the single largest gap in the loser in terms a builder can act on (hierarchy, spacing rhythm, contrast, alignment, density), not taste words. Run the pairing per viewport; a piece that wins at 1440 and loses at 390 has not won.

## What the integrity verifier checks in this domain

Builds and renders at every target viewport declared in `pieces.json`: re-run the render and screenshot commands, confirm exit codes, and confirm an image file exists per viewport with plausible dimensions. No placeholder assets: no lorem ipsum, no gray boxes, no stock placeholder images, no broken image icons, no empty data states presented as final. Reference files present: every `bar/refs/` path in the bar still resolves. Hard constraints hold: any pass or fail brand rule in `bar/bar.md` (including a strictly monochrome palette where declared) is checked here, not by the quality critic. A screenshot that exists but was captured from an old build is a fail: timestamps and re-runs decide, not filenames.

## Common failure modes

- Description substitution: the builder or lead summarizes the layout instead of capturing it. Counter: no screenshot file, no verdict.
- Single-viewport tunnel vision: the piece converges at desktop and breaks on mobile. Counter: every declared viewport gets its own capture and its own pairing.
- Reference rot: `fetch_refs.sh` was never run, so the bar is imaginary. Counter: `validate_bar.py` fails on unresolved paths before the run starts.
- Placeholder creep: gray boxes and dummy text survive to verification. Counter: integrity verifier hunts placeholders explicitly.
- Prompted taste: gaps phrased as "make it more premium". Counter: require gaps in concrete visual terms.

## When this domain is the wrong adapter

Use `code` when the work is judged by behavior rather than appearance; a rendered page with broken logic is a code problem wearing a visual costume. Use `deck` for slide narratives: slides are visual, but the reader-proxy question set and the fabricated-figure checks belong to that adapter. Use `brand` when the deliverable is an identity system with hard constraints across asset classes rather than one component or section. Use `prose` when the words on the artifact matter more than the pixels around them. If no command can turn the work into pixels, it is not a visual piece.
