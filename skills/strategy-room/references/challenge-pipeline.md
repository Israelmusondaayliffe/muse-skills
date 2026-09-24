# Assumption Challenge pipeline

Research-grounded adversarial review. A challenge that isn't grounded in current facts is just confident speculation. This pipeline enforces a research-first workflow so every assumption flagged, contradiction surfaced, and recommendation made is anchored in evidence the user can verify.

## Router variants

Default: run all five phases in sequence on the user's input.

- **"Just research X" / "Get me up to speed on Y"**: run the Research phase only. Return the dossier as the deliverable.
- **"I already have research, just challenge this" / "Skip the research"**: start at the Plan phase with the user's research as input, continue through Challenge, Verify, Synthesize.
- **"Re-verify this report" / "Stress test these findings"**: run the Verify phase on the prior findings, then Synthesize.
- **"Give me a quick gut check" / "Light pass"**: effort mode `light`, full pipeline at reduced depth.
- **"Go deep on this" / "Maximum rigor" / "Stakes are high"**: effort mode `deep`.

If the request is ambiguous, ask one focused question. Do not run the pipeline blind.

## Effort modes

Set once at the start. It shapes every phase.

**Light** (~5 min, low context cost)
- Researcher: 3–5 web searches. Fetch one full source page only if a single source is critical.
- Planner: 3 prioritized lenses (skip alternate viewpoints and meta-analysis unless directly relevant).
- Challenger: 3–5 findings per prioritized lens.
- Verifier: spot-check critical findings, not every finding.
- Synthesizer: ~600 word report — TL;DR, top 3 priorities, top 3 questions, top 3 recommendations.

**Standard** (default, ~10 min)
- Researcher: 8–12 web searches across multiple subtopics. Fetch 2–3 highest-value source pages.
- Planner: all 5 lenses, prioritized by relevance.
- Challenger: 5–8 findings per lens.
- Verifier: every finding verified against the dossier. Confidence calibrated.
- Synthesizer: ~1200 word report, full seven-section structure.

**Deep** (~20 min, high context cost)
- Researcher: 15+ web searches. Fetch 5+ source pages. Cross-reference expert disagreement explicitly. Track recency for every claim.
- Planner: all 5 lenses with explicit hypotheses to test under each.
- Challenger: 8+ findings per lens, including improbable scenarios and second-order effects.
- Verifier: triple-verification. Every claim traced to a dossier entry. Every confidence score justified.
- Synthesizer: ~2500 word report plus appendix with dossier excerpts and verification log.

Default to standard. Escalate to deep only when the user signals high stakes, asks for maximum rigor, or the subject involves consequential decisions (financial, medical, legal, strategic).

## Running the phases

Run phases sequentially. For each phase, either spawn a subagent with the brief below (attach the relevant template and reference files) or run the phase inline for light-mode engagements. Never skip a phase silently: if you condense the pipeline, say so.

### Phase 1 — Research

**Goal:** become a domain expert in the subject through active web search and build a research dossier that later phases can rely on as ground truth. Do NOT critique the user's input here; only gather and organize evidence.

**Inputs:** the user's content, the effort mode.

**Procedure:**
1. Decompose the subject: primary subject, the domains it sits in, the decision points the user implicitly faces, and the claims/assumptions that touch external reality. Write a one-paragraph subject summary at the top of the dossier.
2. Map dimensions to cover (aim for at least four; skip the ones that don't apply and say why): technical, market, user/audience, regulatory/legal, ethical, historical.
3. Execute searches per `references/research-protocol.md`: start broad, then narrow, deliberately seek disagreement ("Why X doesn't work", "X criticism", "Y vs X"), and anchor recency for fast-moving subjects.
4. Write the dossier in `assets/research_dossier_template.md` with source tiering (A/B/C/D), per-finding sources, recency notes, caveats, an explicit expert-disagreement map, and open questions the research could not resolve.

**Output:** research dossier markdown.

### Phase 2 — Plan

**Goal:** turn the dossier into a targeted challenge plan: which lenses to apply, which hypotheses to test under each lens, and which dossier evidence each test draws on. Do NOT execute the challenge here.

**Inputs:** the validated research dossier, the user's original content, the effort mode.

**Procedure:**
1. Re-read the user's input through the dossier. Map every material claim to: **supported**, **contradicted**, **unaddressed** by the dossier, or **assumed** rather than stated.
2. Prioritize the five lenses (defined in `references/analysis-frameworks.md`): hidden assumptions, blind spots, alternate viewpoints, contradictions, meta-analysis. Light mode picks 3; standard and deep use all 5 with explicit hypotheses in deep mode.
3. Write specific, falsifiable hypotheses per prioritized lens, each linked to dossier finding IDs (or explicitly marked "no dossier evidence, will reason from principles").
4. Write the plan in `assets/analysis_plan_template.md`: restated input, claim mapping, lens prioritization with rationale, hypotheses, bias patterns to watch for (from `references/cognitive-biases.md`), and explicit out-of-scope items.

**Output:** analysis plan markdown.

### Phase 3 — Challenge

**Goal:** execute the plan through each prioritized lens, producing raw findings with claims, reasoning chains, draft confidence, and dossier links.

**Inputs:** the research dossier, the analysis plan, the user's original content, the effort mode.

**Procedure:**
1. Load `references/analysis-frameworks.md` and `references/cognitive-biases.md`. Keep the dossier and plan open.
2. For each prioritized lens, work the hypotheses systematically. Each finding follows the structure in `assets/challenge_findings_template.md`:
   - Finding ID (e.g. `L1-F1`), lens, hypothesis tested, claim, step-by-step reasoning chain, dossier evidence by finding ID, draft confidence (High/Medium/Low/Speculative), why it matters.
3. Counts: 3–5 findings per lens (light), 5–8 (standard), 8+ (deep).
4. Lens-by-lens coverage:
   - **Hidden assumptions**: categorize (context, user, technical, market, process); check each against dossier findings (supported, contested, unaddressed).
   - **Blind spots**: information gaps, structural blind spots, temporal blind spots (scale, time, degraded modes), boundary conditions. Tag each reducible, irreducible, or unknown-unknown.
   - **Alternate viewpoints**: 3–5 perspectives the user isn't holding (skeptic, optimist, domain experts from the dossier's disagreement map, stakeholders, temporal, unconventional). Each must surface something the current framing misses.
   - **Contradictions**: goal-method, value, theory-practice, structure-culture, resource conflicts. Classify productive tension (design around it) vs fatal flaw (resolve it).
   - **Meta-analysis**: biases in the input from the taxonomy; limits of this analysis itself.
