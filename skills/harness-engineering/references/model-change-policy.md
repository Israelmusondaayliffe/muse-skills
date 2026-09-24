# Model Change Policy

Treat model-specific compensations as provisional.

When the user requests the latest or current model, check current official documentation before selecting a model or rewriting prompts. Preserve an explicitly named target unless the user asks to change it.

After a major model change:

1. Freeze the current prompt, model, effort, tool inventory, routing state, hashes, and representative behavior suite.
2. Run every case more than once under fixed conditions.
3. Remove one coherent instruction group and compare the shorter candidate with the frozen baseline.
4. Restore any batch that introduces a critical failure, lowers a category, or lowers the overall pass rate.
5. Recheck approval behavior, tool routing, response length, stop conditions, task-start capability context, and completion evidence after installation.
6. Remove reminders the new model follows without them.
7. Keep stable user policy separate from temporary model corrections.

Do not compare runs whose model, effort, tools, or task conditions differ. Rescore frozen raw outputs when evaluation logic changes. Follow `references/prompt-governance.md` for the complete subtraction contract.

Do not invent model names, parameters, prices, or availability.
