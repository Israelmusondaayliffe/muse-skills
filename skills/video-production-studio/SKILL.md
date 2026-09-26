---
name: "video-production-studio"
description: "Coordinate brief-to-video production: route the request, plan, build, and QC the delivery. Use when the user wants a video made (explainers, product launches, PR explainers, website tours, music videos, slideshows, motion graphics, AI-generated clips, captions or overlays on existing footage) or asks for a video production plan. Routes to one production path, renders with the tools the host actually has, and inspects every delivery."
---

# Video Production Studio

Take a video request from brief to an inspected, delivered file. A request for a video is finished only when a rendered file exists, matches the requested size and length, and has been looked at. A plan, a storyboard, or a single title card is not the video unless that is what the user asked for.

## Start here

1. **Name the deliverable.** Finished video or plan only? Target width and height, duration (with a tolerance), platform, narration yes/no, captions yes/no. Take these from the request; fill gaps with the defaults in step 4.
2. **Check the host before choosing a route.** Run `command -v ffmpeg ffprobe`. Look at the current tool list and skill catalog for any generation tool (for example `media.generate_image` or `media.generate_video`), a narration skill, and browser delegation. Record what exists. Never assume a tool is present because a reference mentions it.
3. **Open every supplied asset.** List images, clips, audio, scripts, and URLs with their actual dimensions and durations (`ffprobe` for media). Note anything missing or unreadable.
4. **Pick one route** with the table below and the rules in `references/routing.md`. Fill `route.json` from `assets/route-template.json` and run `python3 bin/validate_route.py route.json`.

Defaults when the user did not say: 1920x1080 for landscape platforms, 1080x1920 for vertical social, 30 fps, h264 + aac MP4, no narration, captions only when there is a script or transcript. State the defaults you used in one line.

A clear request with its assets authorizes the build. Do not stop for storyboard approval, ask the user to confirm routine choices, or re-ask for facts already given. Stop and ask only when a key fact is missing (product claims, names, brand copy), when the user asked to review the plan first, or before any paid generation.

| The request and assets | Route | Runtime | First build step |
|---|---|---|---|
| Images or a deck, "make a video" | `slideshow` | `ffmpeg` | Write a slideshow manifest; run `bin/assemble_slideshow.py` |
| Existing video, "add captions" | `captions-only` | `ffmpeg` | Build the SRT from the supplied script or transcript; run `bin/burn_captions.py` |
| Existing footage, lower thirds or labels | `overlays-only` | `ffmpeg` | `references/graphic-overlays.md` |
| Short unnarrated type, stat, or logo piece | `motion-graphics` | `ffmpeg` | `references/motion-graphics.md` |
| Music track plus images or clips | `music-visualization` | `ffmpeg` | `references/music-video.md` |
| Website tour or product launch from a URL | `website-capture` / `product-launch` | `browser-capture` + `ffmpeg` | `references/website-capture.md` |
| Topic explainer with no supplied visuals | `faceless-explainer` | needs generated or supplied visuals | Check cost approval, or build from typography and supplied stills |
| "Write me a plan for a video" | any route | `none` | `references/planning-bundle.md` |

## Build

1. Work in `~/workspace/videos/<project>/` with the layout in `references/shared-pipeline.md`.
2. Follow the route's guide. Write the storyboard and script to disk as working records and keep building.
3. Paid or metered steps (AI generation, hosted narration) need the user's approval for the count and cost before the first call. Retries count against the same approval. Without approval, build from supplied and bundled assets and say what was left out.
4. Render to `renders/<project>-v1.mp4` at the bound width, height, fps, and duration.

## Inspect (every rendered delivery)

1. Technical: `python3 bin/inspect_delivery.py renders/<file>.mp4 --width W --height H --min-duration D1 --max-duration D2 [--require-audio] --output renders/qc-technical.json`.
2. Visual: extract frames (`ffmpeg -ss <t> -i <file> -frames:v 1 check_<t>.png`) at the opening, a text-heavy moment, a transition, the midpoint, and the end. Look at each one. Check text size and spelling, cropping, stretching, and safe areas (`references/delivery-qc.md`).
3. Record both in `qc-report.md` from `assets/qc-report-template.md`. A successful ffmpeg exit or a playable file is not proof of a good video.

## Worked example (illustrative)

Request: "Here are six product photos. Make a 20-second vertical video for Instagram with a soft music bed. No voiceover."

