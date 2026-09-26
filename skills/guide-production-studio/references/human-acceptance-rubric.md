# Human Acceptance Rubric

Mechanical checks support this review. They do not decide it.

The producer cannot be the reviewer. The reviewer can return `ready_for_human_review`, but only the user (the named human owner) can approve the benchmark, publication, or scale.

## Ten gates

All ten gates pass. Do not hide a critical failure inside an average score.

### 1. Purpose

The reader can state what the guide helps them do and when it is useful.

### 2. Context

The guide gives enough background to understand why the workflow exists and what the reader needs before starting.

### 3. Vocabulary

Unfamiliar terms are explained at first use without reducing the subject's depth.

### 4. Action

The reader can follow the steps, identify inputs, recognize expected results, and find the next decision.

For runnable examples, read the displayed code, then run it with `scripts/check_guide_example.py --workdir-arg` for a normal case, an exercised collision case, and a malformed-input case (see `executable-examples.md`). The helper is not a sandbox. Record the reports as gate evidence.

### 5. Evidence

Important claims, methods, examples, prompts, and results match inspected sources and accurate run status.

### 6. Provenance and privacy

Permitted public lineage is preserved. Private implementation details, identities, paths, and source names remain protected.

### 7. Examples and reuse

Real or properly labeled examples help the reader act. Prompts and templates include their purpose, inputs, limits, and judgment criteria.

### 8. Troubleshooting

Visible problems connect to likely causes, protected elements, the smallest useful next action, and a stop rule.

### 9. Structure and visual teaching

Every page and attachment earns its place. Visual judgments have evidence the reader can inspect.

### 10. Voice and value

The guide is clear, human, direct, curious, and useful. It contains context, intent, quality, and craft rather than internal process language or generic filler.

## Critical failures

Any of these blocks approval:

- Unsupported factual or result claim
- Invented workflow history or example outcome
- Rights or privacy exposure
- Public provenance removed without a legitimate reason
- Producer and reviewer are the same
- Visual subject presented as complete without visual evidence
- Quick start cannot be attempted from the guide
- Internal skill, subagent, validator, routing, or publication commentary appears publicly
- A runnable example can overwrite, move, or delete a file that existed before it ran, in setup, output, or recovery
- Displayed code differs from the code that was run, or the text claims output or reporting the displayed code does not produce
- A runnable example was not exercised for its collision and malformed-input cases (see `executable-examples.md`) before being called usable

## Cold-reader observation

Before bulk production, observe one intended reader using the benchmark without author-only context.

Record:

- What they thought the guide was for
- Where they first became uncertain
- Whether they could complete the first useful action
- What they expected to happen next
- Which section they returned to for reference

Do not replace observation with a model's prediction of reader behavior.

## Verdict rule

- Any missing prerequisite: `blocked`
- Any failed gate: `rejected`
- All reviewer gates pass: `ready_for_human_review`
- The user explicitly approves after reviewing evidence: `human_approved`

Only the final state permits baseline pinning or bulk scale.
