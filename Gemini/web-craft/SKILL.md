---
name: web-craft
description: >-
  Full-stack web visual design, interaction choreography, and headless browser engineering verification
  across static HTML/CSS and Vite, Astro, React, Next.js, Vue, Svelte, or Tailwind. Routes every task
  explicitly into Track A `commerce` (company, SaaS, AI, developer-tool, hardware, consumer-product,
  service, and local-place sites with disciplined screen rhythm, real licensed photography, 931 real
  brand icons, and automated browser gate checks) or Track B `showcase` (motion-first creative sites,
  portfolios, campaigns, URL/video motion replication, spring and follower handfeel tuning, 2D cutout
  image-plane perspective depth, zero-dependency 2D fragment shaders, tactile SVG/Canvas textures, and
  live WebAudio soundscapes). Use when building, redesigning, auditing, replicating, or polishing
  marketing and creative web pages, or fixing pages that look generic, templated, or AI-generated.
  Not for admin dashboards, true 3D mesh/WebGPU/physics engines, fixed-duration MP4 promo videos,
  quantitative statistical charts/reports, or standalone AI bitmap generation.
---

# web-craft

Build complete, production-grade web pages with deliberate visual hierarchy, honest copy, authored motion, and automated headless verification. `<skill>` denotes this skill folder (requires Node 22+, Python 3.10+, and Chrome/Edge/Chromium).

## Scope Boundary

- **In scope:** Interactive browser web pages and frontend surfaces (`HTML/CSS/JS`, `Vite`, `Astro`, `React`, `Next.js`, `Vue`, `Svelte`, `Tailwind`) — commercial websites, SaaS/AI/developer-tool pages, physical product and hardware pages, service and local-venue pages, creative portfolios, launch/campaign microsites, URL or video interaction replication, spring/follower handfeel tuning, scroll-timeline pacing and discoverability audits, 2D cutout planes in a perspective camera, 2D fullscreen fragment shaders, and real-time WebAudio interaction soundscapes.
- **Out of scope (do NOT use this skill for):**
  - Logged-in application back-offices, admin panels, or high-density operational dashboards;
  - True 3D polygon/GLB scenes, WebGPU node-graph shaders, GPGPU particle/fluid compute, PBR lighting/post-processing pipelines, or rigid-body physics simulations;
  - Fixed-duration deterministic `.mp4` promotional videos, offline shutter motion-blur rendering, or TTS voiceover mastering;
  - Quantitative statistical charts, multi-chart data dashboards, or data-backed whitepapers and annual reports;
  - Generating standalone AI raster bitmap files (`.png`/`.jpg`/`.webp`) or reference-guided image edits when the requested output is an image asset rather than web code.

---

## 1. Step 1 — Route to Track A (`commerce`) or Track B (`showcase`)

Web pages follow two measurably distinct design and motion dialects. Mixing their rules causes layout, font, scroll, and hover contradictions. **Classify every request into one track before planning or writing code:**