5. After all lenses, note cross-lens convergences: the same root issue surfacing in multiple lenses. Tag them `cross-lens`; the verifier examines them with extra rigor.

**Output:** challenge findings markdown.

### Phase 4 — Verify

**Goal:** triple-verify every finding against the dossier and plan. Do NOT write the final report here.

**Inputs:** challenge findings, research dossier, analysis plan.

**Procedure:** follow `references/verification-protocol.md`:
1. **Evidence check**: does the cited dossier evidence actually support the claim, or only a weaker version? Is it current enough? Tiered strong enough? If multiple items cited, do they agree?
2. **Reasoning check**: does each step follow? Any hidden inferential leaps (correlation→causation, base-rate→specific case, expert-says→true)? Does the framing smuggle in the conclusion? Could the same evidence support a different conclusion?
3. **Counter-evidence check**: does the dossier contain expert disagreement, temporal evidence, or a competing explanation the challenger missed? Revise or split findings rather than ignoring it.
4. Annotate every finding with a verification status: **confirmed**, **partially confirmed**, **not confirmed by research**, **speculative**. Downgrade or remove failures; "not confirmed by research" findings must be downgraded to speculative or removed before synthesis.
5. Record per `assets/verified_findings_template.md`: verification summary (survival statistics), calibration drift (did most findings get downgraded / stay / get upgraded — and what that signals about the challenger's calibration), biases detected in the challenge itself (generic pattern-matching, adversarial bias, confidence inflation), and verified cross-lens convergences.

**Output:** verified findings markdown.

### Phase 5 — Synthesize

**Goal:** assemble the user-facing report from verified findings only.

**Inputs:** verified findings, research dossier.

**Procedure:**
1. Use `assets/final_report_template.md`. Skim `references/example-reports.md` for tone calibration.
2. Write the TL;DR (3 sentences max — a verdict, not a summary): the most important thing the user needs to know, the highest-leverage change, the confidence in the analysis.
3. Write "If Overwhelmed, Start Here" (1–3 concrete actions, High/Medium confidence, preferably cross-lens convergent, high cost of inaction, within the user's control).
4. Build the seven body sections from verified findings: identified assumptions, blind spots, alternate viewpoints, contradictions, challenges/questions, recommendations for refinement (framed as actions), meta-reflections (biases detected in the input with specific callouts, plus what this analysis could not evaluate).
5. Calibrate confidence throughout: inline qualifiers, bold confidence labels, source citations for the strongest claims. A report that sounds equally confident throughout is uncalibrated — revise it.
6. Do not cite training data. Flag analyst hypotheses as hypotheses. If the dossier could not be built (private internal data only), state the limitation prominently.

**Output:** final report markdown — the only artifact the user sees by default. Intermediates (dossier, plan, raw and verified findings) are surfaced only on request.

## Handoff gates (do not skip)

1. **Research → Plan**: run `bin/dossier_check.py DOSSIER.md --effort <mode> --pace <fast|standard|slow>`. It validates source count, source diversity, recency, and dimensional coverage. If it fails, send the dossier back with the failure reasons. Do not proceed until it passes.
2. **Plan → Challenge**: confirm the plan covers all required lenses for the effort mode and each lens has at least one specific hypothesis to test.
3. **Challenge → Verify**: confirm every finding has a claim, a reasoning chain, and a confidence draft. Return incomplete findings.
4. **Verify → Synthesize**: confirm every finding carries a verification status. Findings marked "not confirmed by research" must be downgraded or removed first.
5. **Synthesize → User**: confirm the report includes TL;DR, all required sections for the effort mode, calibrated confidence, and an "if overwhelmed, start here" section.

## If a phase fails

Do not paper over it. Surface the failure to the user with three options: retry the phase, downgrade the effort mode, or abandon the analysis. Do not silently continue with broken intermediate output. A bad dossier produces a bad challenge; a bad challenge produces a bad recommendation.

## When not to use this route

- Quick yes/no questions where one search beats a five-phase pipeline.
- Pure creative brainstorming where critique would kill divergent thinking.
- Requests that really want validation rather than critique — this route will not flatter.
- Subjects where research is impossible (private internal data only). Run without the research phase and flag the gap prominently in the final report.

## Special considerations for AI prompt analysis

When the input is an AI prompt, the planner additionally checks: is the task clearly defined? Are examples provided? Is the output format specified? Are constraints and guardrails explicit? Is reasoning encouraged? Are edge cases handled? Does the prompt use model-specific capabilities? Are model limitations being overlooked? Is the prompt token-efficient? The researcher should research the specific model's current capabilities (context window, known weaknesses, recent updates) — prompt analysis without current model knowledge produces stale advice.
