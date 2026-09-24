# Attribution

This workspace skill is a native adaptation of the **last30days** plugin published at
https://github.com/Israelmusondaayliffe/plugins (directory `plugins/last30days/`),
which pins the MIT-licensed research engine by Matt Van Horn
(`mvanhorn/last30days-skill`, v3.16.0, commit `249c7a4c040558a903d6838dee31012980d4946d`).

The original engine (`scripts/last30days.py` and its `scripts/lib/` tree, including the
vendored `bird-search` component) was NOT ported: it requires Python 3.12+ runtime
management, API keys the user does not have (ScrapeCreators, Perplexity, Brave, Apify,
etc.), browser-cookie extraction, and Codex/Claude Code/Claude Cowork host hooks and
manifests, none of which apply to this host. Only the methodology (query preflight,
multi-source 30-day sweep, watchlists, briefings, output contract) was adapted to the
capabilities actually available here: Linux terminal with curl, web search and page
fetching, social search, cron, subagents, and workspace files.

The five wrapper workflows of the original (research, health, watchlist, briefing,
router) are consolidated into the single native `SKILL.md` above.
