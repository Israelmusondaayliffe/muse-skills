# Phase Procedures

Full operational detail for each phase of the knowledge-work workflow. Read the section for the phase you are about to execute, not the whole file at once.

---

## 1. Framing Knowledge Work

Turn a rough request into a clear work brief. The brief prevents a polished answer to the wrong question.

**Gate:** For substantial or high-stakes work, do not begin deep research or drafting until the work is framed. If the user already supplied outcome, audience, scope, sources, constraints, and success criteria, summarize the frame and proceed — unless two viable directions would produce meaningfully different results.

**Procedure:**

1. **Inspect available context.** Read project rules, existing brief files, templates, and source locations before asking questions. Resolve discoverable facts through files or connected skills (gmail, google-calendar, etc.).
2. **Define the outcome.** State what must exist when finished, as an observable result not an activity. Weak: "Research employee curiosity." Strong: "Produce a cited decision brief comparing three program models and recommending one pilot."
3. **Define the intended user.** Who reads/uses the result, what they already know, what decision or action should follow, what level of detail they can use.
4. **Define questions and scope.** List the questions the work must answer. Separate included and excluded areas so research does not grow without control. If the request contains several independent deliverables, split them and frame the first one fully.
5. **Identify sources of truth.** Name the files, skills/connectors, datasets, official sources, or people that own the facts. Mark missing or inaccessible sources. Never substitute public search for an available internal source of truth.
6. **Record constraints.** Deadline or freshness window, output format and length, confidentiality, required or forbidden sources, voice/template rules, actions that require approval.
7. **Define success criteria.** Observable checks, e.g.: every key factual claim has direct support; the recommendation answers the named decision; conflicting evidence is surfaced; the requested file and format exist in the approved location.
8. **Resolve open decisions.** Ask one focused question only when a preference cannot be discovered or safely inferred and the answer changes the result. Otherwise state the assumption and proceed. Do not invent user-specific data.

**Output:** For file-based work, use `assets/work-brief-template.md` and save the brief in the user-approved location. For chat-only work, present a compact frame: Outcome / Audience / Questions / Scope / Sources of truth / Constraints / Success criteria / Assumptions.

**Approval rule:** Request approval when the frame introduces a meaningful interpretation, tradeoff, or scope choice. If the request already authorizes a clear execution path, record the frame and continue.

**Review before handoff:** missing audience or decision; questions unanswerable by the named sources; contradictory constraints; vague success criteria; hidden scope expansion.

---

## 2. Planning Knowledge Work

Convert a clear brief into an executable plan where each task creates a reviewable result and states how completion is proved.

**Preconditions:** defined outcome, known audience, clear scope, named sources of truth, binding constraints, observable success criteria. If missing, run Framing first.

**Procedure:**

1. **Map the artifacts.** Brief, research plan, source ledger, claim ledger, analysis notes, draft, review, final deliverable, delivery note. Follow output-path rules.
2. **Define the evidence standard.** Whether primary sources are required, whether current facts need live verification, whether important claims need independent confirmation, how internal and public sources combine, how disputed or missing evidence is labeled.
3. **Split into deliverable units.** Each task has one clear purpose and a result a reviewer could accept or reject independently. Keep tightly coupled actions together.
4. **Write each task completely.** For every task: inputs, specific actions, output, dependencies, evidence requirement, verification method, stop or escalation condition. No placeholders like "research as needed."
5. **Mark approval boundaries.** Decisions that require the user: major scope change, publication, external communication, choosing between materially different recommendations. Do not ask for approval between ordinary authorized steps.
6. **Set the final gate.** The last stage must include: brief coverage review; source and claim audit; citation and link check; current-fact refresh; format and output-path check; delivery-note preparation.

**Output:** Use `assets/knowledge-work-plan-template.md` for file-based plans.

**Self-review before execution:** every brief requirement maps to at least one task; no placeholders or vague verbs; dependencies and order check out; every task has a verification surface; no task silently adds scope.

---

## 3. Systematic Research

Answer important questions through an explicit evidence process. Search results are discovery aids, not evidence by themselves.

