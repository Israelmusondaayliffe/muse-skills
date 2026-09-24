# AI Pattern Taxonomy: 24 Signs of AI Writing

Comprehensive catalog of AI writing patterns sourced from Wikipedia's "Signs of AI writing" guide, maintained by WikiProject AI Cleanup. These patterns come from observations of thousands of instances of AI-generated text.

**Key insight:** LLMs use statistical algorithms to guess what should come next. The result tends toward the most statistically likely result that applies to the widest variety of cases. This is why AI writing feels generic.

**How to use this reference:**
1. Load when running Phase 4, Step 4.1 (AI Pattern Taxonomy Check)
2. Scan output against all 24 categories
3. Prioritize Content Patterns (1-6) and Language Patterns (7-12) first
4. Style Patterns (13-18) and Communication Patterns (19-24) second
5. Each pattern includes watch-words, before/after examples, and detection notes

---

## CONTENT PATTERNS (1-6)

### Pattern 1: Undue Emphasis on Significance, Legacy, and Broader Trends

**Watch-words:** stands/serves as, is a testament/reminder, a vital/significant/crucial/pivotal/key role/moment, underscores/highlights its importance/significance, reflects broader, symbolizing its ongoing/enduring/lasting, contributing to the, setting the stage for, marking/shaping the, represents/marks a shift, key turning point, evolving landscape, focal point, indelible mark, deeply rooted

**Problem:** LLMs puff up importance by adding statements about how arbitrary aspects represent or contribute to a broader topic.

**Before:**
> The Statistical Institute of Catalonia was officially established in 1989, marking a pivotal moment in the evolution of regional statistics in Spain. This initiative was part of a broader movement across Spain to decentralize administrative functions and enhance regional governance.

**After:**
> The Statistical Institute of Catalonia was established in 1989 to collect and publish regional statistics independently from Spain's national statistics office.

**Detection:** Look for "marking a" + significance word, "broader" + trend noun, "contributing to the" + abstract concept.

**Severity:** High. One of the most common AI tells.

---

### Pattern 2: Undue Emphasis on Notability and Media Coverage

**Watch-words:** independent coverage, local/regional/national media outlets, written by a leading expert, active social media presence, has been cited in, garnered attention

**Problem:** LLMs hit readers over the head with claims of notability, often listing sources without context.

**Before:**
> Her views have been cited in The New York Times, BBC, Financial Times, and The Hindu. She maintains an active social media presence with over 500,000 followers.

**After:**
> In a 2024 New York Times interview, she argued that AI regulation should focus on outcomes rather than methods.

**Detection:** Lists of media outlets without specific claims. "Active social media presence." Unsupported notability assertions.

**Severity:** Medium. Common in biographical and organizational writing.

---

### Pattern 3: Superficial Analyses with -ing Endings

**Watch-words:** highlighting/underscoring/emphasizing..., ensuring..., reflecting/symbolizing..., contributing to..., cultivating/fostering..., encompassing..., showcasing...

**Problem:** AI tacks present participle ("-ing") phrases onto sentences to add fake depth without actually saying anything new.

**Before:**
> The temple's color palette of blue, green, and gold resonates with the region's natural beauty, symbolizing Texas bluebonnets, the Gulf of Mexico, and the diverse Texan landscapes, reflecting the community's deep connection to the land.

**After:**
> The temple uses blue, green, and gold colors. The architect said these were chosen to reference local bluebonnets and the Gulf coast.

**Detection:** Sentences ending with ", [verb]-ing [abstract concept]" constructions. Multiple -ing clauses chained together.

**Severity:** High. Extremely common. The -ing phrase almost always adds zero information.

---

### Pattern 4: Promotional and Advertisement-like Language

**Watch-words:** boasts a, vibrant, rich (figurative), profound, enhancing its, showcasing, exemplifies, commitment to, natural beauty, nestled, in the heart of, groundbreaking (figurative), renowned, breathtaking, must-visit, stunning

**Problem:** LLMs have serious problems keeping a neutral tone, especially for cultural or travel topics. Everything becomes a tourism brochure.

**Before:**
> Nestled within the breathtaking region of Gonder in Ethiopia, Alamata Raya Kobo stands as a vibrant town with a rich cultural heritage and stunning natural beauty.

**After:**
> Alamata Raya Kobo is a town in the Gonder region of Ethiopia, known for its weekly market and 18th-century church.

**Detection:** "Nestled," "vibrant," "rich" (figurative), "stunning," "breathtaking" anywhere. "Boasts a" construction.

**Severity:** High. Instant AI tell.

---

