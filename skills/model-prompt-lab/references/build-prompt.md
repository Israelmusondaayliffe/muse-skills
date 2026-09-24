# Build a Production Prompt

## Intake (ask if missing)

The task the model performs, the target model, the prompt surface (ChatGPT, GPT
Builder, API system/developer message, custom agent harness), the tools the
model will have, the output contract (schema, sections, length, tone), and
latency/cost constraints. Missing items get one round of questions; the prompt
still needs the user's real business details — never invent them.

## Structure

Default to lean Markdown headers, each section short, detail only where it
changes behavior. Use the model's native scaffold (GPT-5.6: Role / # Goal /
# Success criteria / # Constraints / # Autonomy / # Output / # Stop rules;
Fable 5: brief intent plus symptom-driven guards). If a section adds nothing,
remove it.

XML blocks only when they earn their place: a measured recurring failure mode,
a high-stakes invariant, a structured output contract for downstream parsing, or
a task-specific tool-orchestration block. Justify each block in the delivery.

## Discipline

- State each instruction once, in the right section.
- Absolute words (ALWAYS, NEVER, must) only for invariants. Judgment calls get
  decision rules: condition + response.
- One compact autonomy policy: what is safe without asking, what requires
  confirmation, which ambiguities trigger a question.
- Explicit stopping conditions for any agentic prompt.
- Expose only the tools the task needs; document return shapes, types, and
  error behavior.
- For short-answer requirements, add a must-include contract: what a short
  answer must still include (facts, decisions, caveats, next steps).

## Validate

Run `scripts/validate_prompt.py` on the finished prompt and report the results.
Fix FAILs; resolve WARNs by removing, consolidating, or justifying.

## Delivery format

```
## <Model> <Use Case> Prompt

### Model Configuration
- Model: [exact string]
- Reasoning effort / verbosity / mode: [values and why]
- Caching, persisted reasoning, safety identifier: [decisions]

### Prompt
[The complete, copy-pasteable prompt in its own code block]

### Structure Applied
- [One line per section: why it exists]

### Justified Blocks (if any)
- [Each block: the measured failure mode or invariant it addresses]
- If none: "None. The lean body covers the requirements."

### Customization Notes
- [What the user can change without breaking the prompt]
- [Which sections to add or remove for different scenarios]

### Validation Results
- [Output of validate_prompt.py or manual checklist]
```
