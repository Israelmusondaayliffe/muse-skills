# Model Routing

Model profiles are **decision contracts, not live capability claims**. Confirm the
selected surface before any live use.

## Contract

Every model decision records: the model and profile version checked, the
verification date, supported inputs, reference behavior, audio, duration,
editing modes, known constraints, recurring failure patterns, and the
external-action approval policy.

Status is one of:

- `planning-only` — transforms records and identifies missing decisions. No
  service calls, no capability claims.
- `delegated` — the user has explicitly chosen a named model surface; I may pass
  the complete normalized packet to that surface (browser task or the user's own
  workflow) after approval. I still do not claim model-specific syntax or
  availability.
- `unverified` — may not claim a surface capability or emit its syntax.

## Rules

- AI Film Studio always produces a complete model-neutral packet first.
- Never infer availability, duration, cost, reference limits, beta access, or an
  interface from a model name. Verify against the provider's current docs or the
  user's own account before live use.
- No silent substitution: an explicitly selected model stays selected; a future
  model starts `unverified` and cannot emit surface syntax until current evidence
  is recorded.
- The film-prompt station leaves `compiled_prompt` and `prompt_sha256` empty and
  marks the validator `unrun` unless a formatter owns the grammar.
- A valid packet does not prove a video was generated or inspected.

## Available in this skill

There is no bundled video-model formatter in this host. Model choice is recorded
in the packet (`target_model`); actual surface syntax, cost confirmation, and
generation are handled by the user's chosen surface (via live browser, their
account, or their own tools) with the approval gates in `approval-gates.md`.
