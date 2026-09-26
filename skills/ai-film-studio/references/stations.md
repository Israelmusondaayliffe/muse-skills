# Station Checklists

Detailed checklists for each workflow station in `SKILL.md`. Templates referenced
here live in `../templates/`.

## 1. Wayfinding grill

Ask one material question at a time; skip only when a supplied record already
answers it. For each answer record: decision, alternatives considered, why the
choice won, source/owner, confidence, and next proof still needed.

Cover: intent, audience, story, runtime, visual language, sound language,
resources, budget, schedule, rights, target models, distribution, risk, approval
policy, smallest test scene.

A concept is ready when every material field is decided or explicitly left open
with a stop gate. Stop with a named open decision when an answer would materially
change the premise, test scene, cost, rights, or safety boundary. Use
`../templates/practical/` scratch notes if needed; the decisions themselves live
in `FilmBrief.json`.

## 2. Film brief

`FilmBrief.json` must name: format, duration range, delivery intent, audience;
story premise, central pressure, scene objective; continuity-sensitive cast,
locations, props, states, sound needs; visual rules, geography risks, prohibited
assumptions; proof required at each handoff; cost, rights, safety, and
external-action gates. Keep model claims out unless evidence for the actual
selected surface is supplied. Status must be `approved` (by the user) before
station 3.

## 3. Architecture

`project-record.json`: project id, naming convention (`@type_project_descriptor`),
authoritative records list, sequence/scene graph, dependency order
(brief → assets/geography → shots → verified records → tests → post), owners per
handoff, schedule, cost envelope, failed-attempt budget. No folders, accounts,
remote destinations, or live jobs are created without direct authorization.

## 4. Asset bible

Per asset (`AssetRecord.json`): id, name, type, state, descriptor, reference role,
downstream use, stress test. Characters: identity reference, full-body view,
back/alternate view, neutral controllable lighting, visible material detail,
living eyes — never bake scene grade or camera style into the identity. Locations:
playable anchor, depth planes, entrances, light rationale, material logic,
explicit reverse-angle test where continuity requires it. Props: scale, material,
state, hand/placement relationship, readable content to verify. Approve only
against named evidence. One isolated edit at a time; preserve the approved master.

## 5. Performance

Per recurring character (`performance-bible.json`): body history, center of
gravity, tempo, posture, movement pattern; locked vocal identity; signature
behavior + trigger; social mask + the concrete condition that breaks it; eye
life (gaze target, blink, catchlight); scene-independent continuity rule. Every
scene adaptation: objective, obstacle, active listening, physical task, motivated
distance; two or more observable beat changes when duration permits; a reaction
that begins before or during the partner's final cue. Avoid frozen stillness,
synchronized ensemble responses, or an instant reset after a serious event.
Speaking roles reference a stable voice descriptor; the line itself belongs only
in the shot's audio field.

## 6. Geography

Per location (`geography-lock.json`): visual priorities (material logic,
brief-derived palette, depth, anchor, one motivated light rationale); fixed
landmarks, entrances, playable routes, foreground/midground/background,
camera-side rule; screen axis and crossing rule; positions relative to a landmark
with useful distances; motivated primary light direction and exposure priority;
each character's allowed start position, facing, gaze target, movement path, and
prop contact. A reverse or new angle is a continuity test, not evidence the
unseen space is known.

## 7. Shot direction

Per shot (`ShotRecord.json`): describe only the current shot. Set first-frame
occupancy deliberately (visible cast/objects, positions, facing, gaze, landmark
contact). One format: continuous take, or an explicit sequence of cuts each with
a stated purpose and continuity locks. Action as bounded, physically possible
time blocks naming position, action, camera behavior, and critical prop/sound
conditions. Optics matched to the narrative task (observed outcome over brand
labels). Physics, light direction, audio limits, positive constraints only where
they protect an identified risk. Attach a performance adaptation per visible
character. Requires approved asset IDs and a geography-lock ID for
continuity-sensitive work.

## 8. Prompt packet

From the skill folder, run `python3 bin/film_advisor.py shot <shot_record.json> <model_id>`
to build a complete model-neutral `PromptPacket.json`: asset references with
positive/negative controls, geography lock, first-frame intent, timed action
beats, performance, camera, lens, light, physics, dialogue, sound, constraints,
source hashes, target model, approval policy. `compiled_prompt` and
`prompt_sha256` stay empty until a formatter owns the grammar. Never emit
model-specific syntax from memory.

## 9. Iteration

Per attempt (`iteration-record.json`): hypothesis, acceptance conditions,
baseline, exact record versions/assets/adapter decision before testing, observed
evidence, earliest-failure classification (source asset, geography, performance,
direction, adapter uncertainty, inconclusive), the one changed variable, next
route. Recommend the smallest useful experiment; execution is a separately
approved action (see `approval-gates.md`).

## 10. Post & delivery

Edit preserving source IDs and prompt/adapter records needed to recreate any
selected shot. Cleanup before color/sound: prioritize faces, hands, readable
text, continuity anchors, narrative comprehension. Unify adjacent shots before a
scene look. Plan sound: dialogue clarity, ambience, effects, music — distinct
from any model-generated audio artifact. Delivery acceptance conditions, file
provenance, credits/rights checks, review audience. `DeliveryReceipt.json` for
release readiness; capture learning as a testable change to doctrine, record
structure, or future test design. Package only — no publish/upload/replace/send
without separate explicit approval for the exact target.
