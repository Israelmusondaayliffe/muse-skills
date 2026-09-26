---
name: ai-film-studio
description: "Explicit-only AI film-production planning: concept grill, film brief, production records, shot packets, and iteration supervision. Triggers when the user asks to plan an AI film project, build a film brief or shot list, or invokes it by name (e.g. 'use AI Film Studio')."
---

# AI Film Studio

## Purpose

An explicit-only planning system that takes a film project from concept through brief,
production records (assets, performance, geography, shots), model-neutral prompt packets,
generation iteration, and delivery readiness — without ever starting a live generation,
upload, purchase, or publication on its own.

## Activation

Explicit-only. This skill is active only when the user deliberately asks for it:
"Use AI Film Studio", "film brief", "plan my AI film project", or names this skill
directly. Do **not** activate from a quoted name, a negated or conditional mention,
an incidental reference, or ordinary filmmaking conversation. An ordinary request to make
a video belongs to the video production skill, not here.

## Start here

1. **Name the station deliverable.** Which record or records come back (brief, asset
   bible, geography lock, shot record, prompt packet, iteration log, delivery receipt),
   and for which project. A request for a shot packet is finished only when the packet
   file exists, not when a plan for it exists.
2. **Inventory supplied records.** Open each one and note its `id` and `status`. Records
   marked `approved` are decisions; do not reopen them with grill questions.
3. **Start at the earliest station whose required inputs are not approved.** With an
   approved brief, assets and geography lock, go straight to shot direction. With no
   brief, start at Wayfinding. If an upstream record is missing or draft, deliver what
   the approved records allow and name the record that blocks the rest.
4. Work in the project's `records/` folder (see Output contract). Before writing a
   record, check that the file name is free; if it exists, write a new version
   (`_v2`) instead of overwriting.

## Host capabilities (what runs where)

This skill was adapted from a Codex/Claude plugin; its manifest, hook, agent, and
slash-command formats do not transfer. Use these native equivalents instead:

