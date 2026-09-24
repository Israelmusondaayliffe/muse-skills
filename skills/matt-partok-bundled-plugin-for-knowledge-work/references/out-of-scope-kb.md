# Out-of-Scope Knowledge Base

`.out-of-scope/` at the repo root stores persistent records of **rejected
feature requests**. Two purposes: institutional memory (why something was
rejected) and deduplication (surface the prior decision instead of
re-litigating it when a similar request returns).

## Layout

One file per **concept**, not per issue — multiple requests for the same thing
group under one file:

```
.out-of-scope/
├── dark-mode.md
├── plugin-system.md
└── graphql-api.md
```

## File format

Relaxed and readable — a short design doc, not a database entry. Paragraphs,
examples, and code samples are welcome.

```markdown
# Dark Mode

This project does not support dark mode or user-facing theming.

## Why this is out of scope

The rendering pipeline assumes a single color palette defined in
`ThemeConfig`. Supporting multiple themes would require:

- A theme context provider wrapping the entire component tree
- Per-component theme-aware style resolution
- A persistence layer for user theme preferences

This is a significant architectural change that doesn't align with the
project's focus on content authoring. Theming is a concern for downstream
consumers.

## Prior requests

- #42 : "Add dark mode support"
- #87 : "Night theme for accessibility"
```

- **Name the file** with a short, descriptive kebab-case concept:
  `dark-mode.md`, `plugin-system.md`, `graphql-api.md`.
- **Write a substantive reason** — not "we don't want this" but why: project
  scope/philosophy, technical constraints, strategic decisions. Reasons must
  be durable — avoid temporary circumstances ("we're too busy right now");
  those are deferrals, not rejections.

## Checking during triage

Read all `.out-of-scope/*.md` files when gathering context on a new request.
Match by **concept similarity**, not keyword ("night theme" matches
`dark-mode.md`). On a match, surface it: "We rejected this before because
[reason]. Do you still feel the same way?" The maintainer may confirm (append
the new request under "Prior requests", then close), reconsider (delete or
update the file, proceed through triage), or disagree (related but distinct —
proceed normally).

## When to write here

Only when an **enhancement** (not a bug) is rejected as `wontfix`:

1. Check if a matching file already exists.
2. If yes: append the new request to "Prior requests".
3. If no: create the file with concept name, decision, reason, and first
   prior request.
4. Post a comment explaining the decision and mentioning the file.
5. Close with `wontfix`.

Do **not** write here when something is closed as `wontfix` because it's
**already implemented** — that's a built feature, not a rejection; recording
it would poison dedup checks with false rejections. Point to where the
feature lives instead.

## Removing

If the maintainer changes their mind: delete the file. Old closed issues stay
as historical records; the new request proceeds through normal triage.
