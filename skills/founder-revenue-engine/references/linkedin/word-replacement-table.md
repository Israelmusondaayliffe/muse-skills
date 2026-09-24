# Word Replacement Table

Three-tier system. Tier determines when to flag.

**Tier 1:** Always replace. These appear 5-20x more often in AI text than human text.
**Tier 2:** Flag when 2+ appear in the same paragraph. Fine alone; suspicious in clusters.
**Tier 3:** Flag by density only. Normal words AI simply overuses. Flag when they make up ~3%+ of total words, or when they replace specific information that should be there.

Rule Zero applies throughout: if a simpler word conveys the same meaning, that is always the right choice.

---

## Tier 1 — Always Replace

| Replace | With |
|---|---|
| delve / delve into | explore, look at, dig into |
| landscape (metaphor) | field, space, industry, world |
| tapestry | describe the actual complexity |
| realm | area, field, domain |
| paradigm | model, approach, framework |
| embark | start, begin |
| beacon | rewrite entirely |
| testament to | shows, proves, demonstrates |
| robust | strong, reliable, solid |
| comprehensive | thorough, complete, full |
| cutting-edge | latest, newest, advanced |
| leverage (verb) | use |
| pivotal | important, key, critical |
| underscores | shows, highlights |
| meticulous / meticulously | careful, detailed, precise |
| seamless / seamlessly | smooth, easy, without friction |
| game-changer / game-changing | describe what specifically changed and why |
| utilize | use |
| watershed moment | turning point, shift — or describe what changed |
| marking a pivotal moment | state what happened |
| the future looks bright | cut, or say something specific |
| only time will tell | cut, or say something specific |
| nestled | is located, sits, is in |
| vibrant | describe what makes it active, or cut |
| thriving | growing, active — or cite a number |
| despite challenges… continues to thrive | name the challenge and the response, or cut |
| showcasing | showing, demonstrating — or cut the clause |
| deep dive / dive into | look at, examine, explore |
| unpack / unpacking | explain, break down, walk through |
| bustling | busy, active — or cite what makes it busy |
| intricate / intricacies | complex, detailed — or name the specific complexity |
| complexities | name the actual complexities, or use "problems" / "details" |
| ever-evolving | changing, growing — or describe how |
| enduring | lasting, long-running — or cite how long |
| daunting | hard, difficult, challenging |
| holistic / holistically | complete, full, whole — or describe what's included |
| actionable | practical, useful, concrete |
| impactful | effective, significant — or describe the impact |
| learnings | lessons, findings, takeaways |
| thought leader / thought leadership | expert, authority — or describe their actual contribution |
| best practices | what works, proven methods, standard approach |
| at its core | cut, just state the thing |
| synergy / synergies | describe the actual combined effect |
| interplay | relationship, connection, interaction |
| in order to | to |
| due to the fact that | because |
| serves as | is |
| features (as verb in "X features Y") | has, includes |
| boasts | has |
| presents (inflated) | is, shows, gives |
| commence | start, begin |
| ascertain | find out, determine, learn |
| endeavor | effort, attempt, try |
| keen (as intensifier) | interested, eager — or cut |
| symphony (metaphor) | describe the actual coordination |
| embrace (metaphor) | adopt, accept, use, switch to |
| empower | enable, let, allow |
| disruptive / disrupt | change, replace, shift — or describe what it replaces |
| revolutionary | new, different — or describe what changed |
| groundbreaking | first, new — or describe what it changed |
| scalable / scalability | describe what scales and to what |
| robust | strong, reliable, solid (same as above, flagged twice intentionally) |

---

## Tier 2 — Flag When 2+ in Same Paragraph

| Replace | With |
|---|---|
| harness | use, take advantage of |
| navigate / navigating | work through, handle, deal with |
| foster | encourage, support, build |
| elevate | improve, raise, strengthen |
| unleash | release, enable, unlock |
| streamline | simplify, speed up |
| bolster | support, strengthen, back up |
| spearhead | lead, drive, run |
| resonate / resonates with | connect with, appeal to, matter to |
| revolutionize | change, transform, reshape — or describe what changed |
| facilitate / facilitates | enable, help, allow, run |
| underpin | support, form the basis of |
| nuanced | specific, subtle, detailed — or name the actual nuance |
| crucial | important, key, necessary |
| multifaceted | describe the actual facets, or cut |
| ecosystem (metaphor) | system, community, network, market |
| myriad | many, numerous — or give a number |
| plethora | many, a lot of — or give a number |
| encompass | include, cover, span |
| catalyze | start, trigger, accelerate |
| reimagine | rethink, redesign, rebuild |
| galvanize | motivate, rally, push |
| augment | add to, expand, supplement |
| cultivate | build, develop, grow |
| illuminate | clarify, explain, show |
| elucidate | explain, clarify, spell out |
| juxtapose | compare, contrast, set side by side |
| transformative / transformation | describe what changed and how |
| cornerstone | foundation, basis, key part |
| paramount | most important, top priority |
| poised (to) | ready, set, about to |
| burgeoning | growing, emerging — or cite a number |
| nascent | new, early-stage, emerging |
| quintessential | typical, classic, defining |
| overarching | main, central, broad |
| underpinning / underpinnings | basis, foundation, what supports |

---

## Tier 3 — Flag at High Density (3%+ of total words)

These are normal words. Only flag when the text is saturated with them.

| Word | Fix |
|---|---|
| significant / significantly | Replace some with specifics: numbers, comparisons, examples |
| innovative / innovation | Describe what's actually new |
| effective / effectively | Say how, or cite a metric |
| dynamic / dynamics | Name the actual forces or changes |
| compelling | Say why it compels |
| unprecedented | Name the precedent it breaks, or cut |
| exceptional / exceptionally | Cite what makes it an exception |
| remarkable / remarkably | Say what's worth remarking on |
| sophisticated | Describe the sophistication |
| instrumental | Say what role it played |
| world-class / state-of-the-art / best-in-class | Cite a benchmark or comparison |

---

## Template Phrases (Always Replace)

These slot-fill constructions signal generated prose. If a phrase has a blank where any word could go and still sound the same, it's too generic.

- "a [adjective] step toward [adjective] AI infrastructure" → describe the specific capability or outcome
- "a [adjective] step forward for [noun]" → say what actually changed
- "Whether you're [X] or [Y]" → false-breadth construction. Pick one audience or cut.
- "I recently had the pleasure of [verb]-ing" → just say what happened: "I talked to," "I read"
- "In today's [fast-paced / rapidly evolving] world" → cut entirely, or state the specific context
- "In an era where" → cut, or state the specific situation
- "Navigate the [landscape / ecosystem / space]" → name what they're doing in it

---

## Copula Avoidance Replacements (Always Fix)

AI text avoids "is" and "has" by substituting fancier verbs. Default back.

| AI version | Human version |
|---|---|
| serves as | is |
| stands as | is |
| boasts | has |
| features (as main verb) | has, includes |
| presents | is, shows |
| represents | is |
| functions as | is |
| offers (inflated) | has, gives |

Unless a more specific verb genuinely adds meaning, use "is" or "has."

---

## Vague Endorsement Phrases (Cut or Replace)

These substitute a generic thumbs-up for a specific reason. Say why something matters instead.

- worth reading
- worth paying attention to
- worth a look
- worth exploring
- worth checking out
- worth your time
- worth noting

---

## Source

Tier system adapted from avoid-ai-writing (conorbronsdon, MIT license) and humanizer/blader. Table extended with Rule Zero (simple words always preferred) and OQE-v3 patterns.
