---
name: last30days
description: "Research what people have actually said about any topic in the last 30 days: recent social, community, market, and web signals with honest source coverage. Runs single-topic research, A-vs-B comparisons, trend discovery, recurring topic watchlists, and daily/weekly briefings. Use when the user asks what's new about a topic, wants community sentiment, wants to compare options, asks what's trending, or wants ongoing monitoring with briefings."
---

# Last30Days (native workspace skill)

## Purpose
Produce honest, recency-disciplined research: what people, communities, and markets have said about a topic **inside the last 30 days**. Separate fresh evidence from stale background, and name sources that failed instead of calling them quiet. No credentials needed for the default lanes.

## Route the request
First, fix the window: today's date and the date 30 days earlier. Every recency label uses these two dates.
- Fresh topic research and A-vs-B comparisons: **Workflow: Research** below.
- "What's trending / what's new in <domain>" with no single topic: **Workflow: Discovery**.
- The user supplied saved lane output (API JSON, fetched page text, a collection log) or said not to search live: **Research** from those files only. Each file is a lane; its log line decides returned evidence / returned nothing / failed. Do not add live searches.
- "Monitor X / add a topic / what's changed": **Workflow: Watchlist**.
- "Morning brief / weekly summary of my topics": **Workflow: Briefing**.
- "Something isn't working / which sources can I use": **Workflow: Health**.
- Compound request: health, then research, then watchlist update, then briefing, in that order. Skip health when research can proceed normally.

## Workflow: Research

### 1. Get a real topic
- No topic given: ask one short question. Do not research, do not run searches, just ask.
- Keyword trap (see `references/query-preflight.md`: gift-shopping phrases, numeric/age traps, how-to concepts, generic single nouns): reframe or ask ONE clarifying question before the sweep.
- Person topic (founder, creator, CEO): resolve their social handle, GitHub username, and home subreddits first via web search; ask the user if ambiguous rather than guessing.

### 2. Sweep sources in the 30-day window
Work the lanes that fit the topic; you don't need every lane every time. Prefer keyless APIs first, then my search tools, then (with explicit consent) the live browser for logged-in sources. Exact commands and endpoints live in `references/sources.md`.
Track every lane as one of: **returned evidence / returned nothing / failed**. Failures go in the coverage note; never silently dropped, never relabeled as "quiet".
- Web and news: `browser.search` with a recency filter, `browser.open` for page text. Undated or older-than-30-days pages are background, not evidence - label them.
- Social listening: `social.search` for what people are posting (covers public posts on platforms that skill supports).
- Hacker News: Algolia `search_by_date` with `numericFilters=created_at_i>{epoch_30_days_ago}`.
- GitHub: `api.github.com/search/issues` with `created:>YYYY-MM-DD` (60 unauthenticated req/hr; `GITHUB_TOKEN` raises it).
- Polymarket: Gamma `public-search` for prediction-market sentiment on the topic.
- Reddit: direct `.rss`/`.json` from this VM is blocked; use `social.search`, `browser.search`, and `browser.open` instead.
- YouTube / TikTok / X logged-in views: ask the user first, then delegate a live-browser task to the parent agent. I cannot drive the user's logged-in browser myself.
- Tech news river: Techmeme RSS via curl.

### 3. Synthesize per the Output Contract
- Corroborate: a claim carried by two or more independent sources beats one viral post. One angry thread is one angry thread, not a trend.
- Engagement without a verified date is not evidence of recency: present an item as "last 30 days" only if you verified its date.
- Never invent quotes, handles, numbers, or citations. If a detail can't be traced to a fetched page or API response, say so.

## Workflow: Discovery (what's trending)
1. Sweep HN front page, the Techmeme river, and web/social search for the domain; nominate candidate topics.
2. Give each nomination a quick research pass before ranking it.
3. A thin or empty result is valid: report "nothing solid in this window" honestly. Never retry around it or fabricate topics.

## Workflow: Watchlist (recurring monitoring)
State lives at `~/workspace/last30days/watchlist.json` unless the task names another folder. Layout, a safe add command and the delta order are in `references/watchlist.md`. Never invent topics.
- `add "TOPIC"`: add it without disturbing existing topics, run Research, and save dated findings to `topics/<slug>/<YYYY-MM-DD>.md`. Create a cron job only when the user asked for daily or weekly runs.
- `delta "TOPIC"`: compare the newest findings file with the previous one. Report new items, engagement changes (old and new values), and coverage changes first.
- `list` / `remove "TOPIC"` (confirm the exact topic first) / `pause`.
- Delivery: briefings arrive as Feed units or chat messages by default. Webhooks or any other external send need explicit user approval naming the destination.

