# Issue Tracker Setup

The flow's skills speak about "the issue tracker" - this is how it maps to a
real surface. Default to **local Markdown**; use a real tracker (GitHub,
GitLab, Linear…) only when already configured and the active task authorizes
creating/changing tracker state.

## Local Markdown conventions

- One feature per directory: `.scratch/<feature-slug>/`
- The spec: `.scratch/<feature-slug>/spec.md`
- Tickets: one file per ticket, `.scratch/<feature-slug>/issues/<NN>-<slug>.md`,
  numbered from `01` in dependency order (blockers first) - never a single
  combined file
- Triage state: a `Status:` line near the top of each issue file (role strings
  in the mapping table below)
- Comments/conversation history: appended under a `## Comments` heading at the
  bottom of the file

## Triage role mapping

The canonical role names; the right-hand column is the actual label string
used on the tracker (edit to match the project's vocabulary):

| Canonical role      | Label string     | Meaning                                  |
|---------------------|------------------|------------------------------------------|
| `needs-triage`      | `needs-triage`   | Maintainer needs to evaluate this issue  |
| `needs-info`        | `needs-info`     | Waiting on reporter for more information |
| `ready-for-agent`   | `ready-for-agent`| Fully specified, ready for an AFK agent  |
| `ready-for-human`   | `ready-for-human`| Requires human implementation            |
| `wontfix`           | `wontfix`        | Will not be actioned                     |

Tickets written for delegation carry the `ready-for-agent` role by
construction.

## Domain docs

Before exploring a codebase for engineering skills, read:

- `CONTEXT.md` at the repo root, or `CONTEXT-MAP.md` (points at one
  `CONTEXT.md` per context - read each one relevant to the topic);
- `docs/adr/` - ADRs touching the area about to be worked on (in
  multi-context repos, also `src/<context>/docs/adr/`).

If any of these don't exist, **proceed silently** - don't flag the absence or
suggest creating them upfront. Domain modeling creates them lazily when terms
or decisions actually resolve.

## External trackers (only when configured and authorized)

- **GitHub**: use the `gh` CLI. `gh issue create --title … --body …`
  (heredoc for multi-line bodies); `gh issue view <n> --comments`;
  `gh issue list --state open --json …` with label filters; `gh issue comment
  <n>`; `gh issue edit <n> --add-label/--remove-label`; `gh issue close <n>
  --comment …`. The repo is inferred from `git remote -v` inside a clone. A
  bare `#42` may be an issue or a PR - check both with `gh pr view` /
  `gh issue view`. PRs are triaged as "an issue with attached code" only if
  the project treats external PRs as a request surface (ask and record the
  answer in the setup config); then list external PRs by `authorAssociation`
  of `CONTRIBUTOR`, `FIRST_TIME_CONTRIBUTOR`, or `NONE`.
- **GitLab / Linear / others**: same state machine and label roles; adapt the
  CLI/API to the tracker's native blocking/sub-issue relationships where it
  has them, otherwise use a "Blocked by" convention in the body.

## Wayfinder map conventions (local Markdown)

- **Map**: `.scratch/<effort>/map.md` with the body sections Destination,
  Notes, Decisions so far, Not yet specified, Out of scope.
- **Child ticket**: `.scratch/<effort>/issues/NN-<slug>.md`, numbered from
  `01`, question in the body. A `Type:` line records
  `research`/`prototype`/`grilling`/`task`; a `Status:` line records
  `claimed`/`resolved`.
- **Blocking**: a `Blocked by: NN, NN` line near the top. A ticket is
  unblocked when everything it lists is resolved.
- **Frontier**: open, unblocked, unclaimed tickets; first by number wins.
- **Claim**: set `Status: claimed` and save *before* any work, so concurrent
  sessions skip it.
- **Resolve**: append the answer under an `## Answer` heading, set `Status:
  resolved`, then append a one-line gist plus path link to the map's
  Decisions so far.
