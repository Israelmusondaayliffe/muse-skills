# Domain adapter: deck

Summary row: a piece is a narrative arc, an individual slide, or a visual system. The bar is reference decks in the category. Inspection is `render` and `reader-proxy`. Blind comparison is strong. Integrity checks: no fabricated figures, every number sourced.

## What counts as a piece

Three piece types, and only these:

1. **Narrative arc.** The slide-order argument of the whole deck or a self-contained section of it: ask, evidence, next step. Judge it from rendered slides read in order, never from an outline.
2. **Individual slide.** One slide that must carry weight alone: the ask slide, the traction slide, the pricing slide. Its artifact path is one rendered slide image or one page of the rendered PDF.
3. **Visual system.** The type scale, grid, chart style, and color rules applied across the deck. Judged by rendering several representative slides and comparing them as a set.

A "make the deck better" piece is not a piece. Split it. A piece whose artifact is speaker notes or a content plan belongs to `prose`, not here.

## What a valid bar looks like here

Real reference decks in the same category, stored as files in `bar/refs/` (PDF or per-slide PNG exports), plus a fetch script when they come from the web. `validate_bar.py` fails the bar if a reference path does not resolve. Descriptions of decks are not a bar. "Investor-grade" is not a bar. The bar states which reference deck each piece is compared against and at what rendered size.

Every deck bar also carries a numbers rule: each figure that appears on a slide must have a claim-ledger row, and `claim_audit.py` must report zero `unsupported` rows.

## Three worked bar examples

**1. Seed pitch deck, narrative arc piece.**
Bar: `bar/refs/frontrow-seed-deck.pdf` and `bar/refs/ycombinator-demo-deck.pdf`, both real files.
Render: `npx @marp-team/marp-cli slides/deck.md --pdf -o rounds/pitch-arc/004/inspection/deck.pdf` (exit 0 required).
Acceptance: blind critic picks our rendered PDF over the reference in 2 consecutive rounds, and the reader-proxy answers all four fixed questions without guessing.

**2. Quarterly board update, metrics slides piece.**
Bar: last year's strongest board deck at `bar/refs/board-2025q4.pdf`, plus the numbers rule.
Inspection: `render` as above, then `python3 "<plugin-root>/scripts/claim_audit.py" --run-dir .gauntlet/runs/20260802-0930-board-deck --piece metrics-slides`.
Thresholds: `unsupported` count 0, every source reachable, citation ratio 1.0 for on-slide figures.

**3. Workshop teaching deck, visual system piece.**
Bar: per-slide PNG exports of two reference workshop decks in `bar/refs/workshop-a/` and `bar/refs/workshop-b/`.
Render: export slides 1, 5, 9, and 14 at 1920x1080 to `rounds/visual-system/002/inspection/` via `screenshot` of the rendered HTML deck.
Acceptance: blind critic, shown our four slides and the reference's four slides as neutral sets, picks ours in 2 consecutive rounds; type scale and grid are consistent across all four of ours.


When a worked example's `inspection_command` is written into `pieces.json` at brief time, resolve `<plugin-root>` to the absolute path of the installed gauntlet plugin. Stored commands are re-run as evidence outside the plugin context, so they must carry resolved absolute paths, never an environment variable.

## Inspection methods, in priority order

1. `render`. Mandatory every round. Produce the actual PDF or slide images with a declared `inspection_command`. A round where rendering fails is a failed round; do not proceed to judgment.
2. `reader-proxy`. Mandatory. The question set is fixed for this domain and frozen at brief time: what is the ask, what is the evidence, what is the next step, what would make you say no. Do not add, remove, or soften these questions per piece. The proxy sees rendered slides only, in order, nothing else. Every guess or unanswerable question is a gap.
3. `claim-audit`. Required for any piece whose slides carry figures. Run `claim_audit.py` against the piece's ledger every round the numbers change.
4. `screenshot`. Supporting method for per-slide and visual-system pieces, and the input format for blind pairing.

`read` on the source markdown is never sufficient and never substitutes for `render`.

## Blind comparison feasibility and how to set it up

Strong. Decks render to comparable artifacts, so pair them directly. Export ours and the reference to the same format and resolution (per-slide PNGs preferred, one PDF each acceptable). Run `blind_pair.py` so both land at neutral paths with neutral filenames, metadata stripped, sealed map written outside `runs/`. The critic receives the two rendered sets, the goal, and the acceptance criterion. It never receives the source markdown, the builder's notes, or filenames that reveal provenance. For narrative-arc pieces, instruct the critic to read each set in slide order before judging.

## What the integrity verifier checks in this domain

- No fabricated figures. Every number visible on any slide traces to a claim-ledger row with a reachable source that says what the slide says. One invented figure fails the piece regardless of quality votes.
- Every number sourced: `claim_audit.py` output present in `claims/<piece-id>/audit.json` with zero `unsupported` rows.
- The render command actually ran: inspection directory contains the rendered artifact and the recorded exit code, not a description of one.
- Reference files in `bar/refs/` exist and are the files the bar named.
- Chart data matches the ledger. A chart that exaggerates a sourced number is a fabrication.

## Common failure modes

- Judging the outline or the markdown source instead of rendered slides. Violates INV-3.
- A bar made of adjectives ("clean, punchy, VC-ready") with no reference files on disk.
- Illustrative numbers invented to make a chart look right, left in at ship time.
- Softening the four reader-proxy questions when answers come back wrong. They are frozen.
- Narrative-arc pieces sized so large that the critic can only name vague gaps. Re-split by section.
- Reference decks described from memory instead of stored in `bar/refs/`.

## When this domain is the wrong adapter

- The artifact is a memo, script, or speaker-notes document: use `prose`.
- The deck is a vehicle for a decision and the real work is options, assumptions, and a recommendation: use `strategy` for those pieces, `deck` only for the rendering.
- The deliverable is an interactive web presentation or product UI: use `visual`.
- The work is gathering and validating the numbers themselves: use `research`, then feed its ledger into deck pieces here.
