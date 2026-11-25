# Track B (`showcase`) — Interaction Handfeel Math & 20 Pattern Recipes

Physics-based feel diagnostics, frame-rate-independent follower filters, projective corner-pin math, Verlet solvers, and ready-to-use implementation patterns for **Track B (`showcase`)**.

---

## 1. Handfeel Diagnosis & Physics Primitives

Diagnose feel complaints by mechanical root cause before touching constants. Keep state (`vel`, `acc`, `oldX`) in closures/refs, never React state, and clamp `const dt = Math.min(rawDt, 1 / 30)`.

| User Complaint | Mechanical Root Cause | Fix |
|---|---|---|
| "四平八稳 / 太机械" | Monotonic lerp with zero weight/overshoot | Underdamped spring (§1.1) |
| "顺但是没劲" | Position moves without velocity attitude or environment response | Velocity lean (§1.2) + secondary jelly (§1.4) |
| "自己在乱跳 / 误触发" | Trackpad inertial wheel tail (~1s) firing extra steps | Accumulate-threshold + cooldown guard (§1.3) |
| "跟手但总差一点 / 追不上" | First-order filter chasing a moving target lags by `speed / k` | Add velocity lead term `target + targetVel / k` (§1.6) |
| "画面一抖一抖" (moving & parked) | Offset/correction added *after* the filter gets undone next frame | Filter correction separately and bake into target (§1.6) |
| "30/60/120fps 手感不一样" | Fixed per-frame `x += (t - x) * 0.1` changes bandwidth with FPS | Exponential decay `1 - Math.exp(-k * dt)` (§1.6) |
| "按键瞬间身体硬掰" | Pose driven directly by raw input rather than acceleration | Acceleration → critically damped spring `c = 2√k` (§1.6) |
| "撞击没力 / 抖成一团糊" | Missing shake, or multiple shake impulses summed | `Math.max` amplitude, split X/Y frequencies (§1.7) |

### 1.1 Underdamped Spring (Things That Land With Weight)
```js
vel += (target - x) * STIFFNESS * dt; // STIFFNESS: 60–90
vel *= DAMPING;                       // 0.86 playful, 0.90 jelly, 0.93 calm (convert to Math.pow(DAMPING, dt*60) for strict FPS parity)
x += vel * dt;
```

### 1.2 Velocity Coupling (Lean / Stretch Into Travel)
```js
const lean = Math.max(-22, Math.min(22, vel * 0.5));
el.style.transform = `translate3d(${x}px, ${y}px, 0) rotateZ(${baseTilt + lean}deg)`;
```

### 1.3 Trackpad Wheel Momentum Guard
```js
if (now < lockedUntil) return;
if (Math.sign(delta) !== Math.sign(acc)) acc = 0;
acc += delta;
if (Math.abs(acc) >= 90) { step(Math.sign(acc)); acc = 0; lockedUntil = now + 600; }
// decay acc *= 0.92 each rAF frame
```

### 1.4 Secondary Jelly Wobble & Asynchronous Idle Breathing
```js
jVel += (Math.max(-1.4, Math.min(1.4, primaryVel)) - j) * 55 * dt;
jVel *= 0.90; j += jVel * dt;
// Volume-preserving squash & stretch (vary gain/sign/phase per background element: ×1.0, ×1.6, ×2.1):
el.style.transform = `scale(${1 + j * k}, ${1 - j * k}) rotate(${j * deg}deg)`;
// Idle breathing — use incommensurate frequencies (0.7 / 0.9 / 1.1 Hz) so elements never pulse in unison:
const bobY = Math.sin(t * 1.1) * 1.6, swayZ = Math.sin(t * 0.7) * 1.2;
```

### 1.5 Alpha-Masked 2.5D Lighting on Flat Cutouts
Overlay `.glow` (`mix-blend-mode: screen`, warm white radial at `--light-x/--light-y`) and `.shade` (`mix-blend-mode: multiply`, cool dark radial at `100% - light`) both clipped with `mask-image` / `-webkit-mask-image` of the cutout's alpha, paired with `≤14°` stage tilt. *CORS trap:* `file://` blocks external `mask-image: url(img/x.webp)` while allowing `<img>`; inline the alpha mask as a compact `data:` URI (~4 KB at 320px) when supporting offline single-file playback.

