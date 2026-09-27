---
name: wayfinder
description: "Use when planning a huge chunk of work (more than one agent session can hold) as a shared map of decision tickets on the issue tracker, and resolving them one at a time until the way to the destination is clear."
---

Invocation: user-invoked only

A loose idea has arrived, too big for one agent session, wrapped in fog: the way from here to the **destination** isn't visible yet. Wayfinding is about finding that way, not charging at the destination. Chart the way as a **shared map** on the issue tracker, then work its **decision tickets** (questions whose resolution is a decision, not slices of a build to execute) one at a time until the route is clear.

## Hard rules

- **Plan, don't do.** Wayfinder is planning by default: each ticket resolves a decision, and the map is done when the way is clear, with nothing left to decide before someone goes and does the thing. The pull to just do the work is usually the signal you've reached the edge of the map and it's time to hand off. An effort can override this in its map **Notes**, carrying execution into the map itself; absent that, produce decisions, not deliverables.
- **Never resolve more than one ticket per session**, with the exception of research tickets.
- **Refer by name.** Every map and ticket has a name: its title. In everything the human reads (narration, the map's Decisions-so-far), refer to it by that name, never by a bare id, number, or slug.
- **Claim first.** A session claims a ticket by assigning it to the dev driving the map before any work, so concurrent sessions skip it.
- **Blocking uses the tracker's native dependency relationship** (falls back to a body convention only if the tracker lacks native blocking). A ticket is **unblocked** when every ticket blocking it is closed; the **frontier** is the open, unblocked, unclaimed children.
- The issue tracker should have been provided. If not, tell the user to run `/setup-matt-pocock-skills`. Consult the tracker doc's "Wayfinding operations" section; with no tracker, default to the local-markdown tracker.

## Ticket types

Every ticket is either **HITL** (human in the loop, worked with a human who speaks for themselves; a HITL ticket only resolves through that live exchange) or **AFK** (driven by the agent alone).

- **Research** (AFK): reading documentation, third-party APIs, or local resources to surface a fact a decision waits on. Use when knowledge outside the current working directory is required. Resolve by spinning up a subagent working from the research brief (`subagents/research.md`).
- **Prototype** (HITL): raise the fidelity of the discussion by making a cheap, rough, concrete artifact to react to (an outline, rough take, stub, or UI/logic code). Links the prototype as an asset. Use when "how should it look" or "how should it behave" is the key question. Resolve by working from the prototype brief (`subagents/prototype.md`).
- **Grilling** (HITL): conversation. The default case. Resolve by working from both the grilling brief (`subagents/grilling.md`) and the domain-modeling brief (`subagents/domain-modeling.md`).
- **Task** (HITL or AFK): manual work that must happen before a decision can be made: nothing to decide, prototype, or research, but the discussion is blocked until it's done. This is the one type that does rather than decides, and it earns its place by unblocking a decision, not by delivering the destination. The agent drives it alone where it can (AFK); otherwise it hands the human a precise checklist (HITL). Resolved when the work is done; the answer records what was done and any resulting facts later tickets depend on.

## The map

The map is a single issue on the issue tracker, labelled `wayfinder:map`, the canonical artifact. Its tickets are child issues of the map. The map is an **index**, not a store: it lists the decisions made and points at the tickets that hold their detail; a decision lives in exactly one place, its ticket, so the map never restates it, only gists it and links.

The map body:

```markdown
## Destination

<what reaching the end of this map looks like: the spec, decision, or change this effort is finding its way to. One or two lines; every session orients to it before choosing a ticket.>

## Notes

<domain; skills every session should consult; standing preferences for this effort>

## Decisions so far

<!-- one line per closed ticket, enough to judge relevance, then zoom the link for the detail the ticket holds -->

- [<closed ticket title>](link): <one-line gist of the answer>

## Not yet specified

<!-- in-scope fog you can't ticket yet; graduates as the frontier advances -->

## Out of scope

<!-- work ruled beyond the destination; closed, never graduates -->
```

Each ticket is a child issue of the map with a body containing just `## Question` (the decision or investigation this ticket resolves), sized to one 100K token agent session, carrying a `wayfinder:<type>` label (research, prototype, grilling, or task).

## Fog of war

The map is deliberately incomplete: don't chart what you can't yet see. Beyond the live tickets lies the **fog of war**: decisions and investigations you can tell are coming but can't yet pin down, because they hang on questions still open. Resolving a ticket clears the fog ahead of it, graduating whatever's now specifiable into fresh tickets, one at a time, until the way to the destination is clear and no tickets remain.

**Fog or ticket?** The test is whether you can state the question precisely now, not whether you can answer it now. Ticket when the question is already sharp, even if blocked; Not yet specified when you can't yet phrase it that sharply. Don't pre-slice the fog into ticket-sized pieces: one patch may graduate into several tickets, or none.

**Out of scope** is separate: work beyond the destination is not fog. When an existing ticket turns out to sit past the destination, close it and leave one line in the Out of scope section: the gist plus why it's out of scope, linking the closed ticket.

## Chart the map

User invokes with a loose idea.

1. **Name the destination.** Work from both the grilling brief (`subagents/grilling.md`) and the domain-modeling brief (`subagents/domain-modeling.md`) to pin down what this map is finding its way to: the spec, decision, or change. The destination fixes the scope, so it's settled first.
2. **Map the frontier.** Grill again, breadth-first this time: fan out across the whole space rather than deep on any one thread, surfacing the open decisions and the first steps takeable now. **If this surfaces no fog** (the way to the destination is already clear, the whole journey small enough for one session), you don't need a map. Stop and ask the user how they'd like to proceed.
3. **Create the map** (label `wayfinder:map`): Destination and Notes filled in, Decisions-so-far empty, the fog sketched into **Not yet specified**.
4. **Create the tickets you can specify now** as child issues of the map, then wire blocking edges in a **second pass** (issues need ids before they can reference each other). Everything you can't yet specify stays in the fog.
5. **Fire the research subagents** in parallel for each research ticket, resolving them and capturing findings with a context pointer from the ticket.
6. Stop: charting is one session's work; it hand-resolves nothing.

## Work the map

User invokes with a map (URL or number). A ticket is optional: without one, you pick the next decision, not the user.

1. Load the **map**: the low-res view, not every ticket body.
2. Choose the ticket. If the user named one, use it; otherwise take the first frontier ticket in order. **Claim it** before any work.
3. Resolve it. **Zoom as needed**: fetch the full body of any related or closed ticket on demand; call the Skill tool for whichever skills the `## Notes` block names.
4. Record the resolution: post the answer as a **resolution comment**, **close** the issue, and **append a context pointer** to the map's Decisions-so-far.
5. Add newly-surfaced tickets (create-then-wire); graduate any fog the answer has made specifiable, clearing each graduated patch from **Not yet specified** so it lives only as its new ticket. If the answer reveals a ticket sits beyond the destination, **rule it out of scope** rather than resolving it. If the decision invalidates other parts of the map, update or delete those tickets.

The user may run unblocked tickets in parallel, so expect other sessions to be editing the tracker concurrently.
