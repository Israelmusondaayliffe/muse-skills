# Music video (beat-synced)

Route `music-visualization`: the user supplies a music track (audio file, or
a video to pull audio from) and wants visuals cut to it. The music is the
spine — establish one track before anything else.

## Step 0 — Setup

Copy the track to `assets/bgm.mp3` (extract from video first if needed:
`ffmpeg -y -i video.mp4 -vn -c:a copy assets/bgm.mp3`). Stage any
user-supplied images/videos for weaving in on the beat grid. If the user
gave no music, ask — do not synthesize a genre choice silently. Typography
alone can carry a complete video; assets are optional.

## Step 1 — Analyze the music

One canonical analysis, trusted downstream. With `librosa` available:

```bash
python3 - <<'EOF'
import librosa, json
y, sr = librosa.load("assets/bgm.mp3")
tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
onsets = librosa.onset.onset_detect(y=y, sr=sr, units="time")
print(json.dumps({"bpm": round(float(tempo),1), "duration": round(librosa.get_duration(y=y,sr=sr),2),
                  "n_onsets": len(onsets), "beat_times": [round(float(b),2) for b in librosa.frames_to_time(beats, sr=sr)[:64]]}, indent=1))
EOF
```

Without librosa, fall back to ffmpeg energy/silence detection:

```bash
ffmpeg -i assets/bgm.mp3 -af silencedetect=noise=-30dB:d=0.5 -f null - 2>&1 | grep silence_end
```

Judgment call: if the music is genuinely rhythmic, cut on the beat grid;
if it is calm/ambient, the grid is a metronome the tracker imposed — pace
by phrases and energy instead, never hard-cut to it.

## Step 2 — Frame skeleton

Cut the track into **frames** at real musical changes: hard stops, energy
surges/drops, long silences, big density shifts. One frame = one visual
treatment; extra density goes *inside* a frame. Expect ~1–6 frames for a
typical track. For each frame set: time span, pacing (`beat_cut` or
`phrase_flow`), mood, one-line feel. Leave template/copy/color choices for
Step 3.

## Step 3 — Plan (user gate)

Fill each frame: kinetic-typography treatment, template, or motion-graphic
combo (references/motion-graphics.md); weave user images in with
beat-cut / Ken Burns on the grid. Present the plan; get approval.

## Step 4 — Build and assemble

Build frames as clips, then assemble on the beat grid with hard cuts at
frame boundaries (crossfades only inside calm `phrase_flow` sections).
`bin/assemble_slideshow.py` covers image-led frames; AI-generated motion
frames come from references/ai-assets.md. Sync check: the first frame of
each new section must land within ±2 frames of its musical anchor.

## Step 5 — QC

references/delivery-qc.md, plus: watch the full video once at speed and
once with eyes on the waveform — late/early cuts are the #1 failure.
