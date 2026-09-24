# Evidence and Artifact Policy

Every workflow should leave the user with a result they can understand,
reuse, and correct.

## Evidence labels

Keep these categories visibly separate:

- Verified source material: checked against the cited source.
- User-supplied material: provided by the user but not independently checked.
- User decision: a choice the user made.
- Proposal: generated work offered for consideration.
- Assumption: a working belief that affects the result.
- Unresolved gap: information still missing or disputed.

Never upgrade a proposal, assumption, or promising result into proof.

## Artifact behavior

Use the skill's template as a coverage check, not a rigid form.

- Return a complete portable Markdown artifact in the response when it is
  reasonably sized.
- For a large or multi-file deliverable, save the authorized files under
  `~/workspace/` and return a compact receipt with paths, key decisions,
  evidence status, and unresolved gaps. Do not duplicate the full package in
  chat.
- If a large deliverable needs file output but file creation is not
  authorized, show the proposed package and ask before generating it.
- Use JSON or CSV only when structured comparison, tracking, or later
  automation benefits from it.
- Write to Gmail, Calendar, or another connected destination only when the
  user requests that destination.
- Do not create every possible deliverable. Workshop Workbench and Session
  Compounder must recommend useful outputs and wait for the user's selection
  before producing a large package.

## Claims and links

For material public claims, keep the claim close to its citation. Include
access dates when recency matters. Mark unknown price, availability, ownership,
or performance instead of guessing.

Before completion, check:

1. The artifact answers the user's actual decision or job.
2. Important claims have appropriate support.
3. Assumptions and unresolved gaps are visible.
4. Links point to the underlying source.
5. The next action is concrete and authorized.

## Personal data

Do not invent user-specific material: writing samples, business details,
names, credentials, private schedules, or contact data. Ask the user when a
workflow needs personal input, and record supplied personal facts only in
memory or files the user has authorized.
