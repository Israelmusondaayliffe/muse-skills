---
name: "signal-to-system"
description: "Turn knowledge, evidence, and repeated work into useful outcomes across ten workflows: rank messy ideas (curiosity-compass), scan current public signals (signal-scout), turn research into a decision record (research-to-decision-map), diagnose and redesign a recurring workflow (workflow-clinic), match an outcome to a person/tool/service with a handoff brief (capability-matcher-and-brief-builder), design a cheap falsifiable experiment with an append-only ledger (experiment-designer-and-ledger), build workshop deliverables (workshop-workbench), run a source-of-truth control pack for a creative project (creative-project-control-room), compound session notes into decisions and reusable material (session-compounder), or map proven work into a reusable product form (proof-to-product-mapper). Trigger on verbs like rank, scan, decide, test, workshop, facilitate, debrief, or productize."
---

# Signal to System

One skill, ten independent workflows for turning knowledge, evidence, and
repeated work into useful outcomes. There is no fixed pipeline: pick the
workflow that owns the user's job. Workflows may consume one another's
artifacts (e.g. a scout snapshot feeding a decision map, an experiment
ledger feeding productization).

## Route the request

| User's situation | Workflow | Stage |
| --- | --- | --- |
| Scattered ideas, unclear what deserves attention | curiosity-compass | sense |
| "What's changing now" in a field, community, or market | signal-scout | sense |
| Evidence gathered; needs a visible path to a decision | research-to-decision-map | sense |
| Recurring work that is slow, fragile, or wasteful | workflow-clinic | decide |
| Must choose who/what should do the work | capability-matcher-and-brief-builder | decide |
| One important assumption needs a cheap test | experiment-designer-and-ledger | decide |
| Planning or building a workshop, class, or facilitated session | workshop-workbench | make |
| Coordinating multi-asset creative production | creative-project-control-room | make |
| Meeting/interview/session notes should produce more than a summary | session-compounder | compound |
| Proven or promising work should become a reusable product | proof-to-product-mapper | compound |

If the request doesn't match any row, say so instead of forcing a fit.

## Shared rules (all workflows)

Read [references/source-and-tool-policy.md](references/source-and-tool-policy.md)
when current public facts matter, and
[references/evidence-and-artifact-policy.md](references/evidence-and-artifact-policy.md)
for evidence labels, links, and artifact behavior. Never invent user-specific
data (writing samples, business details, names, credentials); ask the user
when a workflow needs personal input.

Read [references/advanced-execution.md](references/advanced-execution.md)
before parallelizing: only signal-scout, research-to-decision-map,
capability-matcher-and-brief-builder, and workshop-workbench have an optional
subagent path. Single-agent sequential work is the default and must remain
fully supported.

## Workflow procedures

### curiosity-compass — rank messy ideas

1. State the decision the ranking supports, the intended beneficiary, and any
   real constraints supplied. Do not use for a settled choice that already
   has a research record.
2. Normalize raw ideas into distinct candidate directions; merge duplicates
   without erasing meaningful differences.
3. Choose 4–6 criteria that fit (expected value, urgency, evidence, fit,
   effort, reversibility, learning value, downside). Show criteria and
   relative importance; ask only when a missing preference could change the
   winner.
4. Search the current web only when live facts would materially change a
   score. Score consistently, explain the strongest differences, show
   uncertainty — never hide weak evidence behind a precise number.
5. Apply a viability floor. Recommend 0–3 directions; if none clears it, say
   so and name what evidence could make one viable. For each viable
   direction: why it matters, why now, what could make it wrong, the
   cheapest useful first test.
6. Do not reward an idea for being exciting, easy to describe, or already
   favored. Surface a surprising winner when the criteria support one.
Template: `assets/curiosity-compass-template.md`. Short decisions may live in
chat; save the artifact when the user asks for a durable record.

### signal-scout — scan current public signals

1. Establish audience, question, geography, time window, and the decision the
   scan informs. Ask only when materially different readings change the
   search.
