# Track A (`commerce`) — Photography, Micro-Motion, Moments, Effects & Finish Gate

Media sourcing, restrained motion layer, creative moments/effects budgets, and automated browser gate rules for **Track A (`commerce`)**.

---

## 1. Licensed Photography & Stand-Ins (`scripts/photos.mjs`)

Every `<img>` carries `data-source` (`client`, `commissioned`, `phone`, `supplier`, `library-057`, `stand-in`) and `data-subject`, starts at `opacity: 1` from first paint, and carries **zero shader/print/halftone/dither/duotone filters** and **zero visible captions**.

### Four Photo Paths
1. **Client's own photographs:** Always lead when supplied.
2. **Curated library (`photos.mjs pick`):** Vetted Wikimedia Commons & Unsplash detail frames (`quality ≥ 7`, hands/tools/materials/process — never recognizable faces, rival signs, or whole rooms). By default capped at **≤ 1/3 of page photos** (`--draft-lead --pictures 12` lifts the cap for draft `place` pages; `--place "<region>"` deals regional land as lead for remote inns/lodges).
3. **Live Wikimedia search (`photos.mjs search`):** Licensed `≥1600px` `CC0 / CC BY / CC BY-SA` candidates stored in `.web-craft/found.json` (`f1`, `f2`...). Mandatory for **physical products/hardware without client photos**, **games without key art** (search setting: `"flooded coastal town"`), and thin-library trades (`restaurant`, `pottery`, `yoga`). Inspect every candidate at full resolution: reject readable rival logos/names, faces passed off as staff/customers, or mismatched colour grades. List every stand-in in the final report.
4. **No photo:** Show live HTML product UI (`software`), typography, or — **only when the brief explicitly asks for 3D** — a custom `product-render` spec.

```bash
node <skill>/scripts/photos.mjs pick --trade cafe --sections hero,bar,bar,coffee,beans --draft-lead --pictures 12 --history .web-craft/history.json
node <skill>/scripts/photos.mjs search "cargo bicycle" --count 8 --out .
node <skill>/scripts/photos.mjs fetch <ids> [--hero <lead-id>] --out .
node <skill>/scripts/photos.mjs credits --out . --write    # run AFTER markup uses the fetched files
```

- **Sizing & text-on-photo:** Hero uses `fetchpriority="high"` + `780×975` (`4:5`) `<picture>` mobile source with `data-phone-fill` (`≤400 KB`); below-fold photos use `loading="lazy" decoding="async"` (`≤250 KB`, total page `<2400 KiB`). Never place text on a photograph on `place` pages; on other kinds, text sits only on a naturally calm dark/light region in the hero and at most one `photo-band` (never a CSS scrim/gradient).
- **Credits:** One single line in the footer legal row (`Photographs via Unsplash and Wikimedia Commons`, linking `credits.html` written by `photos.mjs credits --write`). Never list per-photo links in the footer (`credit-wall` FAIL).

---

## 2. Track A Motion Layer (`assets/motion`)

Every Track A page moves in **exactly three places** (`<html data-motion>`, `assets/motion/motion.css`, `assets/motion/motion.js`):

1. **Hero entrance (`data-enter` on `<section class="hero">` + inline `<head>` `m-enter` timer):** Runs once on load (`~1.1s`, `--m-ease-enter: cubic-bezier(.22,1,.36,1)`): `<h1>` rises line-by-line out of word masks (`700ms`, `80ms` stagger), lead/buttons fade up `12px`, hero photo settles `1.05 → 1` (never hidden). Stands as written under reduced motion, without JS, and in headless shots unless `data-motion="live"`.
2. **One or two dealt section moments (`data-moment`):** Scrubbed or triggered strictly inside their own section (`1` on short pages, `2` on `≥8`-section pages). Outside `[data-moment]` and tech `[data-big-scene]`, **nothing animates on scroll** (no scroll reveals, text parallax, Lenis, or wheel hijacking).
3. **Hover & press micro-interactions (`(hover: hover) and (pointer: fine)`):**
   - **Buttons (`.btn`):** Fill steps `14%` toward ink + `1px` lift (`150ms` in / `120ms` out); `:active` presses `1px` down + `scale(.985)` (`90ms`). Never override `.btn` `transform`/`transition` in page CSS. Arrow `svg.m-arrow` shifts `+3px`.
   - **Links (`.link`, nav/footer words):** Left-to-right `1px` underline draw (`150ms`); nav mega/card panel opens after `150ms` intent (`200ms` fade + `6px` drop).
   - **Linked cards & photos:** Linked `.card` lifts `2px` (`180ms`; unlinked cards use `.m-nolift`); linked photo (`.m-zoom` or `img.frame__img` in linked frame) scales `1.02–1.03` inside `overflow: hidden` (`600ms` in / `400ms` out). Zero card tilt or magnetic buttons.
   - **Tech loops & counts:** At most `1` timed hero/`[data-visual]` loop + `1` fragment loop per card group (`2.5–4s` cycle, `32px` `.loop-pause` button on anything moving `>5s`) + at most `1` number count (`data-m-count` or `counter-rolls`, never both).

