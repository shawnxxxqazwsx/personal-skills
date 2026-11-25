---
name: onetake
license: PolyForm Noncommercial 1.0.0 (free for noncommercial use; see LICENSE)
metadata:
  author: Patrick (github.com/feitangyuan)
  lineage: otk-7f3e1c
description: "Render fixed-duration deterministic product motion videos and narrated feature demos (10–60 s .mp4, 1080p30 drafts / 4K60 180° shutter motion-blur final) from a single pure-function HTML composition (window.__seek(t)), measured move/carry library, real-page recordings or HTML-rebuilt UI with causal cursor interactions, room-matched synthesized/recorded SFX (-16 LUFS), multilingual TTS/Whisper/timeWarp voiceover & subtitles, and an anti-slideshow rhythm & continuity oracle. Trigger on 动效短片 / 产品发布视频 / 宣传片 / 介绍视频 / launch video / promo / teaser, real-page or HTML-rebuilt feature demos (产品功能演示 / 不录屏复刻界面), multilingual narrated/subtitled cuts (配音 / 字幕 / 多语言本地化), or auditing/fixing slideshow-like videos (像 PPT / 切镜生硬 / 缺乏节奏或连续转场). Do NOT use for interactive websites or landing pages meant for free browser scrolling/clicking, long-form or talking-head video editing, or projects where the user explicitly requests Remotion or HyperFrames."
---

# onetake

Deterministic short product motion films (`.mp4`) built from a single HTML composition (`window.__seek(t)`), a measured
move/carry library (`lib/motion.js`), real or HTML-rebuilt product UI, room-matched sound, and an automated oracle that
checks rhythm, continuity, motion blur, and framing before human review.

## When to use — and when not

- **Use** for 10–60 s launch clips, promos, teasers, kinetic-type films, reference-driven cuts (§1), real-page or
  HTML-rebuilt narrated/multilingual feature demos (§4, `references/product-demo.md`), and diagnosing slideshow-like cuts.
- **Do NOT use** for interactive web pages or sites meant for free user scrolling/clicking in a browser, long-form or
  talking-head video editing, or projects where the user explicitly requests Remotion or HyperFrames.

## The protocol — in this order, no skipping

### 1 · Deconstruct the reference before touching anything (硬规则)

```bash
python3 scripts/analyze_ref.py ref.mp4 --out ana/     # energy map, cuts, stillness, contact sheets, motion line
```

Read the energy map and contact sheets and record the target numbers before designing beats: stillness ratio, cut
positions/bursts, element scale, `motion:` median `t80` (snaps vs. S-curves), and smear (shutter blur vs. sharp).
See `references/reference-deconstruction.md`.

### 2 · Concept — three central ideas before any beat sheet (硬规则)

A concept is one sentence about the *visual mechanism*, not a feature list. Propose three concepts with genuinely
different central ideas — never three stories wrapped around the same card template:

- **one element transforms through everything** — e.g. a dot becomes caret → list → loading ring → spring curve → mark;
- **one camera move through scale** — e.g. year → day → half hour → back (`cases/clearing-15s/README.md`);
- **a before/after split** or **chain reaction** — every beat is the collision that triggers the next (`cases/knockon-15s/README.md`);
- or a physical metaphor, continuous surface, or typographic system.

For each concept specify: hook frame, carry mechanism across every boundary, what it excludes, and **its look** — a
named preset from `looks/` (`python3 scripts/look.py sheet` → `gallery/sheets/looks.png`: `paper`, `dusk`, `tabletop`,
`ultramarine`, `riso`, `ember`), extracted from product screenshots (`look.py from-shot shots/*.png --out look.json`),
or bespoke. Let the user pick before writing a beat sheet. Never default to the template's story or the last film's look.

### 3 · Storyboard as rhythm *and* carry

Write the chosen concept as a beat sheet: `t · beat · what moves · what is still · what carries into the next beat`.

- **Rhythm.** Vary shot lengths by ≥ 4× (e.g. 0.25 s hits beside 2.5 s holds), include ≥ 1 truly still rest in picture
  and sound, tell one story rather than a feature catalogue, and keep elements small on a generous ground.
- **Carry.** At every section boundary, name what survives and visibly moves or scales into the next beat (`morphRect`,
  `iris`, `zoomThrough`, `gather` → `seal`, persistent hand/subject). Bare cuts belong only to staccato hit bursts and
  the end card. See `references/rhythm.md`.

### 4 · Footage from the real thing — or HTML-rebuilt UI

