---
name: capability-operator
description: Operate Muse's capability inventory on Hatch. Routes ambiguous or multi-domain requests to the right workspace skill, inventories ~/workspace/skills/, audits for duplicate or overlapping skills, and verifies new skills are discoverable. Use when a request could be handled by more than one skill, before creating or installing a skill, when consolidating skills, or when auditing which skills are available and why. Explicit user selections always win.
---

# Capability Operator

Keep Muse's capabilities intentional: know what skills exist, pick one primary route per request, find duplicates and trigger collisions, and confirm new skills are discoverable.

A routing request is finished when one primary skill owns it and work has started there. An audit is finished when every overlap group has a state from `references/classification.md` and every trigger collision has quoted trigger text and a recorded decision. Nothing is deleted or merged without the user's authorization.

## Start here

| The request | Do this first |
|---|---|
| The user named a skill or method | Use it. Explicit selection wins; do not re-route. |
| A narrow action with one obvious owner | Go straight to that skill; no router needed. |
| Ownership unclear, or the request spans domains | Check the reviewed collisions in `references/routing-policy.md`, then pick one primary route. |
| "What skills do I have", before creating or installing a skill, consolidation | Build an inventory. |
| "Are any of these duplicates / overlapping" | Inventory, then the overlap audit. |
| "Is my new skill working" | Discoverability check. |

## Route one request

1. Pick exactly one primary route. Read only that skill's `SKILL.md`; load companions only at a documented handoff.
2. For data work, choose the connector that owns the data first, then the workflow skill. Connector choice does not decide workflow ownership.
3. Record a collision decision when two skills fit: the distinguishing phrase, `primary`, `companions`, `excluded_routes`, and a one-line `reason` (`references/routing-policy.md`).
4. A route that reaches an owner is final. If that skill says the request is not its job, name the reviewed owner once; never bounce the request back.
5. No skill fits: say so and ask which route to take; do not invent ownership.

## Inventory and overlap audit

Run from this skill's directory. Both scripts overwrite their output path, so each audit writes into a new folder:

```bash
D=~/workspace/scratch/capability-audit-$(date +%Y%m%d-%H%M%S) && mkdir -p "$D"
python3 scripts/collect_inventory.py --skills-root ~/workspace/skills --output "$D/inventory.json"
python3 scripts/find_overlaps.py "$D/inventory.json" "$D/overlap-report.json"
```

- `collect_inventory.py` is read-only. It records name, path, SHA-256 of each `SKILL.md`, and the description. It exits 1 when any `SKILL.md` has missing or malformed frontmatter, and still writes the inventory; report each error. `--include-bundled` adds `/opt/hatch/skills` read-only.
- `find_overlaps.py` finds exact-name groups only. Classify each with `references/classification.md` (`identical-mirror`, `drifted-copy`, `cross-layer`, `superseded`, `unresolved`).
- Trigger collisions need judgment: read descriptions side by side and record `trigger-collision` with both trigger strings quoted.
- Never delete or consolidate without explicit authorization and a saved copy of the current inventory.

## Discoverability check

1. `SKILL.md` exists with frontmatter `name` (matching the folder, lowercase-hyphen) and a `description` that says what it does and the phrases that should find it.
2. The trigger phrases match how the user actually asks; a generic description fails.
3. Re-run the overlap audit for collisions.
4. File presence is not discovery. Ask the user to start a fresh session, or use the host's skill listing if one exists, and confirm the skill appears. Until then report it as "installed, discovery unconfirmed".

## Worked example (illustrative, synthetic)

Request: "Audit this skills folder and tell me who should own 'grill me on this pricing decision'." Folder holds `essay-editor`, `essay-editor-v2`, `decision-grill`, `pricing-coach`, `meeting-notes`.

- Inventory: 5 skills, exit 1 because `meeting-notes/SKILL.md` has no frontmatter; report it as not discoverable until fixed.
- Overlaps: one exact-name group `essay-editor` in two folders with different hashes: `drifted-copy`. Recommend reviewing both and naming a canonical one; do not pick by folder name or recency.
- Collision by reading: `decision-grill` claims "grill me", `pricing-coach` claims "grill me on pricing". Judgment: the request is about a price, and "on pricing" is the distinguishing phrase. Primary `pricing-coach`; companions none; excluded `decision-grill` (it owns general decision pressure-tests); reason: "the pricing phrase is specific to pricing-coach's owned job".
- No files changed.

A wrong version would report only the exact-name group, name two primaries, or recommend deleting `essay-editor-v2` because it looks newer.

## When something goes wrong

| Symptom | Likely cause | Next move | Stop when |
|---|---|---|---|
| `collect_inventory.py` exits 1 | Malformed frontmatter in some `SKILL.md` | Report each error; audit the rest | never "fix" skills during an audit |
| `find_overlaps.py` prints usage | Wrong argument count | Pass `INVENTORY.json OUTPUT.json` | valid |
| Inventory disagrees with what a search shows | Stale inventory or a different root | Re-run the inventory for the root in question | still disagrees: report both |
| Two skills both claim the request | Trigger collision | Record one decision with the distinguishing phrase | no phrase separates them: ask the user |
| New skill missing after install | Not reloaded, or bad frontmatter | Check frontmatter, then a fresh session | still missing: report discovery unconfirmed |

## Operating rules

- Inventory and audit are read-only. Changing skills is separate, explicitly authorized work.
- Do not load the full inventory into context to route one request.
- Never infer that one skill supersedes another from recency alone.

## Resources

- `scripts/collect_inventory.py` (read-only inventory), `scripts/find_overlaps.py` (exact-name groups).
- `references/classification.md` (overlap states, disposition rules), `references/routing-policy.md` (collision decisions, reviewed collisions, handoffs).
