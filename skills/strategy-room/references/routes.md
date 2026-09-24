# Strategy Room routes

One decision operation per engagement. Pick the route from the trigger, run its procedure, deliver its output, and stop before execution.

## Route selection

- **interview**: the brief is vague, incomplete, or held in the user's head. → `references/grill-me.md`
- **wayfind**: the destination is meaningful but the route is obscured by several dependent decisions. Map the fog, name one blocking edge; do not turn it into a generic project plan.
- **challenge**: hidden beliefs or external facts could reverse the choice. → `references/challenge-pipeline.md`
- **explore**: the option set is narrow or repetitive.
- **synthesize**: options and evidence are ready for a recommendation.
- **register**: uncertainty must remain visible after the decision.
- **prioritize**: messy ideas, questions, or opportunities need a ranked focus.
- **match**: the decision is who or what should perform a bounded job.
- **productize**: existing proven or promising work may deserve a reusable form.

If evidence is insufficient for an irreversible choice, route to `challenge` or `register` before `synthesize`.

---

## wayfind — Decision Wayfinder

Make uncertainty legible without pretending the full route is known. The deliverable is a decision map and the next blocking edge, not a complete project plan.

1. State the destination (the observable state that would mean the effort succeeded), owner, horizon, evidence of arrival, and explicit exclusions.
2. Inspect the conversation and the closest local sources first. Preserve already-settled decisions; never re-ask known facts.
3. List material decision nodes. Connect each node to its prerequisites and to the downstream choices it unlocks.
4. Mark each node `settled`, `frontier`, `fog`, `blocked`, or `deferred`. Fog is not yet understood; frontier is understood enough to decide next.
5. Identify the frontier decision with the greatest effect on downstream decisions. This is the next blocking edge.
6. Name what evidence or user judgment can resolve it. Recommend a default when evidence supports one.
7. Resolve only that decision, update the map, and recalculate the frontier.
8. Stop when the next blocking edge is named, or continue one edge at a time if the user asks.

Record the map with `assets/decision-map-template.md` when file output is authorized. A node stays compact: stable ID, precise label, status, prerequisites, what it unlocks, owner, evidence source, current options, recommendation, acceptance test, and a decision record when settled.

The result is complete when another fresh context could locate the map and take up exactly one next decision without rereading the full conversation.

---

## explore — Multi-Direction Explorer

Create genuinely different paths from one seed, then help choose the strongest.

1. Identify the axis of variation: audience, tone, format, risk level, medium, business goal, visual language, time horizon, or technical approach. See `references/variation-axes.md` for the full axes list.
2. Generate at least 10 meaningfully distinct directions (strategy, not synonym swaps). Give each a short label and a one-sentence logic of the direction.
3. Remove weak filler options before delivery.
4. Optionally enforce breadth on a written options file: `bin/check_option_count.py FILE 10`.
5. Present the options in `assets/options-matrix-template.md`: option, core idea, best for, tradeoff, score.
6. Recommend the top 2–3 when a decision is needed, with reasons.

---

## synthesize — Decision Synthesizer

Converge on one recommendation without hiding uncertainty. The choice, conditions, and reasons must be inspectable by someone who did not join the working session.

1. State the decision and the decision owner in one sentence.
2. Collect only evidence and options relevant to that decision.
3. Compare options on decision-specific criteria, keeping facts separate from judgment:
   - Cite or qualify every material factual claim.
   - Compare against specific criteria, not a generic scorecard.
   - State what would change the recommendation and which conditions must hold.
   - Prefer a reversible test when evidence is weak and the cost of being wrong is high.
4. Choose one recommendation. Name its conditions, risks, reversibility, and confidence (`low` / `medium` / `high`).
5. Fill `assets/decision-record-template.json` and validate: `bin/validate_record.py decision-record.json assets/decision-record-schema.json`.
6. Return a handoff that identifies the execution owner without starting execution.

If no option clears the minimum evidence bar, recommend a bounded test rather than a false final choice. If options are not meaningfully distinct, route back to `explore`. If a load-bearing assumption remains untracked, add it to the assumption register before delivery. End with one recommendation, not a list disguised as a conclusion.

---

## register — Assumption Register

Keep uncertainty durable after a decision. The register shows which beliefs are load-bearing, how they will be tested, and what result should change the plan.

1. Extract the assumptions that must be true for the decision or plan to work.
2. Separate factual, behavioral, capability, and timing assumptions.
3. For each, record: statement, status, confidence, reversibility, owner, test, and kill condition. A kill condition names the observable evidence that stops or redirects the plan.
4. Use `assets/assumption-register-template.json` and validate: `bin/validate_record.py assumption-register.json assets/assumption-register-schema.json`.