```bash
python3 scripts/record_footage.py footage.json --out footage/
```

Drives real pages via Playwright at target size, injects a magenta action marker at input start, and outputs 30 fps
JPEGs plus the pointer path so the composition redraws the cursor as the visible cause.

**Or rebuild the UI in HTML.** For app walkthroughs (especially narrated or multilingual), capture only reference shots
and rebuild the UI in HTML in the reference's pixel frame: strings in one table, pure `set(state)`, DOM-measured
highlights (`lib/ui_kit.js`). Generate narration/timestamps/subtitles via `scripts/vo_tools.py`. Add languages with
`?lang=` on the same composition, aligned via `UIK.timeWarp` knots and verified pixel-identical for the source language
with `scripts/frame_diff.py`. See `references/product-demo.md`.

### 5 · Compose — one file, pure functions of time, library moves

```bash
mkdir -p cases/my-film && cp templates/comp.html lib/motion.js cases/my-film/   # loads motion.js → window.OM
python3 scripts/probe.py cases/my-film/comp.html                                # continuity per boundary + curves
```

Pick moves visually from `gallery/sheets/<move>.png` (39 moves across entrances, carries, contact/240 Hz sims, camera,
and fluid sets). Never hand-roll ad-hoc springs/eases with fixed constants. Keep `templates/comp.html`'s contract and
helpers, not its Case 1 beats unless chosen in §2. Preview `?play`, pin `?t=6.4&hud`. See
`references/motion-library.md` and `references/composition.md`.

- **Look & fonts:** `python3 scripts/look.py apply <look|look.json> cases/my-film/comp.html` writes `look.js` (8 color
  tokens + subset inlined OFL faces for `file://`). Load before the comp script, chain `window.__ready` on `LOOK.ready`,
  and pass `--cjk <font>` for CJK glyphs.
- **Operated camera:** key `OM.camera(t, keys)` slightly ahead (~0.1 s `sineInOut`) to chase or at landing (`expoInOut`)
  to whip; add subtle hand float (zero in holds), `OM.shake` on landings, and a faint `OM.lattice` for parallax. Export
  screen boxes in `__track` (`OM.projectBox`), peak screen travel in `__motion(t0, t1)`, and `__meta.inFrame`.

### 6 · Render — 1080p30 drafts, 4K60 only after acceptance

```bash
python3 scripts/stills.py comp.html --times 0.7,2.4,3.8,6.2,9.9,12.7 --out stills.png   # inspect before rendering
python3 scripts/render.py comp.html --out draft.mp4 --sfx sfx.wav                       # 1920×1080 · 30 fps · 180° shutter
python3 scripts/render.py comp.html --out film.mp4 --final --sfx sfx.wav                # 3840×2160 · 60 fps (post-approval)
```

`render.py` integrates real 180° shutter motion blur in linear light across parallel `--workers` (default cores − 2,
max 8), skips byte-identical holds, and adapts samples (4–48) from `window.__motion(t0, t1)` to keep streak spacing
within 6 px without stepping. Tell the user the time estimate before long renders (~0.2 s per Chromium capture). Pass
`--gpu` for WebGL compositions (SwiftShader is ~4× slower; `references/3d.md`).

### 7 · Sound — one palette in one room

```bash
python3 scripts/sfx_palette.py --demo demo.wav     # draft synthetic palette (see templates/sfx_score.example.py)
python3 dump_events.py && python3 score.py         # full mix: comp __events() → recorded + synth score
```

Build the action score before music: use either the 5-material room-matched draft palette (−8 dBFS peak) or a `score.py`
combining licensed/CC0 recorded sources with synthesis timed and panned from `window.__events()`, shared convolution
reverb, ducked music, and −16 LUFS master (ceiling −3.5 to −4 dBTP so AAC stays below −3 dBFS). Check SFX audibility
against music in shared event windows (800–4500 Hz) and avoid stock vibraphone/crotale endings. Default to royalty-free
music (keep source & licence beside the score); use commercial tracks only when supplied by the user. `references/sound.md`.

### 8 · Verify before showing

```bash
python3 scripts/verify_promo.py draft.mp4 --comp comp.html --ref ref.mp4 --shots 0,1.6,3.0,4.8,7.0,9.6,12.1,13.25,14.3
```

Checks `cadence` (shot CV ≥ 0.25), `rest` (≥ 25 % dead-still + ≥ 1.0 s quiet stretch), `burst` (fails if `--ref` has one
and the film doesn't), `audio` (peak ≤ −3 dBFS, 0 clips, ≥ 15 % quiet frames), `continuity` (carry score ≥ 0.5 pass,
< 0.7 warn), `curves` (fails > 80 px/frame moves without shutter blur), and `framing` (`__meta.inFrame`).

