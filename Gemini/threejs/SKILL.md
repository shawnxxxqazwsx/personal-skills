---
name: threejs
description: >-
  Build and debug real-time 3D scenes, procedural geometry, PBR lighting,
  environments, rigid-body physics, and WebGPU/TSL shaders with three.js r185
  (WebGPURenderer with automatic WebGL2 fallback). Use for Three.js/R3F scenes,
  glTF/GLB loaders and viewers, three/tsl node materials and GPGPU compute
  particles/fluids, terrain/water/sky, RenderPipeline post-processing
  (Bloom/AO/SSR/DOF), Rapier/Jolt/Ammo physics, or diagnosing black, slow,
  flickering, draw-order-broken, or leaking 3D canvases. Do not use for pure
  DOM/CSS/GSAP/Framer Motion commercial landing pages, 2D cutout planar parallax
  without rotating 3D meshes, or offline frame-by-frame .mp4 promo video renders.
---

# three.js r185

Default training memory outputs ~2023 three.js (`WebGLRenderer`, `Clock`, `requestAnimationFrame`, `EffectComposer`) — all deprecated or superseded in r185. This skill enforces the r185 baseline and requires measured verification before claiming a scene works.

## Scope

- **Use for:** real-time Three.js / R3F / WebGPU / WebGL 3D scenes, `.glb`/glTF viewers, `three/tsl` node shaders and GPGPU compute, procedural 3D geometry, terrain/water/sky, PBR lighting, `RenderPipeline` post-processing, Rapier/Jolt/Ammo rigid-body physics, and 3D canvas performance/leak debugging.
- **Do not use for:** pure DOM/CSS/GSAP/Framer Motion web layouts or commercial landing pages; 2D cutout planar parallax that needs no 3D mesh rotation; or offline frame-by-frame `.mp4` promotional video rendering.

## Non-negotiables (r185 baseline)

Apply to every scene without being asked:

1. **`WebGPURenderer` (never `WebGLRenderer`).** Automatically falls back to WebGL2 when WebGPU is unavailable; call `await renderer.init()` once before the first render (the old `*Async` render methods are removed).
2. **`renderer.setAnimationLoop(fn)` (never `requestAnimationFrame`).** Required for WebXR and WebGPU async submission.
3. **`THREE.Timer` (never `THREE.Clock`).** `Clock` is `@deprecated since r183`; call `timer.update(timestamp)` each tick and read `timer.getDelta()`.
4. **`three/webgpu` + `three/tsl` + `RenderPipeline`.** Import from `three/webgpu` and `three/tsl` (not bare `three`) for nodes, compute, and post-processing. Use `RenderPipeline` (renamed from `PostProcessing` in r183; replaces legacy `EffectComposer`).
5. **Verify with `scripts/verify_scene.mjs`.** Zero console errors and a clean scene-graph audit are measurements, not assumptions.

Canonical starter skeleton (read [references/canon-r185.md](references/canon-r185.md) before writing a new scene):

```js
import * as THREE from 'three/webgpu';

const renderer = new THREE.WebGPURenderer({ antialias: true });
renderer.setSize(innerWidth, innerHeight);
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.toneMapping = THREE.ACESFilmicToneMapping;
await renderer.init();

const timer = new THREE.Timer();
renderer.setAnimationLoop((timestamp) => {
  timer.update(timestamp);
  const dt = timer.getDelta();
  // ...
  renderer.render(scene, camera);
});
```

Generate scene boilerplate instead of hand-writing an importmap (it resolves the installed `three` depth and falls back to CDN):

```bash
node scripts/new_scene.mjs --dir path/to/scene --title "Name"
```

## Reference router

Load only what the task needs:

| The task involves | Read |
|---|---|
| Anything non-trivial, before writing a helper | [references/capabilities.md](references/capabilities.md) |
| New scene, renderer setup, colour, tone mapping, importmap | [references/canon-r185.md](references/canon-r185.md) |
| Checking whether an API is removed or deprecated | [references/deprecated-r185.md](references/deprecated-r185.md) |
| Shaders, node materials, GPU compute, particles | [references/tsl-language.md](references/tsl-language.md) |
| Sky, water, terrain, fog, HDRI/IBL, scale, planetary distance | [references/environments.md](references/environments.md) |
| Procedural geometry, instancing, CSG, extrusion, LOD | [references/geometry-procedural.md](references/geometry-procedural.md) |
| Animation, mixer, skinning, morphs, cameras, timelines | [references/animation-motion.md](references/animation-motion.md) |
| Rigid bodies, collisions, gravity, ragdolls, vehicles | [references/physics.md](references/physics.md) |
| Bloom, AO, SSR, DOF, godrays, antialiasing, colour grading | [references/postfx-catalog.md](references/postfx-catalog.md) |
| Embedding a canvas in a page: scroll, DOM, mobile, a11y | [references/web-integration.md](references/web-integration.md) |
| Slow, black, flickering, or leaking renders | [references/pitfalls-production.md](references/pitfalls-production.md) |

## Hard rules