- Deliverable: rendered MP4, 1080x1920, 20 seconds (accept 19.5 to 20.5), no narration, audio present.
- Host check: `command -v ffmpeg ffprobe` finds both; no music was supplied.
- Assets: six JPEGs, all landscape 4000x3000. Landscape images in a vertical frame will be cropped, so choose pan motions that keep the product in view, and check the crops in the frames.
- Route: `slideshow`, runtime `ffmpeg`. Six slides at about 3.3 seconds each, alternating `zoom-in` and `pan-left`.
- Audio: no licensed music bed was supplied, and `assets/sfx/` holds effects, not music. Render without a music bed, or with a user-supplied track, and say so. Do not pull music from the web.
- Build: manifest with `"width": 1080, "height": 1920, "fps": 30`, then `python3 bin/assemble_slideshow.py manifest.json -o renders/mugs-v1.mp4`.
- Inspect: `inspect_delivery.py renders/mugs-v1.mp4 --width 1080 --height 1920 --min-duration 19.5 --max-duration 20.5`. Omit `--require-audio` because no audio track was supplied. Extract five frames and confirm each product stays in frame.
- Deliver: the MP4 path, the QC report, and `route.json` with `completion_state: "rendered-partial"` and `missing_requirements: ["soft music bed (no licensed track supplied)"]`. Tell the user the video is partial until they supply a licensed track. It is not `rendered-delivery-complete`, because the request included music.

A wrong version would stop to ask for storyboard approval, deliver a storyboard instead of the file, render 1920x1080 because that is the template default, call a silent video complete when music was requested, or call the job done without opening a single frame.

## When something goes wrong

| Symptom | Likely cause | Next move | Stop when |
|---|---|---|---|
| `command -v ffmpeg` finds nothing | Renderer not installed on this host | Set `completion_state: "blocked"`; deliver the planning bundle as supporting work and name the missing tool | immediately; a plan does not fulfill a requested clip |
| `assemble_slideshow.py` exits 3 | Missing ffmpeg/ffprobe or a failed ffmpeg step | Read the message; fix the bad input (path, image format) once and re-run | the second run fails the same way; report it |
| `inspect_delivery.py` fails width or height | Manifest or filter used the wrong size | Fix the manifest and re-render | never ship a wrong-size file as done |
| Duration outside tolerance | Slide durations don't add up, or audio set the length | Adjust durations and re-render | second miss; report the actual length |
| Frames show cropped or stretched subjects | Aspect mismatch between asset and frame | Change motion or crop and re-render; re-inspect | the asset cannot fill the frame; say so |
| A generation tool is missing or unapproved | Host capability or cost gate | Build from supplied assets; name what the generated parts would have added | the video cannot exist without generated footage; ask |
| Captions requested, no script or transcript | No caption source | Deliver without captions as `rendered-partial` and say why; never guess words | never invent caption text |

Allow one repair per failure within the approved scope. Do not retry blindly or spend beyond the approval. If one part is blocked, finish the rest and name the gap.

## Completion

Record the state in `route.json` with `requested_deliverable` (`clip` or `plan`) and `missing_requirements`, then run `bin/validate_route.py`.

- `rendered-delivery-complete`: a renderer produced the file, the technical check passed at the requested width, height, and duration, the visual inspection is recorded, and nothing the user asked for is missing. Deliver the file path and the QC report.
- `rendered-partial`: a render exists, but a requested element is missing: audio or music, captions, a required asset, or the requested size or length. List each in `missing_requirements` and say so first in the reply. Never call this complete.
- `blocked`: a clip was requested and no usable render exists. Deliver whatever supporting work exists and name the blocker. A plan never fulfills a requested clip.
- `planning-complete`: only when the user asked for a plan.
- Always include a short "What I did not verify" line when anything went unchecked.

## Operating rules

- **Build exactly what was asked.** A title card is a title card. Propose additions; don't add them silently.
- **One route and one runtime decision before building.**
- **No renderer fiction.** Use only tools you confirmed in step 2. HyperFrames, Remotion, and similar renderers are not part of this skill.
- **Media rights.** SFX come from the bundled `assets/sfx/` library (Pixabay Content License, credits in `assets/sfx/CREDITS.md`). Music must be user-supplied or licensed; never rip from the web. Inspect every generated asset before use.
- **Captions need a source.** Script, word timings, or transcript. Without one, do not claim caption accuracy.
- **Text minimums at 1080p:** 72 to 96 px headlines, at least 40 px body, title-safe margins of at least 80 px.
- **Durable handoff.** Write `route.json` and `qc-report.md` to the project folder, not only the chat.

## Resources

- `bin/`: `validate_route.py` (route validation), `inspect_delivery.py` (ffprobe checks, exact or minimum size, duration, audio), `validate_video_prompt.py` (AI prompt structure), `assemble_slideshow.py` (images + motion + audio to MP4; exits 3 when blocked), `burn_captions.py` (SRT or word timings to burned-in captions).
- `references/`: `routing.md`, `shared-pipeline.md`, `rendering-recipes.md`, `voiceover.md`, `captioning.md`, `ai-assets.md`, `website-capture.md`, `pr-explainer.md`, `music-video.md`, `motion-graphics.md`, `graphic-overlays.md`, `delivery-qc.md`, `planning-bundle.md`.
- `assets/`: `route-template.json`, `qc-report-template.md`, `sfx/` (licensed sound effects, manifest, credits).
