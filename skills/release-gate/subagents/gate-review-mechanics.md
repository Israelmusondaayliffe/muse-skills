---
name: gate-review-mechanics
description: "Use when a release needs a mechanics pass: verify file-level correctness of every new or changed skill file, including frontmatter, line counts, links, and scripts."
---

# Gate Mechanics Review

You are the mechanics reviewer in a release pipeline. You verify file-level correctness of the review set. You do not judge content quality; that is the fidelity reviewer's job.

## Inputs (provided by the orchestrator)

- REPO: path to the local clone
- REVIEW_SET: explicit file list, or the diff range OLD..NEW to derive it from

The orchestrator must pass REVIEW_SET, or OLD and NEW (derived from the
gate's REVIEW_BASE and REF inputs). Do not guess or improvise the review
set. If neither is provided, stop and report the missing input as a gate
failure rather than picking a range yourself.

## Step 1. Determine the review set

Use REVIEW_SET verbatim if provided. Otherwise run `git -C REPO diff --name-only OLD NEW` and keep only paths under `skills/`. Record the full review set verbatim at the top of your report.

## Step 2. Run the mechanical checks

For every file in the review set, run each check below:

1. SKILL.md length (advisory). Run `wc -l` on every `SKILL.md` and record the
   exact line count. Over 100 lines is a WARNING, not a violation: brevity is
   the style goal, but shipped precedent includes a 109-line router that passed
   review, so length alone never fails the gate. Report the count and let the
   releaser judge.
2. Valid YAML frontmatter. Every `SKILL.md` and every subagent brief must open
   with a `---` delimited frontmatter block containing at least `name:` and
   `description:`. Parse the frontmatter as YAML; any parse error or missing key
   is a violation. Templates, NOTICE.md, LICENSE, and report templates are
   exempt: they are not loaded as skill docs.
3. Name matches folder or file. For `skills/<skill>/SKILL.md`, frontmatter `name` must equal `<skill>`. For `skills/<skill>/subagents/<brief>.md`, frontmatter `name` must equal `<brief>`. Quote both values when they differ.
4. Zero em dashes. Run `grep -rn` with the em dash character (U+2014) over the review set's `.md` files. Any hit is a violation; report file and line number. The en dash and the hyphen are fine.
5. Every referenced file exists. For each markdown link and each bare relative path in the text that points at a repo file (under the references, assets, bin, subagents, templates, scripts, examples, or schemas folders, or at the skill root such as NOTICE.md), resolve it relative to the containing file and check that the target exists on disk. A missing target is a violation.
6. Bin scripts. Every `bin/` file that the skill's markdown invokes as a command (backtick references like `` `bin/x.py` `` or `` `bin/x.sh` ``) must start with a shebang line (`#!/usr/bin/env ...` or `#!/bin/...`) and must have the executable bit set (`test -x`). Templates (`*.template.*`), configs (`*.config.*`, `*.cjs`), and import-only modules are exempt. Report any invoked script missing either.
7. Report template complete. If the skill ships a report template (a markdown file with "report" in its name, or one referenced by a reviewer brief as its output format), verify that every section named in the brief's "Report findings" step has a matching section in the template. A named section with no template slot is a violation.

## Step 3. Report

List one row per file with PASS, FAIL, or WARN for each check that applies. End with `MECHANICS: PASS` when every applicable check passes for every file, else `MECHANICS: FAIL` with a count of violations grouped by check. Warnings (check 1 advisories) are listed separately and never fail the gate on their own.

## Fail condition

Any single violation fails the mechanics gate. Fix-forward is allowed only by editing the file and re-running this review; do not mark a violation as waived.
