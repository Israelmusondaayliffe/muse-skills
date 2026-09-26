---
name: data-storytelling-studio
description: Turns checked analysis into a decision-facing artifact without recalculating or overstating the source evidence. Routes analysis to the right format, audits charts against their stated claims, and builds answer-first executive readouts. Use when data findings need to become a decision brief or readout, when reviewing visuals for evidence alignment, or when leadership needs a bounded answer from analysis.
---

# Data Storytelling Studio

## Purpose

Take checked analysis and turn it into something a decision-maker can act on — nothing more. The analytical source stays authoritative; this skill never silently recalculates it and never overstates what the evidence supports.

## The three modes

Run the mode that fits; they chain in this order.

1. **Route** — choose the smallest delivery format that can support the audience's decision. See `references/routing.md`. Produces a route brief (JSON, schema-validated).
2. **Audit** — test each chart, panel, or visual caption against its stated evidence. See `references/chart_audit.md`. Produces an audit verdict: `pass`, `revise`, or `block`.
3. **Readout** — build an answer-first executive readout with decisions, risks, caveats, and next actions. See `references/readout.md`. Produces a readout validated against the publish gate.

Each mode writes its artifact from `assets/*-template.json` and validates it before handing off. A failed validation blocks the handoff — fix the artifact, not the validator. Write artifacts to your working folder `$OUT`, never into this skill folder, and run the validators from this skill's directory:

```bash
python3 scripts/validate_route.py "$OUT/route.json"
python3 scripts/validate_audit.py "$OUT/audit.json"
python3 scripts/validate_readout.py "$OUT/readout.json"
```

Each prints `{"valid": ..., "errors": [...]}` and exits 0 only when valid. Templates carry placeholder values and a `_note`; replace every value.

## Workflow

1. Read the supplied analysis, data and draft visuals first. Record the decision question, audience, source artifact paths, and analysis state (`checked`, `partial`, or `disputed`) from them. Copy every number from the checked source as written; if a value the story needs is not in the source, say so instead of computing it. Ask the user only for what the material does not answer and the work cannot proceed without.
2. Route: apply `references/routing.md`, pick one primary format, record evidence limits and production needs. If `analysis_state` is `disputed`, stop and return the disagreement to the analysis owner.
3. Audit: for each visual, run every check in `references/chart_audit.md` and record a verdict. `block` when the source is missing, the denominator is unknown, the chart contradicts its caption, or causality is claimed without causal evidence.
When an audit finds a presentation defect you can repair from the supplied checked evidence, make that correction in the requested output and re-audit the corrected artifact in the same turn. Preserve the original failed audit separately. A too-strong caption can be narrowed to a supported claim; do not invent missing evidence or recalculate the analysis. Update the readout and its readiness from the revised audit. Do not hand a routine correction or recheck back to the user when you can finish it. An audit-only request remains read-only.

4. Readout: assemble the answer-first sequence from `references/readout.md`. Only publish when the route is valid, visuals pass or have documented revisions, every load-bearing claim has a source, and limitations are visible to the decision-maker.
5. When a production step needs a capability that is not available (interactive dashboard, rendered deck, published site), write a self-contained local Markdown story brief: decision question, audience, source artifact paths, analysis state, chosen format, evidence limits, missing production capabilities, risks, and next step. Mark the unsupported production or publication step incomplete and stop — never claim the final artifact was delivered.

## Worked example (illustrative)

Checked source: support tickets fell from 2,450 to 2,010 (18.0%) in the month after a help-center redesign. A billing-page change shipped the same week. Active customers also fell. Draft caption: "The help-center redesign cut support tickets by 18%."

