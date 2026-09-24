# Domain adapter: strategy

Summary row: a piece is an options set, an assumption register, a recommendation, or a risks and reversibility analysis. The bar is a reference decision-memo standard plus an adversarial pass. Inspection is `red-team` and `reader-proxy`. Blind comparison is weak: use a frozen rubric plus red-team. Integrity checks: evidence separated from judgment, assumptions labeled with confidence, kill conditions stated.

## What counts as a piece

Four piece types, and only these:

1. **Options set.** The genuinely distinct options, each with costs, evidence, and what it forecloses. Judged on whether the options are real alternatives, not one favorite plus two straw men.
2. **Assumption register.** Every load-bearing assumption, each with a confidence label and a kill condition. This is its own piece because it is where strategy work silently rots.
3. **Recommendation.** The decision, the reasoning from evidence to choice, and what would change it.
4. **Risks and reversibility.** What breaks, how it is detected, and how far back the decision can be walked.

"Write the strategy" is not a piece. A market-sizing or fact-finding piece belongs to `research`, and its ledger feeds pieces here.

## What a valid bar looks like here

No fair comparator usually exists, so the bar is a rubric frozen at brief time with its hash recorded by `hash_plan.py`, plus an adversarial red-team pass. The rubric names checkable properties (every assumption labeled, every option costed, kill conditions present, evidence and judgment in separate sections), not adjectives. A reference decision memo in `bar/refs/` may anchor the standard, but scoring runs against the rubric, not against pairing.

A rubric edited during a run is an integrity failure, not a refinement. It carries the same weight as a fabricated citation. If the rubric turns out to be wrong, stop the run, re-brief, and start a new run with a new hash.

## Three worked bar examples

**1. Build-versus-buy recommendation piece.**
Bar: `bar/rubric.md`, seven criteria, frozen via `python3 "<plugin-root>/scripts/hash_plan.py" --run-dir .gauntlet/runs/20260801-0900-build-vs-buy` at brief time.
Acceptance: a fresh critic scores every criterion at 4 of 5 or above in 2 consecutive rounds, and the red-team pass produces no objection the memo does not already answer or log as an open risk.
`blind_feasible` is false in `pieces.json`; verdicts record `"blind": false` and the rubric hash.

**2. Market-entry options set piece.**
Bar: `bar/rubric.md` plus `bar/refs/six-pager-standard.pdf` as the anchor document.
Inspection: reader-proxy with the frozen decision-memo question set (state the decision, state the strongest counter-argument, state what would change it), answered from the artifact alone without guessing; then a red-team subagent, fresh context, given only the memo, instructed to overturn the recommendation using the memo's own evidence.
Threshold: reader-proxy answers all three questions, and every red-team attack is pre-answered in the risks section or converted into a named gap.

**3. Pricing-change assumption register piece.**
Bar: rubric criteria include: 100 percent of assumptions carry a confidence label from the set high, medium, low; 100 percent carry a kill condition stating the observable that falsifies them.
Inspection: red-team attacks the three most load-bearing assumptions; each attack must map to an existing register row or the piece loses the round.
Command evidence: red-team output stored at `rounds/assumption-register/003/inspection/red-team.md`.


When a worked example's `inspection_command` is written into `pieces.json` at brief time, resolve `<plugin-root>` to the absolute path of the installed gauntlet plugin. Stored commands are re-run as evidence outside the plugin context, so they must carry resolved absolute paths, never an environment variable.

## Inspection methods, in priority order

1. `red-team`. The domain's distinguishing method. A fresh-context adversary tries to break the recommendation, the options framing, or the assumptions, using only the artifact. Its output is stored as inspection evidence and is what the critic judges against.
2. `reader-proxy`. Mandatory. Frozen question set: state the decision, the strongest counter-argument, and what would change it. Guesses and unanswerable questions are gaps.
3. `read`. Only ever paired with `reader-proxy` or `red-team`, per the closed-set rules. Used for rubric scoring by the fresh critic.
4. `claim-audit`. When the evidence section makes factual claims, run `claim_audit.py` against the piece ledger; any `unsupported` row is an integrity failure.

## Blind comparison feasibility and how to set it up

Weak. Two memos about different decisions cannot be blind-paired meaningfully, and a same-decision comparator rarely exists. Do not fabricate a blind comparison; set `"blind": false` and rely on the frozen rubric plus red-team. Where a genuine same-decision comparator does exist (a prior memo on this exact decision), blind pairing of the two documents via `blind_pair.py` is allowed as a supplement, never as a replacement for the rubric score.

## What the integrity verifier checks in this domain

- `plan_hash_matched` first. The rubric and success criteria hashes match the brief-time record from `hash_plan.py`. A mismatch is `cannot-verify` regardless of artifact quality, and a demonstrated mid-run edit is `failed`.
- Evidence separated from judgment: the memo structurally distinguishes what is known from what is concluded.
- Every assumption labeled with confidence from the closed set, every one with a kill condition.
- Kill conditions stated for the recommendation itself.
- Factual claims traced through the ledger; the red-team pass actually ran (its output file exists and engages the artifact, not a summary of it).

## Common failure modes

- The rubric written or adjusted mid-run to fit the memo. Integrity failure, full stop.
- A rubric of adjectives ("compelling, rigorous") that `validate_bar.py` should have rejected.
- Red-team run with builder context, or by the builder. It must be fresh-context, files-only.
- A pseudo-blind pairing against an unrelated reference memo to claim strong blindness.
- Uniform confidence labels ("all high") that satisfy the letter of the rubric and nothing else. The red-team attack on load-bearing assumptions catches this.
- A recommendation with no kill conditions, defended as "we are committed."

## When this domain is the wrong adapter

- The work is establishing facts, sizing markets, or surveying sources: use `research` first.
- The deliverable is a persuasion artifact for an audience: use `deck` or `prose` for that layer.
- The decision is computable (benchmark it, measure it): use `code` with `measure`.
- The memo exists to define a brand position: use `brand` for the positioning pieces.
