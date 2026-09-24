# Quality Enforcement Rules

Comprehensive validation rules for ensuring hooks don't sound like AI and maintain voice consistency.

## Rule Zero: Simple Words Win

**This rule overrides every other stylistic choice.**

If a simpler word conveys the same meaning, use it. Not trying to sound smart. Trying to sound like a real person.

"Use" beats "leverage." "Start" beats "commence." "Important" beats "pivotal." "Show" beats "showcase." "Get" beats "obtain." "Need" beats "require."

Load `references/word-replacement-table.md` for the full Tier 1/2 replacement list with specific alternatives. Every Tier 1 word in a draft is a mandatory replacement. No debate.

The principle behind the list: when you reach for the fancier word, ask why. If the answer is anything other than "it's the only precise option," use the simpler one.

## Universal Bans (NEVER use)

### AI Clichés (Instant tells)
- delve / delving
- leverage / leveraging
- unlock / unlocking
- journey
- game-changer / game-changing
- paradigm shift
- deep dive / diving deep
- nuanced
- robust
- synergy
- disruptive / disruption (when not literally about disruption)
- innovative (overused to meaninglessness)
- cutting-edge
- state-of-the-art
- groundbreaking
- revolutionary
- transformative

### Business Jargon
- scalable / scalability
- bandwidth (unless literally about internet)
- circle back
- touch base
- move the needle
- low-hanging fruit
- think outside the box
- drill down
- take it offline
- boil the ocean
- drink the Kool-Aid

### Generic Transitions
- however,
- moreover,
- furthermore,
- additionally,
- consequently,
- in conclusion,
- to summarize,
- moving forward,

### Hedge Language (Avoid unless intentional)
- kind of
- sort of
- probably
- maybe
- could be
- might be
- perhaps
- possibly
- arguably
- somewhat
- relatively
- fairly
- quite
- rather

### Banned Opening Phrases
- "Let's talk about..."
- "Here's why..."
- "Here's the thing..."
- "The truth is..."
- "At the end of the day..."
- "When it comes to..."
- "In today's world..."
- "It's no secret that..."
- "We all know that..."

### Punctuation Rules

**Em-dashes (—):**
BANNED. Replace with:
- Period (.) + capitalize next word for new sentence
- Comma (,) + lowercase for continuation

**Examples:**
- ✗ "This is great — it works well"
- ✗ "This is great — It works well"
- ✓ "This is great. It works well"
- ✓ "This is great, really well"

**Colons in titles:**
BANNED. Use period or different structure.
- ✗ "Remote Work: The Hidden Costs"
- ✓ "Remote Work's Hidden Costs"
- ✓ "Remote work. Hidden costs."

## AI Pattern Taxonomy (V3 Addition)

Patterns from Wikipedia's WikiProject AI Cleanup that are especially common in LinkedIn post drafts. Run `scripts/quality_validator.py` for automated detection. See `references/ai-pattern-taxonomy.md` for the full 24-pattern catalog.

### Copula Avoidance (HIGH priority)
LLMs write "serves as" instead of "is." Instantly detectable.

| AI Pattern | Fix |
|-----------|-----|
| "serves as" | "is" |
| "stands as" | "is" |
| "functions as" | "is" |
| "boasts a" | "has a" |
| "features a" | "has a" |
| "offers a" | "has a" |
| "represents a" | "is a" |

### Significance Inflation (HIGH priority)
LLMs inflate importance with empty claims. Common in LinkedIn drafts about achievements or launches.

**Banned phrases:**
- "marking a pivotal moment"
- "a testament to"
- "setting the stage for"
- "reflects broader trends"
- "contributing to the"
- "plays a crucial/vital/key role"
- "underscores the importance"
- "enduring legacy"

**Fix:** Delete the significance claim. If the thing is actually important, the facts will show it.

### Trailing -ing Constructions (HIGH priority)
LLMs tack present participle phrases onto sentences for fake depth. Extremely common in LinkedIn drafts.

**Banned endings:**
- ", highlighting..."
- ", showcasing..."
- ", emphasizing..."
- ", ensuring..."
- ", reflecting..."
- ", demonstrating..."
- ", fostering..."
- ", contributing to..."

**Fix:** Delete the -ing clause. If the information matters, make it its own sentence.

**Before:** "We launched the new platform Tuesday, showcasing our commitment to innovation and highlighting the team's dedication."
**After:** "We launched the new platform Tuesday."