**Gate:** Do not draft conclusions before defining the decision question, research questions, evidence standard, and stop condition. For simple one-source lookups, use the fast path and cite the direct source.

Choose the research bound before searching: **bounded** research answers one decision question within named limits; **broad** research maps a field but still defines a saturation rule and excluded branches.

**Procedure:**

1. **Question map.** Break the brief into answerable questions. For each: why it matters, what evidence would answer it, which source owns the fact, what date/freshness range applies, what would disconfirm the likely answer. Also record the overall stop condition: a source-owner answer, a minimum independent-evidence threshold, a time boundary, or saturation with named remaining gaps.
2. **Source routing, in this order:** (a) the connected skill, file, or document that owns the fact; (b) primary public sources — official documents, filings, datasets, laws, standards, papers, transcripts, first-party records; (c) strong secondary analysis for context; (d) discovery sources that lead to stronger evidence. For technical/platform questions prefer official documentation; for current facts use live research, not memory.
3. **Discovery pass.** Map terminology, key entities, likely primary sources, date ranges, competing explanations. Do not fill the source ledger with weak pages merely because they rank highly.
4. **Evidence pass.** Open and read the sources that can directly answer the questions. Record each useful source in `assets/source-ledger-template.md` format (Source ID, title and location, type, publication/update date, access date, relevant question/claim, limits and conflicts).
5. **Triangulation.** For important claims, seek independent support. Several pages repeating one original report count as one evidence chain. When sources conflict: check dates, definitions, populations, methods, incentives; identify whether the conflict is factual, methodological, or interpretive; prefer the source closest to the original fact; preserve unresolvable disagreement.
6. **Gap and counterevidence pass.** Search for evidence against the emerging conclusion, missing populations or cases, more recent updates, retractions or corrections, and internal evidence that conflicts with public claims. Do not treat the first coherent story as final.
7. **Saturation check.** Stop when the predeclared condition is met: additional searching no longer changes the decision-relevant answer, remaining gaps are named, and the evidence standard is met. If the bound expires first, return the strongest supported answer and the exact unresolved question rather than widening scope silently.

**Source quality questions:** Is this the original source? Is it current enough for the claim? Does it measure or state what the draft will claim? Are definitions and populations aligned? Does the source have a reason to overstate? Can the reader inspect it?

**Citation discipline:** Cite the page that supports the claim, not a search-results page. Place citations near the supported claim. Quote sparingly. Do not cite a source for a broader claim than it supports. Label inaccessible or unverified sources.

---

## 4. Evidence-First Analysis

Test the claims that will carry the deliverable before writing polished prose. A convincing sentence is not evidence.

**Core rule:** Do not mark a claim as supported until the cited evidence directly supports it. If the reasoning extends beyond the source, mark it as inference.

**Procedure, per claim:**

1. **State the claim.** One specific, falsifiable claim at a time. Weak: "Curiosity programs improve culture and performance." Stronger: "In the cited study population, the program was associated with a measured increase in the named engagement score during the reported period."
2. **Define the support test.** What would make the claim acceptable: direct statement or measurement, matching population and context, matching time range, appropriate comparison or baseline, current enough for the decision.
3. **Attach evidence.** Link to source IDs from the source ledger. Read the relevant passage or data, not only a summary or snippet.
4. **Seek disconfirmation.** Look for evidence that weakens, narrows, or contradicts the claim. Record it rather than hiding it.
5. **Assign status** (per `assets/claim-ledger-template.md`): `supported` (evidence directly supports), `inferred` (evidence supports premises, conclusion is analytical), `disputed` (credible evidence conflicts), `unresolved` (support missing or too weak).
6. **Assign confidence:** high, medium, or low, based on source quality, independence, directness, consistency, and freshness. Explain the reason. Do not convert subjective confidence into a fabricated percentage.
7. **Decide what the draft may say.** Supported claims may be stated as facts with citations. Inferred claims must be labeled as analysis. Disputed claims must show the disagreement. Unresolved claims must be removed, narrowed, or presented as open questions.

**Recommendation test:** For each recommendation record the decision it serves, the evidence it depends on, the assumptions connecting evidence to action, plausible alternatives, conditions that would change it, and known costs, risks, or missing information. Recommendations are judgments — cite their factual premises and state the judgment plainly.

