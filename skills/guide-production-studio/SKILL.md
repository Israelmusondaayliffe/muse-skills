---
name: guide-production-studio
description: Build source-grounded practical guides: manuals, how-to pages, prompt guides, reference libraries. Turns supplied sources into a complete guide a reader can follow, with source lineage, reader-first structure, real evidence and examples, visual teaching where judgment is visual, and an honest independent review before anything scales or publishes. Use when a guide must teach someone to do real work, not when only prose polish is needed.
metadata: { "includeInPrompt": true }
---

# Guide Production Studio

Own the teaching product, not merely its prose. A useful guide lets a reader understand the idea, try the work, recognize failure, and decide what to do next without hidden context.

When the user asks for a guide and supplies (or points to) its sources, the deliverable is the finished guide. The contract, review record, and gates support that guide. They never replace it.

## Start here

1. Name the deliverable: which guide, for which reader, in what format and location. "Write a guide from these notes" means a complete guide file, not a plan, outline, or source list.
2. Read every supplied source in full before deciding anything. If a summary points to an available original, read the original.
3. Pick the route:

| The request | Route | What comes back |
|---|---|---|
| Write, build, or rebuild a guide, with sources supplied or reachable | **Full build** (Phases 1 to 3 in one pass, then Phase 4) | Complete guide + short status note |
| "What can we teach or name publicly from these sources?" | **Source map** (Phase 1) | Validated contract + gap list |
| "How should this guide be structured?" | **Architect** (Phases 1 and 2) | Validated contract with architecture |
| "Review this guide" | **Acceptance review** (Phase 4) | Validated review record + findings |
| Many sibling guides at once | **Benchmark first** | One complete benchmark guide; siblings wait for the user's approval of it |

Ask the user only for facts the sources cannot supply and the guide cannot work without, such as who the reader is when nothing indicates it. Otherwise make the routine choices yourself and state them in the status note.

4. Create a new working folder, `~/workspace/guide-production/<guide-id>-<date>-<n>/`, for the contract, review record, check reports, and notes. If the name exists, pick the next `<n>`; never reuse or write over an existing working folder. These records stay private and never appear in the guide.

## Full build (the default for guide requests)

Run the phases below in one pass. Fill the contract as you go; it is a working checklist, not a gate to wait on. Deliver the guide in the same turn.

### Phase 1: Source map
Load `references/provenance-policy.md`.

1. Classify every source: public-attributable, public-reference, private-transform-only, user-owned, or forbidden.
2. Separate three questions: what may inform the guide, what may appear in it, and what must be attributed.
3. Record evidence status per claim or method: verified, user-supplied, observed, unrun, or unknown. Never promote weaker evidence to verified.
4. Keep permitted public lineage (source names, released docs, finished works) that helps the reader judge the method.
5. Keep private machinery out: skill names, private paths, internal prompts and routing notes, memory contents, device names, credentials.
6. List the gaps: claims without support, examples you would have to invent, visuals you lack.
7. Copy `assets/guide-contract.template.json` into the working folder, fill it, and run `python3 scripts/validate_guide_contract.py <contract>.json` from this skill's folder. Fix errors and re-run.

### Phase 2: Architect
Load `references/guide-architecture.md`, and `references/visual-evidence.md` for visual or spatial subjects.

1. Name the reader's job: the action they came to complete, not the topic label.
2. Name the starting point: what a newcomer knows and what an expert returns for.
3. Choose the smallest useful shape: single page, layered page, or parent with child pages.
4. Design a start path (one useful action without reading everything) and a return path (prompts, settings, rules, troubleshooting, easy to find).
5. Keep only components that solve a named reader problem. Put a completed example before any blank template.
6. Record mode, pages, and components in the contract and re-validate.

