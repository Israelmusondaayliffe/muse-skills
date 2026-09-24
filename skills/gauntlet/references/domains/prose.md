# Domain adapter: prose

SPEC 4.1 row: a piece is an argument, an opening, a section, a paragraph class, or transitions. The bar is reference paragraphs at target clarity and compression. Inspection is `read` plus `reader-proxy`, with blind prose pairing. Blind comparison is strong. Integrity checks: claims traced, no invented quotes or sources.

## What counts as a piece

A piece is an argument, an opening, a section, a paragraph class, or the transitions of a document. Good pieces: the opening of an editorial, the argument spine of a memo, the "how it works" section of a guide, the class of all example paragraphs in a long report, the transitions between the six sections of a whitepaper. A paragraph class and a transition set are legitimate pieces because they can be judged as one thing across the document. Bad pieces: "the whole essay" (split into opening, spine, sections, transitions), "make it flow" (adjective), a single sentence (fold into its section). Each piece names its artifact span, for example `drafts/akira-issue-04.md#opening`, in `pieces.json`.

## What a valid bar looks like here

The bar is real reference paragraphs at the target clarity and compression, stored in `bar/refs/` with their sources named in `bar/bar.md`. The reference is a floor for clarity and information density, not a voice to copy. State this in the bar file and in every critic prompt, because a critic handed reference paragraphs will otherwise push the work toward pastiche. The gap it names must be about density, argument order, or deletability, never about sounding more like the reference author. `validate_bar.py` fails a bar that is adjectives ("compelling, punchy"), that has no reference file behind it, or whose reference paths do not resolve. Optional measured floors are valid additions: a word cap, a reader-proxy question set frozen at brief time, a zero-unsupported-claims requirement.

## Three worked bar examples

Example 1, editorial opening. Bar: `bar/refs/reference-openings.md` containing three published openings copied verbatim, with source URLs recorded in `bar/bar.md`. Inspection: `reader-proxy` with frozen questions "What is this piece arguing?" and "Why would a reader continue past line three?", plus blind prose pairing each round. Acceptance: blind critic picks ours over the reference in 2 consecutive rounds, and the reader-proxy answers both questions without guessing.

Example 2, technical explainer section. Bar: two reference sections from best-in-class documentation stored at `bar/refs/reference-explainers.md`, plus a traced-claims floor. Inspection: `reader-proxy` with `questions: ["Configure the feature using only this section. Where did you guess?"]`, and `claim-audit` with `inspection_command: python3 <plugin-root>/scripts/claim_audit.py --run-dir .gauntlet/runs/20260810-0930-sdk-guide --piece auth-section`. Acceptance: blind win in 2 consecutive rounds, zero unsupported ledger rows, zero reader-proxy guesses.

Example 3, executive summary of a forty-page report. Bar: one reference summary at `bar/refs/reference-summary.md` plus a compression floor of 400 words, checked with `measure` and `inspection_command: wc -w drafts/q3-review-summary.md`. Inspection: `reader-proxy` with five frozen questions drawn from what the full report answers, asked of the summary alone. Acceptance: all five answered correctly from the summary, word count at or under 400, blind win in 2 consecutive rounds.


When a worked example's `inspection_command` is written into `pieces.json` at brief time, resolve `<plugin-root>` to the absolute path of this skill (`~/workspace/skills/gauntlet`). Stored commands are re-run as evidence outside the skill context, so they must carry resolved absolute paths, never a placeholder.

## Inspection methods, in priority order

1. `reader-proxy`. Mandatory on every prose piece. A fresh subagent receives the artifact and the target reader profile, nothing else, and does what the artifact exists to enable: says what it argues, follows its instructions, answers its questions. Every guess and unanswered question is a gap. Output goes to `rounds/<piece>/<n>/inspection/` and is what judgment inspects.
2. `claim-audit`. Required whenever the piece makes factual claims. The builder maintains `claims/<piece>/ledger.json`; `claim_audit.py` validates it. Declare the `inspection_command`.
3. `read`. The critic reads the full text end to end during blind pairing. `read` alone is never sufficient: `validate_pieces.py` rejects a prose piece that declares `read` without `reader-proxy` or `claim-audit`.

## Blind comparison feasibility and how to set it up

Strong. Blind prose pairing is the default judgment mechanism: `blind_pair.py` copies our passage and the reference to neutral paths with neutral filenames, strips metadata, and seals the map outside `runs/`. The critic is told one is a reference and one is a candidate, not which, and is instructed not to seek provenance. It reads both fully and picks the passage with more information per sentence, cleaner argument order, and fewer sentences that could be deleted without loss, then names the single largest gap in the loser. Pair like spans: opening against opening, section against section. Restate the floor-not-voice rule in the pairing prompt every round; a gap of the form "adopt the reference's cadence" is invalid and is sent back.

## What the integrity verifier checks in this domain

Claims traced: every factual claim in the piece appears in the ledger, and `claim_audit.py` output shows zero `unsupported` rows for a factual artifact; any unsupported row is an integrity failure, not a style note. No invented quotes or sources: every quotation exists in its cited source, and quote presence is re-checked where the source is fetchable. Sources reachable at verification time. Reader-proxy evidence real: the recorded output exists in `inspection/` and corresponds to the current artifact, not an earlier draft. Frozen question sets unmoved: `plan_hash_matched` is checked before anything else.

## Common failure modes

- Pastiche drift: rounds make the work sound like the reference instead of denser than it. Counter: the floor-not-voice rule in bar, critic prompt, and gap validation.
- Summary judgment: the critic reads an abstract of the piece instead of the piece. Counter: pairing hands over full text only.
- Question softening: reader-proxy questions get easier after wrong answers. Counter: questions frozen with the plan hash at brief time.
- Confident invention: a clean paragraph carrying a fabricated statistic passes quality and poisons the work. Counter: claim-audit runs regardless of how good the prose looks.
- Padding to win: length mistaken for substance. Counter: deletability is an explicit pairing criterion, and word caps are measured.

## When this domain is the wrong adapter

Use `research` when the hard part is sourcing and synthesis rather than the writing: coverage floors and disconfirming quotas live there. Use `strategy` for decision memos where the recommendation, assumptions, and reversibility are the deliverable. Use `deck` when the words ride on slides. Use `prompt-system` for system prompts and skill text, which are judged by executed behavior on test inputs, not by reading quality. If nobody will read the artifact end to end, prose is the wrong lens.
