---
name: "knowledge-work-superpowers"
description: "Run substantial non-coding knowledge work end to end: framing, planning, systematic research, evidence-first analysis, sourced drafting, staged execution, parallel research strands, review, feedback handling, fresh verification, and delivery handoff. Use for research reports, memos, comparisons, recommendations, and decision briefs, or anything multi-source, high-stakes, or expected to guide a decision. Skip for simple lookups or one-step answers, and for grill me, interview me, or pressure-test this decision requests, which belong to strategy-room."
metadata: { "includeInPrompt": true }
---

# Knowledge Work Superpowers

Route substantial knowledge work (research, analysis, planning, drafting, review, verification, handoff) through the smallest set of phases that protects quality. Phase procedures live in the `subagents/<name>.md` briefs; templates in `assets/`; the bundle checker in `bin/verify_research_bundle.py`.

The work is finished when the requested deliverable exists at its agreed location, and every material claim in it traces to a source that supports it, or is labeled inferred, disputed, or unresolved. The fresh checks must have been run. A source list, an outline, or a plan is not the report.

## Start here

1. **Name the deliverable and the decision it serves.** Take the audience, format, and location from the request. If they are all there, record the frame and proceed; do not ask for approval of a frame the user already gave.
2. **Choose fast path or full phases.** Use the fast path for a single lookup, a simple transformation, or a low-stakes answer: answer with the source inline. Use full phases for anything multi-source, decision-guiding, current, disputed, or costly if wrong.
3. **Inventory sources before researching.** Open every supplied file. List each source with an ID, and mark any listed source that is missing, unreadable, or out of bounds (for example "no web access") as `not accessed`, with the reason. Do not cite it.
4. **Run the phases the task needs** (router below), reading each phase's brief in `subagents/<name>.md` first. Skip a phase only when its output already exists; state the reason in one line.
5. **Verify fresh before delivery.** Recompute any calculation with a deterministic tool, open each cited source against its claim, and run the bundle checker when the output is a file bundle.

## Phase router

Dispatch each phase to its brief in `subagents/`:

1. Unclear outcome, audience, scope, or success criteria → `subagents/frame.md`
2. Approved brief or clear multi-step requirements → `subagents/plan.md`
3. Deep, current, disputed, or multi-source research → `subagents/research-systematic.md`
4. Important claims or recommendations need support → `subagents/analyze-claims.md`
5. A sourced draft must be written → `subagents/draft.md`
6. A written plan must be carried out → executing plans (below; no separate brief)
7. Two or more independent research strands, and subagents are permitted → `subagents/parallel-research.md`
8. A draft or deliverable needs quality review → `subagents/review.md`
9. Feedback has arrived → `subagents/receive-review.md`
10. About to call the work complete → `subagents/verify.md` (fresh checks)
11. Verified work needs packaging → `subagents/finish.md` (delivery note)

Default sequence for a new substantial task: frame → plan → research-systematic → analyze-claims → draft → review → verify → finish. This skill is not a substitute for domain-specific legal, medical, financial, or compliance review.

### Executing plans (folded phase, no separate brief)

Load and review the plan; maintain a durable progress record; execute one coherent stage at a time, each with its verification check; re-check the plan after new evidence appears. Stop and ask when authority is missing, a preference cannot be inferred, sources are inaccessible, repeated failures show the plan is wrong, or completion would need a materially different deliverable. Dispatch stages by conditional subagent: deep research → `subagents/research-systematic.md`; claim testing → `subagents/analyze-claims.md`; sourced drafting → `subagents/draft.md`; independent strands → `subagents/parallel-research.md`; draft review → `subagents/review.md`. Complete the plan by running `subagents/verify.md`, then `subagents/finish.md`.

## Trigger boundary (use the sibling skill, not this one)

- Quick adversarial interview about a plan or decision → `matt-pocock-knowledge-work` grill subagent
- Structured decision pressure-test ("grill me", "pressure-test this decision") → `strategy-room`
- Quick single investigation against one source → `matt-pocock-knowledge-work` research subagent
- Rigorous multi-source research with source and claim ledgers → this skill's `subagents/research-systematic.md`
- Conversation handoff to another agent → `matt-pocock-knowledge-work` handoff subagent
- Verified deliverable packaging with delivery note → this skill's `subagents/finish.md`

## Worked example (illustrative, synthetic)

Request: "Using the three attached files, recommend which of two community grant programs our small nonprofit should apply to. One-page memo for the board."

