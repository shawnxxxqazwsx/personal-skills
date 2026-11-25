# Track B (`showcase`) — 2D Cutout Image Planes in a Perspective Camera & Streaming

Building genuine perspective depth, silhouette occlusion, analytic contact shadows, and multi-screen streaming **entirely from flat 2D image cutouts** (Ladder Rung 5 — zero 3D polygon modelling required whenever silhouettes do not need to rotate in depth).

---

## 1. Upstream Asset Pipeline (Scripted Metadata Before Runtime)

Never hand-nudge placement numbers in JS — generate cutouts and `elements.json` (`{ w, h, cx, baseline, crown, coverage, paint }`) from a build script:

1. **Key against *each plate's own border median*, never hardcoded white:**
   ```python
   edge = np.concatenate([rgb[:8].reshape(-1,3), rgb[-8:].reshape(-1,3), rgb[:,:8].reshape(-1,3), rgb[:,-8:].reshape(-1,3)])
   bg = np.median(edge, axis=0)
   alpha = np.clip((np.linalg.norm(rgb - bg, axis=2) - 7.0) / 42.0, 0, 1)
   alpha = ndimage.median_filter(np.where(alpha < 0.035, 0.0, alpha), size=3)
   ```
   - *White-studio render variant:* Ramp luminance `235 → 250` gated by `max(rgb) - min(rgb) < 12` (protects bright gold/vermilion highlights), then **un-premultiply** `(rgb - 255*(1 - alpha)) / alpha` to prevent bright edge halos on dark grounds.
   - **Mandatory `coverage` gate:** Print opaque pixel fraction for every asset (`20–60%` normal; `~100%` = background kept; `~0%` = subject eaten).
2. **Crop to `alpha > 0.06` bbox + `4px` margin:** Large empty transparent rects make the eye read rectangular stickers. *Exempt horizontal band layers* (`ground-band`, `ridge`: crop X only, keep full Y).
3. **Line art & atmosphere plates (`constant RGB + information in alpha`):** Never `multiply` opaque white paper on transparent destinations (paints a ~52% white wash). Convert line art via linear ramp `alpha = clip((250 - lum) / 250, 0, 1)` with flat ink RGB `(62, 52, 40)`. Author fog/wave atmosphere as **one white PNG-8 master** (`-pot` power-of-two dimensions for `RepeatWrapping`, `LinearFilter` without mipmaps) and tint 15 depth layers via `MeshBasicMaterial({ color })` at zero shader cost.
4. **Measure anchors in the same pass:**
   - `cx`: alpha-mass centroid `(col * arange(w)).sum() / col.sum() / w`.
   - `baseline`: lowest row with `rowSum > 0.02 * max(rowSum)` divided by `h` (ignores faint bottom scree).
   - `crown`: highest row with real paint — **never hang attachments (dust, flags, callouts) at `realH`**, because `planeH = realH / baseline` assumes paint touches row 0!
   - `paint`: `[u0, u1, v0, v1]` at `alpha > 200` (`≥1%` row/col coverage) for tight affordance rings.
5. **Per-element magnification budget (`source_px / screen_px_at_dpr2`):** Evaluate at the **closest camera stop**, remembering to multiply `geometry.width * mesh.scale.x`. Background washes may dip `<1.0×`; interactive hero plates must keep headroom `≥1.0×` (or swap `images/` → `0.76×` `images-tablet/` + `dpr ≤ 1.75` on mobile).
6. **Serving-distance texture density:** A far `280m` haze texture (`mean 0.936`) disappears when reused on an `8m` foreground gust. Give near layers a solid body plus density modulation (`mix(0.45, 1.0, smoothstep(0.99, 0.86, grain))`), scale UV tiling with plane growth, and fade edges radially rather than rectangularly.

---

## 2. Two Proven Topologies (`Camera Moves` vs `World Moves`)

Choose topology before placing the first plane:

| Axis | Topology A · **Camera Moves** (Dolly Into a Place) | Topology B · **World Moves** (Read a Page With Depth) |
|---|---|---|
| **Driver** | Camera dollies along `(x,y,z)` path on scroll | Camera parked (`z = 1200`); `containerGL.y` & `containerCSS.y` translate on scroll |
| **Lens (`fov`)** | **Long lens `fov ≈ 26°`** — compresses depth so `3m` near and `21m` far silhouettes touch | **Normal lens `fov ≈ 50°`** — panels read as editorial layout with natural parallax |
| **Scale budget** | Magnification changes along path → enforce per-element ratio table (§1.5) | Constant pixel scale (`1 world unit = 1px` or print grid) → zero magnification blur |
| **Shaders needed?** | Only when artwork is erased/peeled/lit dynamically | Often **zero `ShaderMaterial`** (`MeshBasicMaterial` + UV drift + asymmetric camera wave impacts) |

