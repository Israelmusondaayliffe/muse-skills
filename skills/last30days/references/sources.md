# Source Coverage Cookbook

Verified from the Hatch VM on 2026-09-23. Endpoints marked "keyless" need no API key. Everything below is read-only HTTP GET.

## 30-day window helpers

```bash
EPOCH30=$(date -d "30 days ago" +%s)      # for numericFilters on Algolia
DATE30=$(date -d "30 days ago" +%Y-%m-%d)  # for created:> qualifiers
```

## Hacker News (keyless, Algolia)

```bash
# Stories from the last 30 days
curl -s -m 20 "https://hn.algolia.com/api/v1/search_by_date?query=QUERY&tags=story&numericFilters=created_at_i>$EPOCH30&hitsPerPage=30" -A "Mozilla/5.0" | python3 -c "
import json,sys
for h in json.load(sys.stdin)['hits']:
    print(h['created_at'][:10], h['points'], h['num_comments'], '-', h['title'][:90], '|', h['url'] or 'https://news.ycombinator.com/item?id='+str(h['objectID']))"

# Front page right now (discovery)
curl -s -m 20 "https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=20" -A "Mozilla/5.0" | python3 -c "
import json,sys
for h in json.load(sys.stdin)['hits']:
    print(h['points'], '-', h['title'][:90], '|', h['url'])"
```

## GitHub issues/PRs (keyless, 60 req/hr unauthenticated)

```bash
curl -s -m 20 "https://api.github.com/search/issues?q=QUERY+created:%3E$DATE30&sort=created&order=desc&per_page=20" \
  -H "Accept: application/vnd.github+json" -A "Muse" | python3 -c "
import json,sys
d=json.load(sys.stdin)
print('total:',d.get('total_count'))
for i in d.get('items',[]):
    print(i['created_at'][:10], i['comments'], '-', i['title'][:90], '|', i['html_url'])"
```

## Polymarket (keyless Gamma API)

```bash
curl -s -m 20 "https://gamma-api.polymarket.com/public-search?q=QUERY" | python3 -c "
import json,sys
for e in json.load(sys.stdin).get('events',[])[:10]:
    mk=e.get('markets',[{}])[0]
    print(e['title'][:80], '| prob:', mk.get('lastTradePrice'), '|', 'https://polymarket.com/event/'+e['slug'])"
```

## Techmeme river (keyless RSS)

```bash
curl -s -m 20 "https://www.techmeme.com/feed.xml" -A "Mozilla/5.0" | python3 -c "
import sys,xml.etree.ElementTree as ET
for it in ET.fromstring(sys.stdin.read()).find('channel').findall('item')[:20]:
    print(it.findtext('pubDate')[:16], '-', it.findtext('title')[:90])"
```

## Reddit (VM network blocked for direct curl)

- Do NOT curl `reddit.com/.rss` or `/.json` from `muse.exec`: the VM egress is blocked (serves a "Blocked" page).
- Use `social.search` (public Reddit posts surface there), `browser.search` with `site:reddit.com` and a recency filter, and `browser.open` on specific thread URLs.
- Engagement figures from third-party summaries are approximate: label them as such.

## Web, news, and background (no key)

- `browser.search` with the `since:` filter for the recent window; `browser.open` to read full pages.
- Supplement with the image search or shopping skills only when the topic calls for them; don't reach for them by default.

## Logged-in lanes (consent required, parent delegation)

- X/Twitter timelines, YouTube comments, TikTok, LinkedIn posts, Instagram: I cannot drive a logged-in browser. Ask the user, then hand the parent agent a browser task with the exact URLs/handles to inspect.
- Never ask for or handle raw cookies, session tokens, or passwords to reach these lanes.

## Health probes

```bash
for u in "https://hn.algolia.com/api/v1/search?query=test&hitsPerPage=1" \
         "https://gamma-api.polymarket.com/public-search?q=test" \
         "https://api.github.com/search/issues?q=test&per_page=1" \
         "https://www.techmeme.com/feed.xml"; do
  code=$(curl -s -m 15 -o /dev/null -w "%{http_code}" -A "Mozilla/5.0" "$u")
  echo "$code  $u"
done
```

All 200s = lanes working. Anything else = that lane is failed or blocked: say so in the coverage note, don't silently skip it.
