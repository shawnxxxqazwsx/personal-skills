# Track B (`showcase`) — Render Layers, 2D Fragment Shaders, Ink Outlines & Tactile Textures

Choosing what draws the page, running zero-dependency 2D WebGL2 fragment shaders, avoiding silent GLSL bugs, building `11 Hz` hand-drawn outline passes, and layering SVG/Houdini/Canvas tactile textures. *(True 3D polygon scenes, WebGPU/TSL node graphs, and PBR/physics pipelines are out of scope.)*

---

## 1. Choosing the Render Layer Before the Mechanic

Decide and declare the render layer up front (`verify_case.py --layer <dom|svg|canvas2d|webgl>` enforces it, plus the web-font gate requiring `@font-face` or `--draws-own-type`):

| Layer | Choose When | Cost & Boundary |
|---|---|---|
| **DOM + CSS** | Reading order, selectable text, discrete UI states (`<60` moving nodes) | Compositor `transform`/`opacity` only |
| **Inline SVG** | Crisp scalable geometry meant to be read (`<2k` nodes): dials, paths, wobbly frames | Cheap `d` / `stroke-dashoffset` updates; no per-pixel shading |
| **Canvas 2D** | Hundreds of procedural marks, Verlet glyph curtains, generative sleeves/discs | Single draw surface, manual clear; pair with a live DOM readout for accessibility & input probes |
| **WebGL2 (2D / Screen-Space)** | Fullscreen 2D organic backgrounds, liquid transitions, ripple/grain passes, instanced silhouette ink passes | Needs DPR cap (`≤2.0`), off-screen pause, and `prefers-reduced-motion` static fallback |

**Hybrid split is standard:** World/field in Canvas/WebGL2 (`pointer-events: none`), hand-drawn chrome in inline SVG, selectable headings/controls in DOM (`cases/ink-crowd`).

---

## 2. Zero-Dependency Vanilla WebGL2 Fullscreen Shader Runner

Never pull in a 600 KB 3D engine just to run a 2D background or image-transition fragment shader. Compile `#version 300 es` directly:

```js
export function mountFragmentShader(canvas, fragBody, { maxDpr = 2.0 } = {}) {
  const gl = canvas.getContext('webgl2', { antialias: false, powerPreference: 'low-power' });
  if (!gl) return null; // leave CSS ground / fallback image visible
  const vs = `#version 300 es
    in vec2 aPos; out vec2 vUv;
    void main() { vUv = vec2(aPos.x * 0.5 + 0.5, 0.5 - aPos.y * 0.5); gl_Position = vec4(aPos, 0.0, 1.0); }`;
  const fs = `#version 300 es
    precision highp float; in vec2 vUv; out vec4 fragColor;
    uniform vec2 uResolution; uniform float uTime; uniform vec2 uMouse; uniform float uProgress;
    ${fragBody}
    void main() { fragColor = mainImage(vUv); }`;
  const compile = (src, type) => {
    const s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s);
    if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) { console.error(gl.getShaderInfoLog(s)); gl.deleteShader(s); return null; }
    return s;
  };
  const vShader = compile(vs, gl.VERTEX_SHADER), fShader = compile(fs, gl.FRAGMENT_SHADER);
  if (!vShader || !fShader) return null;
  const prog = gl.createProgram();
  gl.attachShader(prog, vShader); gl.attachShader(prog, fShader); gl.linkProgram(prog);
  if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) { console.error(gl.getProgramInfoLog(prog)); return null; }

  const buf = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, buf);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1,-1, 1,-1, -1,1, -1,1, 1,-1, 1,1]), gl.STATIC_DRAW);
  const loc = gl.getAttribLocation(prog, 'aPos');
  gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);

  const uRes = gl.getUniformLocation(prog, 'uResolution'), uTime = gl.getUniformLocation(prog, 'uTime');
  const uMouse = gl.getUniformLocation(prog, 'uMouse'), uProg = gl.getUniformLocation(prog, 'uProgress');
  let mx = 0.5, my = 0.5, progress = 0, raf = 0, running = true, pinnedT = null;

  const resize = () => {
    const dpr = Math.min(window.devicePixelRatio || 1, maxDpr);
    const w = Math.max(1, Math.floor(canvas.clientWidth * dpr)), h = Math.max(1, Math.floor(canvas.clientHeight * dpr));
    if (canvas.width !== w || canvas.height !== h) { canvas.width = w; canvas.height = h; }
  };
  resize();
  const onMove = (e) => { mx = e.clientX / innerWidth; my = 1 - e.clientY / innerHeight; };
  window.addEventListener('pointermove', onMove, { passive: true });

  const draw = (ms) => {
    if (!running) return;
    gl.viewport(0, 0, canvas.width, canvas.height);
    gl.useProgram(prog);
    gl.uniform2f(uRes, canvas.width, canvas.height);
    gl.uniform1f(uTime, pinnedT ?? ms * 0.001);
    gl.uniform2f(uMouse, mx, my);
    gl.uniform1f(uProg, progress);
    gl.drawArrays(gl.TRIANGLES, 0, 6);
    raf = requestAnimationFrame(draw);
  };
  const io = new IntersectionObserver(([e]) => {
    running = e.isIntersecting && !matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (running) { cancelAnimationFrame(raf); raf = requestAnimationFrame(draw); }
  });
  io.observe(canvas);
  return {
    setProgress: (p) => { progress = p; },
    pinClock: (t) => { pinnedT = t; draw(t * 1000); },
    destroy: () => { running = false; cancelAnimationFrame(raf); io.disconnect(); window.removeEventListener('pointermove', onMove); }
  };
}
```
*SSR / Next.js note:* Mark client shader components `'use client'` or load via `dynamic(..., { ssr: false })`, and pause/fallback to a static frame on `<768px` or `prefers-reduced-motion: reduce`.

---

## 3. Core 2D GLSL Recipes & Silent Failure Traps

### Reusable 2D Fragment Snippets
- **2D Simplex Noise (`snoise`):** Hash-based polynomial noise (`permute(x) = mod(((x*34.0)+1.0)*x, 289.0)`) — never loop `sin`/`cos` octaves per pixel on mobile.
- **Pointer Ripple Displacement:** `vec2 d = uv - uMouse; float r = length(d); if (r < 0.15) uv += normalize(d) * (1.0 - r / 0.15) * 0.03;`
- **Liquid Crossfade:** Displace `uv1 = uv + snoise(uv*4.0 + uTime*0.2)*0.1*uProgress` and `uv2 = uv - noise*0.1*(1.0 - uProgress)`, then `mix(tex1, tex2, uProgress)`.
- **Analytic-Ellipse 2.5D Cutout Parallax:** Sum 2–4 smoothstepped ellipses (`head`, `face`, `nose`, `torso`) to synthesize `vDepth ∈ [0, 1]` without an external depth map, shifting `vUv - uPointer * vDepth * 0.01` and discarding `a < 0.02`.
- **Damp-Chain Ribbon Trail:** Cascade 6 points via exponential damp (`lambdas: 16, 8.4, 5.2, 3.1, 1.85, 1.05` — ~1.7× spacing so the tail neither freezes stiff nor detaches) and evaluate `segmentDistance(vUv, p_i, p_{i+1})` SDF.
- **Text-as-Texture:** Rasterize real browser typography onto an offscreen 2D `<canvas>` (`ctx.scale(dpr, dpr)`) once and sample as `sampler2D` for refraction/liquid distortion — avoids full MSDF font pipelines and supports CJK out of the box.