### Pattern 5: Vague Attributions and Weasel Words

**Watch-words:** Industry reports, Observers have cited, Experts argue, Some critics argue, several sources/publications (when few cited), is of interest to researchers

**Problem:** AI attributes opinions to vague authorities without specific sources.

**Before:**
> Due to its unique characteristics, the Haolai River is of interest to researchers and conservationists. Experts believe it plays a crucial role in the regional ecosystem.

**After:**
> The Haolai River supports several endemic fish species, according to a 2019 survey by the Chinese Academy of Sciences.

**Detection:** "Experts believe/argue/say" without naming experts. "Industry reports" without citing reports. "Some critics" without naming critics.

**Severity:** High. Fabricates authority to support unsourced claims.

---

### Pattern 6: Outline-like "Challenges and Future Prospects" Sections

**Watch-words:** Despite its... faces several challenges..., Despite these challenges, Challenges and Legacy, Future Outlook, looking ahead, poised to

**Problem:** AI adds formulaic "Challenges" sections with generic optimism. The "Despite these challenges" pivot is a dead giveaway.

**Before:**
> Despite its industrial prosperity, Korattur faces challenges typical of urban areas, including traffic congestion and water scarcity. Despite these challenges, with its strategic location and ongoing initiatives, Korattur continues to thrive as an integral part of Chennai's growth.

**After:**
> Traffic congestion increased after 2015 when three new IT parks opened. The municipal corporation began a stormwater drainage project in 2022 to address recurring floods.

**Detection:** "Despite" appearing twice in close proximity. "Challenges and [positive word]" section headers. Generic optimistic conclusions.

**Severity:** High. The "Despite... Despite..." structure is one of the most recognizable AI patterns.

---

## LANGUAGE AND GRAMMAR PATTERNS (7-12)

### Pattern 7: Overused "AI Vocabulary" Words

**High-frequency AI words:** Additionally, align with, crucial, delve, emphasizing, enduring, enhance, fostering, garner, highlight (verb), interplay, intricate/intricacies, key (adjective), landscape (abstract), pivotal, showcase, tapestry (abstract), testament, underscore (verb), valuable, vibrant

**Problem:** These words appear far more frequently in post-2023 text. They often co-occur in clusters.

**Before:**
> Additionally, a distinctive feature of Somali cuisine is the incorporation of camel meat. An enduring testament to Italian colonial influence is the widespread adoption of pasta in the local culinary landscape, showcasing how these dishes have integrated into the traditional diet.

**After:**
> Somali cuisine also includes camel meat, which is considered a delicacy. Pasta dishes, introduced during Italian colonization, remain common, especially in the south.

**Detection:** Run `scripts/quality_validator.py` for automated detection. Two or more of these words in same paragraph = strong AI signal.

**Severity:** High. Already covered in `references/negative-style-guide.md`, included here for completeness.

---

### Pattern 8: Copula Avoidance

**Watch-words:** serves as, stands as, marks, represents [a], boasts, features, offers [a], functions as

**Problem:** LLMs substitute elaborate constructions for simple "is," "are," "has." This is one of the most subtle and pervasive AI patterns.

**Before:**
> Gallery 825 serves as LAAA's exhibition space for contemporary art. The gallery features four separate spaces and boasts over 3,000 square feet.

**After:**
> Gallery 825 is LAAA's exhibition space for contemporary art. The gallery has four rooms totaling 3,000 square feet.

**Detection:** "serves as" (should be "is"), "stands as" (should be "is"), "boasts" (should be "has"), "features" (often should be "has" or "includes"), "offers a" (often should be "has a").

**Severity:** High. Extremely common, extremely easy to fix. Just use "is," "are," "has."

---

### Pattern 9: Negative Parallelisms

**Watch-words:** Not only...but..., It's not just about..., it's..., It's not merely...it's..., more than just

**Problem:** "Not only...but..." and "It's not just about..., it's..." constructions are heavily overused by LLMs.

**Before:**
> It's not just about the beat riding under the vocals. It's part of the aggression and atmosphere. It's not merely a song, it's a statement.

**After:**
> The heavy beat adds to the aggressive tone.

**Detection:** "Not only" + "but also." "It's not just" + "it's." "More than just a."

**Severity:** Medium. Occasionally appropriate, but AI uses it 10x more than humans.

---

### Pattern 10: Rule of Three Overuse

**Problem:** LLMs force ideas into groups of three to appear comprehensive. Three adjectives, three examples, three features.

**Before:**
> The event features keynote sessions, panel discussions, and networking opportunities. Attendees can expect innovation, inspiration, and industry insights.

