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
an incidental reference, or ordinary filmmaking conversation.

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

## Output contract

- Records live in a per-project directory (e.g. `~/workspace/film-projects/<project>/records/`).
- Every claim traces to a user decision, a supplied record, or a labelled assumption.
- `FilmBrief.json` status must be `approved` before stations 3–10 proceed.
- Continuity-sensitive shots require approved asset IDs and a geography-lock ID.
- Template and reference locations are listed in `references/stations.md`.