### Phase 3: Build
1. Open with the reader's job: what the guide helps them do, when it is useful, what they need first.
2. Define unfamiliar terms at first use, plainly, without making the subject shallow.
3. Give a short mental model of the whole shape before detailed steps.
4. One action per step: input, action, expected result, and why the step matters when the reason changes judgment.
5. Use real examples from the sources with their provenance. Label run status at first use. A planning-only example is allowed only when no suitable real one exists, and it says so.
6. For any code, command, or script the reader will run, follow `references/executable-examples.md`: a work-folder argument (unique folder when none is given), no overwrites during setup, output, or recovery, every promised report actually printed, and the exact executed code displayed. Read the example, then run `scripts/check_guide_example.py --workdir-arg` for the normal, collision (`--collide`, plus `--collide-at` for rename or move destinations), and malformed-input (`--seed`) cases. All must report `"valid": true`, and the collision case must show `collision_exercised: true`, before the guide is called usable. The helper is not a sandbox and observes only its own work folder; say so in the status note.
7. Label limits where they occur: planning-only, unrun, version-sensitive, user-supplied.
8. Make prompts usable: when to use it, what to provide, what it returns, what it cannot decide, how to judge the result.
9. Teach failure recognition: visible symptom, likely cause, what to protect, smallest next action, when to stop.
10. Teach visually when the judgment is visual. If the needed visual is not available, say what the reader should look for and mark the section reference-only.
11. Strip internal language: no skill names, paths, validators, routing notes, or review commentary.
12. Run `python3 scripts/validate_public_guide.py <guide>.md`. Fix every finding and re-run.

Writing standard: clear enough for an intelligent adult new to the subject; short direct sentences; no course or lesson framing unless asked; no invented first-person experience; opinionated recommendations only where evidence supports them.

### Handling gaps without abandoning the guide
Gaps shape the guide; they do not cancel it.

- A claim has no support: cut it, narrow it to what the source says, or label it unverified in the text. Do not invent support.
- No real example exists for a step: teach the step without one, or use a clearly labeled planning-only example.
- A visual is missing: describe what to inspect and mark the section reference-only.
- Current platform behavior has no current source: state the version or date the source describes.
- Privacy and provenance cannot be separated for a source: leave that source out, finish the guide from the rest, and name what was left out.

Stop the whole guide only when the sources cannot support its core job at all, for example when every method step would have to be invented. Then deliver what the sources do support (source map, architecture, the teachable sections) and name exactly what is missing.

## Phase 4: Independent acceptance review
Load `references/human-acceptance-rubric.md`.

The reviewer must read fresh, without the producer's notes. Spawn a subagent with only the contract, the candidate guide, and the sources. If no separate context is available, do not fill a review record: the validator rejects any record whose reviewer is the producer. Instead run the ten gates yourself as a producer self-check, fix what it finds, save it as `self-check.md` in the working folder, and report the review status as "independent review not run". Never self-approve.

1. Read cold and record the first point where purpose, vocabulary, or next action becomes unclear.
2. Try the first useful action using only the guide. For runnable examples, read the displayed code, copy it into a file, and run `scripts/check_guide_example.py --workdir-arg` for the normal, collision, and malformed-input cases. An overwrite, a missing promised report, or a collision that was not exercised is a critical failure.
3. Trace claims, examples, provenance, and run status against the contract and sources.
4. Check structure and visual teaching for unearned components and missing inspectable evidence.
5. Mark privacy exposure and unsupported claims as critical. A limitation is not resolved merely because it is disclosed.
6. Fill `assets/guide-review.template.json` with evidence for every gate and run `python3 scripts/validate_guide_review.py <review>.json`.

Verdicts: `blocked` (source, rights, evidence, or independence missing), `rejected` (a gate fails), `ready_for_human_review` (every gate passes). Only the user can set `human_approved`.

If the review rejects the guide, make one repair pass on the named findings, re-run the review once, then deliver with the remaining findings listed. Do not loop.

## Worked example (illustrative)

Request: "Here are my notes and two public docs on setting up a home backup with rsync. Write a guide my non-technical partner can follow."

