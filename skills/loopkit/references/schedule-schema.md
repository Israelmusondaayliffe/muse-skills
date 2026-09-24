# Schedule record (Hatch adaptation)

```json
{
  "cadence": "User-approved cadence and timezone",
  "task_prompt": "Self-contained task prompt with workspace and run directory",
  "manual_tested_at": "UTC timestamp of successful manual test",
  "stop_condition": "When the schedule must pause or be removed",
  "no_op_behavior": "What to return when nothing meaningful changed",
  "evidence_return": "What proof each meaningful run returns",
  "ui_dependencies": [],
  "cron_job_id": null,
  "schedule_surface": "hatch-cron"
}
```

The scheduling step adds `schema_version` and `updated_at`. On Hatch the scheduling surface is the cron tools (`cron.add`, `cron.list`, `cron.update`, `cron.remove`); record the real `cron_job_id` only after the job is actually created. The original plugin's `codex_schedule_id` field is renamed here; older runs carrying it can still be read.
