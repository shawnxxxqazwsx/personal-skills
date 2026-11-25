# Stacks, Tokens, Scales, Performance & Production Polish

Engineering substrate shared across **Track A (`commerce`)** and **Track B (`showcase`)**, with explicit per-track overrides where the two dialects diverge.

---

## 1. Two Independent Stack Ladders

Never let the page framework dictate the animation engine or vice versa — a single static `.html` file can run a WebGL2 shader, and a Next.js app can ship zero JS motion. Climb only when a lower rung cannot meet a concrete requirement:

### A. Page Authoring Ladder
| Rung | Stack | Use When |
|---|---|---|
| **0** | Plain `.html` + `.css` + `.js` (`starter.html` in Track A; single-file in `cases/`) | Single-route landing, portfolio, or campaign page; fastest iteration loop |
| **1** | **Vite** + vanilla TS/JS | Single/few pages needing npm modules (GSAP, Three) and HMR without UI state trees |
| **2** | **Astro** + opt-in islands | `≥5` routes, `.md`/`.mdx` collections, SEO-heavy sites; ships near-zero JS by default |
| **3** | **Next.js** (App Router; `output: 'export'` when running Track A `gate.mjs --root out`) | Shared codebase with an authenticated product, database, or dynamic server actions |

*Never scaffold Create React App or custom Webpack configs.* Separate reusable `ui/` primitives (`Button`, `Field`, `Card`) from single-use `sections/` (`Hero`, `Pricing`, `Footer`).

### B. Motion Execution Ladder (Track B — see Track A rules in `commerce-media-and-moments.md`)
| Rung | Mechanism | Reaches | Climb Only When |
|---|---|---|---|
| **1** | CSS transitions / keyframes (`linear()` springs) | Hovers, focus, `:active`, `<dialog>` `@starting-style`, `<details>` | Driven by continuous pointer/scroll |
| **1.5** | Native CSS `animation-timeline: scroll()/view()`, `sibling-index()` | Compositor-thread scrubbed parallax, progress bars, list stagger | Needs pinning, seekable timeline, or Firefox motion parity (wrap in `@supports`, author finished state first!) |
| **2** | Vanilla `rAF` springs, Verlet chains & `1 - exp(-k·dt)` followers | Cursor/camera follow, velocity lean, wheel rails, flipbooks | Flat cutout needs directional light |
| **3** | Alpha-masked `screen`/`multiply` radial gradients + subtle tilt | Convincing 2.5D light/shadow on a single cutout (`handfeel` §5) | Multi-element orchestration or pinning needed |
| **4** | Framer Motion / GSAP `ScrollTrigger` | Pinned sequences, multi-element timelines, route `AnimatePresence` | Camera must dolly/pan through a deep multi-layer space |
| **5** | Flat 2D cutout planes in a `PerspectiveCamera` (`motion-image-plane-3d.md`) | Real perspective foreshortening, occlusion, contact shadows from 2D art | Object silhouette itself must rotate 360° in 3D (out of scope) |

---

## 2. Three-Level CSS Token Architecture & Cascade Layers

Declare cascade order once so utilities beat components without `!important`, and never put a CSS `transition: transform` on an element whose `transform` is driven per-frame by `rAF` or GSAP:

```css
@layer reset, base, layout, components, motion, utilities, overrides;

@layer reset {
  *, *::before, *::after { box-sizing: border-box; }
  * { margin: 0; }
  html { -webkit-text-size-adjust: 100%; interpolate-size: allow-keywords; scrollbar-gutter: stable; overflow-x: clip; }
  body { min-height: 100svh; line-height: 1.5; -webkit-font-smoothing: antialiased; overflow-x: clip; }
  img, picture, video, canvas, svg { display: block; max-width: 100%; }
  input, button, textarea, select { font: inherit; color: inherit; }
  p, h1, h2, h3, h4 { overflow-wrap: break-word; }
  h1, h2, h3 { text-wrap: balance; }
  p { text-wrap: pretty; }
  :target { scroll-margin-block: 5svh; }
}
```

