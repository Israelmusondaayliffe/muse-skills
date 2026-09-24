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

If a supplied image is authoritative, preserve its information hierarchy. Otherwise select exactly one visual direction (or none) using references/selection-guide.md — never mix multiple broad style directions. Record it in the route record and validate:

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

**The user must approve the plan before any code is written.** On approval signals, proceed; on feedback, revise and re-present. If the description is too vague, ask at most two focused questions, then plan with stated assumptions. If the request is beyond scope (e.g. native mobile), say so honestly and offer a scoped alternative.

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

Critical issues go back to the builder — never deliver code with critical issues. Warnings are delivered with explanations; the user decides. Deliver in plain English: what was built, completed checklist, how to use it, quality report, confidence level. The user must confirm the output works before the task is complete; iterate until they signal completion.

### 7. Verify rendered behavior

Rendered browser flows are the primary completion surface for user-facing behavior. File and test checks cannot replace them.

1. **Live Chromium** via a delegated browser task (login-required flows, forms, purchases) — execute every acceptance flow, save pass/fail/blocked evidence.
2. **Playwright CLI** from the terminal for repeatable automation and diagnostics: `scripts/playwright_cli.sh` (needs `npx`). See references/playwright-cli.md and references/playwright-workflows.md.

Without a rendered surface, report the implementation paths and test evidence, mark rendered and visual acceptance **incomplete**, and name the exact browser flows and comparisons still required.

## Output Contract

- When an output root is authorized, keep all build artifacts there and record status at `<output-root>/web-product-studio/delivery-status.md` (route, flows status, visual gate status, rendered verification status, remaining proof).
- Without an authorized output root, return the complete status in the current task and ask before writing files.
- Never invent user-specific data (business names, writing samples, credentials, personal details): ask the user when the build needs personal input.
- Keep changes local; never claim a commit, pull request, backend, or specialist security review you cannot verify.

## Operating Rules

1. Choose exactly one route and one visual direction (or none). Record rejected alternatives.
2. Diagnostic-only tasks never authorize implementation.
3. Functional completion and visual completion are separate: a working interface is not a visually accepted one.
4. Freeze secondary features until the independent hero review scores ≥ 7 with no P0/P1/P2 visual gap.
5. Never mark a flow passed from code inspection alone when the requirement is rendered behavior.
6. Plans are approved before building; reviews happen before delivery; the user confirms before the task is complete.
7. Code Doctor runs in review; critical findings return to the builder.
8. Keep the implementation context small: load only the references needed for the current phase (routing, then flows, then architecture, then the chosen design direction, then the rubric for visual review).
