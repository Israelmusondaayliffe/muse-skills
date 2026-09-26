# Watchlist state

Default state folder: `~/workspace/last30days/`. A task may name another folder; use it for every read and write in that task. Never write state inside this skill folder.

```
<state>/watchlist.json                     {"topics": [{"topic", "slug", "schedule", "added"}]}
<state>/topics/<slug>/<YYYY-MM-DD>.md      one findings file per run
```

`schedule` is `null` unless the user asked for recurring runs (`"daily"` or `"weekly"`).

## Add a topic without losing existing ones

Run with `STATE` set to the watchlist path. It creates the file when absent, keeps every existing topic, and refuses to add a duplicate. A malformed existing file makes it stop with an error instead of overwriting.

```bash
STATE="$HOME/workspace/last30days/watchlist.json" TOPIC="heat pumps in cold climates" python3 - <<'EOF'
import json, os, re, datetime
path, topic = os.environ["STATE"], os.environ["TOPIC"]
data = json.load(open(path)) if os.path.exists(path) else {"topics": []}
slug = re.sub(r"[^a-z0-9]+", "-", topic.lower()).strip("-")
if any(t["slug"] == slug for t in data["topics"]):
    print("already watched:", slug)
else:
    data["topics"].append({"topic": topic, "slug": slug, "schedule": None, "added": datetime.date.today().isoformat()})
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp, path)
    print("added:", slug)
EOF
```

Create the state folder first (`mkdir -p`). Save each run's findings as `topics/<slug>/<today>.md`; if that file already exists, append a run suffix (`-2`) rather than overwrite.

## Scheduling

Only when the user asks for recurring monitoring: set `schedule`, then create one cron job that re-runs the Research workflow for that topic and writes the dated findings file. Report the job you created. Removing a topic removes its cron job; confirm the exact topic first.

## Delta

Compare the newest findings file with the previous one for the same slug:

1. New items: present now, absent before (match on item id or URL).
2. Engagement changes on items present in both (points, comments), with old and new values.
3. Coverage changes per lane (for example, "github: nothing to evidence", "web: not run to evidence").
4. Items that dropped out of the 30-day window.

Report them in that order, before a short line for no-change items.