2. Create distinct search lanes (official change, practitioner experience,
   repeated pain, alternatives, counter-signal). Use current web search, open
   underlying pages, record dates when recency matters. Search for
   disconfirming evidence; prefer primary owners for facts and forums/reviews/
   social for experience and language.
3. Keep a compact search log: query/lane, access result, limitation. Record
   blocked or inaccessible sources rather than omitting them silently. Stop
   when searches repeat known patterns or cannot affect the decision.
4. Cluster into named signals: what's happening, who appears affected,
   evidence strength and freshness, representative links, counter-evidence or
   bias, why it might matter, a safe next check. Rank only against the user's
   stated purpose; never turn search frequency into a population claim.
5. Classify honestly: `current scan`, `partial scan`, `unavailable`, or
   `no qualifying signal`. Partial/unavailable must name what was attempted,
   what failed, and which claims cannot be made.
Template: `assets/signal-scout-template.md`. A dated snapshot, not monitoring.
For genuinely independent lanes, use 2–4 bounded subagents; a sequential
single-agent run stays fully supported.

### research-to-decision-map — research into a decision record

Pass one (provisional map):
1. State the decision, options, decision owner, constraints, and decision
   horizon. Inventory supplied research, separating verified facts, supplied
   claims, assumptions, judgment, and missing evidence.
2. Map each option against the criteria; preserve disagreements and show
   which source or value produces each difference. Search only to verify
   unstable claims or close a material gap that could change the result.
3. Judge sufficiency honestly: `recommend` (adequately supported),
   `recommend provisionally` (reversible choice, named uncertainty, review
   trigger), or `decline pending evidence` (a material gap could change the
   choice). For a consequential or disputed decision, an independent critic
   (subagent) may test the map — integrate the critique, don't append it.

Decision gate: present the provisional map; ask the user to choose, correct a
value, or delegate. Never record a final user decision before this gate.

Pass two (final record): selected option, rationale, confidence, accepted
risks, rejected alternatives, unresolved evidence, review trigger, immediate
next action. Preserve a different user choice without rewriting the evidence.
Template: `assets/research-to-decision-template.md`. Further execution needs
its own authority. Route person/tool/service selection to
capability-matcher-and-brief-builder; evidence-grade tests to
experiment-designer-and-ledger.

### workflow-clinic — diagnose and redesign a recurring workflow

1. Define the recurring trigger, desired result, people affected, frequency,
   volume, and acceptable failure. Map the current path: inputs, decisions,
   transformations, handoffs, waits, rework, approvals, evidence.
2. Identify actual failure modes — distinguish process problems from
   training, authority, data, incentive, or tooling problems. Establish a
   baseline from supplied observations or clearly labeled estimates; never
   invent time or cost savings.
3. Redesign deliberately per step: human ownership (judgment, relationships,
   accountability, ambiguity), AI assistance (bounded interpretation,
   drafting, classification, synthesis with review), automation (stable,
   deterministic, permissioned repetition), or removal (no defensible value).
   Recommend tools only after the job and constraints are clear; search the
   web when current product capabilities affect the design.
4. Outline the pilot: boundary, owner, baseline, success signal, stop
   condition, rollback path, review date. Falsifiable predictions, sampling,
   and a reusable ledger belong in experiment-designer-and-ledger.
5. Never implement integrations or change live systems without explicit
   authorization. Template: `assets/workflow-clinic-template.md`. Complete
   when another person can run the pilot and say why each step belongs to a
   human, AI, automation, or nowhere.

### capability-matcher-and-brief-builder — match outcome to candidate

1. State the outcome, deliverable, required capabilities, constraints,
   timing, budget (if supplied), collaboration style, exclusions, and
   success evidence. Separate must-haves from preferences.
2. Build the candidate set: preserve user-supplied candidates unless clearly
   ineligible; research current public professional evidence when the choice
   depends on current work, features, price, or availability; add stronger
   alternatives when the set is thin. Use only public professional
   information for people; never infer sensitive characteristics, private
   circumstances, willingness, or availability. Mark unverified cost,
   capacity, geography, compatibility as unknown.