- Route: Full build. Reader: a non-technical adult at home. Job: "make a working backup of the photos folder and check it worked."
- First actions: read the notes and both docs in full; mark the notes user-owned and the docs public-attributable; note that the notes mention a scheduled job the docs do not cover and that the user never recorded running.
- Shape: single page. Start path: one copy command with the expected output. Return path: a short table of flags and a troubleshooting table.
- Gap handling: the scheduled job is labeled "not yet tested" in the guide instead of being dropped or presented as working. The command's exact wording comes from the docs.
- Delivered: the complete guide file, a validated contract, a review record from a subagent reviewer (or, without one, a producer self-check and the status "independent review not run"), and a status note naming the untested scheduled job and the fact that no cold reader has tried it yet.

A wrong version would return only an outline, stop because the scheduled job lacks evidence, or claim the guide is approved.

## When something goes wrong

| Symptom | Likely cause | Next move | Stop and ask when |
|---|---|---|---|
| Contract validator lists errors | Missing or placeholder fields | Fill them from the sources; re-run | a required fact exists nowhere in the sources |
| `validate_public_guide.py` flags a path or internal term | Working language leaked into the guide | Rewrite that line for the reader; re-run | never |
| A step cannot be written without inventing behavior | Evidence gap | Label it, narrow it, or leave it out; keep building | the step is the guide's core job |
| A source can't be opened | Access or link failure | Try once more by another route (file path, browser); then build from the rest and name the missing source | the missing source is the only source |
| `check_guide_example.py` reports `no_overwrite: false` | The example writes to a fixed or existing name, or its recovery step skips the guard | Use the work-folder argument, exclusive creation, and a guarded recovery step; re-run all cases and re-paste the code |
| `collision_exercised: false`, or `--collide` refused | The example ignores the work-folder argument, or the destination name was not given | Add the work-folder argument; pass rename or move destinations with `--collide-at` | never count an unexercised collision as a pass | the second repair still fails; mark the example not safe to run |
| `check_guide_example.py` reports missing expected output or `displayed_code: false` | The code does not do what the text says, or the guide shows different code | Make the code print what the text promises, or change the text; paste the exact file that ran | never |
| Review validator reports errors | Reviewer is the producer, or a gate lacks evidence | Fix missing evidence, or fall back to the producer self-check; never edit the record just to pass | never |

## Completion

The task is complete when the user has:

- the full requested guide (or, for a narrower route, the requested contract or review);
- a validated contract, and a clean `validate_public_guide.py` run;
- for guides with runnable examples, valid `check_guide_example.py` reports for the normal, collision (`collision_exercised: true`), and malformed-input cases, or a stated reason a case does not apply, or the label "self-reported cases only"; the displayed code matches the executed file;
- a validated review record with its true status, or a producer self-check labeled "independent review not run";
- a short status note: choices you made, labeled limits, missing sources, review status, and what still needs a human (approval, cold-reader test, publication).

`ready_for_human_review` is not approval. Publication and bulk production stay blocked until the user approves a specific destination and the benchmark. A cold-reader observation with a real person comes before scale; a model's prediction does not replace it.

## Operating rules

1. Never invent examples, results, workflow history, or platform behavior. Label everything you did not run.
2. Never publish, share, or export a guide without the user's explicit approval for a specific destination.
3. Never approve your own guide. Independence means a separate read with separate context.
4. Keep contract and review records in the private working folder; re-validate after every edit. Contracts keep `publication.authorized` false and `bulk_scale_allowed` false.
5. Build one benchmark before any scale. Siblings wait for the user's approval of the benchmark.
6. Not for simple copyediting (use `writing-quality`), workshops, research-only work, PDF conversion, or publication-only requests. `python3 scripts/evaluate_guide_trigger.py --task "<request>"` gives a quick routing check when unsure.

## Companion skills

- `knowledge-work-superpowers` when source collection or evidence synthesis is substantial.
- `writing-quality` for a final prose pass only after the guide's teaching, evidence, and structure pass review.
- Connected publishing capabilities only after explicit publication approval.
