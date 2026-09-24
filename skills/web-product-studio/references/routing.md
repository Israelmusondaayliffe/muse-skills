# Web product routes

Classify the request before doing anything else. Exactly one primary route.

- **greenfield**: new product or major new surface. Implement directly in the user-approved project or output root.
- **redesign**: improve an existing rendered interface. Use references/design-audit.md. Work with the existing stack; do not migrate frameworks.
- **image-first**: implement from a screenshot, mockup, or visual reference. Use references/image-first.md (generate or accept design comps, analyze, then build).
- **targeted-fix**: scoped code or interaction repair. Plan briefly, fix, re-run the affected acceptance flows.
- **quality-assurance**: inspect behavior and rendering without implementing unless authorized. Without a rendered surface, return the exact inspection plan and mark rendered proof blocked.

Add the **visual-fidelity gate** before general implementation when the route depends on a supplied or named visual reference, likeness, photorealism, cinematic or material realism, procedural graphics, shaders, WebGL, WebGPU, 3D, simulation, an immersive picture-led experience, or a motion-led hero. The route stays `greenfield`, `redesign`, or `image-first`; the gate is a required specialist and stop condition, not a competing primary route.

Do not add the gate merely because a routine product has colors, spacing, icons, charts, or a generic request to look clean.

## Rendering verification surfaces (in order of preference)

1. **Live Chromium browser** via a delegated browser task: full interactive proof including logins, forms, and purchases. This is the primary completion surface for user-facing behavior.
2. **Playwright CLI** from the terminal for repeatable automation and diagnostics: `scripts/playwright_cli.sh` (needs `npx`). See references/playwright-cli.md and references/playwright-workflows.md.

File and test checks cannot replace rendered proof. Without a rendered surface, report the implementation paths and test evidence, mark rendered and visual acceptance incomplete, and name the exact browser flows and comparisons still required.

## High-visual-stakes rule

For high-visual-stakes work, a running app, clean console, or complete feature list cannot replace a fresh same-size comparison. Freeze secondary features until an independent hero review reaches at least 7 out of 10 with no P0, P1, or P2 visual gap. Below that boundary, repair, switch method, or report the work as visually incomplete.

## Fallbacks

- Without an authorized output root, return the status in the current task and ask before writing files.
- Diagnostic requests do not authorize implementation.
- Keep changes local; never claim a commit, pull request, backend, or specialist security review you cannot verify.

Record the decision in `assets/route-template.json` and validate with `scripts/validate_route.py`.
