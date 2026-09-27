---
name: setup-pre-commit
description: "Use when the user wants to add pre-commit hooks, set up Husky, configure lint-staged, or add commit-time formatting, typechecking, or testing."
---

Invocation: model or user

# Setup Pre-Commit Hooks

Trigger: the user wants pre-commit hooks in the current repo.

Procedure: detect the package manager from the lockfile (package-lock.json for npm, pnpm-lock.yaml, yarn.lock, bun.lockb; default to npm if unclear), then install husky, lint-staged, and prettier as devDependencies. Run npx husky init to create .husky/ and add the prepare script to package.json. Write .husky/pre-commit with npx lint-staged plus npm run typecheck and npm run test (adapting the package manager command to the detected one, and omitting the typecheck/test lines if those scripts don't exist in package.json, telling the user why). Create .lintstagedrc with "*" mapped to "prettier --ignore-unknown --write". Create .prettierrc only if no Prettier config exists, with the skill's defaults (2-space, 80 print width, semicolons, es5 trailing commas, double quotes, always arrow parens).

## Verify

- [ ] `.husky/pre-commit` exists and is executable
- [ ] `.lintstagedrc` exists
- [ ] `prepare` script in package.json is `"husky"`
- [ ] `prettier` config exists
- [ ] Run `npx lint-staged` to verify it works

## Commit

Stage all changed/created files and commit with message: `Add pre-commit hooks (husky + lint-staged + prettier)`. This runs through the new pre-commit hooks: a good smoke test that everything works.
