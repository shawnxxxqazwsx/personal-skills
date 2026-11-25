# Track B (`showcase`) — Choreography Arcs, Generative Mechanics, Tokens & Spec

High-level motion architecture, runtime creative ideation, token scales, and specification template for **Track B (`showcase`)** builds.

---

## 1. Five Choreography Arcs

Pick **one** dominant page-level energy curve before writing animation code (mixing arcs without hierarchy makes a page feel noisy yet unfocused):

| Arc | Energy Curve | Best Fit | Signature Timing & Scroll Behaviour |
|---|---|---|---|
| `cold-open` | Quiet entry → rising density → `40–70%` peak → isolated quiet CTA | Product showcases, design tools, narrative launches | Entry `1.2s ease-out-expo` (`0.1s` stagger) → midpoint `0.8s` (`0.06s` stagger) → peak `0.6s` decisive snap |
| `broadside` | Instant hero impact (`0–20%`) → sustained pinned tension (`20–80%`) → late inversion/breath | Studios, bold campaigns, manifesto launches | Entry `0.4s cubic-bezier(.65,0,.45,1)` (`0s` stagger) → pinned `scrub: 1` or sticky stack → sharp wipe/inversion |
| `editorial` | Measured line-by-line cadence paced by reading speed | Portfolios, essays, interviews, case studies | `clip-path: inset(0 0 100% 0) → inset(0)` `0.7s cubic-bezier(.77,0,.18,1)` (`0.08s`/line); image `1.05→1` (`1s`) |
| `ambient` | Continuous low-amplitude field at rest + anchored static foreground + hover/pointer ripples | AI/creative atmospheres, single-screen instruments | Continuous GPU/Canvas loop + single `0.8s` foreground load fade + `0.2–0.3s` pointer response (degrade on mobile) |
| `staccato` | Crisp, rhythmic arrivals or discrete ticks; stillness carries the contrast | Technical indexes, developer showcases, archival walls | Tight `0.04s` stagger (`0.3s ease-out`) or zero-transition tick arrivals (`88%` frame stillness) |

**Arc failure fixes:** Never spend 100% of the motion budget in the hero (reserve a `60–80%` depth payoff); isolate the final CTA with stillness so nothing competes with the ask; define an explicit non-pinned mobile degradation for every pinned arc.

---

## 2. Generative Mechanic Synthesis & Used-Mechanics Graveyard

When a brief is open-ended (`freeform-build`), sample 3–5 current live award winners (the actual sites, never gallery chrome) for structure and type scale, extract the subject's **literal physical verbs** (e.g., coffee → pour/grind/convection; typography → keystroke/carriage return/ink bleed; radio → frequency lock/noise floor), and generate 3 candidate mechanics using these **6 operators**:

1. **Literal Physics (直译物理):** Turn the domain's real physical mechanism directly into the page control (e.g., each wheel notch advances a carriage return with mechanical detent).
2. **Input Inversion (输入反转):** Swap controller and controlled (e.g., object mass drags the cursor halo; world moves around a fixed datum).
3. **Dimension Remap (维度替换):** Bind a standard input to an unexpected axis (`scroll → time-rate / turbidity`, `pointer Y → gravity vector`, `dwell duration → ink saturation`).
4. **Medium Immersion (介质想象):** Submerge all UI in a physical medium (magnetic repulsion, viscous fluid, taut strings, raking sun).
5. **Primitive Hybrid (杂交):** Weld two distinct primitives (`frame-scrub × heartbeat clock`, `Verlet chain × corner-pin homography`).
6. **Physical Rule Break (物理化破规):** Violate one web convention with clear physical causality (`wheel` inflates/rotates an instrument instead of scrolling `scrollY`).

Prototype the chosen mechanic in a minimal single-file sketch (`<15 min`), drive it with real wheel/pointer sweeps, and **kill it if it bores after 10 seconds or if two screenshots cannot communicate the rule**. Design the static page (blueprint, copy, `visual-bank.json` archetype, 3-level tokens) *before* embedding the mechanic.

