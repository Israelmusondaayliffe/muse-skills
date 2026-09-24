# Ownership and source boundaries

Loop Observatory owns cross-loop ingestion, normalization, portfolio metrics, and judge calibration. It does not design, execute, schedule, or repair an individual loop.

- **LoopKit runs** are discovered under `$LOOPKIT_STATE_ROOT` (default `~/workspace/loopkit/`), matching the loopkit workspace skill. An explicit `--loopkit-root` path can be supplied instead.
- **External run roots** (anything that is not a LoopKit run directory) are read only from roots recorded by `register-root`. Never scan arbitrary directories for run data.
- Source files are opened for reading and fingerprinting only. The CLI hashes each source tree before and after reading and refuses to normalize a source that changed mid-read.

Repair routing is advisory only. Flagged records are handed to the capability that owns the loop: the `loopkit` workspace skill (Diagnose phase) for LoopKit runs, the `agent-ops` workspace skill for everything else. The repair handoff never claims a repair occurred.

Missing acceptance, token, or cost evidence must remain unknown rather than being inferred. Null in a normalized record means the source provided no trustworthy evidence for that field.