**Common failures:** citation laundering (citing a secondary page that repeats an unsupported claim); source stretching (narrow finding → universal statement); correlation inflation (causal language for correlational evidence); date collapse (combining evidence from different periods); definition drift (treating similar terms as identical); confidence theater (precise numbers for subjective certainty).

**Verification before drafting:** every key claim has a status; every supported/inferred/disputed claim links to known source IDs; counterevidence is recorded; unresolved claims are not presented as settled.

---

## 5. Drafting From Evidence

Build the deliverable from verified claims rather than writing first and searching for citations afterward.

**Preconditions:** a clear brief, a source ledger, a claim ledger (or explicit claim assessment), a known audience and decision. If important claims remain unresolved, narrow the draft or return to research.

**Procedure:**

1. **Choose the decision structure.** Organize around what the reader must understand or decide, not the order sources were found. Default: decision or answer → most important evidence → reasoning and alternatives → risks, conflicts, limits → recommended action. Follow the user's required template when one exists.
2. **Draft from supported claims.** Factual statements with nearby citations; wording no broader than the evidence.
3. **Label analysis.** Signal interpretation explicitly ("This suggests…", "I infer…", "Taken together, the evidence points to…"). Do not hide inference behind a citation.
4. **State recommendations as judgments.** Name the recommendation, the evidence behind it, the assumptions making it reasonable, and what would change the decision.
5. **Preserve conflicts and limits.** Include material disagreement, missing data, stale evidence, inaccessible sources, or scope limits where they affect the answer — not buried in a generic disclaimer.
6. **Cite precisely.** Each citation near the claim it supports. Prefer direct links to primary or authoritative sources. Multiple citations only when each adds independent support. Never attach one citation to a paragraph of unrelated claims. Check quotations preserve meaning.
7. **Write for the audience.** Reader's language, required detail, outcome first. Keep methods and source notes available without making the main document read like a research diary.

**Quality check — read the draft once per lens:** brief (answers the requested question?), evidence (every factual claim traces to support?), reasoning (assumptions and alternatives visible?), reader (can the intended user act on it?), language (plain, specific, free of inflated claims?).

---

## 6. Executing Knowledge-Work Plans

Carry out an approved plan without losing its constraints or drifting into a different task.

**Procedure:**

1. **Load and review the plan.** Before acting, check for contradictory tasks or constraints, missing inputs, unclear source ownership, unverifiable tasks, and approval boundaries. Resolve blockers before executing; fix small defects inline only when the intended result is clear and scope is unchanged.
2. **Establish progress state.** For long work, maintain a durable progress record beside the plan: completed tasks, outputs, checks, open findings, next task. After a resumed session, trust the artifacts over recalled conversation history.
3. **Execute a coherent stage.** For each task: load the named inputs; perform only the planned actions; create the planned output; run the task's verification check; record the result and any limitation. Do not mark a task complete because effort was spent — complete means the verification surface passed.
4. **Use conditional phases.** Deep research → §3; claim testing → §4; sourced drafting → §5; independent strands → §7; draft review → §8.
5. **Re-check the plan after new evidence.** Pause and revise when a source of truth contradicts a core assumption, required evidence is unavailable, the user's decision changes, a task no longer answers the brief, or the work would exceed approved scope or permissions. Explain the new fact and its effect; do not continue mechanically with an invalid plan.
6. **Complete the plan.** Review brief coverage and open limitations; then run Verification (§10), and only after it passes, Finishing (§11).

**Stop and ask for direction when:** required authority is missing; a meaningful user preference cannot be inferred; sources are inaccessible with no safe substitute; repeated failed attempts show the plan or evidence model is wrong; completion would require a materially different deliverable.

---

## 7. Dispatching Parallel Research

Use subagents to shorten independent research work without creating duplicated searches, inconsistent evidence standards, or conflicting edits.

**Permission gate:** use only when subagents are available, user/developer/platform instructions permit delegation, at least two research strands are independent, and agents will not edit the same files or shared state concurrently. If any condition fails, execute sequentially.

