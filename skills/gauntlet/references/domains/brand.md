# Domain adapter: brand

Summary row: a piece is a positioning line, an identity element, an asset class, or a channel piece. The bar is reference identity systems plus the project's hard constraints. Inspection is `render` plus cross-asset consistency checks. Blind comparison is strong. Integrity checks: hard constraints hold, including the strictly monochrome personal palette with no chromatic accents.

## What counts as a piece

Four piece types, and only these:

1. **Positioning line.** A line or short set of lines whose job is instant comprehension of who this is and for whom. Text, so it is knowledge work: `read` must pair with `reader-proxy`.
2. **Identity element.** Wordmark, type system, grid, spacing rules. Judged from rendered exports at the sizes where the element must survive.
3. **Asset class.** A family of templates (social cards, carousel frames, slide masters). Judged as a set: every member rendered, consistency inspected across them.
4. **Channel piece.** One concrete deployment (a banner, a profile set, a one-pager) built from the system.

"Refresh the brand" is not a piece. Decompose into the four types above.

## What a valid bar looks like here

Two layers, kept separate on purpose:

1. **Reference identity systems.** Real image exports of best-in-class systems stored in `bar/refs/` (or fetched by `bar/refs/fetch_refs.sh` before the run starts). A missing reference file fails bar validation. These set the craft bar for the quality critic.
2. **The project's hard constraints.** Written in `bar/bar.md` under non-negotiables. For this user that includes the strictly monochrome personal palette with no chromatic accents. Hard constraints are pass or fail, never a matter of taste, and they are checked by the integrity verifier, not the quality critic. References may themselves be chromatic; the critic judges craft against them while the constraint check runs separately by script.

## Three worked bar examples

**1. Personal wordmark and type system piece.**
Bar: `bar/refs/identity-a/` and `bar/refs/identity-b/` (PNG exports of two reference systems), plus the monochrome constraint in `bar/bar.md`.
Render: export the wordmark at 32 px, 120 px, and 800 px widths to `rounds/wordmark/003/inspection/renders/` with a declared `inspection_command`, exit 0 required.
Measure: `python3 tools/check_monochrome.py --dir rounds/wordmark/003/inspection/renders --max-channel-delta 0` (a pixel where R, G, and B differ is chromatic). Threshold: zero chromatic pixels, pass or fail.
Acceptance: blind critic picks our renders over the reference set in 2 consecutive rounds, and the measure passes.

**2. Positioning line set piece.**
Bar: `bar/refs/reference-positioning.md`, real lines from comparable practitioners.
Inspection: `reader-proxy` with frozen questions: after one reading, say what this person does, for whom, and what you would click next. Guesses are gaps.
Blind: blind prose pairing of our lines against the reference lines via `blind_pair.py`.
Acceptance: 2 consecutive blind wins plus reader-proxy answers all three questions without guessing.

**3. Social template asset class piece (five carousel frames).**
Bar: `bar/refs/carousel-refs/` renders plus hard constraints.
Screenshot: `npx playwright screenshot templates/carousel-01.html rounds/social-templates/002/inspection/carousel-01.png` at 1080x1350, repeated for all five frames.
Measure: the monochrome check across the whole `inspection/` directory, threshold zero chromatic pixels, plus a token check that every frame uses only the type sizes declared in `templates/tokens.json`.
Acceptance: blind set-versus-set win in 2 consecutive rounds, both measures pass.

## Inspection methods, in priority order

1. `render`. Mandatory for every visual piece: real exports at every declared size and format, produced by a command with a recorded exit code. Never judge a description or a source file.
2. `measure`. The hard-constraint check, scripted: chroma scan, token conformance, contrast floors. This is the enforcement layer for pass-or-fail constraints.
3. `screenshot`. For HTML or app-surface assets, and to capture cross-asset consistency: render all members of an asset class and inspect them side by side as one evidence set.
4. `reader-proxy`. Mandatory for positioning lines and any text-bearing piece.
5. `read`. Only ever paired with `reader-proxy`; never sufficient alone.

## Blind comparison feasibility and how to set it up

Strong for rendered assets. Export ours and the reference to the same format and resolution, run `blind_pair.py` to neutralize paths and filenames, strip metadata, and seal the map outside `runs/`. For asset classes, pair set against set, not frame against frame, so cross-asset consistency is part of what the critic sees. One caveat: when the constraint makes ours visually distinctive (monochrome against chromatic references), the blind cannot fully hide provenance. Record that honestly in the verdict; instruct the critic to judge craft (hierarchy, spacing, type, composition) and never to treat palette as a gap in either direction, because palette is the integrity verifier's territory.

## What the integrity verifier checks in this domain

- Hard constraints hold, checked here and not by the quality critic. The strictly monochrome personal palette with no chromatic accents is pass or fail, never taste: the `measure` output must exist for the current round and report zero chromatic pixels.
- Renders actually executed: exports present in `inspection/` at every declared size, exit codes recorded.
- No placeholder assets, stock temp images, or lorem text in shipped pieces.
- Reference files in `bar/refs/` exist and match what the bar named.
- Positioning claims that state facts trace through the claim ledger.

## Common failure modes

- Routing the monochrome check to the quality critic, where it decays into a taste debate. It is a scripted integrity check.
- Accepting "nearly monochrome" or a single chromatic accent as an intentional exception. There are no exceptions without a re-brief that rewrites the hard constraint.
- Judging source SVGs or CSS instead of rendered pixels. Violates INV-3.
- References described from memory instead of stored as files.
- Converging every asset individually while never inspecting the class as a set, shipping five frames that do not look like one system.
- Rendering only at the large flattering size and skipping the 32 px survival test.

## When this domain is the wrong adapter

- The artifact is a full web page or product UI where layout and interaction dominate: use `visual`, importing brand hard constraints as per-piece checks.
- Long-form brand copy, manifesto, or about page: use `prose`.
- Deciding the positioning strategy itself (options, assumptions, recommendation): use `strategy`.
- Audience or market research behind the brand: use `research`.
