---
name: "signal-to-system"
description: "Turn knowledge, evidence, and repeated work into useful outcomes through ten workflows: rank a messy idea pile (curiosity-compass), scan current public signals (signal-scout), turn research into a decision record (research-to-decision-map), redesign a recurring workflow (workflow-clinic), match a job to a person, tool, or service with a handoff brief (capability-matcher-and-brief-builder), design a cheap falsifiable test with an append-only ledger (experiment-designer-and-ledger), build workshop materials (workshop-workbench), run a creative project control pack (creative-project-control-room), compound session notes into decisions and reusable material (session-compounder), or map proven work to a product form (proof-to-product-mapper). Not for grill me or pressure-test interviews, or ranking, matching, or productizing framed as a pre-commitment decision (strategy-room), nor for filing sessions into workspace memory (continuity-vault)."
---

# Signal to System

One skill, ten independent workflows for turning knowledge, evidence, and
repeated work into useful outcomes. There is no fixed pipeline: pick the
workflow that owns the user's job. Workflows may consume one another's
artifacts (e.g. a scout snapshot feeding a decision map, an experiment
ledger feeding productization).

A workflow is finished when its artifact answers the user's actual decision or job, with evidence labels visible and the next action concrete. A search log, a criteria list, or a proposal to create outputs is not the finished artifact unless that is what was asked.

## Start here

1. **Open everything supplied** (notes, transcripts, lists, research) and note the date, completeness, and any stated constraints such as budget, hours, audience, or permissions.
2. **Pick one workflow** from the table below, and check the ownership table under it. Say which workflow you chose in one line.
3. **Run that workflow's procedure** below, using its template in `assets/` as a coverage check.
4. **Search the web only when live facts could change the result** and the request allows it. A "don't search" instruction is binding; say which claims stay unverified.
5. **Deliver the artifact** in the reply, or as a file when it is large or a location was named. Run the completion check in `references/evidence-and-artifact-policy.md` first.

A direct request for named outputs counts as selection. Workshop Workbench and Session Compounder then build those outputs without a separate selection round. They pause to recommend and ask only when the user has not said what to produce.

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

### Ownership with adjacent skills

Each row below has one terminal owner. Once a request lands in this skill,
the selected workflow finishes it here; do not hand the same job to
another skill and back.

| Request | Owner |
| --- | --- |
| Rank a messy idea pile with no decision framed yet | here, curiosity-compass |
| Rank options for a decision that already has an owner and stakes, or any grill me / pressure-test request | `strategy-room` |
| Build a candidate shortlist and handoff brief for a job, or map proven work to a product form, when the user names this skill or wants the working artifact | here |
| The same match or productize question framed as "should we commit, pressure-test it" | `strategy-room` |
| Turn session notes into decisions, commitments, and reusable material | here, session-compounder |
| File a session into durable workspace records or memory | `continuity-vault` |

If a request still fits both owners, ask one question naming both, then
proceed with the answer.

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
its own authority. When the record's next action is choosing a person, tool,
or service, or running an evidence-grade test, name
capability-matcher-and-brief-builder or experiment-designer-and-ledger as the
next action and stop; that follow-on runs as a new request.

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
   condition, rollback path, review date. If the pilot needs falsifiable
   predictions, sampling, and a reusable ledger, name
   experiment-designer-and-ledger as the next action and stop there.
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
   explain and ask the user which to create. A request that already names
   the outputs counts as the selection.
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

## Worked example (illustrative, synthetic)

Request: "Here's the transcript of our member interview session. Turn it into an FAQ for the public website."

- Workflow: session-compounder. The output is named (a public FAQ), so no selection round is needed.
- Extraction: six recurring questions with answers given by the host; one member's detailed story about leaving a job; one decision ("we'll pilot office hours"); two proposals that were not agreed.
- Permission judgment: the transcript records consent for internal notes only, and nobody agreed to public reuse. The public FAQ can use the explanations given by the host, who is the user. The member's story is identifiable and has unknown public permission, so it stays out; there is no de-identification permission either. Leave a marked gap: "Story example pending member consent." The proposals are not presented as decisions.
- Deliver: the FAQ draft marked as a proposal awaiting approval, a permissions table per reusable item, and the gap with its owner (host asks the member).

A wrong version would quote the member's story, paraphrase it lightly and call it anonymous, present a proposal as a decision, or publish the FAQ.

## When something goes wrong

| Symptom | Likely cause | Next move | Stop when |
|---|---|---|---|
| No workflow row fits | The request belongs to another skill or is not a job here | Say so and name the owner from the ownership table | always; do not force a fit |
| Web search fails or is not allowed | Access, rate limit, or instruction | Record the attempt in the search log; classify the scan `partial scan` or `unavailable` | the remaining claims cannot be made; say which |
| Supplied evidence is too thin to rank or recommend | Early-stage ideas | Apply the viability floor; recommend zero and name the evidence that would make one viable | always a valid result |
| Reuse permission is unknown | Consent not recorded | Leave identifiable material out of outward-facing outputs; mark the gap and its owner | never guess permission |
| A step needs a logged-in or rendered page | Live-browser work | Follow operating rule 6 | the browser task is unavailable |
| The user asks to send, publish, recruit, buy, or change a live system | External action | Prepare the artifact; stop at the action | the user gives explicit authorization for that action |

## Completion

- **Delivered:** the workflow's artifact with evidence labels, visible assumptions and gaps, and one concrete authorized next action.
- **Delivered with limits:** the artifact plus named unverifiable claims (for example `partial scan`, or unknown permission).
- **Not owned here:** a one-line statement naming the owning skill from the ownership table.

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
   A workflow may name another as the next action. It does not start that
   workflow in the same request unless the user asks, and the follow-on
   never routes the job back.
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
   form, text fetching does not suffice. If you are the main assistant, run
   it as the host's live-browser task with the user's confirmation. If you
   are a subagent, return that exact step (URL, what to check) to the
   parent and finish the rest. If no live browser is available, mark the
   claim `unchecked: needs live browser` in the artifact and stop that step.
   Never loop the step between agents.