| Dimension | Track A · `commerce` (Commercial, Product & Place) | Track B · `showcase` (Creative, Motion & Replication) |
|---|---|---|
| **Target briefs** | Company sites, SaaS, AI, devtools, fintech, games, hardware, consumer goods, clinics/firms/agencies, cafes/hotels/shops/local venues | Motion-first creative sites, portfolios, studios, event/campaign pages, URL/video motion replication, handfeel/timeline/affordance audits, 2D image-plane 3d, 2D shaders, WebAudio |
| **Macrostructure & width** | **One section per screen** (`100svh`/`200svh` via `--h: 1\|2`), hero alone on screen 1; equal `.wrap` edges (`1280px`, `1200px` on `place`) | Mechanic-driven shape (`1vh` instrument or `7–57vh` acts / single-scene / editorial / index); **no global `body { max-width }`**, per-element `.measure`, `≥3` distinct section shapes |
| **Scroll & curves** | Native scroll only (no Lenis, no wheel hijack); monotonic ease-outs (zero bounce/overshoot); scroll motion **only** inside 1–2 dealt `[data-moment]` sections or 1 tech `[data-big-scene]` | Underdamped springs, `1 - exp(-k·dt)` + `speed/k` lead followers, native CSS `animation-timeline` (`@supports`), Framer/GSAP, or explicit `--rail` / `--stack` choreography |
| **Typography & fonts** | Curated Google Fonts pairings via `start.mjs` (`display=swap`); display weight `400` (`500` on tech), text `400`/`500`, never `700`/`800`; bans default grotesks | Extreme scale jump (`display ÷ body ≥ 4×`, target `≈8×`) via `clamp()` with `rem` floor; self-hosted `.woff2` or OFL base64-inlined faces via `subset_fonts.py` + metric overrides |
| **Hover & components** | Product dialect + `assets/motion` layer: linked cards lift `2px`, linked photos zoom `1.02–1.03`, buttons step `1px` & press `.985`, tech card loops `2.5–4s` with pause disc | Creative dialect (median `1` radius, `0` shadows, `0` nav CTAs, 2-col footer); element-specific hover (no uniform card lift); product controls allowed inside a creative canvas |
| **Verification gate** | `copy-lint.mjs` + `consistency.mjs` + `assets/layout/check.mjs` + `perf.mjs` + `gate.mjs` | Still-frame slop gate (`prefers-reduced-motion` screenshot first) + `verify_case.py` + `measure_structure.py` / `measure_churn.py` |

- **Tie-breaker:** When conversion clarity, live product UI, or physical venue/goods trust leads → **Track A**. When an expressive interaction mechanic, spatial narrative, or reference motion feel leads → **Track B**.
- **Hybrid boundary:** An interactive Track B instrument (`cases/string-clock`) keeps **Creative** page chrome (one radius, zero shadows, quiet masthead) while giving its embedded control strip **Product** affordance (pill segmented toggle, crisp `:focus-visible`).

---

## 2. Shared Non-Negotiables & Foundations (Both Tracks)

1. **Copy before layout, zero fabrication:** Layout responds to real text length. Name what is sold and for whom in `<h1>`; write verb+object buttons (`Book a room`, `Start free trial`, never `Learn more` or `Get started`). Never invent customer counts, percentages, named quotes, client logos, street numbers, postcodes, VAT/register IDs, or phone numbers. Mark permitted assumptions (`data-assumed` in Track A; `[…]` slots reported explicitly in Track B). See [shared-anti-slop-and-copy.md](references/shared-anti-slop-and-copy.md).
2. **Zero AI-slop palette defaults:** Never use violet/indigo/lavender (`#6366f1 → #a855f7` or OKLCH hue `275°–330°`) as page ground, accent, glow, or gradient, and never use multi-hue rainbow cycling. Keep chrome 90%+ neutral with one committed accent. Real third-party brand marks keep their authentic colours (`icons.mjs --colour`).
3. **Still-frame & reduced-motion integrity:** With `prefers-reduced-motion: reduce` or JS disabled, every piece of content must stand complete, readable, and navigable — nothing stuck at `opacity: 0` or mid-keyframe. Author the finished state first and layer motion on top.
4. **Accessibility, responsive & GPU floor:** Set `<html lang>`, `<title>`, `<meta name="description">`, OpenGraph (`og:image`), favicon, skip link, exactly one `<h1>`, sequential headings, visible `:focus-visible`, `@media (hover: hover)` guards, and `≥44×44px` touch targets. Reserve width/height or `aspect-ratio` on all media (`CLS < 0.05`). Zero horizontal overflow at `320`, `375`, `390`, `768`, `1024`, and `1440` (`overflow-x: clip`, never `hidden` on `html` when using `sticky`). Cap canvas DPR (`≤2`, `≤1.5` on heavy shaders) and hold `≤4` live WebGL contexts per page, pausing off-screen and in hidden tabs.
5. **CJK & multilingual discipline:** Pair Latin display faces with explicit CJK fallbacks (`'Noto Sans SC'`, `'Source Han Sans SC'`, `'PingFang SC'`), set `line-break: strict` + `word-break: auto-phrase`, keep CJK body line-height `1.65–1.8`, and never set `letter-spacing < 0` on Chinese/Japanese text.
6. **Framework parity:** Static builds copy `<skill>/assets` to `./assets`; Vite/Astro/Next/SvelteKit put kit assets under `public/assets` and CSS tokens in `tokens.css` (mapped into Tailwind `@theme` when Tailwind v4 is requested). See [shared-tokens-and-polish.md](references/shared-tokens-and-polish.md) and [shared-components-states.md](references/shared-components-states.md).

