---
name: setup-ts-deep-modules
description: "Use when wiring dependency-cruiser into a TypeScript repo so each package becomes a deep module, with implementation hidden in subfolders and reachable only through its entry-point files."
---

Invocation: user-invoked only

## Procedure

Make every package a **deep module**: a lot of behaviour behind a small interface. A package's public surface is its **entry points** (the files at the package root); everything in its subfolders is hidden.

For the vocabulary (deep module, interface, seam, depth), use the codebase-design brief's language throughout.

### The shape this enforces

```
src/packages/
  <name>/
    index.ts        ← entry point (public). Import this from outside.
    client.ts       ← packages may expose SEVERAL small entry points.
    lib/            ← implementation: hidden from outside, free to import each other.
    tests/          ← co-located tests + fixtures (a subfolder, so private).
```

**Entry points, not a barrel.** The public surface is *every* root file, so a package can expose several small entry points instead of funnelling everything through one giant `index.ts`. Barrel files re-exporting a whole subtree are discouraged.

Four rules, all `error`:

1. **Entry-point boundary**: code outside a package may import only its entry points (root files), never its subfolders.
2. **Intra-package freedom**: a package's own files import each other freely.
3. **Tests through the entry points**: files under `<pkg>/tests/` may import any package's entry points and their own fixtures, never any package's subfolder internals (not even their own).
4. **No cycles**: no dependency cycles.

Layering (which packages may depend on which) is a separate concern, left as a commented stub.

### 1. Detect the environment

- **Package manager**: `pnpm-lock.yaml` means pnpm, `yarn.lock` means yarn, `bun.lockb` means bun, else npm. Use it for every command.
- **Packages root**: if `src/` exists use `src/packages`, else `packages`. Confirm with the user if the repo already has a different obvious convention.
- **Existing config**: check for `.dependency-cruiser.*`. If one exists, do **not** overwrite: merge the four rules and options in, and tell the user what was added.

Done when: package manager, packages root, and existing-config status are all known.

### 2. Install dependency-cruiser

Install `dependency-cruiser` as a devDependency with the detected package manager.

Done when: it is in `devDependencies`.

### 3. Write the config

Copy the bundled `bin/dependency-cruiser.config.cjs` to the repo root as `.dependency-cruiser.cjs`. Set `PACKAGES_ROOT` to the root from step 1. The rules are path-depth based and extension-agnostic, so nothing else needs adapting.

Done when: the config exists with the correct `PACKAGES_ROOT` and the four forbidden rules present.

### 4. Wire it into the checks

- Add a `lint:boundaries` script: `depcruise <packages-root>`, and fold it into the repo's umbrella check command (the one that already runs typecheck, e.g. `check` / `ci` / `validate`). Do **not** touch `tsconfig` or add path aliases.
- If there is no umbrella script, add `lint:boundaries` and tell the user to include it in CI.

Done when: `lint:boundaries` exists and runs as part of the same command as typecheck.

### 5. Scaffold the example package

Create a committed `<packages-root>/example/` as a copy-me template:

- `index.ts`: an entry point exporting one function that delegates to an internal file, so the package is visibly *deep*, not a pass-through.
- `lib/impl.ts`: an internal file in a subfolder, imported by `index.ts`, not reachable from outside.
- `tests/example.test.ts`: imports **only** `../index` and asserts against the public function.

Tell the user this is a starter template to copy or delete.

Done when: the example package exists, exposes behaviour through a root entry point, and hides `impl` in a subfolder.

### 6. Prove the rules bite

A config that doesn't fail on a violation is worthless.

1. Run `lint:boundaries`. It must **pass** on the clean example.
2. Temporarily add a deep import to `tests/example.test.ts` (e.g. `import { thing } from "../lib/impl"`). Run again; it must **fail** with `tests-through-entrypoints`.
3. Revert the deep import. Run once more; it must **pass**.

Done when: you have observed pass, then fail on the deep import, then pass again. If step 2 does not fail, the rules are not wired correctly: fix before finishing.

### 7. Document the convention

Write `<packages-root>/README.md` covering: the layout (entry points at the root, `lib/` for implementation, `tests/` for tests), "import only through a package's entry points (its root files)", how to run `lint:boundaries`, and an explicit discouragement of barrel files. Keep it to the copy-me snippet plus the four rules in one paragraph each.

Then add a **context pointer** from the repo's agent-instructions file (`CLAUDE.md` if present, else `AGENTS.md`, creating it if neither exists). One line is enough, e.g. `Packages are deep modules: see src/packages/README.md before adding or importing one.`

Done when: the README exists and discourages barrels, and the agent-instructions file links to it.

### Notes

- The config's `$1` back-references let a package reach its own internals while outsiders can't; don't flatten them into per-package rules. Public vs private is decided by **depth**: root files are entry points, any subfolder is private, so a new folder never needs a config change and adding an entry point is just adding a root file, no barrel. Packages are **flat**: one tier of children under the root; internals may nest, but a package may not contain another package. Use `.cjs` (not `.js`) so `module.exports` works even in `"type": "module"` repos.

## Knowledge-work port

- Enforce "entry points" for a knowledge project: one README and a few public briefs at the root; drafts and raw research stay in subfolders.
- Never cite or paste from internals: reference only the public documents.
- Validate against the public brief alone, never against internal notes; if the brief alone can't support the claim, the boundary is too thin.
- Document the convention once, in the root README, and link it from your working notes.