### Used-Mechanics Graveyard (Do Not Reuse Verbatim — Diverge From These 19)
1. **Turnaround scrub:** Mouse X scrubs curated yaw frames (`Math.round` hard cut) + wheel spin impulse (`cases/toy-flipbook`).
2. **Stop-motion 11 Hz jitter:** Quantised `11 fps` micro-offset/boil clock inside a `60 fps` loop (`toy-flipbook`, `ink-crowd`).
3. **Pendulum swing:** Underdamped hanging rock kicked by wheel angular impulse.
4. **Leap carousel:** Diagonal/arc item trajectory with path-tangent rotation.
5. **Jelly wobble field:** Primary velocity feeding loose volume-preserving squash/stretch springs on background elements.
6. **Depth-slice parallax:** Single cutout sliced into `preserve-3d` height layers.
7. **Fake-light 2.5D hero:** Pointer-driven alpha-masked `screen`/`multiply` radial gradients on a flat cutout.
8. **Desk-toy hop:** High-velocity scrub kicks tabletop props upward with landing squash (`toy-flipbook`).
9. **Multi-gain scrub linkage:** One normalized driver feeding distinct signed gains across every layer.
10. **Jacquard weave-in:** Scroll advances a shuttle accumulating woven rows below loose warp threads.
11. **Erase-to-reveal:** Pointer path wipes an overlay mask and self-heals after release.
12. **Verlet text curtain:** 24 horizontal-link-free glyph chains energized by scroll and parted by pointer (`cases/char-curtain`).
13. **Traverse-a-world:** Sections placed as spatial locations reached by camera dolly rather than vertical bands.
14. **Sun-scroll room:** Scroll sweeps directional sun dawn→dusk across 3D/DOM shadows together.
15. **Sediment scroll:** Scroll dissipates agitation (`1 - scrollP`) so heavy elements settle early and pointer velocity re-stirs locally.
16. **Tuner-sweep dial:** Scroll scrubs frequency through static noise into detented station locks.
17. **Hanging Verlet card chain:** Cards corner-pinned (`matrix3d`) between Verlet nodes so cards physically bend (`pattern-recipes` #17+#18).
18. **Slack string readout:** Elastic sagging Verlet body paired with a stiff `k = 1600` datum tip spring (`cases/string-clock`).
19. **Cumulative emergence:** `167 ms` grid with skipped ticks dealing overlapping cards (`--z` = arrival order, FIFO DOM cap, zero entrance easing).

*Asset preparation notes when user supplies/requests sprites:* Turnaround sheets need monotonic yaw curation (drop the symmetry-breaking head-on frame); cutout sets slice by alpha-gap segmentation; hero renders bake AO/form shading **without** cast floor shadows so the page can animate ground contact dynamically.

---

## 3. Motion Tokens (`duration`, `easing`, `spring`, `stagger`)

### Duration & Stagger Scales
- **Durations:** `instant` `80–100ms` (cursor/tooltip) · `fast` `150–200ms` (hover/press/toggle) · `standard` `280–350ms` (panel/drawer) · `medium` `400–500ms` (section reveal) · `slow` `600–800ms` (hero/route enter) · `cinematic` `1000–1400ms` (cold-open wipe). *If you cannot justify a duration by intent, halve it.*
- **Staggers:** `tight-grid` `0.04s` · `standard-list` `0.07–0.08s` · `editorial-line` `0.08–0.10s` · `dramatic-cascade` `0.12–0.18s` · `no-stagger` `0s` (single decisive CTA). In modern CSS, `animation-delay: calc(sibling-index() * 60ms)` removes manual `--i` inline indices (safe fallback: `0ms` delay).

### Easing Curves & Spring Presets
- **CSS / Tween curves:**
  - `ease-out-expo`: `cubic-bezier(0.16, 1, 0.3, 1)` (default soft landing; GSAP `expo.out` / `power4.out`)
  - `ease-in-expo`: `cubic-bezier(0.7, 0, 0.84, 0)` (exits only)
  - `ease-in-out-quart`: `cubic-bezier(0.76, 0, 0.24, 1)` (symmetrical travel; GSAP `power2.inOut`)
  - `ease-sharp`: `cubic-bezier(0.65, 0, 0.45, 1)` (`broadside` openings)
  - `ease-out-circ`: `cubic-bezier(0, 0.55, 0.45, 1)` (crisp mechanical decel)
  - `ease-out-back`: `cubic-bezier(0.34, 1.56, 0.64, 1)` (playful hover overshoot; GSAP `back.out(1.7)`)
  - **CSS `linear()` sampled springs** (broadly supported, matches JS spring feel on buttons/chips without a library):
    `transition-timing-function: linear(0, 0.32 8%, 0.79 20%, 1.03 30%, 1.01 46%, 1);`
- **Framer / Spring presets (`stiffness / damping / mass`):**
  - `gentle` `100 / 15 / 1` · `default` `200 / 22 / 1` · `snappy` `350 / 28 / 1` · `bouncy` `200 / 10 / 1` · `heavy` `150 / 35 / 1.5` · `stiff` `500 / 40 / 1`.

---

## 4. `MOTION_SPEC.md` Contract (For Complex or Multi-Phase Builds)

When user requests `spec` mode or provides a complex multi-reference brief, produce a concise `MOTION_SPEC.md` before building (never fabricate unmeasured easing/timing from an uninspected clip — mark unverified values explicitly):

1. **Goal & Dialect:** Track (`showcase`), macrostructure, blueprint spine, component dialect, primary action.
2. **Choreography Arc:** Opening beat (`0–1s`), scroll/input rhythm, peak (`40–70%`), quiet CTA release, mobile degradation.
3. **Motion Tokens:** Fast / standard / slow durations, primary & secondary easings, spring constants, stagger rules.
4. **Interaction & Affordance Map:** Hover (`@media (hover: hover)`), `:focus-visible`, `:active`, click-vs-drag (`6px` up-decision), touch fallback, painted-bbox invitation marks (`window ⊇ dwell`).
5. **Horizontal Scroll Schedule:** Every track (`art`, `copy`, `camera`, `affordance`, `audio`) plotted against `0.0 → 1.0` with money-frame ranges and zero coinciding unintentional plateaus.
6. **Render Layer, Assets & Fallbacks:** Layer (`dom` / `svg` / `canvas2d` / `webgl`), DPR cap, WebGL context count (`≤4`), per-element resolution headroom, `prefers-reduced-motion` static design, and numeric verification oracles (`__seek`, `__hold`, `__probe`).