### 2.1 Seven Page Blueprints & Visual Archetypes
Commit to one blueprint cadence before laying out sections ([shared-anti-slop-and-copy.md](references/shared-anti-slop-and-copy.md)) and one visual system from [visual-bank.json](data/visual-bank.json) (30 curated archetypes) or `start.mjs` in Track A — never mix two archetypes on one page:

| Blueprint | Track Fit | Canonical Section Cadence | Signature Restraint |
|---|---|---|---|
| `editorial` | Track B / A | Masthead → thesis hero → alternating essay/plate spreads → colophon | Asymmetric measure (`58–65ch`), generous margin air, zero card grids |
| `studio` | Track B / A | Quiet index header → flagship case stage → numbered work roster → contact | Work speaks at full bleed; zero self-congratulatory adjectives |
| `product` | Track A | Hero + live `app-frame` → 3 workflow proofs → spec/integration band → CTA | Real HTML product UI and real tool marks; zero abstract blobs |
| `tool` | Track A | Command/demo hero → interactive benchmark or code/output split → docs/install | Immediate runnable or inspectable artifact above the fold |
| `docs` | Track A | Sticky rail + prose column + right TOC → runnable examples → prev/next | High scan clarity, `tabular-nums`, zero decorative scroll effects |
| `campaign` | Track B / A | Cold-open or poster hero → 3 narrative acts → release/ticket/drop action | One committed theatrical mechanic; exits cleanly at CTA |
| `personal` | Track B | Voice-first opening + live craft artifact → selected notes/work → direct mail | Human register, small footprint, zero SaaS chrome |

### 2.2 Baseline Semantic Token, Fluid Type & Reduced-Motion Skeleton
```css
:root {
  --ground: #f6f4ef; --surface: #ffffff; --ink: #151412; --muted: #666258;
  --line: color-mix(in oklab, var(--ink) 14%, transparent); --accent: #b8441e;
  --step-body: clamp(1rem, 0.96rem + 0.22vw, 1.125rem);
  --step-display: clamp(2.5rem, 1.4rem + 5.2vw, 6.5rem); /* rem + vw keeps browser zoom working */
  --ease-out: cubic-bezier(0.22, 1, 0.36, 1);
  --ease-editorial: cubic-bezier(0.77, 0, 0.18, 1);
}
*, *::before, *::after { box-sizing: border-box; }
html { overflow-x: clip; -webkit-text-size-adjust: 100%; text-size-adjust: 100%; }
body { margin: 0; background: var(--ground); color: var(--ink); font-size: var(--step-body); line-height: 1.55; }
img, svg, video, canvas { display: block; max-width: 100%; }
.measure { max-width: 62ch; }
.num { font-variant-numeric: tabular-nums; }
:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important; animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important; scroll-behavior: auto !important;
  }
}
```
Declare render layer explicitly on Track B (`dom`, `svg`, `canvas2d`, or `webgl` via `verify_case.py --layer`): keep selectable text and controls in DOM, crisp vector chrome in inline SVG, generative glyph/particle fields in Canvas 2D, and fullscreen organic fields or MRT silhouette passes in zero-dependency WebGL2 ([motion-2d-shaders-textures.md](references/motion-2d-shaders-textures.md)).
Keep physics state in plain JS closures/refs (`dt = Math.min(rawDt, 1/30)`), use exponential decay `1 - Math.exp(-k * dt)` with velocity lead `target + targetVel / k` for followers that must arrive without FPS drift, and guard trackpad wheel detents with accumulate-threshold + cooldown ([motion-handfeel-and-recipes.md](references/motion-handfeel-and-recipes.md)).

