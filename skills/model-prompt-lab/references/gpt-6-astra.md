# GPT-6 Astra — Evidence-Boundary Procedure

Use for Astra prompts, Astra migration, or Astra prompt audits. Astra is a
model family whose details (slugs, parameters, pricing, availability, rollout)
are not yet pinned down. The procedure protects you from turning early reports
into permanent harness policy.

## Evidence boundary

1. Ask the user for their accepted field observations first, and record them.
   Those are the only Astra facts you may act on.
2. Never invent an Astra model slug, API parameter, effort enum, price,
   availability date, or rollout state.
3. In a prompt delivery, write the target as `GPT-6 Astra` in prose and mark
   configuration as **verify on the target host** until the owning surface
   exposes exact values.
4. Local availability is required only for runtime acceptance; preparing and
   auditing the prompt overlay does not require it.

## Routes

- **New prompt:** follow `references/build-prompt.md`, but keep the model
  configuration section as a verification list instead of concrete values.
- **Existing prompt moving to Astra:** follow `references/migrate.md`; audit for
  overcomplicated interfaces, landing-page bias, and extra controls or labels.
- **Existing Astra prompt with a specific failure:** follow
  `references/diagnose.md`; diagnose against the user's field evidence before
  adding instructions.

## Audit checklist (Astra overlay)

- Strip controls or labels that assume parameters not in the user's evidence.
- Resist landing-page bias: copy text from announcements is not behavior data.
- Keep effort and cost restraint explicit but unverified: name the lever, not
  the value.
- Over-instruction in the overlay is the main failure mode — same subtraction
  discipline as every other model here.