## Workflow: Briefing
1. Read findings in `~/workspace/last30days/` since the last briefing.
2. Present in this order: (1) important new findings and notable engagement changes, (2) topics with failed, stale, or partial collection, (3) coverage summary, (4) no-change topics compressed into one short line.
3. No topics on the watchlist: say so and point to the Watchlist workflow. Never fabricate a briefing.
4. Offer to schedule it daily or weekly via cron.

## Workflow: Health
Run the connectivity checklist with `muse.exec` + curl (see `references/sources.md` for the exact probes):
- Report each lane as: **working / failed / not configured**. A configured-but-unverified source is not healthy until it returns real data.
- Optional tools (`yt-dlp`, `gh` CLI): describe the install command and destination first, get user approval before installing anything.

## Worked example (illustrative)

Topic "heat pumps in cold climates", today 2026-09-25, window from 2026-08-26. Lanes: social search returned a dozen dated posts, the web lane three pages (one dated 2026-06-02, one undated), HN one thread, GitHub was skipped as irrelevant, Reddit failed with a "Blocked" page, and Polymarket returned zero markets.

- Evidence: the social posts and the HN thread are dated in window. The June page is background: useful for how defrost cycles work, not "recent". The undated page is neither.
- Pattern judgment: "defrost cycles are louder than owners expected" appears in several unrelated social posts and a dated installer blog, so it is a pattern. One viral post claiming a 60% bill cut is one post, cited as that, not a trend.
- Coverage note: "social, web, HN returned evidence; Polymarket returned nothing; Reddit failed (blocked); GitHub skipped." Reddit is not "quiet".

A wrong version would list the June page among this month's findings, say Reddit had no discussion, or repeat the 60% figure as typical savings.

## When something goes wrong

| Symptom | Likely cause | Next move | Stop when |
|---|---|---|---|
| A lane returns a "Blocked" page or HTTP 403/429 | Egress block or rate limit | Record it as failed; use another lane from `references/sources.md` | never retry the same blocked endpoint in a loop |
| Items have no date | Page or API omits it | Treat them as background; say so | never present them as last-30-days evidence |
| Every lane returns nothing | Quiet topic or a bad query | Try one reframed query (`references/query-preflight.md`) | second empty sweep; report "nothing solid in this window" |
| Watchlist file will not parse | Corrupt or hand-edited state | Leave it untouched and report the error | always; do not overwrite user state |
| User asks for a briefing with no watched topics | Empty watchlist | Say so and point to Watchlist | never fabricate a briefing |

## Completion

Done means the requested answer follows the Output Contract, every "recent" claim cites a dated item inside the window, and the coverage note names each lane's outcome. For watchlist work, the state file and dated findings exist in the state folder, and any cron job created was requested. If a lane or step is blocked, deliver the rest and name it.

## Output Contract
- First line: `📰 last30days · synced {YYYY-MM-DD}`, one blank line, then `What I learned:` followed by bold-lead-in paragraphs, then `KEY PATTERNS from the research:` and a numbered list. No invented title lines, no `##` section headers in a general-topic body.
- Comparison queries: title line `# {A} vs {B}: What the Community Says (last30days)`, then Quick Verdict, per-entity notes, Head-to-Head, Bottom Line.
- End every response with the coverage note (which lanes returned evidence, which returned nothing, which failed) and one invitation: deeper dive, add to watchlist, or compare.
- Use ` - ` instead of em/en dashes except inside direct quotes.
- Citations: inline links on claims; no trailing link-dump block.

## Auth
No credentials required for the default keyless lanes. Optional: `GITHUB_TOKEN` via the Secure Vault for higher GitHub rate limits. Browser-cookie access and any logged-in scraping: ask first, never read cookies without explicit consent. Never print secrets, cookie values, or keys.

## Operating Rules
1. Read-only by default. Ask before: installing tools, reading browser cookies, saving credentials, publishing anything publicly, or sending data to a webhook.
2. Do not present background older than 30 days as current evidence; label it as background.
3. Do not call a source "quiet" when it failed, timed out, or was never configured.
4. Keep user research data in `~/workspace/last30days/`, never inside this skill directory.
5. Ask the user for personal input (handles, subreddits, business details, preferences) instead of guessing.
