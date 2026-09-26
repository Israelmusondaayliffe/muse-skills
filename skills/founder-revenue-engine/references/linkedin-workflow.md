# LinkedIn Content Workflow

Create LinkedIn posts that break consensus systematically while staying human and fact-true. Feeds on verified claims from the `narrative` or `icp` route only.

## Rule Zero (sits above everything)

Simple words win. "Use" beats "leverage." "Start" beats "commence." When a word has a simpler equivalent that carries the same meaning, the simpler word is correct by default. Enforce with `references/linkedin/word-replacement-table.md`.

## No-fabrication rule

Everything in the post must trace to user input. Never add numbers the user didn't give, claim results they didn't share, or name tools they didn't mention. With partial info, work with what's given and flag what's missing.

## Voice profile

The default profile; replace with the user's own voice markers when known (ask the user rather than inventing them):

- Curious, practical, collaborative; direct without warmth loss.
- Short sentences, concrete over abstract, questions over statements when exploring.
- Shows work, shows uncertainty when present, asks for input rather than preaching.
- No fluff, no hype, no emojis unless requested.
- Banned: em-dashes (use period+capitalize or comma+lowercase), AI cliches (delve, leverage, unlock, journey, game-changer), business jargon (synergy, scalable, robust, disruptive), hedge language, generic transitions, copula avoidance ("serves as" → "is"), significance inflation, trailing -ing constructions, negative parallelisms, generic conclusions, sycophantic artifacts.

## Six-phase workflow

### Phase 0: Context and fact extraction

Extract user-provided facts into a mental inventory. Validate: no added numbers, no claimed results, no named tools beyond what was given, enough specifics for a strong post.

### Phase 1: Consensus mapping

Map the "zone of indifference" (p > 0.90) before being contrarian. Identify the niche, check `references/linkedin/consensus-patterns.md`, generate the 5 most common takes if unmapped, list standard buzzwords, and explain why the consensus is stale.

### Phase 2: Dual-method hook generation

- **Method A — Tail sampling:** 3–5 contrarian angles from `references/linkedin/tail-angle-templates.md` (Economic Arbitrage, Hidden Tax, Structural Limit, False Freedom, etc.), with probability scores 0.04–0.10.
- **Method B — Template selection:** 3–5 fitting templates from `references/linkedin/hook-templates.csv` (69 templates).
- **Synthesis:** match angles to templates; generate 5–7 hook options with both statistical edge and engagement structure.

### Phase 3: PRISM humanization

Pattern break (imperfection markers), rhythm (vary sentence length), imperfection (fragments, lowercase emphasis), start mid-thought, meta (self-aware commentary). Replace ALL em-dashes. See `references/linkedin/prism-examples.md`.

### Phase 4: Body writing

Choose a structure: Story-Driven (Hook → Context → Discovery → Insight → Application), Teaching-Driven (Hook → Framework → Details → Evidence → Action), or Results-Driven (Hook → Setup → Process → Results → Takeaway). Short paragraphs (1–3 sentences), one idea per paragraph, liberal line breaks, no fabricated details.

### Phase 5: Quality enforcement

Load `references/linkedin/quality-enforcement-rules.md` and enforce:

1. **Rule Zero check** — every Tier 1 word replaced.
2. **AI pattern taxonomy scan** — 24 patterns in `references/linkedin/ai-pattern-taxonomy.md` (copula avoidance, significance inflation, -ing constructions, negative parallelisms, forced triplets, generic conclusions, sycophancy, promotional language).
3. **Extended pattern scan** — 12 more in `references/linkedin/extended-patterns.md` (novelty inflation, emotional flatline, false concession, rhetorical stalls, confidence calibration, "Let's" openers, "Whether you're X or Y", vague endorsement).
4. **Negative style check** — no AI tells, em-dashes, banned phrases.
5. **Divergence enforcement** — clear stance, no hedging.
6. **Voice validation** — voice markers present.
7. **Fabrication validation** — all facts from the user.
8. **Run the quality scripts:**
   ```bash
   python3 scripts/quality_validator.py --file "$OUT/draft.txt" --verbose
   test -e "$OUT/draft.clean.txt" && echo "draft.clean.txt exists; pick a new name" || python3 scripts/emdash_replacer.py "$OUT/draft.txt" "$OUT/draft.clean.txt"
   ```
   Run from this skill's directory with drafts in your working folder `$OUT`. The validator scores style only; a perfect score does not check facts, so the fabrication check above still applies.

### Phase 6: Multi-option delivery

Present 2–3 complete post options, each with full hook and body, rationale, quality score, pattern-scan result, fabrication validation, and when to use each.

## References (under references/linkedin/)

- `word-replacement-table.md` — Rule Zero Tier 1/2 replacements
- `hook-templates.csv` — 69 viral templates
- `consensus-patterns.md` — pre-mapped boring takes
- `tail-angle-templates.md` — 15+ contrarian frameworks
- `prism-examples.md` — humanization before/after
- `quality-enforcement-rules.md` — full validation rules
- `copywriting-principles.md` — framework guidance
- `ai-pattern-taxonomy.md` — 24-pattern AI writing catalog
- `extended-patterns.md` — 12 additional patterns

## Critical reminders before every output

- Rule Zero check, fabrication check, em-dash check, AI pattern check, extended pattern check, voice check, consensus check, quality score ≥ 80/100.
- NEVER: complex words where simple ones work, fabricated details, em-dashes, AI cliches, "serves as", significance inflation, ", highlighting..." constructions, generic optimism, filler emphasis ("It's worth noting", "Interestingly"), "Let's dive in" stalls, "Whether you're X or Y" framing, skipping consensus mapping, presenting only one option.
