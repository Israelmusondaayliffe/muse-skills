---
name: "web-product-studio"
description: "Design and build web products end to end: route the request (greenfield build, redesign, image-first implementation, targeted fix, QA), define browser-verifiable acceptance flows, build through a plan → approval → review pipeline, and enforce a visual-fidelity gate for picture-led work. Use when the user asks to build a website or web app, redesign an existing site, match a screenshot or mockup in working code, generate premium web design comps, or verify a site through rendered browser flows."
metadata: { "includeInPrompt": true }
---

# Web Product Studio

Coordinate coherent frontend and web app work from brief through rendered verification.

## Purpose

Take a web product request from brief to proven delivery: choose the build mode, lock what success looks like as browser-observable flows, build through mandatory planning and approval, review against the plan with deterministic checks, and verify the rendered result — with a strict visual gate for picture-led work.

## Workflow

### 1. Route first

Read the request, the brief, any supplied images, and the rendered state when available. Choose exactly one route using references/routing.md:

- **greenfield** — new product or major new surface
- **redesign** — improve an existing rendered interface (use references/design-audit.md)
- **image-first** — implement from a screenshot, mockup, or visual reference (use references/image-first.md)
- **targeted-fix** — scoped code or interaction repair
- **quality-assurance** — inspect without implementing unless authorized

Diagnostic requests do not authorize implementation. Stop at diagnosis when the task is diagnostic-only.

Record the decision in `assets/route-template.json` and validate it:

```bash
python3 ~/workspace/skills/web-product-studio/scripts/validate_route.py route.json
```

### 2. Define acceptance flows before building

Turn the brief into browser-verifiable user flows (actors, goals, starting states, critical paths, failure paths). One flow per material outcome; every action atomic with a visible expected observation and named evidence. Use assets/acceptance-flow-template.json and references/flow-writing.md, then validate:

```bash
python3 ~/workspace/skills/web-product-studio/scripts/validate_flows.py flows.json
```

A flow that cannot be observed is marked **blocked**, never passed.

### 3. Set one visual direction

If a supplied image is authoritative, preserve its information hierarchy. Otherwise select exactly one visual direction (or none) using references/selection-guide.md — never mix multiple broad style directions. Put the direction name (or `null`) in the route record's `design_constitution`, record the selection with evidence and rejected alternatives in `assets/selection-template.json` format, and validate that selection file:

```bash
python3 ~/workspace/skills/web-product-studio/scripts/validate_selection.py selection.json
```

**Visual-fidelity gate.** When the picture is load-bearing — likeness, realism, a named visual reference, procedural graphics, shaders, WebGL/WebGPU, 3D, simulation, an immersive experience, or a motion-led hero — set `visual_gate_required: true` and run the gate before general implementation:

1. Fill `assets/visual-contract-template.json`: one first-glance sentence, exactly three required traits, exactly three forbidden failures, named viewports, framing, default and extreme states, selected medium (plus rejected media), an observable switch condition, and the source path.
2. Validate: `python3 scripts/validate_visual_contract.py contract.json`. Resolve contradictions before building.
3. Build or inspect only the representative **hero spike**. Keep secondary features frozen unless they are part of the hero itself.
4. Capture fresh rendered comparisons at the contract viewports (live browser delegation; Playwright via `scripts/playwright_cli.sh` for repeatable captures).
5. Hand the contract, references, and fresh captures to an **independent reviewer** — a separate subagent who did not build the hero. They score against references/visual-fidelity-rubric.md and fill `assets/visual-review-template.json`.
6. Validate the review: `python3 scripts/validate_visual_review.py review.json`.
7. Proceed to full build only when the score is **≥ 7**, no P0/P1/P2 gap remains, and all hashes are current. Below 7: repair the hero, switch the declared method, or report the work as visually incomplete.

Do not trigger this gate for ordinary colors, spacing, icons, charts, CRUD work, or a generic "look clean" unless resemblance or picture quality is an explicit acceptance condition.

### 4. Plan, then get approval

Research requirements, edge cases, and technology choice. Produce a complete plan with assets/plan-template.md — plain English, every section filled, folder structure, data flow, edge cases, build checklist, honest confidence level. See references/architecture-patterns.md for structural decisions and references/error-catalog.md for defensive coding patterns.

Plan depth follows the route. **Greenfield, redesign and image-first** work needs the user's approval of the plan before code is written, unless the request already approves building ("go ahead and build it", an approved spec). **Targeted fixes and authorized QA** with decided expected behavior need no separate plan approval: write a three-line plan (cause, change, proof) into the delivery status and build. On feedback, revise and re-present. If the description is too vague, ask at most two focused questions, then plan with stated assumptions. If the request is beyond scope (e.g. native mobile), say so honestly and offer a scoped alternative.

### 5. Build

Build in dependency order (data layer → business logic → API → UI → integration → error handling). Deliver **complete, runnable code only**:

- No placeholders: never `// ...`, `// TODO`, `// implement here`, `// similar to above`, bare `...` standing in for omitted code.
- No structural shortcuts: no skeletons passed off as implementations, no describing what code should do instead of writing it.
- If output approaches the token limit, stop at a clean breakpoint and end with `[PAUSED — X of Y complete. Send "continue" to resume from: next section name]`, then pick up exactly where you stopped on "continue".

