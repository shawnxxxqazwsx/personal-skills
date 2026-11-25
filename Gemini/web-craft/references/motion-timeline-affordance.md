# Track B (`showcase`) — Multi-Track Scroll Timelines & Affordance Discovery

Diagnosing dead scroll stretches, pacing multi-layer timelines, choosing pinning topologies, and ensuring visitors actually discover interactive elements without instructional copy.

---

## 1. Multi-Track Scroll Timeline Orchestration

### 1.1 Read Schedules Horizontally & Keep One Easing Layer
- **Dead beats are coinciding plateaus:** A dead stretch where frame delta collapses is rarely one slow track — it is 2–3 tracks hitting their tail/hold/zero-velocity keyframe simultaneously. Plot all tracks (`art`, `copy`, `camera`, `atmosphere`, `interactable`) as horizontal rows against normalized scroll `p ∈ [0, 1]` and shift overlapping plateaus apart.
- **Ease in one layer only:** Keep the scroll→progress driver **strictly linear** and apply easing inside individual element windows. Applying `smoothstep` to both the act timeline and the element window multiplies them — squaring the midpoint into a sudden 4-notch cliff and flattening both ends.
- **Zero-velocity keyframes create flat heads:** Any `smoothstep`/`smootherstep` segment starts with derivative `0`, making the first 1–2 wheel notches nearly static. Before adding filler motion, check for stale timestamps left from an earlier edit; otherwise either accept authored stillness or bridge the seam with an abutting title/secondary ramp.

### 1.2 Weight Sweeps by Visual Ink/Area, Never Raw Axis Length
Sweeping a wipe/peel linearly down a tapered object spends notches on near-empty pixels and dumps the heavy base in 2 notches. Apply a power curve (`k ** 0.62`) or blend stroke-segment windows by ink share:
```text
segment_window = 0.85 × (segment_ink / total_ink) + 0.15 × (1 / N)
```
The `0.15` floor prevents tiny details (a finial, a dot) from falling between frames while keeping them a brisk flick rather than a dead pause.

### 1.3 One Window, One Event & Container Lifetimes
- **A fade consumes everything sharing its window:** Fading an element over `0.69–0.83` while running its internal motion in the same range hides the internal motion completely. Restrict fade-in to the **first ~10%** of the window; run consecutive acts (`fall → brush → scatter`), never stacked alpha soups.
- **Draw → Say → Hand off:** Never render copy referencing an element (`"抹掉这条轮廓"`) before that element finishes drawing, and never overlap two annotations.
- **Containers exit on their content's schedule:** Rods, frames, captions, and `"scroll"` hints must exit when their content finishes — never back-derive container exit from the *next* act's start.
- **Sentence-level copy stagger:** Stagger multi-block copy by `≈0.022` of scroll (`dateline → title → sentence 1 → sentence 2 → smallest credit last`), placing the lightest element last when the artwork is nearly full.

### 1.4 Money Frames, Histogram Dissolves & Stillness Ratio
- **Every act owes a money frame (定妆帧):** Verify in a printed table over `p` that a non-empty scroll interval exists where `art == 1.0`, `copy == 1.0`, and `interactable > 0` simultaneously. **Whenever you move a dwell window, update its `interactable` / `affordance` window in the exact same edit.**
- **Threshold-map dissolves require flat histograms:** Using raw paper/cloud noise (`values ∈ [0.45, 0.52]`) as a dissolve threshold produces 1 frozen notch followed by a 45%-area hard cut. **Histogram-equalize** the threshold map (replace each pixel with its rank in `[0, 1]`) and map across the full soft-edge range `T = amt * (1 + 2 * W) - W` on a linear driver.
- **「灵动 vs 飘」 is a stillness ratio, not an easing curve:** Easing never changes how many distinct states appear per second. If a piece feels floaty (`<15%` near-identical adjacent frames vs `~50%` on crisp references), quantise the **subject's** drawing clock (`const tq = Math.floor(t * 15) / 15`) while keeping camera/render at `60 fps`, or apply `smootherstep` between every pair of pose anchors.
- **Two mutually exclusive pinning architectures (choose before layout):**
  1. **Hijacked wheel + translated rail (`cases/wheel-rail`):** `window.scrollY` stays `0`; `position: sticky` **never fires** inside a transformed ancestor, so parked layers must be counter-translated manually; hero elements starting on screen at `t=0` need a load clock rather than scroll progress.
  2. **Native scroll + `position: sticky; top: 0; height: 100svh` stack (`cases/press-stack`):** Give each screen `margin-bottom: 100svh` to buy 1 viewport of dwell (`progress = (scrollY - top) / vh` during dwell; exit effects on `(scrollY - top - vh) / vh`), and keep key content in the **upper two-thirds** because the incoming screen covers the bottom first.

