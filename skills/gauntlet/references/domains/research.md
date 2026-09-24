# Domain adapter: research

SPEC 4.1 row: a piece is a question, a source set, a claim ledger, or a synthesis. The bar is a primary-source coverage requirement, a claim-to-citation ratio, a reference review, and a disconfirming-evidence quota. Inspection is `claim-audit`, `source-reach`, `reader-proxy`. Blind comparison is partial. Integrity checks: sources reachable and saying what is claimed, no fabricated citations, disagreement represented.

## What counts as a piece

A piece is a question, a source set, a claim ledger, or a synthesis. A well-shaped research run usually decomposes into: one piece per commissioned question, one source-set piece that gathers and stores the evidence base, one claim-ledger piece that traces every factual statement, and one synthesis piece that argues from the ledger. Good pieces: "What is the actual pricing behavior of the top five vendors?", the source set for that question, the synthesis section that answers it. Bad pieces: "research the market" (split by question), "be thorough" (adjective), a synthesis with no ledger behind it (blocked until the ledger piece exists). Pieces name their artifact paths, for example `sources/`, `claims/vendor-pricing/ledger.json`, `drafts/market-brief.md#pricing`.

## What a valid bar looks like here

The bar has three parts, and all three are required: a coverage requirement (how many primary sources, of what kind), a citation ratio floor, and a disconfirming-evidence quota. A research gauntlet without a disconfirming quota converges on a confident, one-sided document, so `bar/bar.md` states the quota as a number, not an intention. A reference review or brief in `bar/refs/` may serve as the comparison document for pairing the synthesis. `validate_bar.py` fails a bar that names no numbers, no source kinds, and no reference file: "well-sourced and balanced" is adjectives. Every threshold is checkable by `claim_audit.py` or by counting rows in the ledger.

## Three worked bar examples

Example 1, competitive landscape brief. Coverage: at least 12 distinct sources, of which at least 6 are primary (filings, official documentation, first-party announcements, primary datasets), stored or linked under `sources/`. Ratio floor: at least 0.95 of factual claims carry a citation, zero `unsupported` rows. Disconfirming quota: at least 3 ledger rows that cut against the working hypothesis, represented in the synthesis text. Inspection: `claim-audit` with `inspection_command: python3 <plugin-root>/scripts/claim_audit.py --run-dir .gauntlet/runs/20260805-1100-vendor-scan --piece landscape-synthesis`, plus `source-reach` over every ledger URL, plus `reader-proxy` answering the three commissioned questions from the brief alone.

Example 2, technical literature review. Coverage: at least 15 papers or technical reports, at least 8 primary (peer-reviewed or original technical reports), each saved to `sources/` or reachable by URL recorded in the ledger. Ratio floor: 1.0 on quantitative claims. Disconfirming quota: at least 2 credible sources that disagree with the majority position, named in the synthesis with their argument stated fairly. Reference review: `bar/refs/reference-review.md`, a published survey at the target depth, used for blind pairing of the synthesis. Acceptance: audit thresholds met and blind critic picks our synthesis in 2 consecutive rounds.

Example 3, vendor claim ledger feeding a decision memo. Coverage: every shortlisted vendor claim traced to a primary document, no secondary-only vendors. Ratio floor: 1.0; any `unsupported` row blocks convergence. Disconfirming quota: at least 1 negative review, incident report, or contradicting benchmark per shortlisted vendor. Inspection: `claim-audit` with `inspection_command: python3 <plugin-root>/scripts/claim_audit.py --run-dir .gauntlet/runs/20260812-0900-crm-eval --piece vendor-ledger`, plus `source-reach` on every row.


When a worked example's `inspection_command` is written into `pieces.json` at brief time, resolve `<plugin-root>` to the absolute path of the installed gauntlet plugin. Stored commands are re-run as evidence outside the plugin context, so they must carry resolved absolute paths, never an environment variable.

## Inspection methods, in priority order

1. `claim-audit`. The primary instrument. The model extracts the ledger; `claim_audit.py` does the arithmetic: total claims, unsupported count, claim-to-citation ratio, duplicate-source concentration, quote presence where the source is fetchable. Declare the `inspection_command` on every ledger-bearing piece.
2. `source-reach`. Confirm every cited source resolves (HTTP fetch or file existence) and, where fetchable, contains the supporting quote. Requires network; if the precheck recorded no network, reachability is `cannot-verify`, never assumed.
3. `reader-proxy`. Mandatory on synthesis pieces. A fresh subagent receives the brief's commissioned questions and the synthesis, nothing else, and answers them. Unanswerable questions and guesses are gaps.

`read` alone never qualifies; on any research piece it must pair with `claim-audit` or `reader-proxy`, and `validate_pieces.py` enforces this.

## Blind comparison feasibility and how to set it up

Partial. The synthesis document pairs well: `blind_pair.py` copies our synthesis and the reference review to neutral paths, strips metadata, seals the map, and the critic picks the document with better evidence-per-claim, cleaner argument order, and fairer treatment of disagreement, then names one gap. The coverage requirement, ratio floor, and disconfirming quota are not blind at all: they are measured thresholds from `claim_audit.py` and ledger counts, judged as numbers. Do not blind-pair source sets or ledgers; there is no fair comparator for them. Set `"blind": true` only on synthesis pieces with a real reference review in `bar/refs/`; everywhere else set `"blind": false` and judge against the measured bar.

## What the integrity verifier checks in this domain

Sources reachable and saying what is claimed: re-run the audit, fetch each source, confirm the supporting quote is present. No fabricated citations: a URL that never existed, a paper with the wrong authors, a page that does not contain the quote all fail the run regardless of quality votes. Disagreement represented: the disconfirming quota is met in the ledger and the disconfirming evidence actually appears in the synthesis text, not buried in an appendix row. Any `unsupported` row in a factual artifact is an integrity failure, not a style note. Duplicate-source concentration is reported: twelve citations to one blog post is not coverage. Coverage counts are recomputed from the ledger, never taken from the narrative.

## Common failure modes

- One-sided convergence: every round makes the document more confident and less true. Counter: the disconfirming quota is a numeric floor checked every audit.
- Citation laundering: secondary sources cited as if primary. Counter: `support_type` is per row and coverage counts only `primary` rows.
- Link rot at verification: sources reachable at build time, gone at verify time. Counter: save fetchable sources under `sources/` at collection time.
- Quota theater: disconfirming rows exist in the ledger but the synthesis ignores them. Counter: the verifier traces quota rows into the text.
- Ratio gaming: claims rephrased as hedges to dodge the ledger. Counter: the reader-proxy answers the commissioned questions; a document of hedges cannot answer them.

## When this domain is the wrong adapter

Use `strategy` when the deliverable is a recommendation with assumptions and kill conditions; research feeds it but is judged differently. Use `prose` when the sourcing is settled and the work is clarity and compression of an already-traced document. Use `code` for data pipelines that produce the evidence; the pipeline is a code piece even inside a research campaign. If the goal has no factual claims to trace, there is nothing for this adapter to audit.