Statuses: `untested` (no adequate evidence exists), `supported` (current evidence directly supports the stated scope), `weakened` (evidence reduces confidence but does not falsify), `falsified` (the plan should change), `expired` (evidence or time window no longer current). Reversibility: `reversible`, `partly-reversible`, `irreversible`.

- Do not convert opinions into supported assumptions without evidence.
- If an assumption has no owner or test, mark it untested rather than omitting the gap.
- If a kill condition is vague, replace it with an observable threshold or event.
- Flag High criticality + High fragility + Hard observability assumptions as critical risks.
- Revisit the register when evidence changes and preserve prior statuses in the durable record.

---

## prioritize — Curiosity Compass

Turn scattered curiosity into a defensible focus without pretending an interesting idea is a proven opportunity. Use only when there are multiple rough ideas and the decision is which deserve attention or a bounded test.

1. State the attention decision, intended beneficiary, constraints, and the consequence of choosing badly.
2. Normalize the raw ideas into distinct candidate directions. Merge duplicates without erasing meaningful differences.
3. Choose four to six criteria that fit the decision (expected value, urgency, evidence, fit, effort, reversibility, learning value, downside). Show each criterion and its relative importance. Ask when a missing preference could change which candidates clear the floor.
4. Inspect supplied sources first. Verify current public facts only when they could materially change a score. Mark unknowns; do not turn thin evidence into precise confidence.
5. Score every candidate on the same scale, explain material differences, and show the uncertainty behind each score.
6. Apply a visible viability floor. Recommend zero to three directions — it is valid for no candidate to qualify.
7. For each qualifying direction, name why it matters, why now, what could make it wrong, and the cheapest useful first test.

Do not reward novelty, excitement, or the user's prior attachment unless it satisfies a stated criterion. Surface a surprising result when the criteria support it.

Record with `assets/curiosity-compass-template.md`. Stop at the ranked focus and test recommendation. Research, purchasing, publishing, assignment, and execution need separate authority.

---

## match — Candidate Matcher and Brief Builder

Match a bounded outcome to a qualified person, agent, tool, product, or service, then make the handoff usable.

1. Define the match: outcome, audience, deliverable, must-have capabilities, preferences, constraints, timing, supplied budget, collaboration needs, exclusions, permissions, and acceptance evidence. Separate qualification gates from preferences.
2. Build the candidate set. Preserve user-supplied candidates unless clearly ineligible. Add candidates only when the set is insufficient and research is authorized or required. Use current public evidence when features, work, price, geography, compatibility, or availability could change the result.
   - For people, use only public professional information. Do not infer sensitive traits, private circumstances, willingness, capacity, or availability.
   - Mark unverified cost, capacity, geography, fit, and compatibility as unknown.
3. Decide. Apply every must-have as a qualification gate and compare all viable candidates against the same visible criteria. Return exactly one status:
   - `qualified match`: one recommended candidate plus a ranked shortlist.
   - `provisional match`: a lead candidate whose named unknown could still disqualify it.
   - `no qualified match`: failed must-haves plus the smallest next search or fallback.
4. Build the handoff with `assets/candidate-match-template.md`. Create the final handoff brief only for a qualified match; a draft clearly marked non-authorizing for a provisional match; a search or fallback brief for no qualified match.

For each finalist show evidence, gaps, tradeoffs, and disqualifiers. Do not force a winner, infer missing facts, or create false precision from thin evidence. Contacting a person, assigning work, buying a product, installing a tool, changing permissions, or sending the brief requires separate user authorization.

---

## productize — Proof-to-Product Mapper

Choose the form that fits the evidence, not the most impressive container.

1. Grade the proof. Identify the problem, beneficiary, repeated method, observed result, context, and source of each material claim. Classify:
   - `proven`: repeated evidence supports the result in the relevant context.
   - `promising`: some evidence exists, but material uncertainty remains.
   - `unproven`: the work is mainly an idea or proposal.
   
   Promising and unproven work may continue, but the recommendation must focus on validation, not product certainty. Never invent demand, revenue, differentiation, adoption, or repeatability.
2. Compare possible forms across three separate axes:
   - Delivery form: guide, template, workshop, service, software tool, skill, plugin, or operating system.
   - Access model: internal, private client, member or community, or public.
   - Economics: free, cost-recovery, paid, sponsored, or undecided.
   
   Compare only plausible forms against user need, context of use, proof strength, repeatability, support and maintenance, distribution, customization, risk, rights, privacy, and effort to a useful minimum version. Check current alternatives only when they could materially change the form or validation path.
3. Recommend one primary form, access model, and economics choice, plus one strong alternative. Record with `assets/productization-brief-template.md`: intended user, promise, inputs, outputs, smallest useful scope, exclusions, evidence, risks, distribution hypothesis, acceptance test.
4. For promising or unproven work, design the cheapest validation that could change the recommended form. Stop at the brief and validation recommendation.

Building, publishing, selling, distributing, or installing requires a separate request and authority.
