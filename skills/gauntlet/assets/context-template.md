# CONTEXT.md: {{run_id}}

This file is append-only and permanent. Never edit an existing entry in place. Corrections are appended to the decision log with a date and a reason. Every session reads this file first.

## What this project is

- Goal, one line: {{goal_one_line}}
- What is being made, for whom, and why now: {{project_description}}
- Domain, primary: {{domain_primary}}
- Execution shape: {{execution_shape}}
- Run directory, absolute: {{run_dir_abs}}

## The bar

- Bar definition: {{bar_definition}}
- Why this comparator is fair: {{bar_rationale}}
- Bar files and reference paths: {{bar_paths}}
- How the bar is inspected: {{bar_inspection_method}}
- Rubric hash, if a frozen rubric is used, else "none": {{rubric_hash}}

## Decision log (append-only)

One dated entry per decision, newest last. Append corrections as new entries; never rewrite an old one.

### {{YYYY-MM-DD}}: {{decision_title}}

- Decision: {{what_was_decided}}
- Reason: {{why_it_was_decided}}
- Recorded by: {{session_or_agent}}

### {{YYYY-MM-DD}}: {{decision_title}}

- Decision: {{what_was_decided}}
- Reason: {{why_it_was_decided}}
- Recorded by: {{session_or_agent}}
