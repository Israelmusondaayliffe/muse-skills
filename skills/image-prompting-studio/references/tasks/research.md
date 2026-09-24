# Task: Research prompts (facts for imagery)

Scope: research facts and visual references for image prompts about real entities, current events, data, geography or scientific subjects.

Read first: `../prompt-contract.md`. When a model is named, consult only its entry in `../model-profiles.md`.

## Workflow

1. Identify the facts the image actually needs: entities, appearance, date, event, labels, units, geography, structure. Prefer the authoritative owner source; record the date relevant to the subject, not just the browse date.
2. Separate verified facts, unknowns, and deliberately speculative content.
3. Research before writing (web search and page fetching are available on this host). Place the resulting fact inventory directly into the prompt so it stays usable on a generation surface with no search. If the workflow intentionally searches at generation time, include a specific retrieval target, a date anchor, and what to do when a fact is unavailable. Do not assert that one provider uniquely supports search or that a SEARCH label guarantees retrieval.
4. Define the visual container around the facts: hierarchy, region, map extent, chart encoding, required labels, source line. Preserve values and units across alternatives. For scientific imagery, distinguish appearance from verified structural/anatomical relationships. Mark proposed future scenes as speculative.

## Recipes

Use `../recipes/research_prompts/gpt-search.md` for current events, entities, weather/data, geography, brands, taxonomy. Its search instructions are templates to adapt to this host's actual browsing. Deliver prompts plus concise source links supporting the facts used. Check facts and text inventory before delivery; inspect rendered labels only when a result exists.