---

## 3. Creative Moments (`scripts/moments.mjs`)

13 active moments in `assets/moments/<id>/` (all 5 legacy retired moments are removed). Deal via `moments.mjs`, never by taste, keeping total page live WebGL contexts **`≤ 4`**:

```bash
node <skill>/scripts/moments.mjs pick --page <kind> --count 1|2 --fits section,statement [--scene <id>] [--effects <ids>] [--contexts <n>] --photo --history .web-craft/history.json
node <skill>/scripts/moments.mjs check index.html --page <kind>
```

| Moment ID | Kind · Fits | Allowed `--page` | Phone / WebGL |
|---|---|---|---|
| `photo-chapters` | `scroll · section` (`3–4H` live, full-width chapter photos) | `place`, `product`, `service` | Runs on phone · 0 GL |
| `picture-develops` | `transition · section` (`1.6s` film develop once on enter) | `place`, `product`, `service` | Runs on phone · 0 GL |
| `word-highlight` | `scroll · statement` (words light in ink across scroll) | All 6 kinds | Runs on phone · 0 GL |
| `pinned-chapters` | `scroll · section` (`2H` sticky frame + `2–4` steps) | `software`, `gaming`, `tech`, `product`, `service` | Static rows · 0 GL |
| `counter-rolls` | `text · statement` (proof figures roll once; never in card) | `software`, `gaming`, `tech` | Static figures · 0 GL |
| `giant-type-pass` | `scroll · statement` (mid/dark photo through giant type) | `software`, `gaming`, `tech` | Static · 0 GL |
| `letters-assemble` | `scroll · statement` (`2–5` large words lock into line) | `software`, `gaming`, `tech` | Static · 0 GL |
| `marquee-row` | `scroll · between` (words/formats/cities — **never logos**, has pause) | `software`, `gaming`, `tech` | Wrapped row · 0 GL |
| `line-carries-colour` | `transition · section` (climbing line reveals new ground) | `software`, `gaming`, `tech` | Static · 0 GL |
| `iris-opens` | `transition · section` (accent-ring disc opens new ground) | `software`, `gaming`, `tech` | Static · 0 GL |
| `cursor-spotlight` | `hover · hero` (only when dealt hero lists it) | `software`, `gaming`, `tech` | Off on touch · 0 GL |
| `liquid-type` | `liquid · hero,statement` (SVG filter ripple on `≤6` words) | `software`, `gaming`, `tech` | Static · 0 GL |
| `liquid-hover` | `liquid · section,hero` (WebGL ripple on detailed photo) | `software`, `gaming`, `tech` | Plain photo · **1 GL** |

*Mount:* Copy section structure from `assets/moments/_demo/in-page.html` or `in-page-service.html` (never sit a moment inside a `.card`), add the `mo-js` `<head>` guard + `modulepreload` links (`moments.js`, `lib.js`, `<id>/moment.js`); `system.js` boots `moments.js`. One pointer effect per page max (`hover`/`liquid` moment excludes `fx-button`, `fx-spotlight`, and pointer-turning objects).

---

## 4. Tech Effects, `fx-*` Parts, 3D Product Builder & Big Scenes

**Strict trade gate:** Shader grounds (`assets/effects`), WebGL `fx-*` parts (`assets/components`), code prints (`assets/objects/print-*`), and `data-big-scene` (`assets/scenes`) are **strictly for `software`, `gaming`, and `tech`** — `place`, `service`, and non-tech `product` pages carry **0** effects (except plain `fx-photo`, still-baked OpenStreetMap `fx-map` via `assets/components/fx-map/bake.mjs` when a real street is given, and `product-render` stills when the brief explicitly requests 3D).

