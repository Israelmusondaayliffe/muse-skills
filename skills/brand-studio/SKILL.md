---
name: "brand_studio"
description: "Develop brand strategy, briefs, identity systems and brand reviews with current brand context and independent creative judgment. Use when the user asks for branding, positioning, a brand brief, a logo system, identity guidelines, identity boards, or a brand consistency review."
---

# Brand Studio

## Purpose

Produce brand strategy, briefs, identity systems and reviews from the user's current supplied or confirmed material, with proposed choices and confirmed decisions kept visibly distinct.

## Start Here

Read `references/brand-context.md` before any phase. Work from current supplied or confirmed material, defaulting to the user's current brand when none is named; an explicitly named alternate brand is a valid target.

Choose **one primary phase** by the requested deliverable. Do not run all four; a specialist completes independently without requiring another phase's document first. For a request spanning deliverables, agree on the smallest useful scope first.

| Requested result | Phase | Supporting material |
|---|---|---|
| Decide audience, positioning, promise, personality, or brand direction | **Strategy** | `references/identity-methods.md` — Brand strategy first |
| Turn current decisions into a usable production brief | **Brief** | `references/brief-controls.md`, `assets/brand-brief-template.json` |
| Develop symbols, logo concepts, color, typography, applications, or identity boards | **Identity** | `references/identity-methods.md`, `assets/board-prompt-template.md` |
| Inspect brand consistency or identify repairs | **Review** | `references/review-controls.md`, `assets/brand-review-template.json` |

## Workflow

### Strategy

1. Establish the decision and evidence: what the brand does, who it serves, what people should understand or feel, and what is already confirmed. Use existing user context before asking questions.
2. Examine the category, audience needs, product function, emotional promise, cultural position, trust expectations and differentiating behavior. Mark proposed claims and unsupported assumptions. Use the category-to-symbol table in `references/identity-methods.md` when translating meaning into visual possibilities.
3. Develop the requested number of directions. When the direction is open, offer a small set of materially different positions, each with consequences for voice, imagery, symbols and experience. Do not fabricate customer research or competitors' behavior.
4. Recommend a direction with reasons tied to the user's purpose and evidence. Preserve meaningful tensions (e.g. experimental expression with institutional trust) instead of flattening them into generic adjectives.
5. Deliver the strategy or decision comparison: audience, positioning, promise, supporting evidence, personality, meaningful difference, visual implications and unresolved decisions. Match the requested length and format.

A short strategy question gets a short answer. Research only when a live fact could change the decision. Keep a proposed strategy visibly provisional until the user chooses it.

### Brief

1. Identify the brand, audience, intended response, positioning, deliverables, existing assets and constraints.
2. Translate each relevant attribute into visible choices using `references/brief-controls.md` (e.g. precision affects spacing, typography, grid and image selection).
3. State visual principles, color and type boundaries, permitted variation, likely drift to avoid, source references and the authority of each decision. Split genuinely different audiences or formats into named tracks.
4. Deliver a model-neutral brief that another person or tool can use independently. Leave unsettled positioning labeled proposed or unknown; do not manufacture approval to fill a field.
5. If JSON is requested, use `assets/brand-brief-template.json` and validate it with `python3 bin/validate_artifact.py ARTIFACT.json --schema assets/brand-brief-schema.json` (run from this skill's directory). Validation checks structure, not approval or taste.

Finish when deliverables and constraints are clear, their source is traceable, and consequential gaps are visible. A production issue that changes positioning is a decision for the user.

### Identity

1. Establish what the identity must express. Use the known category, audience, promise and core metaphor; label creative hypotheses when these are open. Do not impose a strategy interview on a settled brief.
2. Read only the needed sections of `references/identity-methods.md`: strategy and symbol logic for a new concept; logo methods for a mark; color/type/application sections for a system; board composition and visual modes only for a board or presentation.
3. Develop meaningful symbol concepts through monogram, product action, metaphor fusion, negative space or construction geometry. Explain the connection to the brand. Combine at most two methods.
4. Build a system around the chosen or proposed concept: logo variants, proportions and spacing, typography hierarchy, color roles, imagery/materials, layout rhythm and the requested applications. Preserve supplied marks, exact wording and confirmed colors.
5. If a board is requested, choose layout, density, light/dark treatment and panel sequence for this brand. Use `assets/board-prompt-template.md` only for a board brief, adapting its open fields to the chosen direction. Presets: 3×3 full system, 2×3 cinematic deck, 2×2 compact concept, 1×3 strip, 4×2 contact sheet, or custom.
6. Deliver the complete system, concepts or board brief in the requested form. Explain only consequential choices.

A logo concept is a proposed design, not proof of trademark uniqueness. If rendering is requested, generate with the image-generation (media) skill, inspect the result and state any mismatch. This skill works without any image generation access.

### Review

1. Identify the brief, reference assets, decisions and exact artifact set. Inspect available images and documents directly. For missing artifacts, state which checks remain untested.
2. Apply `references/review-controls.md` to each relevant artifact: message, composition, hierarchy, spacing, color roles, typography, imagery, logo treatment, text and requested exclusions. Distinguish allowed variation from drift against the governing principle.
3. Report material findings with artifact, visible evidence, affected requirement and the smallest useful repair. State when a conclusion is an aesthetic recommendation rather than a requirement failure.
4. Use pass, fail or blocked only for assistant assessment against the stated scope. Pass requires all mandatory checks tested with no material issue remaining. If authority is missing, offer explicitly provisional feedback and leave conformance blocked.
5. For structured output, use `assets/brand-review-template.json` and validate with `python3 bin/validate_artifact.py ARTIFACT.json --schema assets/brand-review-schema.json` (run from this skill's directory). A valid file is not visual proof.

Deliver the review without silently modifying the assets. The user owns final creative acceptance: record it only on their explicit decision, never infer it from a pass, download or selection.

## Output Contract

- Each phase returns a complete, self-contained result in the requested form.
- Proposed choices are labeled proposed; confirmed decisions are labeled confirmed with their source; gaps that affect the result are stated.
- JSON artifacts, when requested, validate against their schema in `assets/`.

## Operating Rules

1. **Evidence tiers.** Keep supplied facts, confirmed decisions, proposed directions and unresolved questions separate at all times. Never fabricate customer research, competitor behavior, color values, or approval.
2. **Acceptance discipline.** The user makes all final creative selections. Structural checks and proposed directions never establish acceptance. Save a preferred direction or replace confirmed guidance only after explicit selection.
3. **Ask, don't invent.** Do not invent user-specific details (business facts, writing samples, names, assets). Ask when the absence materially changes the result; otherwise proceed with labeled proposals.
4. **Review before finishing (checklist).** Before delivering: meaning/symbol consistency, legibility, color roles, application range and reference fidelity checked; evidence tiers intact; missing evidence stated; no silent asset changes (review); nothing in the result implies approval that was never given.
5. **Rendering.** If image rendering is requested, use the image-generation (media) skill; if unavailable for the session, deliver the board brief or board prompt text instead and say so. Brand work must remain usable without image tooling.
6. **Scope and handoff.** Generated artwork, publication and a saved preferred direction each require their own requested scope. Pass a self-contained brief (direction, source assets, open decisions) only if the user explicitly asks to collaborate with another tool.
7. **Parallel exploration.** When comparing materially different directions, spawning parallel subagents to develop each independently is allowed.
8. **Saving results.** If the user wants the brand decisions kept, save them into the relevant goal workspace or `~/workspace/your_files/`; do not scatter copies. Transient working notes stay out of the user's files.