---

## 3. Track A (`commerce`) Workflow

### 3.1 Classify Business Kind
Set `<html data-type="...">`, `<meta name="page-type">`, and `<meta name="site-kind">` (`place` also sets `<meta name="page-kind" content="place">`):

| Brief | `page-type` | `site-kind` | `--page` / `--kind` | Visual & Effect Policy |
|---|---|---|---|---|
| SaaS, AI, devtool, fintech, app | `software` | `software` | `software` | Live HTML product UI (`app-frame` + `assets/ui` fragments), real tool icons, 0–2 pulsing diagrams, 1 dealt effect/scene, 1–2 moments; 60–80 words/screen outside UI |
| Game or game launch | `software` | `gaming` | `gaming` | Game name + genre in `<h1>`, full-bleed key art/trailer (or setting stand-ins via `photos.mjs search`), Steam/PlayStation/Epic icons, no SaaS UI fragments |
| Tech hardware / device | `product` | `tech` | `tech` | Real or stand-in photos of the device whole (≤3 sections) + use/parts (`product-render` only when 3D is requested); 1 dealt effect allowed |
| Consumer product / brand | `product` | `other` | `product` | Photographs lead (whole in ≤3 sections, swatch swaps image, every headline promise pictured); flat grounds, **0 shader effects** (`product-render` only on 3D ask) |
| Clinic, firm, agency, studio | `service` | `other` | `service` | Real work/team/room photos, services list, real tool icons, ≤1 still diagram; flat grounds, **0 shader effects** |
| Cafe, bakery, hotel, shop, venue | `place` | `other` | `place` | Photographs lead (12–20 full, 8–12 compact, `<8` 3-screen short page), screen-2 Visit block, 2 distinct photo compositions + 1 display-type moment, flat grounds, square photos, phone `actionbar`, **0 effects/loops/diagrams** |

### 3.2 Ten Track A Layout & Media Rules
1. **Screen-unit heights (`--h: 1` or `--h: 2`):** Every section is `100svh` or `200svh` on desktop (`min-height` on mobile); never use `scroll-snap-type`.
2. **Hero owns screen 1 alone:** Deal one of the 11 heroes via `assets/layout/deal.mjs` (or the dedicated `place` hero); keep primary CTA visible above the fold.
3. **Clean `.wrap` edges:** Every row starts on the left `.wrap` line and ends on the right `.wrap` line (or bleeds symmetrically to both viewport edges).
4. **Word economy:** Keep 60–80 words per screen outside live UI frames; one clear claim per section.
5. **Heterogeneous cards:** Never stack 3 identical icon-heading-blurb boxes; vary card scale/content or use a ruled list, split proof band, or live UI frame.
6. **Live HTML product UI (`software`):** Build real interactive DOM inside `app-frame` (`assets/ui` fragments); never fake an app with grey skeleton bars.
7. **Licensed photographs (`photos.mjs`):** Never write captions underneath visuals — write one combined credit line in the footer (`photos.mjs credits --write`).
8. **Authentic icons (`icons.mjs`):** Resolve all brand/file/UI icons locally from the 931-entry catalog; never hand-draw third-party brand SVGs.
9. **Restrained motion (`moments.mjs`):** Deal 1–2 moments (`[data-moment]`) per page and enter the hero once on load; all other sections remain calm on scroll.
10. **Kit integrity:** Never edit copied files under `assets/` or `scripts/` (`kit-edited` is an unwaivable FAIL); put overrides in page CSS/markup.