**After:**
> The event includes talks and panels. There's also time for informal networking between sessions.

**Detection:** Multiple triplet structures in same paragraph. Adjective triplets ("seamless, intuitive, and powerful"). Noun triplets ("innovation, inspiration, and insights").

**Severity:** Medium. Natural writing sometimes uses three items, but AI forces everything into triplets.

---

### Pattern 11: Elegant Variation (Synonym Cycling)

**Problem:** AI has repetition-penalty code causing excessive synonym substitution. The same entity gets renamed every sentence.

**Before:**
> The protagonist faces many challenges. The main character must overcome obstacles. The central figure eventually triumphs. The hero returns home.

**After:**
> The protagonist faces many challenges but eventually triumphs and returns home.

**Detection:** Same entity referred to by 3+ different names in close proximity. Unusual synonym choices that feel forced.

**Severity:** Medium. Often results in confusion about whether different terms refer to same thing.

---

### Pattern 12: False Ranges

**Problem:** LLMs use "from X to Y" constructions where X and Y aren't on a meaningful scale.

**Before:**
> Our journey through the universe has taken us from the singularity of the Big Bang to the grand cosmic web, from the birth and death of stars to the enigmatic dance of dark matter.

**After:**
> The book covers the Big Bang, star formation, and current theories about dark matter.

**Detection:** "From [X] to [Y]" where X and Y aren't endpoints of a logical spectrum. Often paired with poetic language.

**Severity:** Medium. Common in introductions and conclusions.

---

## STYLE PATTERNS (13-18)

### Pattern 13: Em Dash Overuse

**Problem:** LLMs use em dashes more than humans, mimicking "punchy" sales writing.

**Before:**
> The term is primarily promoted by Dutch institutions---not by the people themselves. You don't say "Netherlands, Europe" as an address---yet this mislabeling continues---even in official documents.

**After:**
> The term is primarily promoted by Dutch institutions, not by the people themselves. You don't say "Netherlands, Europe" as an address, yet this mislabeling continues in official documents.

**Detection:** Run `scripts/emdash_replacer.py`. Already a Critical Rule in this skill.

**Severity:** Critical. Non-negotiable replacement rule.

---

### Pattern 14: Overuse of Boldface

**Problem:** AI mechanically emphasizes phrases in boldface, creating visual noise.

**Before:**
> It blends **OKRs (Objectives and Key Results)**, **KPIs (Key Performance Indicators)**, and visual strategy tools such as the **Business Model Canvas (BMC)** and **Balanced Scorecard (BSC)**.

**After:**
> It blends OKRs, KPIs, and visual strategy tools like the Business Model Canvas and Balanced Scorecard.

**Detection:** More than 5% of text in bold. Multiple bold phrases in same sentence. Bold used for every proper noun or acronym.

**Severity:** Medium. Already in `references/negative-style-guide.md` formatting anti-patterns.

---

### Pattern 15: Inline-Header Vertical Lists

**Problem:** AI outputs lists where items start with bolded headers followed by colons. Everything becomes a formatted list.

**Before:**
> - **User Experience:** The user experience has been significantly improved with a new interface.
> - **Performance:** Performance has been enhanced through optimized algorithms.
> - **Security:** Security has been strengthened with end-to-end encryption.

**After:**
> The update improves the interface, speeds up load times through optimized algorithms, and adds end-to-end encryption.

**Detection:** Bullet points with bold text followed by colon. Three or more items in this format. Information that could be a paragraph forced into a list.

**Severity:** Medium. Very common AI output pattern. Often contains redundancy (header repeats the content).

---

### Pattern 16: Title Case in Headings

**Problem:** AI capitalizes all main words in headings.

**Before:**
> ## Strategic Negotiations And Global Partnerships

**After:**
> ## Strategic negotiations and global partnerships

**Detection:** Heading lines where most words are capitalized. Exception: proper nouns and first word.

**Severity:** Low. Subtle but detectable.

---

### Pattern 17: Emojis in Professional Content

**Problem:** AI decorates headings or bullet points with emojis.

**Before:**
> 🚀 **Launch Phase:** The product launches in Q3
> 💡 **Key Insight:** Users prefer simplicity

**After:**
> The product launches in Q3. User research showed a preference for simplicity.

**Detection:** Emoji characters at start of lines or bullet points.

**Severity:** Medium in professional contexts.

---

### Pattern 18: Curly Quotation Marks

**Problem:** ChatGPT specifically uses curly quotes instead of straight quotes.

**Before:**
> He said \u201cthe project is on track\u201d but others disagreed.

**After:**
> He said "the project is on track" but others disagreed.