3. Score against the same visible criteria with every must-have as a
   qualification gate. Outcomes: `qualified match` (recommendation + ranked
   shortlist), `provisional match` (named confirmation pending), or
   `no qualified match` (failed must-haves + fallback). Show evidence, gaps,
   tradeoffs, disqualifiers per finalist; never force a winner from thin
   evidence.
4. Build a handoff brief only for a qualified match: outcome and audience,
   context and source links, deliverables and exclusions, constraints and
   permissions, milestones or review points, acceptance evidence, open
   questions. Provisional matches get a clearly labeled draft; no-match gets
   a search/fallback brief. Template: `assets/capability-match-template.md`.
   Contacting a person, buying, installing, or assigning external work needs
   separate authorization.

### experiment-designer-and-ledger — cheap falsifiable test

1. State the decision the experiment informs. Write one falsifiable
   assumption and why it matters. Record current evidence strength:
   unsupported, suggestive, promising, or repeated.
2. Define the smallest test that could meaningfully shift confidence —
   prefer reversible, low-cost tests. Set prediction, sample, method, success
   measure, failure signal, stop rule, timebox, and permission/ethical
   constraints before any result exists. Name confounders and what the test
   cannot prove.
3. Create the record with `assets/experiment-design-template.md`; use
   `assets/experiment-ledger.csv` for multiple runs, comparison, or later
   automation. The ledger is append-only: stable experiment IDs, new
   versioned records for corrections, never overwrite the original
   prediction, method, raw observation, or result after the outcome is known.
4. When results arrive: preserve raw observations separately from
   interpretation; compare outcome with the precommitted prediction;
   classify as supports, weakens, inconclusive, or invalid (recording the
   exact invalidation reason); record actual sample, deviations,
   confounders, and raw evidence location; update confidence without
   pretending one test proves a broad claim; recommend stop, repeat, revise,
   or scale.
5. Never run a live experiment, recruit people, send messages, or change a
   service without explicit authorization.

### workshop-workbench — build workshop deliverables

1. Read supplied material first. Identify audience, intended change, workshop
   length, delivery setting, source authority, existing assets, missing
   decisions (critical vs non-critical). Do not assume the maximum package.
2. Recommend a right-sized deliverable set (outcome/audience brief, timed
   facilitator run-of-show, facilitator guidance and contingencies,
   participant guide, exercises and demos, logistics/materials checklist,
   source notes and fact-check record, feedback and evaluation, slide
   outline). Explain why each is worth producing. Ask the user to select
   before generating a large package; a direct request for named
   deliverables counts as selection.
3. Build the selected materials as one coherent run-ready package. Keep
   participant material separate from facilitator-only guidance. Never
   invent case-study results, testimonials, or source claims. Never label a
   package run-ready while a critical decision (audience, intended change,
   duration, setting, facilitator ownership, approvals) is unresolved — then
   produce a draft naming the blocker, its owner, and the resolve-by point.
4. For a substantial package, a fresh subagent reviewer may check timing,
   instructions, participant clarity, source boundaries, and completeness;
   the primary run integrates the review. Template:
   `assets/workshop-package-template.md`. Finished visual slides require an
   explicit request and an appropriate presentation tool.

### creative-project-control-room — source-of-truth control pack

1. Record the brief as proposed, draft, or approved: audience, intended
   response, creative proposition, deliverables, channels, constraints,
   deadline, approval authority. Never mark approved without an approval
   source and date.
2. Register source references with provenance, usage rights if known,
   intended influence, and forbidden copying or drift. Inventory every
   required asset: format, owner, source, dependencies, status, version,
   review evidence, delivery location (`assets/asset-register.csv`).
3. Record creative and production decisions separately from open questions;
   every approved decision needs owner, date, approval evidence. Map
   responsibilities, approval gates, risks, blockers, recovery paths. Define
   what counts as approved, delivered, archived.
4. Operate: update from supplied production evidence; never mark an asset
   complete solely because it was started; preserve superseded decisions
   that explain downstream work; flag conflicts between approved brief and
   current assets. Mark licensing/provenance unknowns rather than assuming
   permission. Generate or edit creative assets only when explicitly asked
   and the suitable specialist capability exists. Template:
   `assets/creative-control-pack-template.md`.