- Frame: deliverable is a one-page memo for the board; the decision is which program to apply to; the sources are the three files only.
- Inventory: S1 is Program A's 2025 guidelines, S2 is Program B's 2023 guidelines, and S3 is Program B's 2025 update. S3 supersedes S2 on eligibility.
- Judgment: S2 requires at least two years of operation, and S3 raises that to three years. The nonprofit is two and a half years old. Record "The nonprofit is not yet eligible for Program B" as `supported` (S3). Keep S2 in the ledger as superseded, and do not cite it for the conclusion. Missing this would recommend a grant the nonprofit cannot receive.
- Draft: recommend Program A. Cite S1 for the award size and deadline, and state that Program B becomes an option after the third anniversary (S3).
- Verify: open S1 and S3 again beside each cited sentence; recompute the deadline countdown with a date tool.

A wrong version would average the two Program B documents, cite the 2023 rule because it appeared first, or state an award amount from memory.

## When something goes wrong

| Symptom | Likely cause | Next move | Stop when |
|---|---|---|---|
| A listed source is missing, paywalled, or out of bounds | Access or scope limit | Mark it `not accessed` in the source ledger with the reason; mark claims that depend on it `unresolved` | always; never cite an unopened source |
| Two sources disagree | Different dates or definitions | Record both; prefer the most recent authoritative source for that specific claim; mark `disputed` if unresolved | the conflict cannot change the recommendation, or it is shown to the user |
| A recomputed number differs from the draft | Arithmetic, units, or a missed condition (add-on, discount, threshold) | Fix the draft from the recomputation; recheck every figure derived from it | the second recomputation agrees |
| `verify_research_bundle.py` fails | Missing file, placeholder text, bad table row, unknown source ID | Fix the named finding and rerun | the second run fails; report the findings verbatim |
| The request grows mid-task | Scope drift | Finish the agreed deliverable; list the new question as a next action | the user explicitly re-scopes |
| A step needs a logged-in or rendered page | Live-browser work | Main assistant: run the host's live-browser task with the user's confirmation. Subagent: return the exact step to the parent. Otherwise mark the claim `unresolved: needs live browser` | the browser task is unavailable |

## Completion

- **Delivered:** the deliverable at its location, the evidence package (brief, plan, source and claim ledgers, review, verification results), known limitations, and a delivery note with what was delivered, what was verified, the limits, and one next action.
- **Delivered with limits:** as above, with named gaps (for example an inaccessible source) stated in the deliverable and the delivery note, not only in the ledger.
- **Blocked:** the missing input or access, its owner, and every part completed without it.

## Host capabilities

- Internal facts (email, calendar, messages, device galleries): the matching connected skill (`~/workspace/skills/` or `/opt/hatch/skills/`); load its `SKILL.md` first.
- Working documents in `~/workspace/`: file tools (`muse.read`, `muse.write`, `muse.edit`).
- Public current facts: `browser.search` and `browser.open`, unless the request forbids web access. Never treat training memory as current.
- Logged-in sites, forms, purchases, multi-step web interactions: see the live-browser row in the recovery table.
- Calculations and data: rerun with a deterministic tool (shell, `python3`) and check units, denominators, and date ranges.
- Scheduled or event-driven follow-ups: the host's `cron` or `hooks`, only when the user asks for one. If either is unavailable at run time, say so rather than implying monitoring.
- Parallel research strands: subagents when permitted, each with its own artifact path so no two write the same ledger.

## Operating rules

1. Do not present inference as sourced fact, or cite a source that does not support the nearby claim.
2. Do not claim completion without fresh verification.
3. Do not expand scope silently.
4. Do not use subagents when user or platform instructions prohibit it.
5. Preserve progress in files, not chat history. After a resumed session, inspect those artifacts before repeating work. For long research, keep `research-handoff.md` in the output root: source ledger, open questions and conflicts, boundaries and stop condition, next action, verification state.
6. Ask the user for personal input (writing samples, business details, audience facts, credentials, permissions). Do not invent user-specific data.
7. External actions (sending, publishing, sharing, moving, deleting) need separate authority. Without it, prepare the artifact and stop at handoff.

## File-based verification

With `SKILL=~/workspace/skills/knowledge-work-superpowers` (or this skill's actual folder). The self-test runs from any directory and writes only to a system temporary folder:

```bash
python3 "$SKILL/bin/verify_research_bundle.py" --self-test
```

For a bundle: `python3 "$SKILL/bin/verify_research_bundle.py" BUNDLE_DIR --profile research` (brief, plan, ledgers) or `--profile deliverable` (adds `deliverable.md`, `review.md`, `delivery-note.md`). Expected filenames and table columns follow the templates in `assets/`. The checker tests structure and traceability; it does not replace opening sources and checking claim support.