### Six Silent GLSL Traps (Zero Console Error, Broken Frame)
1. **Integer literals in generated GLSL:** String-interpolating `6` instead of `6.0` fails overload resolution in `mix`/`smoothstep`/`pow` and drops the program. Route every injected JS number through `const glFloat = n => Number.isInteger(n) ? n.toFixed(1) : String(n)`.
2. **Reserved GLSL ES identifiers:** Never name variables `flat`, `smooth`, `sample`, `filter`, `input`, or `output`.
3. **WebGL2 `DepthTexture` filtering:** `LINEAR` on a depth texture makes the FBO incomplete and returns `0.0` everywhere — always use `NEAREST`.
4. **Distance shimmering:** Attenuate high-frequency grain/glints with depth (`exp(-vViewZ * 0.028)`, specular `exp(-vViewZ * 0.05)`) to stop crawling sub-pixel aliasing.
5. **Coherent instanced sway:** Drive wind phase from world coordinates (`uTime * 1.6 + origin.x * 0.35 + origin.z * 0.27`) with `smoothstep` root masking and distinct X/Z frequencies — random per-instance phases look like TV static.
6. **Deterministic flicker:** Use two incommensurate sines (`1.0 + 0.1 * sin(t * 13.0) + 0.06 * sin(t * 31.0 + 1.3)`) rather than stateful noise so `window.__seek(t)` is 100% reproducible.

---

## 4. Hand-Drawn Ink Render Recipe (`cases/ink-crowd`)

How to make instanced primitives read as hand-drawn ink rather than shaded 3D:
1. **Unshaded silhouettes + MRT depth-only edges:** Render flat white figures into colour + linear depth targets; fullscreen pass draws outlines **strictly from depth discontinuity** (`uWidth = 2.7px`, `uT0/uT1 = 0.14/0.32`, **`uNormalEdge = 0`** so interior creases disappear and depth reads purely via occlusion). Always build a debug view toggle (`raw color / linear depth / edge`) from frame 1.
2. **Split static `warp` from `11 Hz` `boil`:** Per-instance seeded low-frequency `warp` gives each figure a unique silhouette; `uStep = Math.floor(elapsed * 11)` redraws `boil` (`0.011` on bodies, **`0.07` on ground shadows** — 6× stronger at ground contact) and `22px` block stroke-weight breathing (`±22%`) 11 times/sec inside a `60 fps` camera loop.
3. **Seamless circular rim noise & binary palette:** Sample disc rim wobble on `(cos(a), sin(a))` so `atan` has zero seam; keep palette strictly binary (`#fefefe` paper + `#000000` ink, zero mid-grey washes); scale SVG UI frame jitter to component size (`1.1` on keycaps, `2.6` on cards).

---

## 5. Tactile DOM & Canvas Textures (SVG, Houdini, Noise Tiles)

- **SVG Viscous Goo (`#gooey-liquid`):** `<feGaussianBlur stdDeviation="10" result="b"/><feColorMatrix in="b" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 19 -9" result="g"/><feComposite in="SourceGraphic" in2="g" operator="atop"/>` keeps crisp inner text over liquid-bridged button/chip borders.
- **SVG Paper/Wave Border (`#organic-distortion`):** `<feTurbulence type="fractalNoise" baseFrequency="0.015" numOctaves="4" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="30" xChannelSelector="R" yChannelSelector="G"/>`.
- **CSS Houdini Paint Worklet & `OffscreenCanvas`:** Use `CSS.paintWorklet` for zero-main-thread procedural card grain, or `canvas.transferControlToOffscreen()` inside a Worker when heavy canvas loops share a scrolling page (debounce resize buffer reallocations by `150ms`).
- **Static Offscreen Noise Tile & Anti-Beating Check:** Bake static grain once to a `128×128` offscreen 2D canvas `data:` URL rather than redrawing per frame — **but check tile period against repeating layout bands** (e.g., a `128px` tile over `130.9px` columns beats into vertical Moiré streaks; either choose an incommensurate tile size or write grain directly into the canvas pixels).
