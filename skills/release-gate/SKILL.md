---
name: release-gate
description: Use when the user says 'run the release gate', 'gate this release', or asks whether a skill change is safe to merge or install. User-invoked only; never auto-dispatched.
---

# Release Gate

A standardized pre-merge and pre-install verification for skill changes. Distilled
from real rebuilds: the knowledge-work and matt-pocock rebuilds shipped only after
validator checks, hash verification, drift checks, and two reviewer passes
(fidelity and mechanics) all came back clean. One gate run produces one verdict:
GO or NO-GO.

## Invocation

User-invoked only. This skill never auto-dispatches.

## Inputs

- TARGET_REPO: path to a local clone of the repo under review
- REF: the target ref (branch, tag, or commit) being gated
- MODE: `repo` (gating a repo change) or `install` (gating a local install)
- INSTALL_PATH: required in install mode, the installed skill directory
- TARGET_COMMIT: required in install mode, the repo commit the install must match
- TRACK_UPSTREAM: true only when this release claims to track pinned upstream sources exactly; otherwise pins are advisory
- REVIEW_BASE: in repo mode, the ref the review set is diffed against. The
  review set is the `REVIEW_BASE..REF` range limited to `skills/`. Default:
  the most recent commit reachable from REF, excluding REF itself, that
  changed `skills/`: `git log --format=%H -n 1 REF^ -- skills/`. If no such
  commit exists, use the empty tree (4b825dc642cb6eb9a060e54bf8d69288fbee4904).
- REVIEW_FILES: explicit file list. When provided, it is the review set and
  REVIEW_BASE is ignored.

The judgment checks review exactly the review set defined above; never let a
reviewer improvise it.

Run all five checks in the order below. Collect every failure and report them
all in the verdict. One exception: a repo-mode tree mismatch in the hashes
check aborts the gate immediately, because nothing downstream can be trusted
once the pushed tree is not the reviewed tree.

## Checks

1. **validate** (deterministic): dispatch `subagents/gate-validate.md`. Runs
   `tools/validate_collection.py` against the candidate tree. Passes only when
   the validator reports zero errors. It checks frontmatter presence and naming
   (`name` matching the folder in lowercase-hyphen form, `description` present),
   that relative Markdown links resolve, and that backtick package paths exist.
   It is a structural check, not evidence of skill quality.

2. **hashes** (deterministic): dispatch `subagents/gate-hashes.md`. Compares
   file hashes between the candidate tree and the install target (or the approved
   manifest). Every file must match. Passes only with zero mismatches.

3. **drift** (deterministic): dispatch `subagents/gate-drift.md`. Flags
   uncommitted changes, commits on the gated ref that are not pushed, ref
   ancestry divergence from the remote counterpart, and pinned upstream
   sources that have moved. Passes only when the tree is clean, the ref is
   fully pushed, and no pin drift contradicts the release's claims.

4. **review-fidelity** (judgment): dispatch `subagents/gate-review-fidelity.md`
   with the review set (REVIEW_BASE and REF, or REVIEW_FILES). A reviewer
   reads exactly that review set against its intent and source material
   and flags meaning drift, invented content, or missing behavior. Passes only
   when nothing in the review contradicts the intended behavior.

5. **review-mechanics** (judgment): dispatch `subagents/gate-review-mechanics.md`
   with the review set (REVIEW_BASE and REF, or REVIEW_FILES). A reviewer
   checks mechanics on exactly that review set: zero em dashes, frontmatter
   `name` and `description` conventions, invocation rules (router skills
   explicit-only), and link and path hygiene. Passes only when nothing in
   the review contradicts the house rules.

The validate check runs the gated repo's own `tools/validate_collection.py`.
The hashes and drift checks run via this skill's `bin/` scripts
(`bin/gate_hashes.py`, `bin/gate_drift.py`). Judgment checks run via the
reviewer briefs in `subagents/`.

## Does not cover

This gate does not execute shipped code. A script that compiles and links
cleanly can still carry a runtime defect on one CLI path (this happened with
an installer argparse attribute), and no check here runs it. Runtime behavior,
performance, and anything outside `skills/` (for example `tools/`) are out of
scope. Say so in the report rather than implying coverage.

## Verdict

**GO**: every check passed with zero failures.

**NO-GO**: one or more checks failed. Name each failure as file + check +
what failed, with evidence.

## Report

Produce the verdict using the template in `references/go-no-go-report.md`.
Record the exact review set the judgment checks used: the REVIEW_BASE value
(or REVIEW_FILES list) and the resulting file list. Report blockers plainly;
never invent evidence.
