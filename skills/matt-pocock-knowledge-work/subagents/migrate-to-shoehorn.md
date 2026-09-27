---
name: migrate-to-shoehorn
description: "Use when the user mentions shoehorn, wants to replace `as` in tests, or needs partial test data: migrate test files from type assertions to @total-typescript/shoehorn."
---

Invocation: model or user

# Migrate to Shoehorn

Trigger: the user wants to replace `as` assertions in tests with @total-typescript/shoehorn, or needs partial test data.

Procedure: install with npm i @total-typescript/shoehorn. This is for test code only, never production code. Apply the four migration patterns: large objects where only a few properties matter become fromPartial({ ... }) instead of building the whole fake object; `expr as Type` becomes fromPartial({ ... }) from @total-typescript/shoehorn; and intentionally-wrong-type data (`expr as unknown as Type`) becomes fromAny({ ... }). `fromExact({ ... })` forces a full object (swap with fromPartial later) where partial data is not acceptable yet. Prefer fromPartial for genuinely partial data and fromAny for deliberately incorrect data, and remove the now-redundant manual type annotations the `as` assertions required.

## Workflow

- [ ] Install: `npm i @total-typescript/shoehorn`
- [ ] Find test files with `as` assertions: `grep -r " as [A-Z]" --include="*.test.ts" --include="*.spec.ts"`
- [ ] Replace `as Type` with `fromPartial()`
- [ ] Replace `as unknown as Type` with `fromAny()`
- [ ] Add imports from `@total-typescript/shoehorn`
- [ ] Run type check to verify