### 1.6 Followers That Must Arrive and Stop (Cameras, Cursors, Rails, Tooltips)
```js
// 1. Frame-rate-independent exponential filter (k in 1/s: camera 4.5, yaw 2.2, horizon 0.35):
const follow = (cur, tgt, k, dt) => cur + (tgt - cur) * (1 - Math.exp(-k * dt));

// 2. Cancel steady-state lag (speed / k) when chasing a moving target:
const aim = targetPos + targetVel / k;
pos = follow(pos, aim, k, dt);

// 3. One quantity, one filter, one target — NEVER add a lift/offset after follow():
lift = follow(lift, rawGroundLift, rising ? 18 : 2.2, dt); // fast rise prevents clipping, slow fall prevents drop
camY = follow(camY, baseY + lift, 4.5, dt);

// 4. Acceleration-driven critically damped pose (zero overshoot, free collision reaction):
const k = 120, c = 2 * Math.sqrt(k);
poseVel += (-k * (pose - lateralAccel * LEAN) - c * poseVel) * dt;
pose += poseVel * dt;
```

### 1.7 Screen Shake (`max`, Never `sum`)
```js
shakeAmp = Math.max(shakeAmp, amp); shakeEnd = Math.max(shakeEnd, now + dur); // dur ≤ 0.35s
const e = Math.max(0, (shakeEnd - now) / dur);
wrap.style.translate = `${Math.sin(t * 47) * shakeAmp * e}px ${Math.sin(t * 31 + 1.3) * shakeAmp * e}px`;
```
Disable under `prefers-reduced-motion` and never shake body copy being read.

---

## 2. Pattern Recipes Catalog (#1 – #20)

1. **Line-by-Line Mask Reveal:** Group word spans by `getBoundingClientRect().top`, wrap each visual line in `overflow: hidden`, animate inner `translateY(105% → 0)` (`700ms`, `80ms` stagger, `cubic-bezier(.77,0,.18,1)` or GSAP `SplitText`). Reduced motion: `opacity: 0 → 1`, `0ms` translate.
2. **Magnetic Hover:** On `mousemove`, translate `(clientX - cx) * 0.35`, `(clientY - cy) * 0.35` (`0.1s linear`); on `mouseleave`, return to `0,0` (`0.5s ease-out-expo`). Creative sites only; disable on coarse pointers and reduced motion.
3. **Clip-Path Curtain + Camera Pull:** Container transitions `clip-path: inset(0 100% 0 0) → inset(0)` (`800ms`) while child `<img>` scales `1.15 → 1.0`.
4. **Scroll-Velocity Skew:** Read `velocity = scrollY - lastScroll` (`{ passive: true }`), damp `skew` toward `clamp(velocity * 0.08, -5, 5)`, decay `velocity *= 0.9`, set `will-change: transform` only while `|skew| > 0.05`.
5. **Horizontal Scroll Rail:** `gsap.to(items, { xPercent: -100 * (items.length - 1), ease: 'none', scrollTrigger: { trigger: rail, pin: true, scrub: 1, end: () => '+=' + rail.offsetWidth } })` gated inside `gsap.matchMedia().add('(min-width: 768px)', ...)`; stack vertically on mobile.
6. **Parallax Depth Stack:** Oversize each absolute child inside `overflow: hidden` and drive `translateY(-scrollY * speed)` (`0.2 / 0.5 / 0.8`) in the page's single `rAF` loop.
7. **State-Carrying Custom Cursor:** Fixed `pointer-events: none` element following pointer; morphs into action label/lens over `[data-cursor-expand]`; `display: none` under `@media (pointer: coarse)`.
8. **Route Transition (Framer Motion):** `<AnimatePresence mode="wait">` with `initial={{ opacity: 0, y: 16 }}`, `enter={{ opacity: 1, y: 0, duration: 0.45 }}`, `exit={{ opacity: 0, y: -8, duration: 0.25 }}`.
9. **Scroll-Pinned Step Sequence:** GSAP `timeline({ scrollTrigger: { trigger, start: 'top top', end: '+=200%', pin: true, scrub: 1.5, anticipatePin: 1 } })`; replace with vertical stack `<768px`.
10. **Tabular Number Reveal:** Tween `{ val: 0 } → target` (`1.4s power2.out`, `once: true`) writing formatted fixed-decimal string on `font-variant-numeric: tabular-nums`; render final figure in HTML for no-JS / reduced-motion.
11. **SVG Goo Metaball Unmasking (Zero WebGL):** Leader-follower chain of 6 `<circle>` elements inside `<mask>` filtered by `<feGaussianBlur stdDeviation="22" result="blur"/><feColorMatrix in="blur" type="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 22 -9"/>` (`color-interpolation-filters="sRGB"`), unmasking a second `<image>` layer.
12. **Canonical Lenis + GSAP `ScrollTrigger` Wiring:**
    ```js
    const lenis = new Lenis({ lerp: 0.085, smoothWheel: true, anchors: true });
    const onScroll = () => ScrollTrigger.update();
    const tick = (t) => lenis.raf(t * 1000); // GSAP ticker supplies seconds; Lenis expects ms
    lenis.on('scroll', onScroll);
    gsap.ticker.add(tick);
    gsap.ticker.lagSmoothing(0);             // or lagSmoothing(500, 33) on heavy pages; prevents tab-return jump
    ```
    Any WebGL canvas reads `window.scrollY` directly rather than integrating its own scroll estimate.
