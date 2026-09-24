---
name: founder-revenue-engine
description: "Founder-led early revenue work: turn recent public signals into an evidence-backed ICP, commercial narrative, bounded outreach drafts, founder LinkedIn content, and a first-customer prospect shortlist. Use when a founder needs early customers, design partners, a commercial message, outreach copy, or LinkedIn posts grounded in real evidence. Drafts are never sent, scheduled, or written to a CRM without a separate, explicit authorization."
---

# Founder Revenue Engine

## Purpose

Run founder-led commercial work as one evidence chain: recent public signals → a bounded, confidence-rated ICP hypothesis → a source-traceable commercial narrative → bounded outreach drafts → founder-led LinkedIn content, with first-customer prospecting wherever the evidence supports it.

This skill is research-and-draft only. It never sends messages, schedules sends, writes CRM records, or changes accounts. Every external action stops at an explicit user decision.

## Routes

Pick one primary route at the start. Do not drift into drafting before the evidence route is done.

| Route | What it does | Reference |
|---|---|---|
| `signal-research` | Collect recent public pain, intent, buying, and language signals tied to named sources and dates | `references/research-framework.md` |
| `icp` | Turn signals into a bounded ICP hypothesis with disqualifiers, confidence, and verification gaps | `references/stage-controls.md` |
| `narrative` | Connect audience problem, offer, proof, objections, and call to action in one traceable story | `references/stage-controls.md` |
| `outreach` | Draft a small, evidence-linked message sequence with stop rules; never sends | `references/stage-controls.md` |
| `content` | Write founder-led LinkedIn posts from verified claims using the consensus-breaking method | `references/linkedin-workflow.md` |
| `first-customers` | Find and rank evidence-backed first-customer prospects; produce a standalone HTML report | `references/research-framework.md`, `references/report-artifact.md` |

## Workflow

1. **Define the brief.** Ask the user for (or confirm): the offer in one sentence, the commercial outcome they want (early customers, design partners, beta users, message validation), the evidence window (default: last 30 days), prohibited actions, and any positioning decisions already settled. Ask only when the answer would materially change the work.
2. **Choose the route** using `references/routing.md`. If no evidence exists yet, route to `signal-research` before claiming an ICP.
3. **Research with Hatch tools.** Use `browser.search` and `browser.open` for public sources (forums, reviews, GitHub issues, company pages, job posts, changelogs), and the `social` skill for public posts. Prefer original pages over snippets. Never bypass login walls, paywalls, access controls, rate limits, or robots restrictions.
4. **Produce the route's output.** Follow the reference for that route. Record every claim's source, source type, and publication date (or "date unavailable").
5. **Run the checks.** Apply `references/commercial-copy-checks.md` to all prose. For outreach/narrative/copy, prefer the `writing-quality` workspace skill when it fits; otherwise use the bundled checks. Validate the route artifact with `scripts/validate_output.py`.
6. **Deliver drafts and handoff instructions only.** Return copy plus exact next steps the user (or a separately authorized action) must take. Drafting never authorizes sending.

## Evidence and Safety Rules

These are hard boundaries, not suggestions.

- Every signal traces to a named source with a date. A signal with no source is not evidence.
- An ICP is a confidence-rated hypothesis, never a fabricated market fact. Narrow it by pain, trigger, role, and company state until it can reject weak matches.
- Proof stays inside its real boundary: a pilot, demo, process, or credential must not become a result claim. Missing proof becomes an honest pilot/learning claim or is removed.
- Personalization comes from a named source only. Use a research placeholder when the detail is missing; never invent a relationship, event, pain, or account detail.
- Do not use data brokers, leaked datasets, scraped contact lists, or sensitive personal information. Do not target people using health, financial hardship, political belief, sexuality, religion, or other sensitive attributes.
- Outreach drafts stay under the stage-appropriate ask and carry stop rules: reply, opt-out, invalid address, sequence cap.
- If the offer or positioning is unresolved, write a commercial-decision gap: the evidence, assumptions, open questions, prohibited claims, and the exact next decision. Stop before drafting claims that depend on an invented answer.

## Pre-Action Checklist

(Adapted from the plugin's hooks; run as a procedure, not as a platform hook.)

**Before researching or drafting:**
- [ ] The offer, commercial outcome, evidence window, and prohibited actions are defined.
- [ ] An unresolved offer/positioning decision is either settled by the user or written down as a gap. Never draft around it.
- [ ] The route is chosen; the previous stage's output exists if the route depends on it.

**Before returning any draft:**
- [ ] Every result, number, customer statement, credential, and comparison traces to the approved evidence set, or is labeled a hypothesis.
- [ ] Observed market language is separated from the founder's interpretation.
- [ ] One audience, one offer, one next action. The ask matches the commercial stage.
- [ ] `send_authorized` is false and stated. No send, schedule, CRM write, or account change is implied.
- [ ] For outreach: stop rules are present; personalization is source-backed.

**Session-continuity note:** if a prior run left a commercial-decision gap or an unfinished route, surface it before starting new work rather than re-researching from zero.

## Companion Capabilities on Hatch

All optional. Missing companions do not block any route.

- **Writing quality:** use the `writing-quality` workspace skill for final commercial prose validation; otherwise apply `references/commercial-copy-checks.md`.
- **Gmail / Google Calendar / CRM:** separate, explicit authorization is required at action time for anything sent, scheduled, or written. Drafts never grant it.
- **LinkedIn posting:** drafts stay drafts. Publishing through the live browser requires separate authorization.
- **Visual assets:** the `brand-studio` and `media` (image generation) skills can support campaign assets when requested.
- **Unresolved strategy questions:** write the commercial-decision gap described above; there is no Strategy Room here, so the gap document is the decision vehicle.

## Output Contract

- Each run produces a route artifact JSON matching `assets/route-artifact-schema.json` (template: `assets/route-artifact-template.json`). Validate with:
  ```bash
  python3 scripts/validate_output.py <artifact.json>
  ```
- The `first-customers` route additionally produces a standalone HTML report via `references/report-artifact.md` and `scripts/generate_report.py`, saved under `~/workspace/your_files/` or a goal's files directory when the user wants it.
- Copy outputs (narrative, outreach, LinkedIn) are delivered as text plus their artifact JSON.

## Operating Rules

1. Ask the user for personal input the work needs (offer details, positioning, voice samples, business specifics). Never invent user-specific data.
2. Keep each route narrow: signal research does not write copy, prospecting does not send.
3. Label uncertainty. Stale evidence is labeled stale, inference is labeled inference.
4. Prefer ten strong prospects or five solid signals over a long weak list.
5. Use citations in the response whenever web research was performed.
