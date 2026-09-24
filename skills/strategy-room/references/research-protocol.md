# Research Protocol

How the researcher agent should gather, evaluate, and organize evidence. Loaded by the researcher; useful background for the verifier.

## Source Tiering

Not all sources are equal. Tag every source in the dossier with a tier.

### Tier A: Primary and Authoritative

- Peer-reviewed research papers
- Official documentation from the entity being researched (Anthropic docs about Claude, OpenAI docs about GPT, government regulatory text)
- SEC filings and regulatory disclosures
- Direct interviews with named experts (cited in reputable outlets)
- Government data sources (BLS, Census, Eurostat, OECD)
- Academic textbooks and reference works in the relevant field

These sources can carry the weight of a finding by themselves. They are what verifiers want to see when checking a finding.

### Tier B: Strong Secondary

- Reputable journalism with named bylines and sourced reporting (Reuters, AP, FT, WSJ, NYT, The Atlantic, Wired's reporting desk)
- Established trade publications with editorial standards (Stratechery, The Information, Ars Technica, IEEE Spectrum)
- Books from established publishers
- Named expert essays and opinion pieces from established platforms (Substack newsletters from credentialed practitioners, MIT Technology Review)
- Industry analyst reports from firms with track records (Gartner, Forrester, IDC, when accessible)

These sources support findings when corroborated by another source or when the source's credibility is well-established in the domain.

### Tier C: Supporting

- Reddit threads, forum posts, Twitter/X threads from credentialed practitioners
- Company blog posts (useful for understanding the company's positioning, not as objective evidence)
- Aggregator articles (TechCrunch, The Verge, BusinessInsider, when not original reporting)
- Wikipedia (useful for orientation, not for citation in findings)
- LinkedIn posts from named practitioners

These sources are useful for orientation, signal, and sentiment, not for evidence-grounded claims. A finding that rests only on Tier C sources should be marked Low confidence at best.

### Tier D: Avoid

- SEO content farms
- Anonymous forum posts
- Unverified claims on social media
- AI-generated content masquerading as original analysis
- Sites with obvious affiliate-marketing or content-spam patterns

If the search returns mostly Tier D sources, reformulate the query. Padding the dossier with Tier D content is worse than admitting the dossier is thin.

## Recency Rules

Subject pace determines how recency matters.

### Fast-Moving Subjects

AI/ML, crypto, anything launched in the last 18 months, regulatory changes, current geopolitics.

For these, at least 30% of sources should be from the last 12 months. Sources older than 24 months should be flagged as "potentially stale" in the dossier. Sources older than 36 months should generally be excluded unless they establish foundational context that has not changed.

### Standard-Pace Subjects

Most business, professional services, established industries, mature technology.

Sources from the last 3 years are preferred. Sources up to 5 years old are acceptable for context. Older sources should be used only for historical patterns.

### Slow-Moving Subjects

Foundational science, established academic disciplines, mature engineering practices, historical analysis.

Recency matters less. Established textbooks and well-cited papers from any era are fine.

When in doubt, treat the subject as standard-pace and surface uncertainty about recency to the verifier.

## Search Strategy

### Mapping Queries

Start broad to map the territory. Examples:

- For a business idea: "[industry] market size", "[industry] competitive landscape", "[industry] customer pain points"
- For a prompt: "[model name] capabilities", "[model name] limitations", "[task type] prompt patterns"
- For a strategy: "[strategy type] case studies", "[strategy type] failure modes", "[strategy type] best practices"

### Narrowing Queries

Once the territory is mapped, drill into the specific dimensions that matter for the user's input. Use proper noun searches when relevant entities exist (companies, frameworks, papers, people).

### Disagreement-Seeking Queries

Deliberately query the contrarian position:

- "Why [X] doesn't work"
- "[X] criticism" or "[X] failure"
- "[X] alternatives" (often surfaces the strongest case against X)
- "[Y] vs [X]" where Y is a known competing approach

The dossier should reflect actual expert disagreement, not a one-sided picture. If the search consistently returns only one viewpoint, note this as a potential dossier limitation.

### Recency-Anchored Queries

For fast-moving subjects, use:

- Today's date or "today" / "latest" / "recent"
- The current year as a query keyword
- Date-restricted operators where supported

## Evidence Synthesis

Each dimension in the dossier should have 2 to 5 findings. A finding looks like:

```
Finding 3.2: Workshop pricing in this niche
Claim: Median pricing for 8-week professional development workshops in the AI/ML space is $400 per participant. Range is $200 to $1500. Top quartile (premium positioning) is $800+ and typically requires established instructor brand or institutional credentialing.
Sources:
- Course Hero industry report 2025 (Tier B, accessed [date])
- Maven instructor pricing dashboard (Tier B, accessed [date])
- Dossier source 7 in source list
Recency: All sources within 12 months. Subject is fast-moving (online education post-AI shift), so recency matters.
Caveats: Pricing data skews toward US market. International pricing not well-represented.
```

Findings should be specific enough that the planner can write hypotheses against them and the verifier can check evidence against them.

## Expert Disagreement Mapping

Whenever a finding involves expert opinion, the dossier must capture the disagreement explicitly. Use this structure:

```
Disagreement 4.1: Effectiveness of synchronous vs async cohort-based learning
Position A (advocates: [named experts/orgs]): Synchronous cohorts produce stronger outcomes due to accountability and peer interaction.
Position B (advocates: [named experts/orgs]): Async with strong community produces equal outcomes at lower cost and broader access.
Where consensus exists: Both agree pure self-paced courses without cohort/community produce weaker outcomes than either A or B.
Implications for user input: User's choice of synchronous-online format is a defensible choice but not the only one. The trade-off should be explicit.
```

Burying disagreement is the most common dossier failure. Surface it.

## Open Questions

Every dossier should end with a section listing open questions the research could not resolve. These are inputs to the planner, who may shape some of them into hypotheses to test against reasoning, and to the synthesizer, who will surface them in the final report's Meta-Reflections section.

## When Research is Impossible

For inputs where the relevant evidence is private or non-public (internal company processes, niche B2B without public coverage, novel concepts with no published analysis), the dossier should explicitly state this. The pipeline can still run, but every downstream agent must flag the missing evidence base, and the final report's Meta-Reflections section must note the limitation prominently.