13. **Luminance-Aware Adaptive Header:** Check `.is-dark-section` rects intersecting `probeY = 38px`; for sections whose background morphs mid-scroll, compute live `0.299*R + 0.587*G + 0.114*B < 145` from `getComputedStyle(el).backgroundColor` plus a double-`rAF` settle re-check.
14. **Drawn SVG Annotation Ring (`cases`/Artwork Invitations):** `<svg viewBox="0 0 76 140" preserveAspectRatio="none"><ellipse cx="38" cy="70" rx="36.5" ry="68.5"/></svg>` with `stroke-dasharray: 341; stroke-dashoffset: calc(var(--draw, 0) * 341)`. **Never set `vector-effect: non-scaling-stroke`** (it moves dash lengths into screen space so the ring stops half-drawn). Size to `1.22–1.30×` the **painted** alpha bbox; set `pointer-events: none` when faded out.
15. **Verlet Text Curtain (`cases/char-curtain`):** Independent vertical Verlet columns with **zero horizontal links** (5 Gauss-Seidel passes/frame, soft top hem `p.x += (initX - p.x) * 0.35`, anisotropic pointer push `X × 1.0, Y × 0.35` with `(1 - d/70)² × 4.2` falloff, bounce by reflecting `oldX/oldY`). Scroll injects decaying kinetic energy (`scrollEnergy += |deltaY| * 0.004; scrollEnergy *= 0.97`) rather than position.
16. **Native CSS Scroll Timelines & `sibling-index()` (Progressive Enhancement Order):**
    1. Author the **finished** visible state as normal base CSS (what Firefox and `prefers-reduced-motion` render).
    2. Add `animation-timeline: view()` / `scroll()` inside `@supports (animation-timeline: scroll())` and `@media (prefers-reduced-motion: no-preference)`.
    3. Use `animation-delay: calc(sibling-index() * 60ms)` for zero-JS stagger and `scroll-target-group: auto` + `:target-current` for native scroll-spy.
