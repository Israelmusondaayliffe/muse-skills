# Research Dossier: [Subject]

**Effort mode:** [Light / Standard / Deep]
**Researcher pass date:** [YYYY-MM-DD]
**Subject pace:** [Fast-moving / Standard / Slow-moving]

---

## Subject Summary

One paragraph capturing the primary subject, the domain(s) it sits in, and the implicit decision points the user faces. This is the lens through which all research below is conducted.

---

## Dimensions Covered

List the dimensions researched and the dimensions deliberately skipped.

**Covered:**
- Technical
- Market
- User / audience
- Regulatory
- [add as needed]

**Skipped:**
- [Dimension]: [reason for skipping]

---

## Findings by Dimension

### Dimension 1: [Name]

#### Finding 1.1: [Short title]

**Claim:** [Specific, evidence-grounded statement]

**Sources:**
- [Source name, date, source tier (A/B/C)]
- [Source name, date, source tier]

**Recency:** [How recent the evidence is. Flag if any source is potentially stale for this subject pace.]

**Caveats:** [Limitations, sample biases, regional skew, etc.]

#### Finding 1.2: [Short title]

[Same structure]

### Dimension 2: [Name]

[Same structure]

---

## Expert Disagreement Map

Explicit mapping of disagreements found in the research. Burying disagreement is the most common dossier failure.

### Disagreement A: [Topic]

**Position 1:** [Summary]
- Advocates: [named experts/orgs/sources]
- Reasoning: [why they hold this position]

**Position 2:** [Summary]
- Advocates: [named experts/orgs/sources]
- Reasoning: [why they hold this position]

**Where consensus exists:** [Common ground, if any]

**Implications for user input:** [How this disagreement shapes how the user's input should be evaluated]

### Disagreement B: [Topic]

[Same structure]

---

## Open Questions

Questions the research could not resolve. These flow forward to the planner (some may become hypotheses tested via reasoning) and the synthesizer (surfaced in Meta-Reflections).

- [Open question]
- [Open question]
- [Open question]

---

## Source List

Full list of sources used, with tiers and access dates.

| ID | Source | Tier | Date Published | Date Accessed | Notes |
|----|--------|------|---------------|---------------|-------|
| 1 | [Title] | A | [Date] | [Date] | [Notes] |
| 2 | [Title] | B | [Date] | [Date] | [Notes] |

---

## Self-Validation

Run before handoff:

- [ ] At least 4 dimensions covered, or skipped dimensions explicitly justified
- [ ] Each dimension has at least 2 findings
- [ ] Sources from a mix of domains (no single source dominates)
- [ ] For fast-moving subjects, at least 30% of sources from the last 12 months
- [ ] Expert disagreement is mapped explicitly, not buried
- [ ] Inferences are flagged as "researcher inference" rather than as researched facts

The orchestrator will run `scripts/dossier_check.py` against this dossier. If the script fails, the researcher will be re-invoked with the failure reasons.
