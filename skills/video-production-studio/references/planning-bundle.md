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
`runtime: "none"`, `renderer_available: false`,
`completion_state: "planning-complete"`, `rendering_status` and
`visual_qc_status` as `incomplete`. Validate:

```bash
python3 <SKILL_DIR>/bin/validate_route.py route.json
```

## Completion states

- `planning-complete` — the six artifacts exist and agree; rendering and
  visual QC remain incomplete.
- `rendered-delivery-complete` — a renderer produced the delivery file and
  delivery QC completed technical + visual checks (references/delivery-qc.md).

Never mark `rendered-delivery-complete` without a real rendered file and a
completed QC pass. If source media is missing, stop before inventing
substitutes that change the brief. If platform dimensions are unknown,
state the assumed target and keep the layout adaptable.
