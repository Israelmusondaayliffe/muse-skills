# Research and Qualification Framework

Used by the `signal-research` and `first-customers` routes. Signal collection on Hatch uses `browser.search`, `browser.open`, and the `social` skill for public posts. (The plugin's `last30days` multi-vendor scraper bundle does not transfer: it required third-party API keys and platform-specific hacks. Use native search and social tools instead, which is slower per-source but needs no credentials.)

## Research sequence

### Product brief

Define before any broad search, specific enough to reject weak matches:

- product and promised outcome
- primary user and economic buyer (name both when they differ)
- urgent job to be done
- current alternative or workaround
- likely adoption trigger
- geography or language constraint
- clear disqualifiers

Do not begin prospect collection until this brief rejects weak matches. Ask one concise question only when ambiguity would materially change the search; infer safely and label the inference otherwise.

### Query buckets

Search several buckets rather than repeating one query:

1. **Explicit demand:** "looking for," "recommend a tool," "alternative to," "does anything exist."
2. **Pain:** "takes hours," "manual," "frustrating," "hate," "difficult," "keeps breaking."
3. **Workaround:** spreadsheets, copy-paste, virtual assistants, scripts, templates, repeated manual steps.
4. **Switching:** cancellation, migration, missing feature, pricing complaint, competitor frustration.
5. **Timing:** public launch, hiring, expansion, new workflow, regulation, integration, process change.

Adapt wording to the audience's language. Open the original page with `browser.open` and do not qualify from a search snippet alone.

### Source mix

- forums and public community discussions
- public social posts and replies (via the `social` skill)
- product reviews and app marketplace reviews
- GitHub issues and public feature requests
- public company pages, job posts, changelogs, announcements
- public "looking for a tool" posts and directories

Avoid private groups, gated communities, data brokers, scraped contact databases, and any source that prohibits access. Do not bypass login walls, paywalls, rate limits, or robots restrictions.

## Qualification score

Score every dimension 0–5:

- **Pain strength (25%)** — directness, severity, repetition, cost of the stated problem.
- **Product fit (25%)** — how directly the offer solves the evidenced job.
- **Timing (20%)** — freshness and presence of a current trigger.
- **Public reachability (15%)** — a natural, relevant public or professional contact path exists.
- **Evidence quality (15%)** — specificity, source reliability, confidence the signal belongs to the prospect.

```text
score = pain_strength/5*25 + product_fit/5*25 + timing/5*20 + reachability/5*15 + evidence_quality/5*15
```

- **80–100:** strong first-customer candidate
- **65–79:** promising, validate quickly
- **50–64:** plausible but missing a material signal
- **Below 50:** keep out of the primary shortlist

An old explicit request can still be relevant: reduce timing and label the date. A company that merely matches the industry without an evidenced trigger is not a qualified prospect. A prospect without a cited pain, need, or timing signal is a speculative fit and must not appear in the primary shortlist.

Never claim a prospect is interested, has consented, or will buy. Label the output "potential customer based on public signals."

### Prospect stages

- **High intent:** publicly requesting a solution or actively switching.
- **Problem aware:** clearly describing the pain or expensive workaround.
- **Trigger present:** a current business event makes the offer relevant.
- **Potential fit:** ICP match with incomplete evidence; keep outside the primary shortlist.

## Outreach rules

Draft one opener using this shape:

1. mention the public context naturally
2. connect it to the exact problem
3. explain the product in one sentence
4. ask one low-friction question

Keep it under 90 words by default. Never claim the message was sent. Do not include private emails, phone numbers, personal addresses, family information, or sensitive traits.

## Evidence ledger

For each qualified prospect record:

- displayed company, project, or public professional name
- source title and URL
- visible publication date or "date unavailable"
- source type
- concise pain or timing signal
- observed evidence versus inference
- score breakdown
- freshness warning when relevant

Use citations in the chat response whenever web research was performed.