For larger builds, delegate the build phase to a subagent with the approved plan, the route record, and the visual contract as ground truth.

### 6. Review

Always run a final review on two independent axes — do not merge the verdicts:

1. **Code standards**: correctness risks, maintainability, security, error handling, architecture. Run `python3 scripts/code_doctor.py --mode full <file_or_directory>` for deterministic checks, and load assets/review-checklist.md for the quality gates.
2. **Specification fidelity**: whether delivered behavior matches the approved plan and original intent, including exclusions and edge cases.

Critical issues go back to the builder — never deliver code with critical issues. Warnings are delivered with explanations; the user decides. Deliver in plain English: what was built, completed checklist, how to use it, quality report, confidence level. The user's confirmation is final acceptance; on feedback, iterate.

### 7. Verify rendered behavior

Rendered browser flows are the primary completion surface for user-facing behavior. File and test checks cannot replace them.

Try these in order and record which one you used:

1. **Live Chromium** via a delegated browser task (login-required flows, forms, purchases) — execute every acceptance flow, save pass/fail/blocked evidence.
2. **Playwright CLI** from the terminal for repeatable automation and diagnostics: `scripts/playwright_cli.sh`. It runs `npx --yes --package @playwright/cli`, which downloads the package when it is not cached; check `command -v npx` first and treat a failed download as "unavailable", not as a failed flow. See references/playwright-cli.md and references/playwright-workflows.md.
3. **Nothing renders:** keep each flow `blocked` (never `passed`), report the implementation paths and any script-level test evidence, mark rendered and visual acceptance **incomplete**, and name the exact browser flows and comparisons still required.

Local static pages can be opened as `file://` URLs or served with `python3 -m http.server` from the page folder.

## Worked example (illustrative)

Request: "On phones the menu button does nothing. Tapping it should show the nav links; desktop should stay as it is. Fix it." A static site with one stylesheet and one script.

- Route: `targeted-fix`. The expected behavior is decided, so there is no plan-approval wait and no visual gate (nothing picture-led).
- Inspect first: the script toggles the class `open` on the nav, but the CSS shows the menu only for `.nav.is-open`. The button also never updates `aria-expanded`.
- Change: toggle `is-open` (one line, matching the stylesheet rather than renaming CSS used elsewhere) and set `aria-expanded` to match. Leave the styling alone and add no dependencies.
- Flows: F1 at 375 px, tapping the button shows the links and sets `aria-expanded="true"`, and a second tap hides them. F2 at 1280 px, the links are visible with no button. Validate with `validate_route.py` and `validate_flows.py`.
- Verify: run both flows in a rendered browser and save a screenshot of each state. If no browser is available, both flows stay `blocked`.

A wrong version would ask for plan approval the user already gave, redesign the header, or mark F1 passed because the code "looks right".

## When something goes wrong

| Symptom | Likely cause | Next move | Stop when |
|---|---|---|---|
| A validator prints `"valid": false` | Missing or mistyped field | Fix the named fields in your JSON and re-run once | a field needs a decision the user has not made |
| `npx` missing or the Playwright download fails | No Node or no network | Use the live browser; otherwise mark flows `blocked` | never claim a rendered pass without a render |
| Code Doctor reports a critical issue | Real defect or a false positive | Fix it, or explain in one line why it does not apply | it is a security issue you cannot resolve; report it |
| Hero review scores below 7 | Visual method not working | Repair the hero once or switch the declared medium | second score below 7; report visually incomplete |
| The fix needs a backend, credentials or a paid service | Out of scope | Deliver the front-end part and name the missing service | the requested behavior cannot exist without it |

## Completion

Report three statuses separately in `delivery-status.md` or the reply:

- **Functional:** code builds and runs; review passed with no critical issue.
- **Rendered:** every acceptance flow `passed` with named evidence, or `blocked` with the missing capability.
- **Visual:** gate passed at 7 or higher, or "not required" for non-picture-led work, or incomplete.

The task is complete when all requested statuses are met. The user's own confirmation is final acceptance; deliver the evidence so they can give it without redoing your checks. If one part is blocked, finish the rest and name the gap.

## Output Contract

- When an output root is authorized, keep all build artifacts there and record status at `<output-root>/web-product-studio/delivery-status.md` (route, flows status, visual gate status, rendered verification status, remaining proof).
- A request to fix or build files the user supplied authorizes editing those files or a scratch copy. Without any authorized location, return the complete status in the current task and ask before writing files.
- Never invent user-specific data (business names, writing samples, credentials, personal details): ask the user when the build needs personal input.
- Keep changes local; never claim a commit, pull request, backend, or specialist security review you cannot verify.

## Operating Rules

1. Choose exactly one route and one visual direction (or none). Record rejected alternatives.
2. Diagnostic-only tasks never authorize implementation.
3. Functional completion and visual completion are separate: a working interface is not a visually accepted one.
4. Freeze secondary features until the independent hero review scores ≥ 7 with no P0/P1/P2 visual gap.
5. Never mark a flow passed from code inspection alone when the requirement is rendered behavior.
6. Greenfield, redesign and image-first plans are approved before building; reviews happen before delivery; the user gives final acceptance.
7. Code Doctor runs in review; critical findings return to the builder.
8. Keep the implementation context small: load only the references needed for the current phase (routing, then flows, then architecture, then the chosen design direction, then the rubric for visual review).