## Hard rules

- **Three distinct concepts before beat sheets (§2);** never silently reuse the template story or previous film's look.
- **One composition across languages:** use `?lang=` + `UIK.timeWarp` + `frame_diff.py`, never fork `comp.html`.
- **No metronome cuts** (shot length CV ≥ 0.25) and **no dead-motion fatigue** (true still rests, zero camera drift in holds).
- **Carry every section boundary** with a surviving moving/scaling element; `display:none` swaps are slides (except hit bursts & end card).
- **Small elements, generous ground (~70 %);** never shrink a full page into a thumbnail expecting its motion to read.
- **Visible cause:** redraw the recorded hand path or show the physical subject driving every reaction.
- **Library moves & t80 curves:** pick snaps/springs from `lib/motion.js` rather than uniform hand-rolled S-curves.
- **Real shutter blur on fast moves (> 80 px/frame);** use `render.py`'s shutter, never CSS blur as a substitute.
- **Operated camera & safe framing:** chase/lead subjects with `OM.camera` + `OM.lattice` and guard visibility via `__meta.inFrame`.
- **1080p30 drafts only** until approved; reserve `--final` (4K60) for accepted cuts.
- **No template confetti/speck bursts;** keep motion and flourishes native to the product or type.
- **One acoustic room & action-first mix:** fewer SFX than beats, clear 800–4500 Hz event SNR, no per-event synth beeps.
- **Strict determinism:** `window.__seek(t)` must be pure and idempotent; precompute sims at 240 Hz using `OM.rng(seed)`.

## Files

| path | what |
|---|---|
| `lib/motion.js` · `lib/ui_kit.js` | `window.OM` (39 moves, springs, carries, sims, camera, fluid) · `window.UIK` (UI replica stage, highlights, `timeWarp`, `subAt`) |
| `looks/looks.json` · `looks/fonts/` | 6 starting looks (8 tokens + 3 OFL faces each) and bundled OFL fonts/licences |
| `gallery/gallery.html` · `gallery/sheets/` | interactive move demos (`?demo=<name>&play`), 6-frame + speed sheets, and `looks.png` |
| `scripts/analyze_ref.py` · `probe.py` · `verify_promo.py` | reference energy/flow analysis, composition continuity/curve probe, and acceptance oracle |
| `scripts/record_footage.py` · `stills.py` · `render.py` | Playwright real-time capture, contact sheets, and parallel 180° shutter MP4 renderer |
| `scripts/look.py` · `sfx_palette.py` · `vo_tools.py` · `frame_diff.py` | look/font subsetting, room-matched SFX palette, Kokoro/Whisper VO & subs, pixel-diff check |
| `scripts/gallery.py` · `scripts/test_motion.js` | regenerate move sheets · `node scripts/test_motion.js` unit check |
| `templates/comp.html` · `footage.example.json` · `sfx_score.example.py` | Case 1 (`launch-15s`) composition skeleton, footage config, and example sound score |
| `references/reference-deconstruction.md` · `rhythm.md` | measuring references in numbers; rhythm (Case 1 `launch-15s`) and carry (Pocket Weather) rules |
| `references/motion-library.md` · `composition.md` | full `OM.*` catalogue, `f(t)` contract, hand path, operated camera, natural brush, shutter |
| `references/sound.md` · `product-demo.md` · `3d.md` | room/levels/event-driven SFX; HTML UI replica + multilingual VO; Blender GLB + WebGL `--gpu` pipeline |
| `cases/<film>/README.md` | 13 case breakdowns (beat sheets, numbers, lessons): `launch-15s`, `one-dot-15s`, `knockon-15s`, `clearing-15s`, `pith-21s`, `ebb-15s`, `domino-25s`, `infra-25s`, `clawd-desktop-19s`, `overlap-15s`, `unbroken-15s`, `skill-demo-15s`, `onetake-launch-30s` |

Requires: `python3` (`playwright` chromium, `numpy`, `scipy`, `Pillow`, `matplotlib`, `fonttools`, `brotli`, `opencv-python`),
`ffmpeg` / `ffprobe`, `node`. Narration: `faster-whisper` and Kokoro (`kokoro-onnx`, `soundfile`, plus `misaki[ja]` and
`unidic-lite` for Japanese) in `~/.cache/kokoro/venv`.