*Subtle pointer tilt in Topology B:* Apply `±0.035 rad` (`~2°`) lerp to `sceneRoot.rotation.y`, zeroing it in `beforeUpdate()` and restoring in `update()` so hit-testing and screen-box caches never drift.

---

## 3. Placement, Sorting, Contact Shadows & Batch Unification

1. **Real-unit placement from scripted metadata:**
   ```js
   const planeH = realH / meta.baseline, planeW = planeH * (meta.w / meta.h);
   mesh.position.set(x - (meta.cx - 0.5) * planeW, planeH * (meta.baseline - 0.5), z);
   ```
   Tabulate `world → screen` coordinates at key scroll stops with a 10-line probe rather than hand-deriving `fov` trigonometry (avoids aspect `1.78×` width/height mix-ups).
2. **Interlocking silhouettes & foot-line grading:** Compose so near heads/edges cut across far silhouettes on **one shared contour**, and let ground foot lines step naturally down the frame (`foot_y = horizon + k / (camZ - z)`), keeping all feet strictly inside `innerHeight - safeArea`. Rotate side planes on `rotY` so perspective foreshortens courtyard walls.
3. **Manual transparency sort:** Set `transparent: true, depthWrite: false, side: THREE.DoubleSide` and maintain a written `renderOrder` map with numeric gaps (`-1, 0, 1, 3, 6.5, 9, 9.5, 10.8, 11...`) so near-equal `z` planes never z-fight.
4. **Analytic ground-shader contact shadows (never shadow maps, which cast rectangles):** Register standing planes as vertical cylinders `caster(x, z, radius, height)` (up to ~48 `vec4` uniforms) and solve soft capsule shadows along a low raking sun (`uLightDir = normalize(-0.90, 0.19, 0.30)`, ~`11°` elevation → `5×` height shadows tying the whole floor together).
5. **Cure 「有拼接感」 via batch `R − B` colour-temperature measurement:** Print mean `R`, `G`, `B`, `R − B`, and Rec.601 luminance over `alpha > 200` pixels per asset batch. An outlier batch lit by a cooler sun (`R − B = +13` among `+37..+52` warm plates) pops like a collage; multiply a per-element `uLight` `vec3` (`1.09, 1.01, 0.90`) to match the scene lamp without altering local art hues. (Same diagnostic fixes blue sky-PMREM shadow casts: drop `envMapIntensity` to `0.25–0.45` on pale surfaces.)
6. **Unified world-space atmosphere & `uv.y²` sway:** Sample cloud shadows by `(modelMatrix * pos).xyz` (never element origin, which steps across multi-segment walls), tune paper-dissolve `smoothstep(uNear, uFar, vDist)` to the scene's actual farthest `z` (print `%` dissolved there!), and weight vertex wind by `uv.y * uv.y` with dual incommensurate sines so roots stay nailed to the ground.

---

## 4. DOM ↔ Scene Coordinate Sync & Long-Scene Streaming

### DOM Overlays Over Moving Cameras
- **Tracking an object:** Project the 4 corners of `meta.paint` every frame (`motion-timeline-affordance.md` §2.3) — never hardcode `%` CSS coordinates. If tracking DOM rects into WebGL while a parallax rig moves the visible camera, **unproject through a separate static dummy camera** and keep `pointermove` on `window` (since background canvases have `pointer-events: none`).
- **Placing body copy over empty regions:** Grid rendered frames `6×8` across representative scroll stops and place copy only in cells with consistently low luminance standard deviation (structurally quiet sky/margins). For text that must tilt inside perspective while staying selectable DOM, render `CSS3DRenderer` alongside `WebGLRenderer` with the **same camera**, throttling CSS3D DOM additions/removals to `500ms` desktop / `2500ms` mobile.

### Streaming Scenes With 100+ Plates
1. **Asymmetric screen-window lifecycle:** Activate objects in `[-3, +4.5]` screens around the viewport; leaving the window **disposes** `geometry`, `material`, and `texture` (guard async `img.onload` callbacks with `if (this.disposed) return` and share repeated art via a URL ref-counted cache).
2. **Time-budgeted cooperative scan:** Maintain `yieldedAtIndex` cursor in the activation scan and yield after `~4.17ms` (`1000/240`), resuming next frame.
3. **Sliced oversized uploads:** Chop huge plates into `6×6` sub-planes uploaded one slice per `setTimeout(..., 1)` turn, fanning parent `opacity` out to all 36 slices so fades never tile-tear.