---

## 2. Affordance & Discoverability (`能点 ≠ 看得出能点`)

When a user reports `"点不开 / 只有一个能点 / 没反应"`, **audit discovery before touching hit-test code**. Centre-clicking in a test proves only that the mechanism works if found; it says nothing about whether a first-time visitor ever finds it.

### 2.1 Three Mandatory Discovery Questions
1. **Is it hittable across its region?** Sweep a `12px` pointer grid across the viewport region and assert every target owns `>2%` of cells (`0%` = occluded or mis-projected raycast plane; intersect rays with the **subject's height plane**, never `y = 0` ground when figures have height!).
2. **Does it visibly invite interaction *before* hover?** `cursor: pointer` is invisible until the pointer is already there — it confirms a guess, never prompts one. Every non-button interactive target owes a persistent visual mark.
3. **Does the invitation span the entire dwell (`affordance_window ⊇ dwell_window`)?** Visitors hunt for interactions *after* the camera/scroll parks. Closing an annotation ring `0.01` of scroll before the pin ends hides the door right when the user stops to look. Two invitations in separate screen quadrants do not compete — never let a "tidy screen" rule delete the last entrance.

### 2.2 Drawing Marks That Peripheral Vision Catches
- **Draw edges, don't fade alpha:** Peripheral vision ignores slow alpha ramps (`0.8 px/s`) and locks onto moving edges (`20 px/s`). Draw SVG paths with `stroke-dashoffset` (`pattern-recipes` #14), landing opacity in the first `40%` of each mark's staggered window (`i * 0.17` offset) and drawing the stroke over the remaining `60%`.
- **When static contrast hits its aesthetic ceiling, add a periodic micro-tap:** Pair subtle positional breathing with a crisp `0.25s` inward pull/swell every `6.2s` (phase-staggered by `i * 0.29` across targets, driven by the deterministic scene clock, backed by a paper-coloured `drop-shadow` halo so marks survive dark backgrounds).
- **Use the work's own visual vocabulary:** Avoid generic neon glows; reuse the piece's established accent/ink (e.g., vermilion seal ink composited *before* atmospheric haze so it sits inside the world) and clear the mark as soon as its beat ends.

### 2.3 Painted-Bbox Projection, Gesture Disambiguation & Invisible Handoffs
- **Hug painted pixels, never transparent canvas margins:** Offline, compute `paint = [u0, u1, v0, v1]` where `alpha > 200` with `≥1%` row/col coverage (`Image.getbbox()` on `alpha > 0` fails on faint export haze). At runtime, project **all four corners** through `mesh.localToWorld(v).project(camera)` every frame and size ellipses by `×1.26` (`×1.10` for corner brackets) — handles mirroring/rotation automatically.
- **Click + drag on one element (`按下记坑，抬手判定`):** Record `(downId, downX, downY)` on `pointerdown` with zero navigation; on `pointerup`, trigger click only if `Math.hypot(x - downX, y - downY) <= 6`. Never gate content behind press-and-hold, and restore drag/scrub effects immediately rather than after a long timeout.
- **Copy narrates, never instructs:** Ban `"点击查看 / 拖动试试"`; at most **one** mark in a group carries a 2-character tag (`近看`) positioned away from neighbouring rings. Validate reveal/peel/curl gestures by checking that **meaningful artwork actually sits underneath the gesture zone** (not empty corner paper).
- **Auto-demos never touch `userState`:** After `~2.6s` of idle dwell (measured from absolute timestamps, never clamped `dt` sums), run one light preview into `demoState` (`render = max(userState, demoState)`), calibrated by **artwork-alpha-weighted pixels cleared** rather than stroke length.
- **Shared-element / FLIP handoff (`<3%` frame-0 error):** Incoming detail views must read geometry directly from the picked scene item (never duplicate size literals). Pin `window.__hold(0.002)` and assert `|inH - outH| / outH < 0.03`.
