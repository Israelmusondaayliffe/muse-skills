# Provenance Policy

Use this reference while mapping sources, examples, methods, and public attribution.

## The central distinction

Privacy and provenance are separate decisions.

- Privacy asks what internal material must remain hidden.
- Provenance asks where the public method, evidence, or example came from and what the reader should be told.

Private operating material may contain a method derived from a public production. Hiding the private machinery does not require hiding the public production.

## Source classifications

### Public attributable

The source is public, permitted to cite, and useful to the reader's trust or understanding.

Public guide treatment: name it near the claim or method it supports and link the original source when appropriate.

### Public reference

The source is public and permitted, but naming it is optional because it supplies background rather than meaningful lineage.

Public guide treatment: cite where current behavior or a specific fact requires it.

### Private transform-only

The material may inform the guide but its private name, location, internal instructions, examples, or identifiers may not appear.

Public guide treatment: teach the approved general principle. Trace the principle back to an original public source when one exists.

### User-owned

The user owns or supplied the method, prompt, image, result, or observation and has approved its public use.

Public guide treatment: use only the approved parts. Do not add history, outcomes, labels, or intent that the user did not provide.

### Forbidden

The source may not inform or appear in the public guide because authority, rights, privacy, or scope is missing.

Public guide treatment: exclude it and record the resulting evidence gap.

## Evidence statuses

- `verified`: supported by an inspected authoritative source or direct evidence.
- `user-supplied`: stated by the user as their method or observation.
- `observed`: directly inspected in a source, interface, result, or artifact.
- `unrun`: a proposed example or workflow that has not been executed.
- `unknown`: the evidence is missing or contradictory.

Do not silently promote user-supplied or observed evidence to a broader verified result. Do not present unrun or unknown material as proof.

## Source order

1. User-supplied method and owned evidence
2. Original source or finished work behind the method
3. Current official product documentation
4. Approved public practitioner sources
5. Community discussions for language, pain points, and clearly labeled practice
6. Generalized private operating material for transformation only

If a generalized source stripped origin markers, follow its lineage backward before deciding that provenance is unavailable.

## Example rules

- Prefer a real, rights-safe example over fiction.
- Preserve the real example's public lineage when permitted.
- Use a planning example only when no suitable real example exists or the guide explicitly teaches planning.
- Label the example's run status at first use.
- Never replace available proof with fiction merely because fiction is easier to sanitize.
- Never invent why settings changed, why a result succeeded, or what happened between recorded steps.

## Public output exclusions

Keep these private unless explicitly authorized:

- Skill and subagent names, worker assignments, routing notes
- Private file paths, memory locations, internal workspace paths
- Private profile identifiers and account names
- Internal prompts, instruction text, and validation records
- Review records, review commentary, and approval history
- Memory contents, device names, and connection details
- Credentials, tokens, and anything security-marked

These exclusions do not cover an original public source that is independently permitted and materially supports the teaching.