17. **Projective Corner-Pin Homography (`matrix3d`) + Mandatory Convexity & Tilt Guards:**
    Maps a `w × h` DOM element (`position:absolute; left:0; top:0; transform-origin:0 0`) onto any convex quad `d = [TLx,TLy, TRx,TRy, BLx,BLy, BRx,BRy]` (~`0.016px` CSS round-trip floor):
    ```js
    const adj = m => [m[4]*m[8]-m[5]*m[7], m[2]*m[7]-m[1]*m[8], m[1]*m[5]-m[2]*m[4],
                      m[5]*m[6]-m[3]*m[8], m[0]*m[8]-m[2]*m[6], m[2]*m[3]-m[0]*m[5],
                      m[3]*m[7]-m[4]*m[6], m[1]*m[6]-m[0]*m[7], m[0]*m[4]-m[1]*m[3]];
    const mul = (a,b) => { const c=[]; for(let i=0;i<3;i++) for(let j=0;j<3;j++) c[3*i+j]=a[3*i]*b[j]+a[3*i+1]*b[3+j]+a[3*i+2]*b[6+j]; return c; };
    const mv  = (m,v) => [m[0]*v[0]+m[1]*v[1]+m[2]*v[2], m[3]*v[0]+m[4]*v[1]+m[5]*v[2], m[6]*v[0]+m[7]*v[1]+m[8]*v[2]];
    const basis = (x1,y1,x2,y2,x3,y3,x4,y4) => { const m=[x1,x2,x3,y1,y2,y3,1,1,1], v=mv(adj(m),[x4,y4,1]); return mul(m,[v[0],0,0,0,v[1],0,0,0,v[2]]); };
    function quadOK(d) { // TL, TR, BR, BL winding — prevents w < 0 screen-filling bowtie explosion
      const P = [[d[0],d[1]], [d[2],d[3]], [d[6],d[7]], [d[4],d[5]]];
      let sign = 0;
      for (let i = 0; i < 4; i++) {
        const [ax,ay] = P[i], [bx,by] = P[(i+1)%4], [cx,cy] = P[(i+2)%4];
        const cr = (bx-ax)*(cy-by) - (by-ay)*(cx-bx);
        if (Math.abs(cr) < 1e-6) return false;
        const s = Math.sign(cr); if (!sign) sign = s; else if (s !== sign) return false;
      }
      return true;
    }
    function cornerPin(w, h, d) {
      if (!quadOK(d)) return null;
      const t = mul(basis(...d), adj(basis(0,0, w,0, 0,h, w,h))).map((x,_,a) => x / a[8]);
      return `matrix3d(${[t[0],t[3],0,t[6], t[1],t[4],0,t[7], 0,0,1,0, t[2],t[5],0,t[8]].join(',')})`;
    }
    ```
    **Mandatory edge-tilt clamp:** Clamp each edge normal relative to the **perpendicular of the card's own axis** within `TILT_MAX = w > h ? Math.asin(Math.min(1, h / w)) * 0.85 : Math.PI / 2` (clamping two normals against *each other* fails to stop bowtie flips).
18. **Hanging Verlet Card Chain:** String `N` cards (`CARD_H < REST`, `GRAV = 0.55`, `DAMP = 0.965`, `16` iterations) below pointer `pts[0]` and corner-pin (#17) each card between `pts[i]` and `pts[i+1]` using clamped central-difference normals. **Critical anti-fold rule:** Segment `0` has a pinned head, so give `pts[1]` **`share = 1.0`** (`0.5` on `i > 0`) — giving segment `0` only `0.5` leaves it under-solved so `pts[1]` folds above the anchor and inverts card `0`.
19. **Slack String With Exact Datum Endpoint (`cases/string-clock`):** Hold the data-driven tip on a **stiff spring (`K_TIP = 1600`)** so readout error stays `<0.3°` while running the interior Verlet chain weak (`3` passes at `0.5`) so it sags (`arc/chord ≥ 1.12`) and stretches elastically under drag. Add lateral `-tangent` bias to break vertical buckling symmetry, sweep segment-length caps **forward then backward twice**, and clamp grabs to **container box first, reach second**.
20. **Cumulative Emergence (Zero-Transition Dealing):** Deal items on a `167ms` tick grid with stochastic skipped ticks (`×1 / ×2 / ×3`, **zero** entrance CSS transition, `~88%` still frames). Assign `el.style.setProperty('--z', ++dealt)` (never inline `el.style.zIndex`, which kills `:hover { z-index }`), cap live DOM nodes via FIFO retirement (`CAP = 46`) while the displayed counter keeps climbing, and float opaque foreground panels *over* the pile rather than carving an empty hole in placement coordinates.
