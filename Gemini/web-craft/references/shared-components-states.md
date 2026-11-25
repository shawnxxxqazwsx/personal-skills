# Component Dialects, State Matrix, UI Fragments, Diagrams & Icons

Shared component reference covering both **Track B (`showcase`)** and **Track A (`commerce`)**, plus the Track A production kits (`assets/ui`, `assets/diagrams`, `scripts/icons.mjs`).

---

## 1. Two Measurable Component Dialects (32-Site Baseline)

Measured at `1440×900` and `390×844` across 18 award-winning creative sites and 14 top product-marketing sites:

| Property | Creative Dialect (Track B default) | Product / Commerce Dialect (Track A default) |
|---|---|---|
| Distinct `border-radius` values | **Median 1** (most common button: `0px`) | **Median 8** (`4px / 6px / 8px / 12px / 20px`) |
| Elements with `box-shadow` | **Median 0** | **Median 17.5** (inside panels/overlays) |
| Uppercase button labels | **37%** (always with `+0.08em` tracking) | **1%** (sentence case everywhere) |
| Nav CTA buttons / links | **Median 0 CTAs**, ~5 links, `fixed` (often `mix-blend-mode: difference`) | **1 primary CTA** (+ optional `Sign in`), 4–6 links, `fixed` opaque bar |
| Footer scale | **2 columns, ~4 links** | **4–5 columns, ~20–35 links** + legal row |

- **Shared invariants across both dialects:** Nav height `≈64–72px` (`56–64px` mobile), left-aligned section headings (`76%` vs `21%` centred), base-4 spacing grid, exactly one `<h1>`, zero horizontal overflow at `390px`.
- **Per-surface rule:** Building a creative showcase out of rounded shadowed cards, a violet pill CTA, and a 5-column sitemap footer instantly reads as AI-generated. Conversely, a control widget *inside* a creative instrument (`cases/string-clock`) may use product controls (segmented radios, sliders, pills) as long as the surrounding canvas stays purely creative.

---

## 2. Mandatory 9-State Interactive Matrix & Native HTML Primitives

An interactive component without its off-happy-path states reads as a prototype:

| State | Requirement |
|---|---|
| `rest` | Clean baseline aligned to semantic tokens |
| `:hover` | Wrapped in `@media (hover: hover) and (pointer: fine)` so touch screens never stick; nothing essential hidden behind hover |
| `:active` | Immediate tactile press (`≤90ms`, e.g. `scale(0.985)` or `1px` step) |
| `:focus-visible` | Immediate `2px` high-contrast ring (`≥3:1` on ground; never `outline: none` without an equal replacement; never `:focus`) |
| `disabled` | `disabled` attribute + `opacity: .45; cursor: not-allowed` + nearby explanation |
| `loading` | Lock button width (`visibility: hidden` on label + overlay indicator) so row never reflows; block double-submit |
| `error` | Validate on submit/blur (never per keystroke on empty input); `aria-invalid="true"` + adjacent `aria-describedby` fix text (never colour alone) |
| `empty` | Named filter/search state with a one-click reset action |
| `success` | Persistent inline receipt (only after a real endpoint response — never fake success on a `mailto:` stand-in) |

### Modern Semantic Primitives (Replace Div Soup)
- **Buttons vs Links:** `<a href="...">` navigates; `<button type="button|submit">` acts. Never `<a href="#">`. Keep hit box `≥44×44px` even when the painted label is smaller. Stretch whole-card links via `.card { position: relative } .card a::after { content: ""; position: absolute; inset: 0 }` so text remains selectable and middle-click works.
- **Forms:** Every input has a visible `<label for>` above it (`16px` input font on mobile to prevent iOS auto-zoom), accurate `type` + `inputmode` + `autocomplete`, and `field-sizing: content; max-height: 12lh` on `<textarea>`.
- **Dialogs & Popovers:** Use `<dialog>` + `showModal()` with `@starting-style` entry transitions (`Esc`, focus trap, and `::backdrop` come free; restore focus on close). Use `popover` + `@supports (anchor-name: --a)` for menus.
- **Accordions / FAQs:** Track B uses `<details name="faq"><summary>` + `details::details-content { transition: block-size 260ms, content-visibility 260ms allow-discrete }` (`Ctrl+F` works with zero JS). **Track A (`commerce`) keeps all FAQ answers open in `.faq` with no accordion.**

---

## 3. Track A Feature Cards & Live UI Fragments (`assets/ui`)

Track A software and hardware pages look like `figma.com` and `x.ai` because cards hold **lit pictorial panels** carrying **live HTML product UI** cut at the panel edge — never generic icon boxes and never three nested borders (`card > panel > fragment`, two boxes deep at most: use `.card--open` on light pages or `.panel--flush` on dark pages).

