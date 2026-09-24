# Contract fields

- `goal.title`: short run label.
- `goal.outcome`: observable finished state.
- `evidence.machine_checks`: commands that return an exit code and can be rerun under recorded conditions. The model runs them with `muse.exec`; the scripts never execute them.
- `evidence.judgment_criteria`: human or independent-review criteria that machine checks cannot decide.
- `boundaries.allowed_paths`: locations the run may read or change within the active task's authority.
- `boundaries.forbidden_paths`: explicit exclusions.
- `boundaries.external_actions`: actions that remain approval-gated or forbidden (sends, purchases, deletions, production changes, privacy-sensitive access).
- `iteration.max_iterations`: hard cap supplied or approved by the user.
- `iteration.no_progress_limit`: consecutive no-progress cap supplied or approved by the user.
- `stops`: plain-language rules for success, failure, blocked, and exhausted states.
