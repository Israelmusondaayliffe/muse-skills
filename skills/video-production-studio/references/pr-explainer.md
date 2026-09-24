# PR explainer

Route `pr-story`: turn a GitHub pull request into a code-change explainer
(up to ~3 min). Input is a code change read with `gh`, not a website.

## Step 0 — Ingest

Get the PR ref (URL, `owner/repo#N`, or the checked-out PR). Peek once to
ground the brief:

```bash
gh pr view <PR_REF> --json title,additions,deletions,changedFiles
```

Recommend length from change size (hard cap ~3 min):

| Change size | Recommended length |
|---|---|
| trivial (≲ 50 lines) | ~20–40s |
| focused (~50–200 lines) | ~40–70s |
| substantial (~200–600 lines) | ~70–110s |
| large (≳ 600 lines, or 25+ files) | ~110–180s |

Confirm angle with the user: changelog / feature-reveal / fix-explainer /
refactor-walkthrough (default: infer from the PR). A huge PR with one
headline change still gets a tight video — say so.

## Step 1 — Understand the change

```bash
gh pr diff <PR_REF> > capture/pr.diff
gh pr view <PR_REF> --json title,body,author,commits,files > capture/pr.json
```

Read the diff, not just the title. The story is: what broke or what was
missing → what changed → what it enables. PR facts are read once at author
time and baked in — no live data at render.

## Step 2 — Storyboard + script (user gate)

Beat structure that works for code changes:

1. Hook — the problem in one sentence.
2. Before — the old behavior (minimal code or diagram).
3. The change — the diff's key hunks, narrated as decisions not lines.
4. After — the new behavior, demo or diagram.
5. Impact — who benefits, what to try.

Render code as images (syntax-highlighted screenshot or generated still),
never as AI-video text — generators mangle code. Keep snippets short
(≤ 10 lines per beat).

## Step 3 — Build and deliver

Follow references/shared-pipeline.md Stages 3–7: voiceover, visual build
(code stills + diagrams + AI B-roll), assemble, QC. Avatars: contributors'
GitHub avatars may be used for attribution beats.