- **Why `100svh` and `overflow-x: clip`:** Mobile `100vh` clips behind the browser URL bar; `overflow-x: hidden` on `html` silently breaks `position: sticky`, whereas `overflow-x: clip` preserves sticky containers.
- **Three-level custom properties (`tokens.css` imported first and once):**
  1. **Primitive:** Raw palette hexes (`--ink-900`, `--paper`, `--ember-500`) — never read directly by components.
  2. **Semantic:** Functional roles (`--bg`, `--surface`, `--border: color-mix(in oklab, var(--ink-400) 28%, transparent)`, `--text`, `--text-muted`, `--accent`, `--accent-on`, `--focus`) — component CSS reads **only** level 2. (In Track A, `start.mjs css` emits `:root` `--p-*` tokens consumed by `assets/system.css`.)
  3. **Component:** Local overrides (`--btn-radius`, `--card-radius`, `--p-h`).
- **Tailwind v4:** Define tokens directly in `@theme { --color-bg: ...; --font-display: ...; }` inside CSS — no legacy `tailwind.config.js`.
- **Dark mode without flash:** Commit single-ground pages with `:root { color-scheme: light; }` (or `dark`) so native scrollbars/inputs match. For dual-theme pages, remap **only** semantic tokens via `light-dark(#faf9f7, #0b0b0c)` and stamp `data-theme` in a tiny synchronous `<head>` inline script before first paint.

---

## 3. Macrostructures, Fluid Scales & Font Loading

### Track A (`commerce`) System Tokens (`assets/system.css`)
- **Rhythm:** `--nav: 72px` (`56px` `<640px`), `--padt: 120px` (`96px`), `--padb: 72px` (`48px`), `--gut: 80px` (`24px` `<640px`; `120px` on `place` `≥1024px`), `--bar: calc(64px + env(safe-area-inset-bottom))` when `nav.actionbar` is active on phones.
- **Spacing scale:** `4, 8, 12, 16, 24, 32, 48, 64, 96, 128px` (`--s-1`..`--s-10`).
- **Contrast & type:** Body text `≥16px` (`1.5–1.8` line-height) in `--ink` at `≥7:1`; `--muted` (`≥4.5:1`) for labels/dates/grey heading second sentences only; nothing `<13px`. Brand band text on `place`/`product` must hit `≥7:1`.

### Track B (`showcase`) Macrostructures & Fluid Type Jump
Choose macrostructure from the mechanic (`data/visual-bank.json` provides 7 palettes, 5 type systems, 5 grids):
1. **Single scene:** Camera or world moves along one continuous scroll rail; few/no DOM sections.
2. **Acts:** `3–5` pinned beats, one idea and one money frame per act.
3. **Editorial + set-pieces:** `60–75ch` passages punctuated by `2–4` interactive set-pieces.
4. **Index / archive:** Short scroll per view, URL-backed filtering, motion in hover and `@view-transition`.
5. **Single-screen instrument:** `≈1svh`, zero scroll verb, pure direct manipulation.

**Fluid `clamp()` formula (always keep a `rem` term — pure `vw` breaks WCAG 200% zoom):**
```text
slope     = (maxPx - minPx) / (maxVw - minVw)
intercept = minPx - slope * minVw
clamp( {minPx/16}rem, {intercept/16}rem + {slope*100}vw, {maxPx/16}rem )
```
- **Scale jump:** Body `12–16px` (`line-height: 1.5–1.65`, `letter-spacing: 0`); Heading `1.5–3rem` (`1.15–1.25`, `-0.015em`); Display `3.5–10rem+` (`0.95–1.05`, `-0.03em to -0.04em`; invert for CJK per `shared-anti-slop-and-copy.md`).
- **Zero-CLS fonts:**
  - *Multi-file builds:* Self-host `.woff2`, preload `≤2` above-the-fold weights (`crossorigin`), `font-display: swap`, and add a metric-override fallback (`size-adjust`, `ascent-override`, `descent-override`, `line-gap-override`) so swap shift is `0`.
  - *Single-file `cases/` or offline pages:* Run `python3 <skill>/scripts/subset_fonts.py pack --out /tmp/faces.css Grot=Inter-Variable Ital=InstrumentSerif-Italic` (OFL/Apache faces only — never embed licensed macOS system fonts like Helvetica/Didot/Futura; omit `--text-from` if headlines live in JS strings).

---

## 4. Framework Hygiene & Runtime Performance Budgets