### Negative Parallelisms (MEDIUM priority)
"Not only...but..." and "It's not just...it's..." are overused by LLMs.

**Banned:**
- "Not only...but also..."
- "It's not just about..., it's..."
- "More than just a..."

**Fix:** State the point directly. "It's not just a tool, it's a platform" becomes "It's a platform for X."

### Rule of Three Forcing (MEDIUM priority)
LLMs force everything into groups of three. LinkedIn posts love triplets.

**Before:** "We focused on innovation, collaboration, and excellence."
**After:** "We focused on shipping faster." (or however many items actually matter)

**Fix:** Use the natural number of items. Two is fine. One is better.

### Generic Positive Conclusions (HIGH priority)
Vague upbeat endings that say nothing.

**Banned:**
- "The future looks bright"
- "Exciting times lie ahead"
- "Poised for growth/success"
- "Continue their journey"
- "Step in the right direction"
- "The possibilities are endless"

**Fix:** End with a specific next step, a question, or a call to action. Never end with optimistic filler.

### Sycophantic/Chatbot Artifacts (HIGH priority)
Chatbot language that survives into LinkedIn drafts. Zero tolerance.

**Banned:**
- "Great question!"
- "Excellent point!"
- "I hope this helps!"
- "Let me know if you'd like..."
- "Certainly!" / "Of course!" / "Absolutely!"
- "Here is a comprehensive..."

### Curly Quotation Marks (LOW priority)
ChatGPT uses Unicode curly quotes. Replace with straight quotes.

### Synonym Cycling (MEDIUM priority)
LLMs refer to the same thing by different names every sentence.

**Before:** "The tool saves time. The platform increases efficiency. The solution improves workflow."
**After:** "The tool saves time and improves workflow."

**Fix:** Pick one term and stick with it.

## Extended Pattern Scan

12 additional patterns not in the core 24. These survive a vocabulary-only edit. The only way to catch them is to ask: does this sentence actually say something, or is it performing the act of saying something?

Load `references/extended-patterns.md` for full examples and fixes.

### Novelty Inflation (P1)
"He introduced a term nobody's naming." Most concepts already exist. Describe what the person *did with* the idea, not that they discovered it. Related: "what nobody tells you about," "the insight everyone's missing."

### Emotional Flatline (P1)
"What surprised me most," "I was fascinated to discover." Tell-don't-show. If something is surprising, the content should convey that, not a claim about your emotion. Cut the claim and present the thing directly.

### False Concession Structure (P1)
"While X is impressive, Y remains a challenge." Sounds balanced, says nothing. Both halves are vague. Name the actual tradeoff or pick a side.

### Rhetorical Question Stalls (P1)
"So why should you care?" / "What does this mean for you?" Used to stall before the actual point. If you know the answer, just say it. Exception: a rhetorical question as a hook is fine — one, at the top, earned by context.

### Reasoning Chain Artifacts (P1)
"Let me think step by step," "Breaking this down," "Here's my thought process." LLM scaffolding leaking into prose. State the conclusion, then the evidence. Reader doesn't need to see the reasoning structure.

### Acknowledgment Loops (P0 in published content)
"You're asking about," "To answer your question," "That's a great question. The..." Restating the prompt before answering. Pure filler. Just answer.

### Confidence Calibration Phrases (P2 by density)
"It's worth noting that," "Interestingly," "Surprisingly," "Importantly," "Notably," "Certainly." AI uses these to signal how the reader should feel instead of letting the fact do the work. One per piece is fine. Three in 300 words is AI emphasis stacking.

### "Let's" Constructions (P1)
"Let's explore," "Let's break this down," "Let's take a look," "Let's dive in." False-collaborative opener used to delay the point. Just start with the point. Broader than the banned opening phrases list.

