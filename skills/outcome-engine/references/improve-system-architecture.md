# Improve System Architecture

Find structural friction that causes repeated confusion, weak proof, or unnecessary coordination.

## Use and limits

Use this for systems whose structure affects future work. Do not use it for simple proofreading, one isolated error, or a request that already names a small fix. This is a review skill. Do not implement the proposed changes unless the user asks for implementation.

## Working vocabulary

- Module: a coherent responsibility that hides detail behind an interface.
- Interface: what another person or module must understand to use it.
- Implementation: the detail hidden behind the interface.
- Deep module: a small interface that provides substantial useful behavior.
- Shallow module: an interface nearly as complex as what it hides.
- Seam: the place where behavior can be observed or substituted.
- Locality: related knowledge and change live together.

Use the system's own domain terms for its nouns. Use the vocabulary above only for structure.

## Workflow

1. Define the system, its user, and the result it exists to produce.
2. Read the closest source of truth, including contracts, decisions, process maps, reference files, and real artifacts.
3. Explore organically. Notice where one idea requires bouncing across many places, responsibility is duplicated, ownership is unclear, or proof is separated from the work.
4. Apply the deletion test to suspected shallow modules: if removed, would complexity concentrate in a better home or merely move elsewhere?
5. Draft two to five candidates. Include only candidates supported by observed friction.
6. For each candidate, show current structure, proposed structure, evidence, locality gain, proof gain, risk, and recommendation strength.
7. Use `assets/system-review-template.md`. Add a compact diagram when it makes the before-and-after relationship clearer.
8. Recommend one candidate to examine first.
9. Ask which candidate the user wants to pressure-test. Route the selected candidate to `references/decision-grill.md` before planning a structural change.

## Candidate tests

A useful structural change should reduce what users must understand, put related decisions closer together, create a clearer proof surface, or remove repeated coordination. Reject candidates based only on taste or generic claims about cleanliness.

Respect existing decision records. If a candidate conflicts with one, name the conflict and the evidence that might justify reopening it.
