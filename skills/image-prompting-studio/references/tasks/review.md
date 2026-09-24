# Task: Review (prompt and output QA)

Scope: review image prompts and supplied results against a brief or reference — structural errors, contradictions, continuity drift, task-specific visual defects — then suggest focused repairs.

Read first: `../prompt-contract.md`. When a model is named, consult only its entry in `../model-profiles.md`.

## Workflow

1. A supplied prompt, set of prompts, shot plan or image result is enough; no prior generation workflow is required. Distinguish defects in the written request from defects actually observed in images.
2. Read the brief and references used by the work. Establish the intended count, output form, model if specified, fixed elements and allowed changes.
3. Use `../recipes/prompt_review/review-methods.md` for structure, coverage, continuity, physical/material behavior and targeted repair. Do not impose the old ten-shot photoshoot rules on unrelated imagery.
4. For JSON prompts, run the structural checker when a deterministic check helps:
   `python3 bin/validate_prompt_payload.py <file-or-stdin> [--expect-count N] [--require-path a.b] [--equal-path shared.anchor]`
   It accepts JSON objects, arrays or fenced JSON and reports malformed input rather than skipping it. Count and required/equal paths are optional checks derived from the actual brief. It does not measure visual fidelity or artistic merit.
5. Review the prompt semantically: conflicting change/keep instructions, ambiguous reference roles, wrong aspect ratio or file form, missing exact text, unsupported controls, constraints that erase the source's character. In a set, inspect relevant subject/world continuity and deliberate variation. Read `../recipes/prompt_review/material-review.md` only when physical behavior matters to the intended medium.
6. When outputs are supplied, inspect them against the actual source and prompt; report visible drift, not inferred hidden defects. Without output images, label conclusions as prompt review only. Do not declare images accepted or save a preferred recipe for the user.

Deliver concise findings tied to specific prompts or visible regions, with suggested repairs. If revisions were requested, return corrected complete prompts while preserving useful wording, exact text, formats and unaffected choices. A repeated structural problem merits one shared fix, not a rewrite of the creative set.