### Template Phrases (P1)
"Whether you're X or Y" (false-breadth: pick one audience), "I recently had the pleasure of [verb]-ing" (just say what happened), "In today's fast-paced world" (cut or state specific context), "Navigate the [landscape/space]" (say what they're actually doing in it).

### Vague Endorsement (P2)
"Worth reading," "worth paying attention to," "worth your time," "worth a look." Substitutes a generic thumbs-up for a specific reason. Say why it matters. What specifically will the reader get from it?

### Parenthetical Hedging (P2)
"(and, increasingly, Z)" / "(or, more precisely, Y)" — AI asides that sound nuanced without committing. If the aside matters, give it its own sentence. If it doesn't, cut it.

### Numbered List Inflation (P2)
"5 things you need to know" / "Here are 7 reasons why." Only use numbered lists when the content genuinely has that many discrete parallel items. If you're padding to hit a number, cut the list.

---

## Voice Requirements

### Voice Markers (ALWAYS apply)

**Tone:**
- Curious, not preachy
- Direct, not verbose
- Practical, not theoretical
- Collaborative, not dictatorial

**Style:**
- Shows work over hiding process
- Questions over statements when exploring
- Depth-first, clarity-second, polish-third
- No fluff, no hype, no emojis

**Structure:**
- Economic thinking (who pays? who wins?)
- Structural insight (systemic, not personal)
- Pattern recognition (violated expectations)
- Uncomfortable honesty (no sugar-coating)
- Concrete specificity (numbers, examples, details)

## Quality Markers

### Good Hooks Have:
- Economic or structural insight
- Specific examples or numbers
- Contradiction of mainstream narrative
- Human imperfection markers
- Varied rhythm and sentence length
- Provocative but defensible claims
- Clear perspective without hedge language

### Bad Hooks Have:
- Generic advice or platitudes
- Vague claims without specifics
- Consensus language
- Perfect grammar (suspiciously clean)
- AI clichés or business jargon
- Hedge language throughout
- No clear stance

## Validation Checklist

### Phase 1 (Consensus) Validation
- [ ] 5 distinct consensus takes identified
- [ ] Each has "why it's stale" explanation
- [ ] Banned words list specific to niche
- [ ] Boredom diagnosis specific, not generic
- [ ] No AI clichés in analysis
- [ ] Shows understanding of domain

### Phase 2 (Tail Angles) Validation
- [ ] Each angle contradicts consensus
- [ ] Probability scores between 0.04-0.10
- [ ] Economic/structural insight present
- [ ] No hedge language
- [ ] Specific claims, not vague generalities
- [ ] Defensible with evidence or logic
- [ ] Different angle category per take

### Phase 3 (PRISM Hooks) Validation
- [ ] No em-dashes (all replaced)
- [ ] No banned phrases present
- [ ] No AI clichés anywhere
- [ ] Lowercase used for emphasis
- [ ] Rhythm varies naturally
- [ ] Imperfection markers present
- [ ] Starts mid-thought or with insight
- [ ] Meta-commentary when appropriate
- [ ] Sounds human, not AI
- [ ] Each hook contradicts mainstream

### Voice Consistency Validation
- [ ] Curious, not preachy
- [ ] Direct, not verbose
- [ ] Practical, not theoretical
- [ ] Shows work, not perfection
- [ ] No fabricated details
- [ ] Voice profile evident

## Red Flags

### Immediate rejections (regenerate):
- Contains em-dashes (—)
- Uses "Let's talk about" or "Here's why"
- Has AI clichés (delve, leverage, unlock)
- Multiple hedge words (kind of, sort of, maybe)
- Perfect grammar with no personality
- Generic advice with no structural insight
- Consensus language instead of contrarian

### Warning signs (revise):
- Too many sentences same length
- No lowercase emphasis anywhere
- No personality quirks
- Sounds like could be written by anyone
- No economic or structural thinking
- Safe/boring take disguised as hot take
- Meta-commentary feels performative

## Scoring System

**Quality Score Calculation:**

**Phase 1 (20 points):**
- 5 distinct consensus takes (5 pts)
- Each with "why stale" (5 pts)
- Specific vocabulary trap (5 pts)
- Specific boredom diagnosis (5 pts)

**Phase 2 (25 points):**
- All angles contradict consensus (8 pts)
- Probability scores accurate (4 pts)
- Economic/structural insight (8 pts)
- No hedge language (5 pts)

**Phase 3 (55 points):**
- Rule Zero honored — no Tier 1 words, no complex word where simple works (10 pts)
- No banned elements (10 pts: em-dashes, phrases, clichés)
- PRISM markers present (10 pts: pattern, rhythm, imperfection, mid-thought, meta)
- Voice consistency (10 pts: voice profile consistency)
- Human quality — no extended patterns (10 pts: novelty inflation, emotional flatline, etc.)
- No fabricated details (5 pts)

**Total: 100 points**

**Grading:**
- 90-100: Excellent, ship it
- 80-89: Good, minor tweaks
- 70-79: Acceptable, needs revision
- Below 70: Regenerate

## Common Mistakes

### Mistake 1: Consensus language in tail angles
**Problem:** "Remote work offers both benefits and challenges..."
**Fix:** "Remote work isn't freedom. It's [economic reality]."

### Mistake 2: Perfect grammar in PRISM
**Problem:** "I have stopped calling it 'work from home' and have started calling it..."
**Fix:** "stopped calling it 'work from home' and started calling it..."

### Mistake 3: Hedge language in contrarian takes
**Problem:** "This might suggest that..."
**Fix:** "This is [clear statement]."

### Mistake 4: AI clichés in humanization
**Problem:** "...unlocking the paradigm shift in..."
**Fix:** Rewrite entirely, these words are banned

### Mistake 5: Em-dashes surviving PRISM
**Problem:** "remote work — it's not what you think"
**Fix:** "remote work. it's not what you think" OR "remote work, it's not what you think"

### Mistake 6: No economic insight
**Problem:** "Remote work is hard because it's isolating"
**Fix:** "Remote work converted office rent into your housing costs while giving you isolation as a bonus"

## Self-Audit Questions

Before delivering hooks, ask:

1. **Rule Zero check:** Any Tier 1 word surviving? Any complex word with a simpler equivalent? If yes, replace.
2. **Consensus check:** Would someone in 2020 say this? If yes, regenerate
3. **Economic check:** Does this reveal who pays/who wins? If no, add economic insight
4. **AI check:** Would ChatGPT write this? If yes, apply more PRISM
5. **Voice check:** Does this match the voice profile? If no, adjust to voice
6. **Em-dash check:** Any em-dashes present? If yes, replace immediately
7. **Banned phrase check:** Any "Let's talk about" or "Here's why"? If yes, rewrite
8. **Hedge check:** Multiple "maybe" "could be" "sort of"? If yes, commit to stance
9. **Rhythm check:** All sentences same length? If yes, vary rhythm
10. **Imperfection check:** Too clean/perfect? If yes, add human quirks
11. **Defensible check:** Could this be backed with evidence? If no, make more concrete
12. **Copula check:** Any "serves as" or "stands as"? If yes, replace with "is"/"has"
13. **Significance check:** Any "marking a pivotal moment" or "a testament to"? If yes, delete
14. **-ing check:** Any trailing ", highlighting..." or ", showcasing..."? If yes, delete the clause
15. **Conclusion check:** Does it end with vague optimism? If yes, replace with specific fact or question
16. **Novelty check:** Claiming someone invented or coined a concept? If yes, describe what they did with it instead
17. **Emotion claim check:** Any "what surprised me," "I was fascinated"? If yes, earn the emotion or cut the claim
18. **Rhetorical stall check:** Any "so why should you care?" as a transition? If yes, just answer the question
19. **Calibration phrase check:** Any "notably," "interestingly," "it's worth noting"? Flag if 2+ in the draft
20. **"Let's" check:** Any "let's explore," "let's break this down"? If yes, replace with the actual point
21. **Template phrase check:** Any "whether you're X or Y" or "in today's fast-paced world"? If yes, cut or rewrite
22. **Vague endorsement check:** Any "worth your time" or "worth reading" without saying why? If yes, state the specific reason

## Examples of Good vs. Bad

**Bad Hook (60/100):**
"Remote work can be challenging and may present both opportunities and difficulties for creative teams. It's important to consider the trade-offs."

**Problems:**
- Hedge language throughout (can, may, important to consider)
- No specific insight
- Generic/consensus language
- Perfect grammar
- No personality
- No economic thinking
- Sounds like AI

**Good Hook (95/100):**
"everyone celebrates remote work until they realize creative feedback now arrives at 11pm across three time zones. you didn't escape the office. you just made your bedroom the 24/7 war room."

**Strengths:**
- No hedge language
- Specific insight (time zones, 11pm)
- Contradicts consensus
- Human imperfection (lowercase, fragments)
- Economic reality (always-on cost)
- Clear rhythm
- The voice profile
- Doesn't sound AI

## Final Notes

These rules are strict for a reason. Every banned element is banned because it immediately signals "AI wrote this" to readers. Every voice requirement exists because it makes hooks sound human and authentic.

When in doubt:
- Be more specific
- Remove hedge words
- Add economic insight
- Check for em-dashes
- Apply PRISM markers
- Make it sound like the author wrote it

If a hook scores below 80/100, regenerate rather than polish. Polishing generic hooks doesn't work. You need structural rethinking.