### 3.3 Deal, Build & Gate Sequence
Run sequentially from the project folder (starting from `assets/starter.html`; see [commerce-layout-sections.md](references/commerce-layout-sections.md) and [commerce-media-and-moments.md](references/commerce-media-and-moments.md)):

```bash
# 1. Arm the finish gate before building (use dev URL or --root dist/out for frameworks)
node <skill>/scripts/gate.mjs --start index.html --kind <kind> --category "<what is sold>" --primary "<main action>"

# 2. Deal hero, trade palette + pairing, moments, and optional tech grounds/effects (never pick by taste)
node <skill>/assets/layout/deal.mjs --type <page-type> --has <photo,ui,film,object,setting> --history .web-craft/layout-history.json
node <skill>/scripts/start.mjs deal --page <kind> --trade <trade> --history .web-craft/history.json
node <skill>/scripts/start.mjs css --page <kind> --palette <id> --type <id> --radius soft --history .web-craft/history.json
node <skill>/scripts/moments.mjs pick --page <kind> --count 1|2 --fits section,statement --photo --history .web-craft/history.json

# 3. Resolve photographs, credits, and local full-colour brand/file/UI icons
node <skill>/scripts/photos.mjs pick --trade <trade> --sections <list> --history .web-craft/history.json
node <skill>/scripts/icons.mjs scan index.html --out assets/icons --colour
node <skill>/scripts/photos.mjs credits --out . --write

# 4. Run staged checks (foreground, one headless Chrome at a time, Chrome profile inside OS temp or .web-craft/)
node <skill>/scripts/copy-lint.mjs index.html --kind <kind>
node <skill>/scripts/consistency.mjs index.html --widths 1440,1024,820,768,390 --rhythm-widths 1440,820,768,390 --profile .web-craft/chrome-check --page <kind> --category "<what is sold>" --primary "<main action>"
node <skill>/assets/layout/check.mjs --url index.html --profile .web-craft/chrome-layout --sizes 1440x900,1024x768,820x1180,768x1024,390x844 --shots shots/layout
node <skill>/scripts/shoot.mjs --url index.html --w 1440 --out shots/1440.png --profile .web-craft/chrome-shoot
node <skill>/scripts/perf.mjs index.html --profile .web-craft/chrome-perf
node <skill>/scripts/gate.mjs index.html
```

Record legitimate false-positive waivers (max 5, never for `kit-edited` or `checker-gaming`) in `.web-craft/waivers.json`, and report the final `GATE:` verdict, deal choices, waivers, and stand-ins.

---

## 4. Track B (`showcase`) Workflow

### 4.1 Independent Page & Motion Ladders (Start at the Lowest Rung)
- **Page Stack Ladder:** Rung `0` single `.html`/`.css`/`.js` → Rung `1` Vite vanilla TS/JS → Rung `2` Astro + islands (`≥5` routes / content collections) → Rung `3` Next.js App Router (only when an authenticated product backs the site).
- **Motion Stack Ladder:** Rung `1` CSS transitions → Rung `1.5` native `animation-timeline: scroll()/view()` + `sibling-index()` inside `@supports` → Rung `2` vanilla `rAF` springs, velocity lean, Verlet chains, and `1 - exp(-k·dt)` followers → Rung `3` alpha-masked 2.5D lighting on flat cutouts → Rung `4` Framer Motion / GSAP `ScrollTrigger` (`gsap.context()` cleanup) → Rung `5` flat 2D cutout planes in a `PerspectiveCamera` (when camera moves through depth and silhouettes do not rotate).