- Route: `executive-readout`; one bar chart is enough, a deck is not needed.
- Audit judgment: the chart itself is honest (zero baseline, labeled values), but the caption claims a cause the evidence cannot carry. There is no comparison group, a second change shipped the same week, and counts are not per customer. Claim scope and comparison validity fail, so the verdict is `block`, handed to the analysis owner, with `handoff_ready: false`.
- Revision action: "Support tickets fell 18% (2,450 to 2,010) in the month after the help-center redesign; a billing-page change shipped the same week."
- Readout answer: "Tickets fell 18% after the redesign; we cannot yet attribute the drop to it." Decision: keep the redesign, and ask for tickets per active customer before crediting it. Replace the caption in the requested readout, inspect the revised chart against all seven audit checks, and record a new audit. Set `publish_ready` from that actual review; it stays false if a material gap remains. Do not publish externally without authorization.

A wrong version would polish the causal caption, round 18.0% to "about 20%", compute a per-customer rate the source never gave, or set `publish_ready: true` with a blocked visual.

## When something goes wrong

| Symptom | Likely cause | Next move | Stop when |
|---|---|---|---|
| Validator exits 1 | Missing field, wrong enum, or empty list | Fix the fields it names and re-run once | the field needs evidence you do not have; set readiness false and name it |
| Validator reports "artifact is invalid" | Wrong path or malformed JSON | Check the path and JSON syntax | never; this is a file problem, not an evidence problem |
| `analysis_state` is `disputed` | Source not settled | Write the route brief with `next_skill: analysis-owner` and stop | immediately; do not build the story around a dispute |
| A rate or change has no denominator in the source | Missing base | Show counts only and flag the gap | the decision needs the rate; ask the analysis owner |
| Chart rendering tool missing | Host capability | Deliver a Markdown table plus a chart spec | never claim a rendered chart you did not make |

## Output contract

- Route brief → `assets/route-schema.json`, validated by `scripts/validate_route.py`
- Audit brief → `assets/audit-schema.json`, validated by `scripts/validate_audit.py`
- Readout → `assets/readout-schema.json`, validated by `scripts/validate_readout.py`

All fields required by a schema must be present and honest. When a required input is missing or disputed, set the readiness field (`handoff_ready` / `publish_ready`) to `false` and name exactly what is missing and who must resolve it.

Done means every requested artifact exists and validates, each number matches the source, and the reply states readiness plainly. A validated readout with `publish_ready: false` is a complete, honest deliverable; say what blocks publication and who resolves it. If a production step is unavailable, deliver the story brief and name the missing capability.

## Guardrails

- The analytical source remains authoritative. Do not recalculate metrics or alter source data.
- Every claim points to evidence or is labeled as judgment. No confident conclusions from incomplete data.
- A polished visual cannot repair missing, weak, or contradictory evidence.
- Do not convert association into causality.
- Do not select a deck just because the output is executive-facing when a one-page readout is sufficient.
- Do not promise interactive behavior without a real publishing surface and a test plan.
- Do not claim production, publication, or delivery when the needed capability is absent.
- Separate measured findings from recommendations.

## Production on this host

Companion capabilities are optional and never block routing, audit, or readout work. What exists here:

- **writing-quality** and **knowledge-work-superpowers** skills exist in `~/workspace/skills/` — use them for narrative polish and structured research work.
- Charts and diagrams: build with the media pipeline or as data tables in Markdown; describe what a visual should show in the story brief when I cannot render it.
- Decks, reports, sites: produce self-contained Markdown or HTML files in `~/workspace/`; a public link requires the built-in file storage (expiring links) — say so explicitly instead of implying a published site.

Before a production-dependent step, record which of these you are relying on; if one is missing, fall back to the local story brief per the workflow.

## Hook-equivalent procedures

Run these checks at the corresponding moment; they replace the plugin's event hooks.

- **Before production starts:** confirm the route brief validates and every named production capability is available; otherwise write the local story brief.
- **Before handoff between modes:** re-validate the artifact and set readiness to `false` if the incoming audit verdict was `block` or a material evidence reference is missing.
- **Before claiming completion:** confirm the output contract is met, the publish gate passes, and no guardrail was bent — reread the guardrails if any evidence was contested during the run.