### Framer Motion & GSAP Pre-Flight Rules
- **Framer Motion:** Hoist `variants` objects outside components; gate with `useReducedMotion()`. Use `<AnimatePresence mode="wait">` on route swaps so exit finishes before enter.
- **GSAP:** `gsap.registerPlugin(ScrollTrigger)` once at module scope. Inside React `useEffect`, wrap **all** tweens/triggers in `const ctx = gsap.context(() => { ... }, ref); return () => ctx.revert();` so StrictMode double-mounts never wedge `.from()` opacity at `0`. Gate desktop pins behind `gsap.matchMedia().add('(min-width: 768px)', ...)`. Refresh `ScrollTrigger.refresh()` after late media loads.
- **Compositor & rAF discipline:** Animate `transform` and `opacity` only (`clip-path`/`filter` on small regions only; never `width`, `height`, `top`, `left`, `margin`, `padding`). Run **one** `rAF` loop per page (`≤1ms`/frame), attach scroll listeners with `{ passive: true }`, set `will-change: transform` only during active motion, and reset physics integrators while paused.

### Measured Performance Budgets (`scripts/perf.mjs` & Build Targets)
Run `node <skill>/scripts/perf.mjs <index.html>` (loads at `1440` and `390` in CPU Chrome; timing is median of 3 loads):

| Metric | WARN | Blocking FAIL / Hard Ceiling |
|---|---|---|
| Text transfer (gzipped) / Requests | `>1500 KiB` / `>60` | `>3000 KiB` / `>110` (Track B marketing JS target `<100 KB` gzip) |
| Images total / Single image | `>1200 KiB` / `>350 KiB` | `>2400 KiB` / `>700 KiB` (Track A hero `≤400 KiB`, others `≤250 KiB`) |
| Parsed JS / CSS | `>450 KiB` / `>120 KiB` | `>900 KiB` / `>250 KiB` |
| Font families / files / bytes | `>2` / `>4` / `>160 KiB` | `>3` / `>6` / `>320 KiB` |
| Missing `width`+`height`/`aspect-ratio`, non-lazy below fold, or `>2.2×` oversized images | `1–3` | `≥4` |
| Live WebGL contexts (at rest, scroll end, peak) | — | **`>4` live contexts** (`>24` total created across full scroll) |
| CLS / Broken requests / Horizontal overflow | `CLS > 0.1` | `CLS > 0.25` (target `<0.05`) / **any** broken request or x-overflow |

**Image rules:** Serve AVIF/WebP via `<picture>`/`srcset` + accurate `sizes` (`≤2×` CSS box). Give the single LCP hero image `fetchpriority="high"` (never `loading="lazy"`); give all below-fold `<img>` elements `loading="lazy" decoding="async"`.

---

## 5. Production Polish & Pre-Ship Checklist

Every shipped page (not just framework apps) owes the complete finish layer:

1. **Complete `<head>`:** `<html lang="...">`, `<meta charset="utf-8">`, `<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">`, `<title>` (`40–60` chars: `Brand — category & claim`, distinct from description), `<meta name="description">` (`120–155` chars), `og:type`, `og:title`, `og:description`, **absolute** `og:image` (`1200×630` hero still or card) + `twitter:card="summary_large_image"`, `favicon.svg`/`.ico` + `180×180` `apple-touch-icon.png`, `theme-color`, and `rel="canonical"` (commented out until client domain is known).
2. **Off-happy-path routes & states:** Designed `404` page in the site's typography with a one-click return; `robots.txt` + `sitemap.xml` on multi-route builds; built and visually inspected `loading`, `pending` (locked button width, no double-submit), `error` (`aria-invalid` + adjacent `aria-describedby` fix hint), `empty` (names active filter + reset button), and persistent `success` states.
3. **Micro-polish CSS:** Styled `::selection`, `accent-color: var(--accent)`, `caret-color: var(--accent)`, `text-underline-offset: .18em`, `-webkit-tap-highlight-color: transparent` paired with a real `:active` state, and `.vh` visually-hidden utility (`clip-path: inset(50%)`, never `display: none`) when display type is rendered on `<canvas>` so the DOM still exposes one real `<h1>` and `<header>`/`<nav>`/`<main>`/`<footer>` landmarks.
4. **Ten final verification passes:** (1) Build & typecheck with 0 warnings; (2) Load with JS disabled; (3) Emulate `prefers-reduced-motion: reduce`; (4) Full keyboard `Tab` walk (skip link first, visible focus ring, zero focus traps, header never covers focused node); (5) Width sweep `320 / 375 / 390 / 768 / 1024 / 1440`; (6) Browser zoom `200%`; (7) Contrast check at the **busiest** animation frame; (8) Submit form error + valid paths; (9) Open non-existent route (`404`); (10) Five reloads with zero FOUC/CLS/console errors.
