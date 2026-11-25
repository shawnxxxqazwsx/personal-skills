# Verification Harnesses, Deterministic Probes & Numeric Oracles

Methodology for proving visual, layout, interaction, audio, and frame-rate claims across **Track A (`commerce`)** and **Track B (`showcase`)** without false positives or subjective "quality scores".

---

## 1. Two Iron Laws of Verification

1. **Ban composite "quality scores":** A 6-metric composite script once scored `6/6` on every build a human immediately rejected. Every legitimate oracle encodes **one specific failure mode**, and the strongest domain oracles use **two assertions in tension** (e.g., `verify_case.py --strings` requires endpoint error `≤1.5°` *and* body sag `arc/chord ≥ 1.12` — over-damping fails sag, loosening the tip fails accuracy). Aesthetic judgment stays with human eyes on real frames.
2. **Test the oracle on a deliberately broken copy first:** Before trusting a new probe, feed it a known-broken page (e.g., `preventDefault()` deleted, pointer force `= 0`, `transition: opacity 250ms` injected on a hard-cut flipbook, `preserveDrawingBuffer: false` black-frame trap). If the oracle still passes, the oracle is vacuous — fix the ruler first.

---

## 2. Track A vs Track B Toolchains

- **Track A (`commerce`):** Run sequentially in the foreground (one CPU-WebGL headless Chrome at a time, profile inside OS temp or `.web-craft/`):
  1. `copy-lint.mjs` (`<1s`, static copy tells & device caps)
  2. `consistency.mjs` (`1440,1024,820,768,390` + `320` narrow walk + rhythm widths)
  3. `assets/layout/check.mjs` (`1440x900,1024x768,820x1180,768x1024,390x844` judge-tile framing)
  4. `shoot.mjs` + `perf.mjs` + `gate.mjs` (`GATE: PASS` or disclosed `.web-craft/waivers.json`).
- **Track B (`showcase`):**
  1. **Still-frame gate:** Screenshot under `prefers-reduced-motion: reduce` and clear all A1–A8 gates in `shared-anti-slop-and-copy.md`.
  2. **Reference & churn probes:** `measure_structure.py <url>` (static sections/tokens/radii/overflow) and `measure_churn.py <target> [--against <ref>]` (real-wheel moving element share + mid-transition count).
  3. **Acceptance floor + domain oracles:** `verify_case.py <file-or-url> [--strings|--layer <l>|--follow|--rail|--stack|--flipbook|--curtain|--lyre|--beats|--detent]`. Every run checks zero console/page errors, zero x-overflow at `320/375/414/768/1440`, one `<h1>`, `lang`, `display/body ≥ 4×`, `≥3` section shapes (`--min-shapes 1` for single-screen heroes only), zero undefined CSS custom properties, painted body ground, reduced-motion visibility, **plus a real wheel and real hover smoke test**.

---

## 3. Mandatory Probe Contract (Build In From Frame 1)

Retrofitting determinism into an animated page costs more than authoring it cleanly up front:

```js
window.__seek  = (p) => { scrollP = p; render(); };       // jump static/scrubbed layers
window.__hold  = (t) => { heldT = t; render(); };         // freeze mid-transition (e.g. t = 0.002 FLIP check)
window.__clock = (t) => { ambientT = t; };                // pin all wall-clock weather/boil/breathing
window.__noDemo = true;                                   // suppress idle preview WITHOUT hiding static hints
window.__noHint = true;                                   // hide static hints WITHOUT stopping demo/scene
window.__probe = () => ({ boxes, windows, hitAtPointer, stateExits });
```

- **Determinism precondition:** Any `Math.random()` reachable from a render or audio path shifts downstream samples when a layer is toggled, poisoning A/B subtraction (`7.3 dB` phantom audio swings). Replace global RNG calls on render/audio paths with **per-event deterministic golden-ratio phasers**: `const nextPhase = i => (phase[i] = (phase[i] + 0.618034 * span) % span)`.
- **Match target DPR:** Run visual probes at `deviceScaleFactor: 2` when targeting Retina displays so `1–2px` hairlines and magnification budgets are measured honestly.

---

## 4. Eight Classic Measurement Traps & How to Beat Them

1. **Teleporting (`__seek` / `scrollTo`) lies on lifetime-driven layers & churn:** Jumping straight to `p = 0.85` releases all particles on one frame and skips arrival/exit windows (`--rail`, `--stack`, and `measure_churn.py` all require **stepped real wheel events**, e.g. `0.008` per `40ms`).
2. **Probe-only shortcuts miss dead event handlers:** Setting internal state via `__probe.setAngle()` passed `0.0000°` accuracy on a page whose actual `wheel` listener had an inverted sign. **Every oracle must drive at least one real DOM pointer/wheel gesture** and assert a live DOM readout or computed-style change (pure `<canvas>` pages should mirror minimal live status in DOM for both screen readers and input smoke checks).
3. **Reading `el.style` instead of `getComputedStyle(el)`:** `el.style.opacity` jumps immediately to the JS target even when an accidental CSS `transition: opacity 250ms` smears a hard-cut flipbook across 19 frames. Always read rendered state via `getComputedStyle`.
4. **Fixed settle timeouts vs polling stillness:** A hardcoded `2.6s` wait landed inside a `2.7s` wheel decay and credited residual drift to a zeroed pointer force. **Poll `__probe` until velocity/delta drops below threshold** (and fail explicitly if it never settles). Similarly, on probabilistic or velocity-threshold effects (`|v| > 2.2`), **print peak drive and fail if the driver never cleared the threshold**.
5. **Before/after screen diffs on moving cameras measure the camera:** Half-pixel camera breathing rims every silhouette in white. Either pin `__clock(T)` + `__seek(P)` and subtract an **on/off toggle** (inject `<style>.callout{display:none!important}</style>` so pseudo-elements vanish too), or read **state exits** (`__wipeLevel()`, `__marked()`, weighted by the **artwork's own alpha**, never raw mask area).
6. **Peak Δ without pixel area, or single-image edge contrast:** A `1px` line and a `2px` line have identical peak Δ but `2×` weight — report **both peak Δ and pixel count over threshold** from an on/off diff (never contrast against adjacent pixels in one image, which measures horizon edges).
7. **Aliasing, clamped `dt`, and software-GPU FPS:** Sample periodic events at **`≤ 1/5` of event duration** across multiple windows; compute auto-demo phases from absolute timestamps (`performance.now()`) rather than clamped `dt` sums (headless screenshots stall `rAF`); and **never quote FPS/frame-time verdicts from SwiftShader/software WebGL runs** (check `WEBGL_debug_renderer_info` first).
8. **Ruler resolution floor, `30/60/120fps` parity & scheduled snaps:**
   - Downsampled `120×68` motion meters cannot resolve `2px` spires or `20px` type; `DOMMatrix` serialisation has a `0.016px` floor.
   - Prove `1 - exp(-k·dt)` loops without a browser by stepping identical seeded inputs at `dt = 1/30, 1/60, 1/120` and asserting trajectory drift `< 0.5` units and event-time drift `< 0.2s` vs `120fps`.
   - Exempt **schedule-declared** arrival/hold windows (`±0.14s`) from jerk/smoothness checks so intentional staccato holds are never penalized, and budget dynamic occlusions by **continuous duration (`<2.0s`) and run share (`<8%`)**, not frame averages.
