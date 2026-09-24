# Query Quality Pre-Flight

Run this before any source sweep. A bad query wastes the whole run; one clarifying question is cheaper than a fabricated-looking result.

## Keyword-trap patterns

| Pattern | Example | Fix |
|---|---|---|
| Demographic shopping | "gift for 42 year old man" | Ask what the recipient likes; research communities around the interest, not the literal phrase |
| Numeric / age trap | "best laptop under 700", "for 30 year old" | Ask for the use case or budget framing, then research the use case |
| How-to concept phrase | "how to use Docker" | Ask what they're trying to decide; how-to queries produce tutorials, not community signal |
| Generic single noun | "sneakers", "coffee" | Ask for the angle: brand, trend, purchase decision, subculture? |

If you spot a trap: reframe with the user in ONE short question, then sweep. Never run the engine on the literal trap phrase.

## Topic typing

- **Entity** (company, product, person, coin, repo): resolve canonical name + aliases first. Companies change names; products rebrand; tickers collide.
- **Person**: resolve social handle, GitHub username, and home subreddits (usually via a quick web search). Ask the user when ambiguous - never guess a handle.
- **Event**: pin the date range. "Last 30 days" is the default window, but an event 45 days ago needs the window stated explicitly.
- **Comparison** (A vs B): research each entity independently first, then compare. Don't let the louder entity's results drown the quieter one.

## Before the sweep, confirm

1. I have a concrete topic, not a trap phrase.
2. The window is clear (default: last 30 days from today).
3. For person topics: handle / repo / communities resolved or explicitly asked about.
4. For logged-in lanes: consent obtained before any browser delegation.
