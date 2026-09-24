---
name: capability-operator
description: Operate Muse's capability inventory on Hatch. Routes ambiguous or multi-domain requests to the right workspace skill, inventories ~/workspace/skills/, audits for duplicate or overlapping skills, and verifies new skills are discoverable. Use when a request could be handled by more than one skill, before creating or installing a skill, when consolidating skills, or when auditing which skills are available and why. Explicit user selections always win.
---

# Capability Operator

Keep Muse's capabilities intentional: know what skills exist, pick one primary route per request, avoid duplicates, and make sure new skills are actually discoverable.

## Workflow

### 1. Route an ambiguous request

When ownership is unclear, several skills could fit, or a request spans domains:

1. Honor an explicit user selection as the operating method. Never override it.
2. Route a narrow action straight to the narrow skill; no router needed.
3. Pick exactly **one primary route** — never several equal primaries. One request gets one primary route.
4. Read only the primary skill's SKILL.md (progressive disclosure). Load companions only at a documented handoff.
5. For data work, choose the data-owning connector first, then the workflow skill. Connector choice does not decide workflow ownership.
6. See `references/routing-policy.md` when skills collide or a request spans domains.

### 2. Build an inventory

Run before any skill creation, consolidation, or audit, and after installs:

```bash
python3 scripts/collect_inventory.py \
  --output /tmp/capability-inventory.json
```

Use `--skills-root` to scan a different directory (default: `~/workspace/skills`). Add `--include-bundled` to also list bundled skills under `/opt/hatch/skills` read-only. The collector is read-only: it records name, path, SHA-256 fingerprint of each SKILL.md, and the frontmatter description, and reports missing or malformed frontmatter as errors.

### 3. Audit for overlaps

1. Build a fresh inventory (step 2).
2. Run `python3 scripts/find_overlaps.py /tmp/capability-inventory.json /tmp/overlap-report.json`.
3. Classify each group with `references/classification.md`.
4. For different names that claim the same user intent, record a **trigger-collision** with cited trigger text — the script only finds exact name matches; semantic overlap needs judgment.
5. Never delete or consolidate without explicit user authorization and a backup of the current inventory.

### 4. Verify a new skill is discoverable

After creating or updating a workspace skill:

1. Confirm `SKILL.md` exists with valid frontmatter: `name` and a `description` that names what it does and the trigger phrases that should find it.
2. Confirm the description's trigger phrases match how the user actually asks for the work — discovery follows the description, so generic descriptions are a failing gate.
3. Re-run the overlap audit to confirm the new skill collides with nothing.

## Operating Rules

- Inventory and audit operations are read-only. Changing skills is separate, explicitly authorized work.
- Do not treat filesystem presence as proof that a skill is discoverable or installed correctly — check its frontmatter and run the discovery check.
- Do not load the full inventory into context when only routing one request.
- Never infer that a newer or older skill supersedes the other from recency alone.
- When the inventory disagrees with what a search returns, re-run the inventory before acting; do not guess.

## Resources

- `scripts/collect_inventory.py` — read-only skill inventory.
- `scripts/find_overlaps.py` — exact-name overlap groups.
- `references/classification.md` — overlap states and disposition rules.
- `references/routing-policy.md` — collision and handoff policy.
