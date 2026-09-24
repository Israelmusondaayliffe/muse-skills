# Motion graphics

Route `motion-graphics`: short (usually ≤ 30s), unnarrated, design-led —
motion is the message. Kinetic type, stat/count-up hits, chart/data-viz,
logo stings, lower thirds, callouts, social overlays, animated
headline/tweet/news cards, motion posters, page highlights.

Not for: longer multi-scene or narrated pieces (`general-video`), narrated
website videos (`website-capture`), topic explainers (`faceless-explainer`),
product promos (`product-launch`).

## Approach: asset-first, ffmpeg-native

1. **Decide the asset strategy first.** Does the piece need real material
   (a webpage, tweet, news article, image)? If yes, source it before
   designing the shot — design around what you have. If no, the content is
   user-supplied text/numbers and you skip sourcing.
2. **Design the shot** around the assets: layout, motion, beats.
3. **Build with ffmpeg-native motion**: animated `drawtext` (position as a
   function of `t`), fades (`fade=in/out`), zooms/pans (`zoompan`), and
   composited stills. AI-generated motion plates via references/ai-assets.md
   when ffmpeg alone can't carry the look.

## Kinetic type recipe

Animate text with time-varying drawtext. Example — headline slams in from
the right with a fade:

```bash
ffmpeg -y -f lavfi -i "color=c=0x0a0a0a:s=1920x1080:d=6" -vf \
 "drawtext=fontfile=/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf:text='SHIPPED':fontsize=160:fontcolor=white:\
x='1920-(1920-560)*min(t/0.6\,1)':y=460:\
alpha='if(lt(t\,0.6)\,t/0.6\,1)':enable='lt(t\,4)',\
fade=t=out:st=5:d=1" \
 -c:v libx264 -pix_fmt yuv420p -r 30 kinetic.mp4
```

Stagger lines by offsetting `enable` windows. Keep the easing simple
(linear or eased via `min(t/D,1)` curves) — readability beats cleverness.

## Stat / count-up

Render numbers as a PNG sequence or drawtext with per-frame values is
impractical in one filter — instead generate the count-up as stills and
assemble:

```bash
# frames numbered 000.png..090.png, each showing the current value
ffmpeg -y -framerate 30 -i num_%03d.png -c:v libx264 -pix_fmt yuv420p countup.mp4
```

Generate the stills with Python (PIL) or ImageMagick from the design
system's palette and fonts.

## Chart / data-viz hits

Build the chart as a still (Python/matplotlib or a generated image in
brand colors), then animate: bar-grow via `crop` height as a function of
`t`, line-draw via a reveal wipe, number punch via scale. One idea per
graphic.

## Logo sting / lower third / overlay

Logo sting: fade + scale-up on the mark (user-supplied logo, never
re-drawn from memory), hold, fade out — 3–5s total. Lower thirds and
callouts: references/graphic-overlays.md design rules, drawtext/overlay
implementation.

## Limits (be honest)

ffmpeg-native motion is 2.5D: fades, slides, zooms, wipes, type reveals.
No particle systems, no 3D, no character animation. When the brief needs
that, generate the plate with `media.generate_video` (references/ai-assets.md)
and composite text/overlays in ffmpeg — say so in the plan rather than
faking it.