### Card & Panel Geometry (`assets/ui/cards.css`, `assets/ui/ui.js`)
- **Card text:** Title `20px/18px` weight `500` (1 line); body `16px/24px` in `--c-text` (84% ink, **never** `14–15px` muted grey), `≤2` lines (`≤46ch`); `32px` gap to `.panel` (`--p-h: 264–340px` desktop, e.g. `180px` stacked on phone).
- **Subject fidelity:** Fragments pasted from `assets/ui/<name>/fragment.html` must be rewritten completely to the client's domain, names, metrics, and tool icons (never leave sample copy or `data-ui-load`). Show the **whole product once** across `.wrap` in `app-frame` (`window` list pane beside open item pane); gaming pages use **zero** `assets/ui` fragments (show game captures/world instead).
- **Minimum fragment widths & placements (`.stage` inside `.panel`):**
  - Width floors: `chat` 140, `checklist` 160, `slider` 215, `toggles` 230, `search` 240, `terminal-run` 280, `calendar` 280, `diff-review` 280, `pipeline-board` 280, `stat` 285, `cursor` 290, `files` 300, `notify` 340, `code` 365, `doc` 400, `window` 456.
  - Placements (vary `≥3` across a `2x2` group): `.at-corner` (`28–40px` top-left, cut right+bottom), `.at-rise` (`24–56px` down, cut bottom), `.at-right`, `.at-over` (small `cursor`/`notify` overlapping a window's lower-right, hidden `<1024px`), `.at-center` (compact slider only), `.fit` (`--fit-max`), `.wide` (`--w`), `.to-edge`.
  - Developer-tool rules: `diff-review` keeps reviewed line + comment + `Apply` in top `250px` and cuts bottom via `.stage--fade-b` (never cut right); `terminal-run` and `pipeline-board` sit whole with `≥24px` ground below and no fade.
- **Edges & fades:** Every panel edge either leaves `≥24px` clear ground (`16px` phone) or cuts the fragment by `≥24px` under `.stage--fade-b` / `--fade-r` / `--fade-br` (`--fade-h: 64px`) — never leave a `1–23px` sliver and never fade over the focal row/action.
- **Panel grounds & GPU budget:** At most **one** card group per tech page gets still shader grounds (`ui.grounds(document, fx)` bakes each once at `≤2x` DPR and frees the WebGL context). Use soft fields only (`painterly-landscape`, `grain-gradient`, `gradient-mesh`, `silk-folds` — never grid/contour/halftone patterns behind UI) with lit palettes (`sand`, `sky`, `sage`, or level-mist `painting`) so dark pages never stack four near-black layers.
- **Card loops:** Mark **one** fragment per card group `data-ui-loop` (`3.2s` cycle, seeded on its finished state, `ui.js` mounts a `32px` `.loop-pause` disc beside the card title); sibling fragments hold still (`data-ui-still`) and replay on hover/focus. Never two loops on screen below the hero.

---

## 4. Node-and-Line Diagrams (`assets/diagrams`)

Use `assets/diagrams/diagram.js` (`27` presets in `presets.json`) when the point is **topology or flow** (integrations, fan-in, parallel lanes, sync), never to mock a UI screen:
- **Budgets by kind:** Tech/software/gaming `0–2` per page (pulsing `2.5–4s` cycle, `≤1` per section); product/service `0–1` held still (`"ground": "none"`, `"motion": {"pulse": "none"}`); `place` **0**.
- **Layouts:** `hub`, `ring`, `tree`, `lanes`, `fanin`, `bowtie`, `sync`, `timeline`, `grid`, `free`. Cap at `≤8` spokes / `≤12` nodes per card, plain `1–3` word labels (no `"Orchestration Layer"` jargon), zero `<figcaption>` underneath.
- **Mount:** Link `assets/diagrams/diagram.css`, place `<div class="dg" data-diagram><script type="application/json">{...}</script></div>` with client labels/icons, load `assets/diagrams/mount.js`, then run `icons.mjs scan`.

---

## 5. Real Brand, File & UI Icons (`scripts/icons.mjs`)

Every named tool, platform, or file format shows its **real icon as a local SVG** — never a hand-drawn imitation, letter-in-circle, emoji, or runtime CDN call.

### Pinned Licensed Sources (932 Curated Entries)
- `logos` (`gilbarbara/logos`, CC0): ~1,500 full-colour brand marks — **always first choice**.
- `si` (`simple-icons`, CC0): Brand-hex painted marks only where no colour mark exists (Google Docs/Sheets/Slides, PlayStation, Epic Games, Steam, etc.). *Xbox, Nintendo, and Microsoft Office brand logos are in no permitted redistributable set: write console names in type, and use `file:docx`/`xlsx`/`pptx` for Office files.*
- `file` (`vscode-icons`, MIT): Colour file-type icons (`pdf`, `zip`, `markdown`, `docx`, `xlsx`).
- `ui` (`lucide`, ISC): Single-line interface glyphs (`arrow-right`, `check`, `search`) inheriting `currentColor`.

### CLI Workflow & Placement (`assets/icons/icon.css`)
```bash
node <skill>/scripts/icons.mjs find <query>
node <skill>/scripts/icons.mjs apps --tag dev|ai|gaming|cloud|payments
node <skill>/scripts/icons.mjs fetch slack google-docs file:pdf2 ui:arrow-right --out assets/icons --colour
node <skill>/scripts/icons.mjs scan index.html --out assets/icons --colour   # run last so 0 icons are missing
```
- **Third-party violet rule:** The violet ban applies to the **page's own palette**, never to a real third-party tool's mark (Stripe, Twitch, Datadog, Terraform, Figma). Always pass `--colour` when scanning/fetching tools the product integrates with; use `--mono` only for customer logo strips or footer social links.
- **Tiles & credits:** Link `assets/icons/icon.css` (`.ic-tile`, `.ic-row`, `.ic-chip`, `.ic-grid--mosaic`, `.ic-file`; auto-cropped classes `ic-wide`, `ic-land`, `ic-tall`). When showing brand marks, include `"Product names and logos are trademarks of their owners"` in the footer legal line alongside generated `icons-credits.json`.
