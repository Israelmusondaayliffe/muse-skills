---
name: guide-production-studio
description: Build source-grounded practical guides: manuals, how-to pages, prompt guides, reference libraries. Owns source lineage, reader-first structure, real evidence and examples, visual teaching where judgment is visual, and independent acceptance review before anything scales or publishes. Use when a guide must teach someone to do real work, not when only prose polish is needed.
metadata: { "includeInPrompt": true }
---

# Guide Production Studio

## Purpose

Own the teaching product, not merely its prose. A useful guide lets a reader understand the idea, try the work, recognize failure, and decide what to do next without hidden context. This skill runs practical guide work through five phases: source mapping, architecture, building, independent acceptance review, and a human gate before publication or scale.

## When to use

Use when the request involves source-grounded practical guides where context, evidence, examples, visual teaching, and reader usefulness matter: manuals, how-to pages, prompt guides, reference libraries, workflow documentation.

Route by intent:

- **Map sources / decide what can be taught or named publicly** → Phase 1, source mapper.
- **Choose one page, layered sections, or child pages** → Phase 2, architect.
- **Write or rebuild an approved guide** → Phase 3, builder.
- **Review a candidate as a cold reader** → Phase 4, acceptance review.
- **Full workflow** → Phase 1 → 2 → 3 → 4 → human gate, then scale.

Do not use for simple copyediting (use `writing-quality`), workshops, research-only work, PDF conversion, publication-only requests, or when the user says they do not want a guide.

## Workflow

Use the smallest phase that completes the current request. Do not start a later phase before its inputs exist. Keep all working records (contract, review record, notes) in a private working directory such as `~/workspace/guide-production/<guide-id>/`; they are internal, never part of the published guide.

### Phase 1 — Source map

Load `references/provenance-policy.md` before classifying anything.

1. Read the originals first. When a summary points to an available original source, inspect the original before deciding what the guide may say.
2. Classify every source: public-attributable, public-reference, private-transform-only, user-owned, or forbidden.
3. Separate three questions: what may inform the guide, what may appear in it, what must be attributed.
4. Record evidence status: verified, user-supplied, observed, unrun, or unknown. Never silently promote weaker evidence to verified.
5. Preserve permitted public lineage (source names, finished works, released docs, production history) that helps the reader judge the method.
6. Protect private machinery: skill names, private paths and identifiers, internal prompts and routing notes, memory contents, device names, credentials, implementation details — unless explicitly approved for publication.
7. Identify evidence gaps. Stop if a result claim lacks evidence or a necessary example would have to be invented.
8. Fill the guide contract (copy `assets/guide-contract.template.json`) and validate it:

```text
python3 ~/workspace/skills/guide-production-studio/scripts/validate_guide_contract.py <contract>.json
```

**Stop before design** if provenance and private implementation cannot be separated safely, rights are unclear for a required example or visual, only fiction stands in for available real proof, current platform behavior has no approved current source, or a claimed result is unrun, unknown, or unsupported.

### Phase 2 — Architect

Requires a validated contract. Load `references/guide-architecture.md`; also `references/visual-evidence.md` for visual or spatial subjects.

1. Name the reader's job — the action they came to complete, not the subject label.
2. Name the reader's starting point: what a newcomer probably knows and what an expert still needs.
3. Choose the smallest useful shape: single page, layered page, or parent with child pages.
4. Design a start path: a first-time reader understands the purpose and attempts one useful action without reading everything.
5. Design a return path: an expert finds prompts, parameters, decision rules, examples, troubleshooting quickly.
6. Make every component earn its place (reader problem, action enabled, supporting evidence, why it belongs, what breaks if removed). Remove anything included only because another guide had it.
7. Place a completed example before any blank template; omit templates when copying is not genuinely useful.
8. Limit duplication: parent pages orient and route, child pages teach, downloads support reuse.
9. Record mode, pages, components, visual requirements, and the scale gate in the contract; re-validate.

**Stop before writing** if a component has no named reader problem, the structure is copied from another guide without justification, a child page merely repeats its parent, a blank form is the main teaching experience, or a visual subject has no plan for visual evidence.

### Phase 3 — Build

Requires a validated contract with accepted architecture. Load the references named by the contract.

Build order:

1. Open with the reader's job: what the guide helps them do, when it is useful, what they need before starting.
2. Define unfamiliar terms at first use, in plain language without making the subject shallow.
3. Give a short mental model of the whole shape before detailed steps.
4. One action per step: input, action, expected result, and why the step matters when the reason changes judgment.
5. Use real, rights-safe, tested examples with preserved public provenance. Label run status at first use. Planning-only examples are allowed only when no suitable real example exists or the guide teaches planning.
6. Label limits where they occur: planning-only, unrun, version-sensitive, practitioner, user-supplied.
7. Make prompts usable: when to use it, what to provide, what it returns, what it cannot decide, how to judge the result.
8. Teach failure recognition: visible symptoms → likely causes → protected elements → smallest next action → stop conditions.
9. Teach visually when the judgment is visual: comparisons, crops, frames, diagrams, annotated examples the reader can inspect.
10. Serve returning experts: exact prompts, settings, decision rules, sources, reference tables easy to find.
11. Strip internal language from public copy: no skill names, paths, validators, routing notes, subagent or review commentary.

Writing standard: ELI5 clarity for an intelligent adult; short direct sentences; no course/lesson/module framing unless asked; no fake first-person experience; opinionated craft recommendations only when evidence supports them.

Checks before handoff:

```text
python3 ~/workspace/skills/guide-production-studio/scripts/validate_public_guide.py <guide>.md
```

Fix every finding. Then hand the candidate to Phase 4 for independent review. Do not call it approved, publish it, or launch sibling guides.

### Phase 4 — Independent acceptance review

The reviewer must be a genuinely fresh read, not the producer's own turn. Run it as a separate subagent with only the contract, candidate, and sources — no production notes. If no separate session is possible, do the review after a real break and say so in the record. Never self-approve.

Load `references/human-acceptance-rubric.md`; also the visual-evidence reference for visual subjects.

1. Read cold. Inspect the candidate before any internal rationale; record the first point where purpose, vocabulary, or next action becomes unclear.
2. Try the path: follow the quick start or first useful action using only what the guide provides.
3. Trace claims: factual behavior, examples, provenance, run status, limitations against the contract and sources.
4. Inspect structure and visual teaching: unearned components, repetition, missing inspectable evidence.
5. Separate problem classes: mark privacy and unsupported claims as critical; context, usefulness, examples, structure, voice as qualitative gates.
6. Refuse false resolution: a limitation is not resolved merely because it is disclosed.
7. Populate the review record (copy `assets/guide-review.template.json`) with evidence for every gate:

```text
python3 ~/workspace/skills/guide-production-studio/scripts/validate_guide_review.py <review>.json
```

Verdicts: `blocked` (required source, rights, evidence, or independence missing), `rejected` (a gate fails), `ready_for_human_review` (every gate passes). Never set `human_approved` — only the user can approve after reviewing the evidence.

## Gates and stopping rules (read before starting)

- Inspect actual sources; summaries cannot replace an available original when lineage matters.
- Separate privacy from provenance: hide private machinery, keep legitimate public origin and attribution.
- Choose architecture from the reader's job, never from a standard template.
- Build one benchmark before any scale. Bulk production stays blocked until the benchmark is human-approved.
- Require real evidence or label the material honestly. Never replace available proof with fiction.
- The producer revises; only an independent reviewer (or the user) approves.
- Stop before publication. Publication needs the user's explicit approval and is handled outside this skill.

## Publication and scale

Guide production is ready for human review only when the contract validates, every claim has an approved source or a visible limitation, every component solves a named reader problem, examples carry accurate run status, visual subjects have usable evidence or are labeled reference-only, the review record validates at `ready_for_human_review`, and publication plus bulk production remain blocked.

Only `human_approved` permits baseline pinning or scale — and that requires the user's explicit confirmation plus a completed cold-reader observation before bulk production.

## Companion skills

- Use `knowledge-work-superpowers` when source collection or evidence synthesis is substantial.
- Use `writing-quality` only after the guide's teaching, evidence, and structure pass review.
- Use connected publishing capabilities only after the user's explicit publication approval.

## Operating rules

1. Never invent examples, results, workflow history, or platform behavior. Label everything you did not run.
2. Never publish, share, or export a guide without the user's explicit approval for a specific destination.
3. Never approve your own guide. Independence means a separate read with separate context.
4. Keep contract and review records as JSON in the private working directory; re-validate after every edit.
5. Ask the user when the work needs personal input: their sources, methods, approved examples, rights decisions, the human owner, and the publication destination.
6. Contracts must leave `publication.authorized` as `false` and `bulk_scale_allowed` as `false` until the user approves.