**Independence test:** strands are independent when each can be understood and completed from its own brief and sources, and one strand's result does not determine how another must research. Good split: current market size / competitor offerings / relevant regulation. Poor split: find sources → interpret those same sources → draft from those same interpretations (that is sequential).

**Procedure:**

1. **Define shared standards** before dispatching. Every agent receives: overall decision, its exact research question, scope and exclusions, source hierarchy, freshness requirement, required source and claim ledger fields, citation rules, output location or report contract, stop conditions.
2. **Create focused strands.** One problem domain per agent; remove overlap explicitly; state what the agent must return and must not do.
3. **Dispatch concurrently.** Only strands that can run without shared writes; use separate artifact paths or return reports to the coordinator.
4. **Review each return.** Was the question answered? Check source quality and freshness; confirm claims link to sources; note contradictions, missing evidence, uncertainty; reject outputs that rely on search snippets or unsupported summaries.
5. **Integrate.** The coordinator owns synthesis: merge source and claim ledgers, resolve duplicate source IDs, compare definitions and date ranges, surface cross-strand conflicts. Do not ask a synthesis agent to hide contradictions for a clean narrative.
6. **Verify the combined result.** Run the same evidence and brief checks as single-agent work. Parallel execution changes speed, not the quality standard.

**Agent brief shape:** Research question / Why it matters / Scope / Excluded / Source hierarchy / Freshness rule / Required artifacts / Verification / Stop conditions / Return format.

---

## 8. Reviewing Knowledge Work

Review the deliverable against what it was supposed to do and whether its evidence and reasoning earn the conclusions. Review the artifacts, not the creator's explanation of intent.

**Review package (smallest complete):** work brief or requirements, deliverable, source ledger, claim ledger, named constraints or template, relevant verification results.

**Stage 1 — Brief compliance.** Check each requirement separately: required question answered; intended audience served; scope respected; required sources used; requested format and length followed; success criteria met; no unapproved expansion. Mark each pass, fail, or cannot verify. Missing requirements block approval even when the prose is strong.

**Stage 2 — Evidence and quality:**

- *Sources:* are important sources primary or authoritative where available? Current enough? Are discovery sources being used as final evidence? Are quoted or paraphrased passages represented accurately?
- *Claims:* does each citation support the nearby claim? Is any claim broader or more causal than the evidence? Are inference, dispute, and uncertainty labeled? Are unresolved claims presented as settled?
- *Reasoning:* are assumptions visible? Were credible alternatives considered? Is counterevidence addressed? Do recommendations follow from the decision and evidence? What evidence would change the conclusion?
- *Communication:* does the answer lead with the outcome? Is the structure useful? Is the language plain and precise? Are limits placed where they affect the answer?

**Finding levels:** Critical (could materially mislead, violate the brief, expose sensitive information, or support a harmful decision); Important (required element, key source, claim, or reasoning step missing or weak enough to affect the conclusion); Minor (clarity, structure, consistency, presentation — does not change the conclusion).

**Output:** Use `assets/review-template.md`. Each finding: location, problem, why it matters, evidence, smallest useful correction. End with one verdict: Approved / Approved with noted limits / Revision required. Do not approve while Critical or Important findings remain open.

---

## 9. Receiving Work Review

Treat feedback as claims to evaluate, not commands to accept automatically. Correct feedback improves the work; incorrect or conflicting feedback should be challenged with evidence.

**Procedure:**

1. **Read everything first.** Complete review before editing. Group related findings; identify dependencies or contradictions. Do not revise item by item while later feedback may change interpretation.
2. **Restate each finding.** What the reviewer says is wrong or missing, where it applies, which brief requirement or quality standard it invokes, whether the requested change is explicit or inferred.
3. **Verify against the work.** Inspect the cited section, sources, claim ledger, brief. Classify: correct, correct in part, unclear, incorrect, or in conflict with another binding instruction. Do not rely on the reviewer's confidence alone.
4. **Resolve unclear or conflicting feedback.** Ask for clarification when the answer changes the result and cannot be discovered. If feedback conflicts with the brief or a user instruction, present the conflict and ask which governs.
5. **Prioritize:** factual errors and unsupported claims; brief or policy violations; reasoning gaps affecting conclusions; missing context or counterevidence; structure and clarity; minor presentation issues.
6. **Revise in small batches.** Smallest change that resolves the finding without weakening correct material. Re-check linked claims and citations when one change affects several sections.
7. **Record the disposition** for consequential reviews: accepted and fixed / partially accepted and fixed / rejected with evidence / needs user decision / deferred with reason.
8. **Re-review.** Run the relevant checks again; do not assume a revision solved the issue or left the rest untouched.

