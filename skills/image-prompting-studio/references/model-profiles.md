# Model profiles

> Muse note: this skill writes prompts; the user runs them in their own image tool (Midjourney, ChatGPT Images, Gemini/Nano Banana, Seedream, Recraft, Ideogram, Luma, etc.). These profiles were verified 2026-09-13 against public owner docs and are refreshed only on user request.

Verified September 13, 2026. Stable skills hold the craft; these dated profiles hold model distinctions. Follow the user's named model. With no model, write a broadly compatible non-Midjourney prompt. Refresh these profiles when the user requests an update. A newer release does not silently replace a named version.

Only load the relevant family below. Product names, API identifiers and third-party app labels can differ. Before execution, inspect the actual selected label and exposed controls. API documentation is evidence about that API, not proof every browser product exposes its controls. These profiles authorize no paid API use.

## OpenAI Images

Current release: ChatGPT Images 2.5. OpenAI describes improved reference fidelity, focused editing, multi-turn consistency and complex layouts. API editions are Flare and Sunburst; do not substitute those names for the model label visible in ChatGPT. Sketch and image comments are ChatGPT features, not universal prompt syntax. [Release](https://openai.com/index/introducing-chatgpt-images-2-5/).

Keep the user's detailed NL, JSON envelope and system-style prompt recipes. Clearly separate what changes from preserved identity/composition. For iterative editing, ground each new instruction in the actual latest image. One prompt requesting eight separate images is a supported studio recipe to test on the selected surface; do not infer actual delivery count from the prose. No forced Thinking label, fixed seven-prompt quota, invented latency guarantee or claim that only OpenAI can research.

## Nano Banana / Gemini image

Current owner naming distinguishes Nano Banana 2 (`gemini-3.1-flash-image`), Nano Banana 2 Lite (`gemini-3.1-flash-lite-image`), and Nano Banana Pro (`gemini-3-pro-image`). Lite is not the substitute for a multi-reference or multi-turn task. Owner docs show text/image editing and search-grounded examples; available features depend on the model and surface. [Image guide](https://ai.google.dev/gemini-api/docs/image-generation).

Use the same detailed creative briefs and JSON/system formats when useful. Identify each reference's contribution and distinguish scene changes from identity. Keep coherent material, contact and light response. Do not impose a 120-word cap, ten outputs, mandatory pose change or aspect-ratio tail. State the intended ratio where relevant and verify the rendered result. Structured prompt fields do not automatically become Gemini API parameters. Exact output counts and flawless lettering are not guarantees.

## Seedream

Current researched family: Seedream 5.0 Lite and 5.0 Pro. ByteDance's releases describe stronger instruction following and design work; retain the named variant rather than silently switching it. [5.0 Pro](https://seed.bytedance.com/en/blog/beyond-generation-it-understands-design-introducing-seedream-5-0-pro), [5.0 Lite](https://seed.bytedance.com/en/blog/deeper-thinking-more-accurate-generation-introducing-seedream-5-0-lite).

Start with the shared prompt and tighten redundant prose when useful. Keep subject, action, layout, material, light, exact copy and the few preservation constraints that matter. This concise adaptation is a studio heuristic, not a universal word limit. Attach the actual reference and state the requested change. Preserve requested JSON if the user uses it; do not claim arbitrary JSON is a native provider schema. Verify search/edit/reference features on the chosen host.

## Recraft

Current researched versions: V4 and V4.1, with raster/vector choices where exposed. Use natural language with concrete design terms: shape geometry, contour, line weight, flat fills, palette, hierarchy, composition and intended medium. Choose vector output in the actual control when needed; the word vector alone does not prove an editable vector file was returned. Preserve exact text and verify it after rendering.

Do not carry forward the obsolete claim that styles are limited to V3. For supplied styles and controls, check current owner support. [V4.1](https://www.recraft.ai/docs/recraft-models/recraft-v4-1), [V4 prompting](https://www.recraft.ai/docs/prompt-engineering-guide/prompting-with-recraft-v4), [Styles](https://www.recraft.ai/docs/api-reference/styles).

## Luma Uni

Distinguish the named Uni product version from API model labels. The researched owner material includes Uni 1.1 product language and image API guidance. State spatial relationships, reference roles, perspective, materials and the intended transformation directly. Specify whether a camera change is a fixed-scene study or a new moment. [Release](https://lumalabs.ai/news/uni-1-1-api), [Prompt guide](https://docs.agents.lumalabs.ai/guides/images/prompt-guide), [Model guide](https://docs.agents.lumalabs.ai/guides/model).

Retain the absorbed Uni NL/JSON templates and use-case vocabulary. JSON may serve as structured prose; do not invent a native schema, negative-prompt parameter or seed control. Check the chosen surface before executing multi-reference edits or multiple outputs.

## Ideogram

The researched owner material includes Ideogram 4 structured JSON prompting. Native JSON in the documented Ideogram 4 route is different from arbitrary JSON pasted into a hosted prompt box. Preserve the user's format; adapt to the documented route only when that route is actually used. [JSON introduction](https://ideogram.ai/blog/ideogram-4-json-prompting/), [Owner prompt guide](https://github.com/ideogram-oss/ideogram4/blob/main/docs/prompting.md).

For typography and layout, state exact quoted copy, reading order, hierarchy, composition, medium and background. Check whether Magic Prompt or another rewrite feature is active when exact prompt fidelity matters; preserve the user's choice and do not silently change settings. Inspect rendered lettering and file type rather than assuming the brand promise establishes accuracy.

## Midjourney

Midjourney has its own prompt syntax and operational workflow. Use the two Midjourney prompting skills only when selected or clearly requested. Stable prose should describe the visible result; parameters and reference/profile identifiers belong at the end and must match the selected model and mode.

Current researched documentation includes V8.2, the updated Edit model and newer personalization identifiers. Historical codes remain useful when deliberately reusing source prompts. Do not upgrade a copied prompt's model/profile without request. Current account controls decide compatibility. [Versions](https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version), [Edit model](https://docs.midjourney.com/hc/en-us/articles/48495453462797-Edit-Model), [Personalization](https://docs.midjourney.com/hc/en-us/articles/32433330574221-Personalization), [Creating on web](https://docs.midjourney.com/hc/en-us/articles/33390732264589-Creating-on-Web).


## Maintenance

On an explicit model-update request, check the owner release and prompt guide, record the verification date, compare only claims that affect these skills, and run bounded relevant examples. Keep model numbers out of skill names. Preserve legacy recipe syntax as an example only where still useful; retire unsupported claims instead of inventing replacements. Flux is outside this studio's selected model coverage.