- **Fix world scale (`1 unit = 1 metre`).** Float32 visibly wobbles past ~100 km from origin; scale worlds down instead of pushing coordinates out.
- **Scale-check every effect default.** View/world-space parameters (`ao().radius`, `dof` focus, `ssr` thickness, fog density, shadow bias) silently fail outside tabletop scale; calibrate each in metres.
- **Do not trust `renderer.info` after post-processing.** Multi-pass pipelines reset counters on each pass; set `info.autoReset = false` and reset once per frame.
- **Dispose every removed GPU resource.** Geometries, materials, textures, and render targets are not garbage collected; pair every `remove()` with `dispose()`.
- **Move per-element work to GPU compute before CPU micro-optimisation.** See [references/tsl-language.md](references/tsl-language.md).
- **Build form, material, then light before glow.** Bloom cannot rescue weak geometry.

## Red flags

Stop and check the matching reference before writing any of these:

| Anti-pattern | Why it breaks in r185 |
|---|---|
| `THREE.mrt(`, `THREE.pass(`, `THREE.uv(` | Node functions live on `three/tsl` (or `THREE.TSL.*`), not `three/webgpu` |
| `ao(depth, normal, camera)` with defaults | `radius`/`thickness` are view-space metres; 0.25 bands large scenes or haloes silhouettes |
| `bloom(…)` on a white/near-white backdrop | Backdrop = 1.0 passes every threshold and veils the subject |
| `new THREE.Color(hex).convertSRGBToLinear()` | Hex `Color` is already linear; double conversion silently darkens (in TSL use `color(hex)`) |
| `aoPass.setResolutionScale(` | Effect nodes expose `resolutionScale` as a property; only `PassNode` has the method |
| `THREE.VSMShadowMap` replacing PCF-soft | PCF-soft is alive on `WebGPURenderer`; VSM costs ~8× more |
| `outputEncoding` / `sRGBEncoding` | Removed — use `outputColorSpace` / `SRGBColorSpace` |
| `for (…) positions[i] += …` per frame | CPU bottleneck — move to a TSL compute shader |
| `transparent: true` + `depthWrite: false` | Set explicit `renderOrder` on every transparent object sharing the frame |
| Bare `await RapierPhysics()` | Fetches from CDN, runs its own `setInterval`, has no `step()`/`dispose()`; read `physics.md` |
| `physics.addMesh(instancedMesh, …)` | Overwrites per-instance scale to `(1, 1, 1)` on the first step |
| `vertexColors: true` + `colorNode = vertexColor()` | `NodeMaterial` multiplies the attribute twice and silently darkens; pick one |
| JS `src`/`dst` swap in ping-pong compute | Textures bake into the compiled shader; build both passes and alternate dispatch |
| `i.modInt(` in compute TSL | Not in r185 — use `mod` |
| Advecting only one field in cellular transport | Advect every coupled property riding on the mass or the front stalls |
| `AdditiveBlending` on dense stacked sprites | Saturates to white and blows out bloom; use occlusion for smoke, additive for sparse sparks |
| Bright `colorNode` + bright `emissiveNode` | Sunlight washes pale albedo into sand; use near-black albedo with bright emission |
| Black metallic surfaces | Missing `scene.environment` (`RoomEnvironment` fixes it in one line) |
| Hand-rolled noise/IK/decals/simplify/physics | Check `references/capabilities.md` first — it likely ships |

## Verification loop

Always verify in a real focused Chrome window (never headless Playwright, which throttles `rAF` to ~1 fps):

```bash
node scripts/serve.mjs --port 8765 --root .          # no-store, always
node scripts/verify_scene.mjs --url http://127.0.0.1:8765/ \
     --json report.json --out shot.png --orbit 3
```

`verify_scene.mjs` hooks `__THREE_DEVTOOLS__` automatically (or expose `window.__scene = { scene, camera, renderer, controls }` for explicit capture) and checks three independent axes: **0 console errors/exceptions**, **main-thread ms/frame** (prefer `< 8 ms` mean on 60 Hz; ignore `fps` when `vsyncCapped` is true; `draw calls`/`triangles` use a dedicated single-frame sample), and **scene-graph audit** (`ok` fails on structural faults like wrong normal-map colour space, sky inside fog, or missed shadow frustum). Always pass `--orbit N` and inspect the screenshots directly.

### Deterministic capture contract

1. **Seed randomness** — use a fixed-seed PRNG (e.g. 4-line LCG) instead of `Math.random()` so repeated runs are pixel-identical.
2. **Expose named views via `?view=`** — make every camera preset addressable by query string, not only keyboard shortcuts.
3. **Freeze simulation count via `?steps=N`** — advance exactly `N` fixed steps and halt so screenshots never drift with wall-clock timing.
4. **Warm up steady state via `?warm=N`** — advance `N` steps and keep running so frame-time profiling avoids startup transients.
5. **Overlay reference targets in-page** — when matching a reference image, show it in a corner `<figure>` (~1/6 width, hideable by flag) for direct side-by-side framing and colour comparison.

## Checking a fact

Verify r185 symbols against the installed package instead of guessing:

```bash
grep -rn "@deprecated" node_modules/three/src/ | grep -i "<symbol>"
node -e "const t=require('three'); console.log(typeof t.<Symbol>)"
```
