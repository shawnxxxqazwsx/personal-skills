# Track A (`commerce`) — Screen Rhythm, Heroes, Section Plans & Grounds

Authoritative layout and section architecture for **Track A (`commerce`)** builds (`software`, `gaming`, `tech`, `product`, `service`, `place`). Enforced by `scripts/consistency.mjs` and `assets/layout/check.mjs`.

---

## 1. One Section Per Screen & Judge Tile Geometry

At every judge tile `scrollY = k × H` (`1440×900`, `1024×768`, `820×1180`, `768×1024`, `390×844`), **exactly one section** occupies the viewport — zero neighbour headings or grounds peeking in.
- **Shell:** `body` contains only `header.nav`, `main#top`, `footer.closing`, and optional mobile `nav.actionbar`. No popups, chat bubbles, floating pills, or sticky elements outside `[data-moment]` / `[data-big-scene]`.
- **Section box:** `main > section` and `footer.closing` use `height: calc(var(--h, 1) * 100svh)` (`100lvh` and `--hm` under `640px`), padded `--padt` (`120px` / `96px`) top and `--padb + --bar` (`72px` / `48px + --bar`) bottom. Only `photo-chapters` spans `3–4` live screens (omit `--h` on it).
- **Content height `c` windows (`<h2>` top to last child bottom):**
  - **At `1440×900` (`1H` fits `495–708px`):** `<360px` → merge into section above (quotes, logo rows, short FAQs `<495px` merge `64–96px` below the preceding content with no `<h2>`); `495–708px` → `--h: 1`; `708–1320px` → illegal dead zone (trim to `≤708px`, split into two sections, or use `.g2` two-group layout where row 1 is `360–708px` and row 2 is `420–708px` starting `--padt` below screen 2's top); `1320–1608px` → `--h: 2`.
  - **At `768×1024` & `820×1180` (portrait tablet):** `≤832px` → `1H`; `832–1130px` → trim `--p-h` or use `.fill` to fit `1H`; `1130–1856px` → `@media (min-width: 640px) and (max-width: 1023px) { #<id> { --h: 2 } }`.
  - **At `390×844`:** `1H` fits `464–(700 - bar)px`; `2H` fits `1268–(1544 - bar)px`; use `.g2m` or trim mobile copy in between.

---

## 2. Equal Edges, 12-Column Grid & Dealt Typography

- **One `.wrap` everywhere:** `width: min(100% - 2 * var(--gut), 1280px)` → edges at `x = 80` and `1360` at `1440px` (`place`: `1200px` wide at `x = 120..1320`; `390px` phone: `342px` wide at `x = 24..366`).
- **Grid & two-text-line rule:** `.grid` has 12 columns (`24px` gap desktop, `12px` `<640px`). Every block starts on `x_left` or a column start and ends on a column end, the rightmost hitting `x_right`. Text aligns to **at most two vertical x-lines**: the left `.wrap` edge and one chosen split column (`start-6`, `start-7`, or `start-8`; `place` is always `6/6` at `x = 732`). **Splits are always text left, visual right, top-aligned — never mirrored or alternating**; on tablet/phone, text stacks first.
- **Full-bleed rule:** Only section background `img.layer` (`≥90%` section coverage) or a Place `bleed` frame spans `0..viewport`. Never bleed to one viewport edge only (`bleed-one-side` FAIL).
- **Dealt Google Fonts (`start.mjs` + `library/type.json`):**
  - Run `start.mjs deal --page <kind> --trade <trade>` (add `--axis` for `word`/`editorial` heroes) and keep the `:root` block from `start.mjs css` verbatim (`≤2` font families, `≤4` font files, `display=swap`). Never use `Inter`, `Roboto`, `Open Sans`, `Lato`, `Montserrat`, `Poppins`, `Space Grotesk`, or `Plus Jakarta Sans`.
  - Weights: Display `400` (`500` on `tech`/`software`/`gaming`), body `400`, labels/buttons/titles `500` (`600` only on `.mark--initial`; **never `700` or `800`**).
  - Sizes (`1440 / 390`): `h1` `72/38` (or hero token), `h2` `48/30` (`place`: `32/24`), `h3`/quote `28/24`, lead/card title `20/18`, body `16/26`, small `14`, label `13/500` sentence case, stat `38/28`.

---

## 3. Heroes (`assets/layout/deal.mjs` + Place Hero)

Hero is `100svh` (`--h: 1; --hm: 1`), `<h1>` (`≤3` lines, within `heroes.json` `maxChars`) at `y = 120` (`96` phone), sub-line + `≤2` buttons (`1` on `place`) above the fold, ending by `y = 836` at `1440×900`. At `768`/`820`, stacked visuals must end whole (`≥24px` above bottom) or bleed cleanly (`≥96px` under `.stage--fade-b`, never a `1–95px` sliced card edge). Copy **only** `<section class="hero ..." data-enter>` from `assets/layout/hero-<id>.html`:

- **Dealt heroes (`deal.mjs`):**
  - `split`: `span-5` text left + `span-6 start-7` visual right + 1 opaque float card (`software`, `service`).
  - `photo`: Full-bleed photo layer, copy on calm dark side (`span-6`, `h1` `80px`), 4 facts at foot (`gaming` setting fallback, `product`, `service`).
  - `product`: Top head row (`h1` `cols 1–7`, lead+buttons `cols 9–12`) over full-width stage (`1280×566`, product `≥80%` of `.wrap` width, zero grey box). Mandatory when `--has object` or showing physical hardware/goods at scale.
  - `editorial` (`156px` 3-line headline with inline pill photos, `--axis`), `word` (`144px` headline with 1 live word, `--axis`), `collage` (split + lit product window), `film` (cinema poster + play disc), `statement` (`56px` calm sentence), `triptych` (`span-3` `h1` + changing collage), `centred` (centred `72px` `h1` over full-wrap window).
- **Place hero (always printed on `place`, never dealt):** `.hero.hero--photo` on `html[data-type="place"]` — one full-bleed daylight photograph at the top (`y = 72..552`, `--photo: 480px`, **zero text/scrim/gradient on the photo**; `data-phone-fill` `4:5` crop on `390px`), followed on flat ground below by `6/6` split: `h1` (`48/53`, `≤40` chars) left, `20/30` hours/fact sub-line (`≤80` chars) + one `48px` primary button right (`statement` on `.ground-brand` only when zero photos exist).

---

## 4. Page Plans, Dealing & Domain Rules by Kind

Deal structural variants so two pages of one trade never share a template:
```bash
node -e "for(const l of process.argv.slice(1)){const o=l.split('|');console.log(o[Math.floor(Math.random()*o.length)])}" <nav> <footer> <close> <rhythm> <buttons> <mark>
```
- **Software (`software`):** `"nav-mega|nav-cards|nav-centre" "footer-dark|footer-statement|footer-columns" "close-type|close-word" "dark-band|surface-pairs|space" "solid|pill|tonal|arrow" "wordmark|initial|arc|ring|stack|dots"`
  - *Spine:* `nav` → `hero` → `[docked logo-row]` → **`app-frame`** (mandatory whole-product 2-pane `.ui.app.fill` window in section 2 or 3) → `2–3` varied feature sections (`features-2x2`, `bento`, `split-text-left`, `tabs-tour`, `chapter`, `steps`) → `[integrations diagram or ≥9-tool grid]` → `[quote-stat / customer-proof-row]` → `[pricing-three / pricing-two / comparison-table]` → `faq` → `footer.closing`.
- **Gaming (`gaming`):** `"nav-mega|nav-centre|nav-cards" "footer-dark|footer-statement" "close-word|close-type" "dark-band|media-band|space" "solid|pill|block" "wordmark|initial|arc|ring|stack|dots"`
  - *Spine:* `nav` → `hero` (game name + genre + launch status; key art/trailer or `--has setting` stand-in) → `[trailer client-slot]` → `world` (`1–2` full-bleed sections) → `what you do` (`3–5` verb-led open cards over `16:9` captures) → `[system diagram]` → `platforms & editions` (Steam/PlayStation/Epic icons; Xbox/Nintendo in text) → `[press/faq]` → `footer.closing`.
- **Product & Tech Hardware (`product` / `tech`):** `"nav-cards|nav-split|nav-mega" "footer-columns|footer-dark" "close-photo|close-type|close-word" "dark-band|brand-band" "arrow|solid|block|pill" "wordmark|initial|arc|ring|stack|dots"`
  - *Seven product rules:* (1) Product fills `80–100%` of its frame or stands transparent at anchor scale (`≥8` cols) — never mid-size in a grey panel; (2) Whole product appears in **at most 3 sections** (hero + 2); remaining sections show **use** (setting `≥50%` of frame), **parts close-up**, **people**, or **specs** — never the same view/angle twice; (3) Every headline promise is visibly pictured; (4) Deal distinct section compositions (`bleed`, `pair`, `trio`, `strip`, `tall-small`, plus at most one `split`) with one contrasting `dark-band` or `brand-band`; (5) Colour swatches (`data-product-swatch`) swap the product image, and every offered colour appears on the page; (6) Zero repeated facts between stat strips and spec rows; (7) Without client photos, use licensed stand-in photos of the **exact same product category** (`photos.mjs search`, zero readable rival logos, listed in report) — use `product-render` **only** when the brief asks for 3D.
- **Service (`service`):** `"nav-mega|nav-split|nav-centre" "footer-visit|footer-dark|footer-columns" "close-type|close-photo" "surface-pairs|dark-band|space" "solid|tonal|block|arrow" "wordmark|initial|arc|ring|stack|dots"`
  - *Spine:* `nav` → `hero` → `services-list` (or `peek-list` when every row has its own photo) → `work` (`3–6` project frames) → `steps` → `people-row` (only brief-named staff) → `[proof / pricing-two / faq]` → `booking-form` → `footer.closing`.
- **Place (`place`):** `"nav-split|nav-cards" "footer-visit|footer-columns" "surface-pairs|space|colour-band" "block|solid|arrow" "dots|arc|ring|petal|leaf|stack" "pair|strip|tall-small" "bleed|trio|strip|pair|wall|story" "address|name" "row|side"`
  - *Length by usable photo count* (`photos.mjs pick --draft-lead` + `photos.mjs search`): **Full** (`12–20` photos, `≤6` screens: `hero → visit → offer → place → orders/booking → footer.closing`); **Compact** (`8–12` photos, `4–5` screens); **Short** (`<8` photos, `3` screens `≤2700px` with `data-page-mode="short"`: `hero → combined offer+visit section → footer.closing`, plus `picture-develops` on its photo or a `1H` `word-highlight` statement if `0` photos).
  - *Place rules:* Screen 2 is **always** `section#visit[data-place="visit"]` (`6/6`: `--g-alt` panel with `dl.hours[data-tz]` + street/district map link left, shopfront photo or baked `fx-map` right). Deal **different** photo compositions for offer (`pair|strip|tall-small`) and place (`bleed|trio|strip|pair|wall|story`) + **one** display-type moment (`address` `clamp(48px,7vw,104px)` in `#visit` or `name` in `close-word`). Menu/price rows stay `≥16px` open text (`ul.rows`), square corners (`--r-lg: 0`), mandatory mobile `nav.actionbar`.
- **Client Slots (`client-slots`):** Named trailers, key art, in-engine captures, or CAD renders get finished-looking slots with `<!-- CLIENT FILE ... -->` comments and stand-in posters/frames (never dead `<video controls>` without a playable source, never empty boxes).

---

## 5. Grounds (`assets/backgrounds`) & Layout Check

- **Three base tokens (all kinds):** `--g-main` (`≥55–60%` of page height; light `L 0.80–0.97` on non-tech), `--g-alt` (same hue, `0.06–0.15` darker, `L ≥ 0.70`), `--g-dark` (`L ≤ 0.05`, max 1 body section mid/late page; dark main ground/hero is tech-only), plus `.ground-brand` (`product`/`place` once in second half, all text `≥7:1`). Non-tech pages stay **100% flat CSS colour** (zero gradients, grain, blur, or canvas).
- **Tech CSS grounds (`assets/backgrounds/pick.mjs`):** `16` zero-WebGL CSS grounds (`mist`, `halo`, `ruled`, `dots`, `arcs`, `liquid`, `grain`, `dusk`, `band`, `field`, `photo`, `horizon`, `deep`, `stage`, `paper`, `topglow`). Deal `≤2` per tech page; textured/moving ones (`grain`, `field`, `stage`, `deep`, `liquid`) count as the page's **one** effect.
- **Layout check (`assets/layout/check.mjs`):** Run across `1440x900,1024x768,820x1180,768x1024,390x844` (never `--no-stress`). Every finding (`hero-fold`, `hero-maxchars`, `hero-lines`, `screen-short`, `screen-height`, `sparse`, `neighbour`, `neighbour-ground`, `edge-left`, `edge-right`, `spill`, `bleed-one-side`, `one-sided`, `lines`, `overflow-x`) is a blocking FAIL.