- **One-effect budget on tech:** At most **one** live effect per page — *either* 1 hero/`[data-visual]` shader ground (`effects.mjs pick --page <site-kind> --palette light|dark|colour --slots hero --quiet`), *or* 1 WebGL `fx-*` part (`fx-dither-object` `[headphones|chair|camera|drone]`, `fx-headline`, `fx-stat`, `fx-button`, `fx-prompt`, `fx-search`, `fx-globe`, `fx-avatar`, `fx-pricing`, `fx-progress`, `fx-spotlight`), *or* 1 `print-*` object (`print-cup|wheel|lamp|globe|cards`, `_print-core/auto.js`), *or* 1 `data-big-scene`. Behind UI fragments (`fx-feature-card`, card groups), exclude all pattern/print shaders (`ruled-grounds,grid-pulse,contour-lines,dot-terrain,dotted-globe,ridgeline,halftone-screen,bayer-dither,ascii-shade,line-engraving,duotone-grade`).
- **Product 3D builder (`assets/objects/product-render` — only on explicit 3D ask):** Compose the client's actual product from real measurements (`≤90` parts: `tube`, `beam`, `box`, `panel`, `cylinder`, `sphere`, `torus`, `joint`, `wheel`, `shade`, `seat`, `basket`, `arc`, `spring`, `path`), validate & bake transparent stills + posters via `node <skill>/assets/objects/product-render/make-posters.mjs <spec.json> --profile .web-craft/chrome-posters`, and mount on `data-product-place="stage"` (stills by default, `0` WebGL at rest; `data-product-mode="live"` uses `1` context only when requested).
- **Big scenes (`assets/scenes/<id>`, tech `0–1` per page, counts as the 1 effect):** `descend-through-weather`, `shaped-window-over-fixed-world`, `fixed-hero-object` (`restH: 2`, placed below hero), `powers-of-ten-pullback`, `product-assembles-into-its-action`, `parts-lock-into-the-whole`, `fly-into-the-shape`, `letter-physics`, `object-through-giant-type`, `dot-becomes-the-full-stop`, `letter-bar-floods-the-ground`. Pass `--scene <id>` to `moments.mjs pick` so `avoidMoments` and WebGL context budgets are enforced automatically.

---

## 5. Manual Finish Gate & Waivers (`scripts/gate.mjs`)

Run `gate.mjs` manually in the foreground (`--start` before building, then `node <skill>/scripts/gate.mjs index.html` after step-6 checks). It runs `consistency.mjs --quick --widths 1440,390` (including `320px` overflow/collide/tap walk), `assets/layout/check.mjs --sizes 1440x900,390x844`, `copy-lint.mjs`, plus `kit-edited` (fails if any copied `assets/` file was altered) and `checker-gaming` (fails if page code probes `navigator.webdriver`/headless user agents), holding `hero-enter` and `moment-none` as blocking FAILs.

- **Verdicts (`≤3` fix rounds by default):**
  - `GATE: PASS` → All blocking checks cleared; report and finish.
  - `GATE: FAIL <n> (round k of 3)` → Fix listed findings and re-run (`--quick` previews without spending a round).
  - `GATE: OPEN <n> (rounds used up)` → Stop fixing; list remaining FAILs and waivers in report.
  - `GATE: SETUP (...)` → Target missing or unbuilt framework shell; rebuild/serve locally and re-run.
  - `GATE: ERROR (...)` / `GATE: OFF` → Report exact status line and finish without looping.
  - `GATE: DONE (...)` → Run `gate.mjs --done "<user's exact words, 12+ chars>"` **only** when the user explicitly instructs to stop or ship as-is.
- **Waivers (`.web-craft/waivers.json`, max 5, never on `kit-edited` or `checker-gaming`):**
  ```json
  [{ "check": "one-section", "target": "section#visit", "reason": "hours list fits one screen at 390; phone bar adds padding" }]
  ```
  Each waiver must match **one** specific finding (`target` ≥3 chars, `reason` ≥12 chars) and be disclosed in the completion report.
