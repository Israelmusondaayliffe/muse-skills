# Normalized terminal run schema

Each normalized record contains:

- `record_id`, `engine`, `run_id`, `source_path`, and `source_hash`
- `goal`, `status`, `terminal`, `iteration`, and `duration_seconds`
- `machine_completion` and `human_acceptance`, each boolean or null
- `tokens` and `cost`, each numeric or null
- `stop_reason`, `escalation_reason`, `judge_verdict`, and `human_label`
- `ingested_at`

Null means that the source did not provide trustworthy evidence. A cost-per-accepted-result metric is valid only when accepted results and their costs are both known.