**Detection:** Unicode characters U+201C, U+201D, U+2018, U+2019. Script detects these automatically.

**Severity:** Low but distinctive. Platform-specific tell.

---

## COMMUNICATION PATTERNS (19-24)

### Pattern 19: Collaborative Communication Artifacts

**Watch-words:** I hope this helps, Of course!, Certainly!, You're absolutely right!, Would you like..., let me know, here is a...

**Problem:** Chatbot correspondence language gets pasted into content as if it belongs there.

**Before:**
> Here is an overview of the French Revolution. I hope this helps! Let me know if you'd like me to expand on any section.

**After:**
> The French Revolution began in 1789 when financial crisis and food shortages led to widespread unrest.

**Detection:** "I hope this helps," "Let me know if," "Here is a," "Would you like me to." These should never appear in final content.

**Severity:** High. Dead giveaway of unedited AI output.

---

### Pattern 20: Knowledge-Cutoff Disclaimers

**Watch-words:** as of [date], Up to my last training update, While specific details are limited/scarce..., based on available information...

**Problem:** AI disclaimers about incomplete information get left in text.

**Before:**
> While specific details about the company's founding are not extensively documented in readily available sources, it appears to have been established sometime in the 1990s.

**After:**
> The company was founded in 1994, according to its registration documents.

**Detection:** "As of [month/year]," "While specific details are limited," "based on available information." These are never appropriate in final content.

**Severity:** High. Instantly reveals AI origin.

---

### Pattern 21: Sycophantic/Servile Tone

**Problem:** Overly positive, people-pleasing language. Excessive agreement and praise.

**Before:**
> Great question! You're absolutely right that this is a complex topic. That's an excellent point about the economic factors.

**After:**
> The economic factors you mentioned are relevant here.

**Detection:** "Great question," "Absolutely right," "Excellent point," "That's a fantastic." Any phrase that praises the reader before answering.

**Severity:** High in content. These should never survive into published writing.

---

### Pattern 22: Filler Phrases

**Common filler -> replacement:**
- "In order to achieve this goal" -> "To achieve this"
- "Due to the fact that it was raining" -> "Because it was raining"
- "At this point in time" -> "Now"
- "In the event that you need help" -> "If you need help"
- "The system has the ability to process" -> "The system can process"
- "It is important to note that the data shows" -> "The data shows"

**Detection:** Already covered in `references/negative-style-guide.md` Category 7.

**Severity:** Medium. Common across all AI output.

---

### Pattern 23: Excessive Hedging

**Problem:** Over-qualifying every statement to avoid being wrong.

**Before:**
> It could potentially possibly be argued that the policy might have some effect on outcomes.

**After:**
> The policy may affect outcomes.

**Detection:** Multiple hedge words in same sentence. Already covered in divergence enforcement.

**Severity:** Medium in body text, High in conclusions.

---

### Pattern 24: Generic Positive Conclusions

**Problem:** Vague upbeat endings that say nothing specific.

**Before:**
> The future looks bright for the company. Exciting times lie ahead as they continue their journey toward excellence. This represents a major step in the right direction.

**After:**
> The company plans to open two more locations next year.

**Detection:** "The future looks bright," "exciting times," "continue their journey," "step in the right direction." Final paragraphs containing zero specific information.

**Severity:** High. One of the most common AI tells, especially in business and organizational writing.

---

## QUICK REFERENCE: Detection Priority

**Scan first (most common, highest signal):**
1. Significance inflation (#1)
2. -ing analyses (#3)
3. Promotional language (#4)
4. AI vocabulary (#7)
5. Copula avoidance (#8)
6. Communication artifacts (#19)
7. Generic positive conclusions (#24)

**Scan second (common, medium signal):**
8. Vague attributions (#5)
9. Challenges/prospects (#6)
10. Negative parallelisms (#9)
11. Rule of three (#10)
12. Sycophantic tone (#21)

**Scan third (lower frequency but distinctive):**
13. Synonym cycling (#11)
14. False ranges (#12)
15. Inline-header lists (#15)
16. Title case (#16)
17. Curly quotes (#18)
18. Knowledge disclaimers (#20)

**Already handled by other skill components:**
- Em dashes (#13) -> Critical Rule 1
- Boldface overuse (#14) -> negative-style-guide.md
- Emojis (#17) -> user preferences
- Filler phrases (#22) -> negative-style-guide.md
- Excessive hedging (#23) -> divergence-patterns.md

---

## SOURCE

This taxonomy is based on [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), maintained by WikiProject AI Cleanup. Adapted and extended for production writing contexts beyond Wikipedia.