| Feel Symptom | Mechanical Root Cause | Direct Solver Fix |
|---|---|---|
| Robotic / weightless | Monotonic lerp with zero attitude | Underdamped spring (`K=60–90`, `D=0.86–0.93`) + velocity lean (`vel * 0.5`) |
| Lags moving pointer/scroll | First-order filter steady-state lag `speed / k` | Lead target `aim = target + targetVel / k` before `follow(cur, aim, k, dt)` |
| Different feel at 30/60/120fps | Per-frame constant `x += (t - x) * 0.1` | Frame-rate-independent `1 - Math.exp(-k * dt)` with `dt = Math.min(rawDt, 1/30)` |
| Trackpad double-steps / jitter | Inertial wheel tail or post-filter offset | Wheel threshold + `600ms` cooldown; filter ground/lift offsets *before* target |
| Dead scroll notches / hidden door | Overlapping track plateaus or early ring exit | Offset plateaus horizontally; enforce `affordance_window ⊇ dwell_window` |

### 4.2 Five Choreography Arcs (Commit to One Before Coding)
| Arc | Scroll & Pacing Character | Typical Hero / Act Rhythm | Primary Curve / Solver | Avoid For |
|---|---|---|---|---|
| `editorial` | Calm reading pace, mask line reveals, tactile stillness | Unpinned `85–100vh` hero + asymmetric acts (`≥3` shapes) | `cubic-bezier(.77,0,.18,1)` (`700ms`), `80ms` line stagger | Hyper-kinetic game launches |
| `kinetic` | High-energy velocity skew, elastic detent snaps, bold type | Full-viewport instrument or `--rail` / `--stack` acts | Underdamped spring (`K=75, D=0.88`) + velocity lean | Long-form essays or legal/medical |
| `spatial` | Camera or world travels through layered depth planes | Dolly path (`fov 26°`) or `containerGL.y` depth scroll | Exponential follower (`k=4.5`) + `speed/k` lead | Text-heavy documentation |
| `ambient` | Continuous organic field, subtle pointer ripple, audio breath | Single-scene or slow dissolve chapters (`~50%` stillness) | 2D WebGL2 fragment shader / 11 Hz boil + `smootherstep` | High-SKU e-commerce catalogs |
| `cold-open` | Zero chrome at `t=0`; immediate live mechanic invites touch | Immediate interactive stage; title/credits arrive second | Direct pointer/wheel physics (`dt ≤ 1/30`) | Sites needing instant nav tree |

### 4.3 Reference, Video, Cutout Depth & Audio Protocols
- **Unplayable video / social link:** Check thread replies first for the author's live URL (confirm it is live web DOM/WebGL rather than an offline motion render). For local `.mp4`/`.mov` files, run `python3 <skill>/scripts/measure_frames.py sheet|palette|bands|trace|grounds|wipe ref.mp4`; if unreachable, ask for 2–3 keyframes and state explicit trajectory math before coding.
- **Live URL replication:** Measure the target work directly (never gallery listing chrome) with `measure_structure.py <url>` and `measure_churn.py <url>`. Recreate the physics, timing ratios, and structural rhythm on the user's own content and palette — never copy brand assets or copy.
- **Cutout depth & live audio:** Generate `elements.json` (`w, h, cx, baseline, crown, coverage, paint`) via scripted border-median keying before placing 2D planes ([motion-image-plane-3d.md](references/motion-image-plane-3d.md)). Route live WebAudio through `bgm` / `hand` / `world` buses with `≥15 dB` REST contrast ([motion-scene-audio.md](references/motion-scene-audio.md)).

### 4.4 Deterministic Probes, Fonts & Oracle Verification
1. **Design the still frame first:** Screenshot under `prefers-reduced-motion: reduce` before tuning curves; subset and inline real OFL web fonts via `subset_fonts.py` (`--draws-own-type` only when glyphs are procedurally drawn).
2. **Expose deterministic probes:** Wire `window.__seek(p)` (scroll/timeline `0..1`), `window.__hold(dt)` (deterministic physics step), `window.__clock(t)` (shader/boil clock pin), and `window.__probe()` (domain state readout) so headless scripts measure real mechanics rather than `setTimeout` guesses ([verification-oracles.md](references/verification-oracles.md)).
3. **Run measurement & mechanism oracles:**