### session-compounder — compound session notes

1. Read the transcript/notes. Establish session purpose, participants/roles,
   date, source completeness, privacy or attribution limits. Extract without
   upgrading status: decisions actually made, proposed ideas, commitments
   and owners, questions and unresolved disagreements, reusable
   explanations/methods/stories/examples, exact quotes only when the source
   supports the wording.
2. For every reusable item record reuse permission (allowed / restricted /
   unknown / prohibited), allowed audience, attribution rule, and whether
   de-identification is required. Mark unclear speakers, dates, ownership,
   consent as unresolved.
3. Recommend outputs worth creating (decision record, action list, follow-up
   brief, FAQ, knowledge note, guide seed, workshop material, content brief,
   experiment). Rank by usefulness, evidence, audience, effort, sensitivity;
   explain and ask the user which to create.
4. Produce only selected outputs. Never create for an audience broader than
   the recorded allowed audience. Prohibited reuse means no derivative.
   Unknown or restricted permission means no identifiable material in
   outward-facing derivatives; de-identify only when permission explicitly
   allows de-identified reuse; otherwise leave a clearly marked gap. Never
   publish, message participants, or write to a connected destination
   without explicit authorization. Template:
   `assets/session-compounder-template.md`.

### proof-to-product-mapper — map proven work to a reusable form

1. Grade the evidence: identify problem, beneficiary, repeated method,
   observed result, claim sources. Classify: Proven (repeated evidence
   supports the result in context), Promising (some evidence, important
   uncertainty remains), Unproven (primarily an idea). Promising and
   unproven work must emphasize validation, not productization certainty.
2. Compare forms across three axes: delivery form (guide, template,
   workshop, service, software tool, skill, plugin, operating system),
   access model (internal, private client, member/community, public),
   economics (free, cost-recovery, paid, sponsored, undecided). Compare only
   plausible forms on: user need and context of use, evidence strength and
   repeatability, support and maintenance burden, distribution and
   discoverability, customization vs standardization, risk/rights/privacy,
   effort to a useful minimum version. Search current alternatives when
   market context could change the recommendation; never invent demand,
   revenue, or differentiation.
3. Recommend one primary form + access model + economics choice and a strong
   alternative. Create the smallest useful scope: intended user, promise,
   inputs, outputs, exclusions, evidence, risks, distribution hypothesis,
   acceptance test. For promising/unproven work, design the cheapest
   validation that could change the choice. Template:
   `assets/productization-brief-template.md`. Building, publishing, selling,
   or installing the product requires a separate request and authorization.

## Session hooks (checklists)

The plugin had no portable hooks; the originals depended on Codex/Claude
host events. Translate them into checks run here:

- **Session start:** check MEMORY.md and `~/memory/` for open items from
  this skill — experiment ledger entries awaiting results, control packs
  mid-production, scout snapshots due for comparison, review triggers on
  decision records. Surface them rather than acting.
- **Session end:** if the session produced decisions, commitments, or
  reusable explanations, offer session-compounder before closing out.
- **Recurring (cron, only with user approval):** a saved signal-scout
  snapshot can be re-run on a schedule for comparison — never imply
  activity between runs; an experiment review trigger can remind the user
  when a timebox closes. Each scheduled re-run must be explicitly approved.

## Operating rules

1. Pick exactly one owning workflow per request; never blend procedures.
2. Templates in `assets/` are coverage checks, not rigid forms.
3. Deliver a portable Markdown artifact in the response when reasonably
   sized; for large multi-file deliverables, save under `~/workspace/` and
   return a compact receipt with paths, key decisions, evidence status, and
   unresolved gaps.
4. Keep evidence categories visibly separate; never upgrade a proposal or
   promising result into proof.
5. External writes, messages, purchases, publishing, and live-system changes
   always need explicit user authorization.
6. When a step requires a logged-in site, a rendered/dynamic page, or a
   form, delegate it to the parent for live-browser work instead of
   pretending text fetching suffices.
