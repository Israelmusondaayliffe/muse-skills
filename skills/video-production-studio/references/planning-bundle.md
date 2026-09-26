# Planning bundle (no-renderer path)

When the user asks for a plan — or a video cannot be produced here — write
a self-contained six-file bundle inside the user-approved output root.
Planning can be complete without claiming anything was rendered.

## Artifacts

1. **video-brief.md** — objective, audience, format, duration, aspect ratio,
   message, constraints.
2. **storyboard.md** — ordered scenes: purpose, content, timing,
   transitions.
3. **shot-list.md** — each planned shot: source or creation method,
   framing, duration, status.
4. **asset-ledger.md** — required vs. available media, provenance,
   rights/license state, missing assets.
5. **runtime-requirements.md** — renderer, capture, inspection, codec,
   font, and other production requirements still needed.
6. **delivery-checklist.md** — planned export, audio, caption, technical,
   and visual checks.

## Route record

Record the route in `route.json` (from `assets/route-template.json`) with
`requested_deliverable: "plan"`, `runtime: "none"`, `renderer_available: false`,
`completion_state: "planning-complete"`, `missing_requirements: []`,
`rendering_status` and `visual_qc_status` as `incomplete`. When the user
asked for a clip and rendering is blocked, the bundle is still useful but the
state is `blocked`, with the blocker in `missing_requirements`. Validate:

```bash
python3 <SKILL_DIR>/bin/validate_route.py route.json
```

## Completion states

- `planning-complete` — the six artifacts exist and agree; rendering and
  visual QC remain incomplete.
- `rendered-delivery-complete` — a renderer produced the delivery file,
  delivery QC completed technical + visual checks (references/delivery-qc.md),
  and nothing the user requested is missing.
- `rendered-partial` — a render exists, but a requested element is missing
  (audio, captions, a supplied or required asset, the size or length). List
  each one in `missing_requirements`.
- `blocked` — a clip was requested and no usable render exists. A plan
  never fulfills a requested clip.

Never mark `rendered-delivery-complete` without a real rendered file, a
completed QC pass, and an empty `missing_requirements`. If source media is missing, stop before inventing
substitutes that change the brief. If platform dimensions are unknown,
state the assumed target and keep the layout adaptable.