| Plugin concept | Native equivalent |
|---|---|
| Bundled records in `templates/` | JSON/markdown records in a project directory under `~/workspace/` (one per project) |
| `film_advisor.py` packet routing | `bin/film_advisor.py` — run with `python3` to route a request or build a model-neutral shot packet |
| Subagent "planner / builders / auditor / fixer / verifier" topology | I spawn subagents for parallel draft work; I keep one role per subagent (draft OR audit OR fix OR verify), then integrate results myself |
| "Hooks" (PreCompact, SessionStart) | The checkpoint checklists in this file — run them at the named moments |
| Model-specific prompt formatters | Not available here. Always emit the complete model-neutral packet; verify the live surface myself (web search, docs, or the user's own account) before any live use |

## Workflow

Work stations in order. Each station names its output record; a downstream station may
not start until its required inputs are `approved`.

1. **Wayfinding (concept grill)** — one material question at a time: intent, audience,
   format, duration, premise, protagonist pressure, opposition, irreversible choice,
   emotional question, visual world, sound world, resources, budget, schedule, rights,
   target models, distribution, risks, approval policy, smallest test scene.
   Record decided / assumed / open with alternatives, reasons, and next proof.
   Stop at any choice that would materially change the premise, cost, rights, or
   safety boundary. Do not invent plot, cast, or visual rules to fill gaps.
2. **Film brief** — turn the approved concept into a `FilmBrief.json`: format, duration
   range, delivery intent, audience, premise, central pressure, scene objective,
   continuity-sensitive cast/locations/props/states/sound, visual rules, geography
   risks, prohibited assumptions, proof required per handoff, and cost/rights/safety
   gates. **Stop for explicit user approval.** Status must read `approved` before
   anything downstream.
3. **Architecture** — one `project-record.json`: project id, asset naming convention
   (`@type_project_descriptor`), authoritative records, sequence/scene graph,
   dependency order (brief → assets/geography → shots → verified records → tests →
   post), owners, schedule, cost envelope, and a failed-attempt budget
   (default 12 attempts only if the user hasn't chosen another limit).
4. **Asset bible** — one `AssetRecord.json` per reusable identity in one approved
   state (character, location, prop, costume). Characters: identity reference,
   full-body + back view, neutral lighting, material detail, living eyes; never bake
   scene grade into an identity asset. Approve only against named evidence.
5. **Performance** — one `performance-bible.json` per recurring character: body
   history, tempo, posture, vocal identity (locked when speaking), signature behavior
   and trigger, social mask and the condition that breaks it, eye life, and a
   scene-independent continuity rule. Direct observable behavior under pressure:
   objective, obstacle, tactic, beats, business, gaze, breath, reaction — never an
   emotion label.
6. **Geography** — one `geography-lock.json` per location: fixed landmarks, entrances,
   depth planes, playable routes, camera-side rule, screen axis and crossing rule,
   primary light direction, character starting positions/facing/gaze/paths/prop
   contact. Re-state the lock in every independently generated shot.
7. **Shot direction** — one `ShotRecord.json` per shot: first-frame occupancy (who/what
   visible, positions, facing, gaze, landmark contact), one format (continuous take or
   explicit cuts), physically possible timed action blocks, camera/lens/light/physics/
   dialogue/sound, constraints, and a performance adaptation per visible character.
   Remove inactive characters, stale references, and prior-scene summaries.
8. **Prompt packet** — `bin/film_advisor.py` builds a complete model-neutral
   `PromptPacket.json` from a `ShotRecord.json` + model profile (sha256-bound).
   It never emits model-specific syntax and never claims a generation happened.
   See `references/model-routing.md` before picking a model.
9. **Iteration** — hypothesis, baseline, one changed variable, observed evidence,
   earliest-failure diagnosis (source asset / geography / performance / direction /
   adapter uncertainty / inconclusive). Log every attempt in `iteration-record.json`.
   Change one causal variable at a time; if repeats fail, simplify the shot or reopen
   the earlier decision.
10. **Post & delivery** — edit for story/continuity with source provenance intact;
    cleanup before grade; unify adjacent shots before applying a scene look; plan
    sound as dialogue, ambience, effects, music; define delivery acceptance, rights,
    and review audience. Issue a `DeliveryReceipt.json` and capture learning as a
    testable change to future planning.

## Approval gates (external-action stop)

I may plan, draft, validate, and classify. I must **stop** before any of these and
name the exact approval evidence required; one approval covers one action and target:

| Action | Minimum approval evidence |
|---|---|
| Paid generation | target surface, cost exposure, approval ID |
| Account sign-in | named account or surface, approval ID |
| Upload | destination, files, approval ID |
| Purchase | vendor, amount/pricing exposure, approval ID |
| Destructive replacement | exact target, recovery plan, approval ID |
| Publication | destination, public/private scope, approval ID |
| Material scope expansion | exact scope delta, cost preview, approval ID |

Without approval, return a stopped result: the blocked action, the required evidence,
and the exact next step. Never claim a live generation, upload, or publication
occurred without matching evidence.

## Personal-input rule

Never invent user-specific data: writing samples, names, business details,
credentials, budgets, or rights holdings. Ask the user; record the answer as a
decided grill field with the user as source.

## Draft / audit / repair / verify

For substantial deliverables, separate these as named phases: I draft, then audit
(read-only review), then perform at most **one bounded repair pass**, then verify.
If verification fails, return to planning or escalate to the user — never run an
uncontrolled repair loop. Use subagents for parallel draft/audit work; I integrate
and issue the final verdict.

## Worked example (illustrative)

Request: "Use AI Film Studio. Brief, vendor asset, stall location and geography lock are
approved. Write shot 1 of the market scene and build its packet." The scene note says the
vendor "looks worried when she realizes the cash tin is gone", and the previous scene
ended with her son at the stall.

- Station: 7 then 8. No grill; every upstream record is approved.
- Judgment: "looks worried" is an emotion label, so direct behavior instead: her hand stops
  on empty wood, eyes drop and then sweep the counter, shoulders stay still for the queue.
  The son is a prior-scene carry-over and is not active, so he is removed. Five seconds
  holds two beats (reach, 0 to 2 s; stop and search, 2 to 5 s); a third beat would crowd it.
  Geography comes from the lock: street-side camera, counter-to-street axis, awning pole
  visible.
- Build (from the skill folder, `$OUT` being the project folder):

  ```bash
  P="$OUT/records/prompt_market_stall_001.json"
  test -e "$P" && echo "exists, choose a new name" || python3 bin/film_advisor.py shot "$OUT/records/shot_market_stall_001.json" generic-video > "$P"
  ```

  Then read `status` in the output. `complete_model_neutral` with an empty
  `compiled_prompt` is correct; `stopped` lists the missing fields.
- Deliver the two records and a stopped result for generation: "Paid generation needs the
  target surface, cost exposure and an approval ID."

A wrong version would ask concept questions the brief already answers, keep the son in
frame, write "she looks worried" as the performance, or say a clip was made.

## When something goes wrong

| Symptom | Likely cause | Next move | Stop when |
|---|---|---|---|
| `film_advisor.py` prints `"status": "stopped"` (exit code is still 0) | Missing fields or an id not matching `shot_[a-z0-9_]+` | Add the named fields or fix the id, then re-run once | the missing field needs a decision nobody made; ask |
| An upstream record is `draft` or absent | Station skipped | Deliver what approved records allow; name the blocking record | the user has not approved it; do not approve it yourself |
| A continuity shot has no approved asset or geography id | Asset bible or lock incomplete | Build the missing record as `draft` for approval | the shot depends on it; report blocked |
| A generation attempt fails repeatedly | Wrong layer changed | Classify the earliest failure (asset, geography, performance, direction, adapter) and change one variable | the failed-attempt budget is spent; simplify the shot or reopen the decision |
| A model-specific syntax question | No formatter here | Keep the model-neutral packet; verify the live surface before use | never emit syntax from memory |

## Completion

- **Station complete:** each requested record exists on disk, traces to approved inputs
  or labeled assumptions, and any helper output reads `complete_model_neutral`.
- **Stopped:** an external action (generation, upload, publication) is next. Return the
  action, the approval evidence it needs, and the exact next step.
- **Blocked:** a required upstream decision or record is missing. Deliver the records
  you could build and name the blocker.

## Output contract

- Records live in a per-project directory (e.g. `~/workspace/film-projects/<project>/records/`).
- Every claim traces to a user decision, a supplied record, or a labelled assumption.
- `FilmBrief.json` status must be `approved` before stations 3–10 proceed.
- Continuity-sensitive shots require approved asset IDs and a geography-lock ID.
- Template and reference locations are listed in `references/stations.md`.