```bash
python3 <skill>/scripts/subset_fonts.py list
python3 <skill>/scripts/subset_fonts.py pack index.html --face <family>
python3 <skill>/scripts/measure_structure.py https://example.com
python3 <skill>/scripts/measure_churn.py index.html --against https://example.com
python3 <skill>/scripts/verify_case.py index.html [--strings|--layer webgl --follow|--rail|--stack|--flipbook|--curtain|--lyre|--beats|--detent]
```

### 4.5 Verified Runnable Mechanism Library (`cases/`)
Lift **mechanisms** (solvers, homography guards, boil clocks, probe contracts) verbatim; **never copy skins** (palettes, copy, grids). Author new cases via [AUTHORING.md](cases/AUTHORING.md):
- [string-clock](cases/string-clock/README.md): elastic Verlet hands with stiff datum endpoint (`--strings`) and creative-canvas / product-control split.
- [ink-crowd](cases/ink-crowd/README.md): zero-dep WebGL2 MRT depth-discontinuity outlines + static warp vs 11 Hz boil clock (`--layer webgl --follow`).
- [press-stack](cases/press-stack/README.md): native-scroll `position: sticky` stack with `100vh` dwell, document-read progress, and procedural canvas art (`--stack`).
- [wheel-rail](cases/wheel-rail/README.md): hijacked-wheel translated rail, 3-plane pointer parallax, manual sticky parking, high element churn (`--rail`).
- [toy-flipbook](cases/toy-flipbook/README.md): 4-frame discrete yaw scrub (`Math.round` of spring, zero transition) + 11 Hz jitter + wheel hop/squash (`--flipbook`).
- [char-curtain](cases/char-curtain/README.md): 24 horizontal-link-free Verlet glyph columns parted by anisotropic pointer force (`--curtain`).
- [lyre-crows](cases/lyre-crows/README.md): strummable strings, source rate-limiting, force-clamped steering crows, FIFO tail state (`--lyre`).

---

## 5. Skill Directory Map & On-Demand Reference Index (`references/`)

- **`scripts/`:** Track A Node.js CLIs (`gate.mjs`, `consistency.mjs`, `copy-lint.mjs`, `perf.mjs`, `shoot.mjs`, `start.mjs`, `icons.mjs`, `photos.mjs`, `moments.mjs`, `effects.mjs`) + Track B Python CLIs (`verify_case.py`, `measure_structure.py`, `measure_churn.py`, `measure_frames.py`, `subset_fonts.py`).
- **`assets/` · `library/` · `data/` · `cases/`:** Production CSS/JS kit (`starter.html`, `system.css`, `layout/`, `backgrounds/`, `moments/`, `effects/`, `scenes/`, `objects/`, `ui/`, `diagrams/`, `photos/`, `icons/`, `fonts/`), `library/{palettes,type}.json`, `data/visual-bank.json`, and 7 runnable `cases/`.

Load **only** the reference documents needed for your active track and task:

| Reference | Scope | Load When |
|---|---|---|
| [shared-anti-slop-and-copy.md](references/shared-anti-slop-and-copy.md) | Shared | Every build or audit: still-frame/motion slop gates, category-first copy, voice registers, `copy-lint.mjs` tells, 7 blueprints, CJK copy |
| [shared-tokens-and-polish.md](references/shared-tokens-and-polish.md) | Shared | Scaffolding stacks, 3-level CSS tokens, fluid `clamp()` scales, font metric overrides, `<head>`/OG/404, `light-dark()`, `perf.mjs` budgets |
| [shared-components-states.md](references/shared-components-states.md) | Shared | Creative vs Product dialect table, 9-state interactive matrix, Track A feature cards/UI fragments, diagrams (`assets/diagrams`), `icons.mjs` |
| [commerce-layout-sections.md](references/commerce-layout-sections.md) | Track A | `100svh`/`200svh` screen heights, 11 heroes (`deal.mjs`) + Place hero, `.wrap` 12-col edges, section recipes, `backgrounds/pick.mjs` |
| [commerce-media-and-moments.md](references/commerce-media-and-moments.md) | Track A | `photos.mjs` licensing/stand-ins, `assets/motion` hover/loops, 13 active `moments.mjs`, `effects.mjs`, `fx-*`, `product-render`, `scenes`, `gate.mjs` |
| [motion-choreography-arc.md](references/motion-choreography-arc.md) | Track B | Choosing 5 choreography arcs, ideation & 6 mechanic operators, Used-Mechanics Graveyard, duration/easing/spring tokens, `MOTION_SPEC.md` |
| [motion-handfeel-and-recipes.md](references/motion-handfeel-and-recipes.md) | Track B | Tuning springs, velocity lean, `1 - exp(-k·dt)` + `speed/k` followers, screen shake, and 20 ready recipes (#16 CSS timelines, #17 corner-pin, #18–#20 Verlet/emergence) |
| [motion-timeline-affordance.md](references/motion-timeline-affordance.md) | Track B | Multi-track scroll schedules, dead beats, threshold-map histograms, stillness ratio, discoverability (`window ⊇ dwell`), painted-bbox rings, FLIP handoffs |
| [motion-2d-shaders-textures.md](references/motion-2d-shaders-textures.md) | Track B | Render-layer choice, zero-dep 2D WebGL2 fragment shaders, GLSL silent-failure traps, 11 Hz ink-outline pipeline, SVG goo/turbulence, Houdini/Canvas grain |
| [motion-image-plane-3d.md](references/motion-image-plane-3d.md) | Track B | Cutout keying (`coverage`), scripted `cx/baseline/crown`, `fov 26` vs world-moves topologies, analytic contact shadows, `R−B` batch matching, streaming, DOM projection |
| [motion-scene-audio.md](references/motion-scene-audio.md) | Track B | Live WebAudio `bgm` / `hand` / `world` three-bus mixing, inverse act LUFS curves, hand-triggered ducking, discrete events, filter-Q gain, `≥15 dB` REST oracle |
| [verification-oracles.md](references/verification-oracles.md) | Shared | Designing non-composite numeric oracles, `__seek`/`__hold`/`__clock` probes, deterministic phasers, on/off subtraction, 30/60/120fps checks, churn floor |

---

## 6. Pre-Delivery Quality Checklist (Before Claiming Done)

- [ ] **Track isolation:** Track A pages run native scroll + monotonic ease-outs + `gate.mjs`; Track B pages run Creative chrome + deterministic probes + `verify_case.py` (never cross-wire rules).
- [ ] **Honest copy & marks:** `<h1>` states category + audience; zero invented metrics/quotes/addresses; zero `Learn more` / `Get started`; real brand icons resolved via `icons.mjs`.
- [ ] **Palette & contrast:** Zero indigo/violet defaults (`275°–330°`); body ink `≥ 7:1` (or `≥ 4.5:1` AA floor, `≥ 3:1` large type/UI) verified across every background stop.
- [ ] **Still-frame & reduced-motion:** Page captured under `prefers-reduced-motion: reduce` shows 100% readable headings, copy, and controls with zero `opacity: 0` traps.
- [ ] **Viewport sweep:** Zero horizontal scroll or clipped text at `320`, `375`, `390`, `768`, `1024`, and `1440` (`overflow-x: clip`, `≥44×44px` tap targets, `@media (hover: hover)` guards).
- [ ] **Frame & GPU discipline:** Single `rAF` loop per mechanism (`dt` clamped `≤ 1/30`), DPR capped `≤ 2`, `≤ 4` live WebGL contexts, off-screen/background-tab observers paused.
- [ ] **Automated verdict recorded:** Track A reports `GATE:` line, deals, waivers, and stand-ins; Track B reports `verify_case.py` / `measure_churn.py` numeric readouts and `[…]` copy slots.
