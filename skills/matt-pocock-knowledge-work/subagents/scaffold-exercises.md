---
name: scaffold-exercises
description: "Use when the user wants to scaffold exercises, create exercise stubs, or set up a new course section: create exercise directory structures with sections, problems, solutions, and explainers that pass linting."
---

Invocation: model or user

# Scaffold Exercises

Trigger: the user wants exercise stubs, new exercises, or a new course section.

Procedure: create the directory structure from the plan, then lint and commit. Section names are dash-case XX-section-name/ inside exercises/ (e.g. 01-retrieval-skill-building). Exercises are XX.YY-exercise-name/ inside a section (e.g. 01.03-retrieval-with-bm25). Each exercise needs at least one variant subfolder: problem/ (student workspace with TODOs), solution/ (reference implementation), explainer/ (conceptual material, no TODOs); when stubbing, default to explainer/ unless the plan specifies otherwise. Every variant subfolder gets a readme.md that is non-empty and link-clean (a readme-only stub with a title and description is fine; code subfolders also need a main.ts over 1 line). Then run pnpm ai-hero-cli internal lint and iterate until it passes (no .gitkeep, no speaker-notes.md, no pnpm run exercise commands in readmes). Use git mv, never plain mv, when moving or renumbering exercises so history is preserved, and re-run lint after moves. Commit with git commit when the lint passes.