**Push back when a suggestion would:** introduce an unsupported claim; hide material uncertainty or counterevidence; replace a primary source with a weaker one; violate approved scope or format; add work that does not serve the decision; conflict with a higher-priority instruction. Use concise reasoning and point to the evidence. If your pushback is shown to be wrong, correct it plainly and revise.

---

## 10. Verification Before Delivery

Require evidence for completion claims. A polished artifact and a previous review are not fresh verification.

**Core rule:** Do not say the work is complete, accurate, ready, or verified until the relevant checks have just been run and their results inspected.

**Gate:** identify what would prove the claim → run the complete fresh check → read the result → compare with the brief → fix failures or report actual status → state completion only when the evidence supports it.

**Checklist:**

- *Brief:* every required question answered; scope and exclusions respected; audience and decision served; required format, length, template followed.
- *Evidence:* every key factual claim has support; citations open and support the nearby claim; quotations and numbers match sources; primary sources used where required and available; counterevidence and conflicts represented.
- *Analysis:* fact, inference, dispute, and recommendation distinguished; assumptions visible; recommendations follow from evidence and decision; unresolved claims narrowed, labeled, or removed.
- *Freshness:* time-sensitive facts checked live; publication and update dates inspected; memory or prior notes not treated as confirmed current state.
- *Calculations and data:* rerun with a deterministic tool; units, denominators, date ranges, populations match; tables and charts agree with underlying data.
- *Safety and permissions:* confidential or personal information handled within scope; no external message, publication, or destructive action without authority; domain-specific review used when required.
- *Artifact:* file exists in the correct output location; filename and version follow the rules; file opens, renders, or parses correctly; no placeholders remain; evidence package present when required.

**File-based check:**

```bash
python3 bin/verify_research_bundle.py /path/to/bundle --profile deliverable
```

This structural check does not replace opening sources and inspecting claim support.

**Failed verification:** do not claim completion; state the failing check and evidence; fix it when within scope; re-run the complete affected check; record any unresolved limitation. State what was verified and name the evidence briefly — avoid claims broader than the checks that ran.

---

## 11. Finishing a Deliverable

Turn verified work into a clear, reusable handoff. Finishing is not only sending the main file — it includes the evidence, limits, version, and next action.

**Preconditions:** §10 Verification has run with fresh evidence. If not, return to verification.

**Procedure:**

1. **Confirm the final artifact.** Name, version, exact path or destination, format, intended user, verification performed. Do not silently overwrite an earlier version.
2. **Package supporting evidence.** When the task warrants it, preserve: work brief, research plan, source ledger, claim ledger, review and finding dispositions, verification results. Keep sensitive material only in approved locations.
3. **Record known limits.** Unresolved evidence gaps, stale-data risks, inaccessible sources, disputed claims, material assumptions. Not a generic disclaimer.
4. **Prepare the delivery note** using `assets/delivery-note-template.md`. Keep it short and specific.
5. **Present the handoff.** Lead with the outcome and provide: the exact artifact link or path; what was verified; important limitations; one recommended next action when useful. Do not make the user reconstruct the result from progress updates.
6. **Handle external actions safely.** Sending, publishing, sharing, moving, or deleting may require separate authority. If authorized, perform only that action and verify it. Otherwise, prepare the artifact and stop at handoff.
7. **Preserve recovery state.** For long or reusable work, keep the evidence package and progress record discoverable — a future session should understand what was delivered and why without this conversation.

**Completion conditions:** verified artifact exists in the correct location; version unambiguous; required supporting evidence preserved; known limits recorded; user receives a self-contained handoff. Do not claim publication, delivery to another person, or archival unless that external state was verified.
