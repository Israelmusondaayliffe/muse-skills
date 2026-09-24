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

Each mode writes its artifact from `assets/*-template.json` and validates it with `scripts/validate_*.py` before handing off. A failed validation blocks the handoff — fix the artifact, not the validator.

## Workflow

1. Confirm the decision question, audience, source artifact paths, and analysis state (`checked`, `partial`, or `disputed`). Ask the user for anything missing — do not invent it.
2. Route: apply `references/routing.md`, pick one primary format, record evidence limits and production needs. If `analysis_state` is `disputed`, stop and return the disagreement to the analysis owner.
3. Audit: for each visual, run every check in `references/chart_audit.md` and record a verdict. `block` when the source is missing, the denominator is unknown, the chart contradicts its caption, or causality is claimed without causal evidence.
4. Readout: assemble the answer-first sequence from `references/readout.md`. Only publish when the route is valid, visuals pass or have documented revisions, every load-bearing claim has a source, and limitations are visible to the decision-maker.
5. When a production step needs a capability that is not available (interactive dashboard, rendered deck, published site), write a self-contained local Markdown story brief: decision question, audience, source artifact paths, analysis state, chosen format, evidence limits, missing production capabilities, risks, and next step. Mark the unsupported production or publication step incomplete and stop — never claim the final artifact was delivered.

## Output contract

- Route brief → `assets/route-schema.json`, validated by `scripts/validate_route.py`
- Audit brief → `assets/audit-schema.json`, validated by `scripts/validate_audit.py`
- Readout → `assets/readout-schema.json`, validated by `scripts/validate_readout.py`

All fields required by a schema must be present and honest. When a required input is missing or disputed, set the readiness field (`handoff_ready` / `publish_ready`) to `false` and name exactly what is missing and who must resolve it.

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
