# Anti-Slop Gates, Copycraft & Page Blueprints

Shared baseline for **Track A (`commerce`)** and **Track B (`showcase`)**. Run the still-frame gates with motion disabled (`prefers-reduced-motion: reduce`) before tuning any spring, shader, or scroll trigger, and draft real copy before freezing layout geometry.

---

## 1. Anti-Slop Gates (Still Frame First, Motion Second)

### A. Still-Frame Gates (Motion Off)
1. **A1 · Default centred hero:** Full-bleed section + pill badge + centred H1 + centred one-line subhead + filled/outline two-button pair.
   - *Track A:* Deal from `assets/layout/deal.mjs` (`split`, `photo`, `product`, `editorial`, `collage`, `word`, `film`, `statement`, `triptych`, `centred`) or use the Place hero.
   - *Track B:* Make the mechanic itself the opening with type set into it, or use asymmetric splits (62/38), bottom-edge film framing, or oversized manifesto type.
2. **A2 · Three equal centred icon cards:** Render peer points with asymmetric spans, a promoted lead item (`bento`), an indexed typographic list, or real product UI fragments (`assets/ui`) rather than three identical icon-title-grey-blurb boxes.
3. **A3 · Identical section shapes:** Never repeat `centred headline + paragraph` down the page. Require **≥3 distinct section shapes** per page (varying column spans, full-bleed vs inset, text-beside-media vs media-band, ground switches).
4. **A4 · Violet/indigo gradients & rainbow cycling:** `#6366f1 → #a855f7`, purple-blue meshes, lavender glows, OKLCH hues in `275°–330°`, or multi-hue spectrum accents. Commit to a trade palette (`start.mjs` in Track A) or one visual archetype (`data/visual-bank.json` in Track B): 90%+ neutral ground/ink plus **one** deliberate accent.
5. **A5 · Decoration disguising structural emptiness:** Floating blobs, pervasive grid overlays, or indiscriminate noise added because the page feels bare. Fix structure instead: raise display type contrast and vary section shapes.
6. **A6 · Flat type scale (`16px–48px` band):** No hierarchy jump. Track B requires `display ÷ body ≥ 4×` (award-site median `≈8×`, e.g., `108–218px` display against `12–16px` body); Track A enforces `system.css` / `heroes.json` token jumps (`72–156px` hero display vs `16px` body).
7. **A7 · Hand-drawn fake browser/phone chrome:** Never draw traffic-light window bars or fake IDE shells around `<pre>`. Show live HTML product UI (`app-frame` / `assets/ui`) or real screenshots in clean `<figure>` frames.
8. **A8 · Invented proof:** Fabricated conversion percentages (`+47%`), fake user counts (`50,000+ teams`), placeholder logo walls, or made-up testimonials. Omit proof sections when the brief supplies none, or use plain brief facts.

### B. Motion Gates (Motion On)
1. **B1 · Undifferentiated card hover:** In Track B, uniform `translateY(-4px)` + drop shadow on every card is a template tell — give interactive targets specific semantic responses or cursor/state feedback. (In Track A, linked `.card` elements use the quiet `2px` lift from `assets/motion`, while unlinked cards carry `.m-nolift`.)
2. **B2 · Universal scroll fade-up:** Never fade/slide every block (`opacity 0→1, translateY(20px)`) on scroll. Keep most content present from paint 1; spend motion only on dealt moments (Track A) or intentional choreography beats (Track B).
3. **B3 · Single `0.3s ease` everywhere:** Define at least three duration/easing tiers or physical springs.
4. **B4 · Front-loaded hero budget:** Spending 100% of motion on screen 1 followed by 8 static screens. Schedule beats across scroll depth (`40–80%` peak, quiet breath around final CTA).
5. **B5 · Unmotivated background effects:** Particles on a law firm, shaders on a bakery, or fluid sims unrelated to the subject's physics.
6. **B6 · Rate-only parallax:** Relying solely on scroll-speed differences for depth instead of silhouette occlusion and ground contact.
7. **B7 · Decorative trailing dot cursor:** Never add a passive lerping circle cursor unless it carries state, magnifies, warps, or unmasks content. Always hide custom cursors on `@media (pointer: coarse)`.
8. **B8 · Broken `prefers-reduced-motion`:** Blank sections, unpinned scroll traps, or elements frozen at `opacity: 0`.

---

## 2. Page Blueprints & Section Vocabulary

Measured structural contrast across 32 production sites (`measure_structure.py`):
- **Creative dialect (Track B, n=18):** Median **4.5** sections (`>0.15vh`), bimodal page height (`≈1vh` single-screen instrument or `7–49vh` journey), **83%** full-bleed sections, **32%** ground switches.
- **Product/Commerce dialect (Track A, n=14):** Median **7** sections, **5** distinct section shapes, `~10vh` total height, **32%** full-bleed, mostly inset `.wrap` alignment.

### Section Spines by Archetype
- **Product / SaaS Landing:** `Hero` → `[Proof: real logos only]` → `Problem / App-Frame` → `Deep-Dive / Features ×2–3` (varied shapes: `2x2`, `bento`, `60/40 split`, `tabs-tour`) → `How-It-Works (3–5 steps)` → `[Testimonial]` → `Pricing` → `FAQ` → `CTA + Footer`.
- **Portfolio / Personal:** `Hero (often the mechanic + name + 1-line role)` → `Selected Work ×3–6 (real links, outcome stated)` → `About (1 narrow col, concrete facts)` → `Capabilities (typographic, no skill bars)` → `Direct Contact + 2-col Footer`.
- **Studio / Agency:** `Statement Hero` → `Work Index (≥40% of page height)` → `Services (ruled rows, not icon cards)` → `Approach` → `[Real Clients]` → `Contact + Footer`.
- **Campaign / Event / Launch:** `Act 1 Hook` → `Act 2 Demonstrated Idea` → `Act 3 Date/Place/Price/Action` → `Minimal Footer` (3–5 pinned beats, one money frame each).
- **Editorial Long-Form:** `Oversized Title + ≤30w Deck` → alternating `Passage (60–75ch)` and `2–4 Set-Pieces` → `Pull Quotes / Figures` → `Source Note + Footer`.
- **Index / Archive:** `Header + URL-synced Filter (?tag=...)` → `Scannable Row/Grid List with metadata` → `Designed Empty State` → `Pagination + Footer`.

### Ordering Rules
1. **Each section answers the question raised by the previous one:** What is this? → Does it work / show me? → Why trust it? → How does it work? → What does it cost / edge cases? → What do I do next?
2. **One primary transaction wording:** Repeat the exact primary CTA verb+object in nav, hero, closing CTA, and mobile bar — never scatter competing CTAs in every section.
3. **Information architecture:** Single offer + single decision = one page with meaningful `#anchor` IDs (`#work`, `#pricing`, with `scroll-margin-block`). Browsable work bodies or growing content = index + detail routes.

---

## 3. Copy Integrity, Fact Sheet & Five Hard Rules

### Five Copy Rules
1. **`<h1>` names the category + buyer or place** in 2–8 words (`Payroll app for restaurant teams`, `Bakery on Mill Street, Leith`, `Kelpmoor, a co-op sailing game`). Never a vague riddle, command, or slogan.
2. **First screen carries one hard fact:** A real price, count, place, hours line, or launch status.
3. **Every heading contains a concrete noun** naming the product, part, room, section subject, or brief figure. At most **one** figurative brand line per page, never in `<h1>`, paired immediately with a literal fact underneath. Heading grey run-ons must be two complete sentences (`<h2>Rooms and prices. <span class="muted">Breakfast included.</span></h2>`).
4. **Buttons are `verb + object` (1–5 words):** Start with `Book`, `Buy`, `Order`, `Pre-order`, `Reserve`, `Try`, `Start`, `Get`, `Download`, `Compare`, `See`, `Watch`, `Read`, `Find`, `Join`, `Subscribe`, `Contact`, `Request`. Ban `Learn more`, `Read more`, `Discover`, `Explore`, `Click here`.
5. **Tight word budgets:**
   - Hero sub-line: 15–30 words (Place: ≤80 chars with hours).
   - Paragraph measure: ≤62–68ch, ≤5 lines at `1440px`. Card body: 1–2 sentences (≤25 words).
   - Tech screens (`software`/`gaming`/`tech`): **60–80 words per screen** outside UI mocks and diagrams. Non-tech screens: ~34–47 words per screen; full page ≤900 words excluding footer.

### Honesty, Contacts & Credits Contract
- **What may be assumed when absent from brief:**
  1. A **coined brand name** — never a real company in that trade and never AI-cliché names (`Kestrel`, `Halcyon`, `Lumen`, `Nimbus`, `Fieldnote`, `Brightloop`, `Acme`, `Northwind`, `Apex`, `Zenith`, `Vertex`). Record search checks in `names.json` (`{"searched": false}` if offline).
  2. On **Track A `place` pages only**, plausible uneven local-currency prices (`3.60 €`, not `4.00 €`) and trade hours, each tagged `data-assumed` on its element (`data-assumed` hours never drive `[data-open-now]`). Products/services without prices write `Price on request` or omit prices.
  3. On **Track B drafts** with zero user facts, draft real-length copy and mark every placeholder factual slot `[…]`, listing every slot in the completion report.
- **Zero sample/residue text:** Never ship `lorem ipsum`, `[Company Name]`, `{{token}}`, `(sample)`, `illustrative`, markdown `**`/`##`, or `href="#"`.
- **Privacy-safe contacts (unless explicitly supplied by brief):**
  - **Addresses:** Street + district only (`Elmgatan, Malmö-Möllevången`), or district alone if no street is given. Never invent house numbers, postcodes, or GPS coordinates.
  - **Map links:** Open `https://www.openstreetmap.org/search?query=<street>+<district>` (`Get directions` with street; `See the area` with district only; omit map link if town only). Never embed map iframes.
  - **Phones & IDs:** Omit phone numbers/`tel:` links unless supplied. Never invent VAT, tax, or company register numbers.
  - **Forms & Email:** Post to `data-endpoint` when given; otherwise `action="mailto:hello@brand.example"` as a stand-in reported to the user, never printed as visible `.example` text on the page.
- **Visual captions & credits:** Track A forbids captions/apologies under any image, render, or diagram; place all photo/map/trademark attributions into **one** footer legal line (`Photographs via Unsplash and Wikimedia Commons` via `photos.mjs credits --out . --write`, ≤110 chars). Track B editorial pages may use `<figcaption>` only when it carries genuine editorial content.

### CJK vs Latin Copy & Typography Rhythm
- Write idiomatic Chinese clauses (display lines `6–12` characters, never translated English syntax or comma-spliced calques). Use full-width punctuation with zero space before `，`/`。`, and keep a non-breaking space before Latin units (`4.5 ms`).
- **Invert Latin display tracking/leading on CJK:** Latin display tightens (`line-height: 0.95–1.05`, `letter-spacing: -0.03em to -0.04em`); CJK display needs **zero or slightly positive tracking** (negative tracking closes counters on 黑体) and **looser leading (`1.4–1.6`)**. Declare the Latin typeface first in mixed `font-family` stacks so numerals and English words match optical weight.

---

## 4. Voice Registers & Per-Page Device Budget

Avoid the **default LLM house voice** (warm, wry, modest, ending every paragraph on a deadpan twist, calling itself *honest / calm / quiet / thoughtful / intentional*). Record a Voice Card in your plan by selecting one register fitted to the trade:

| # | Register | Core Move | Best Fit |
|---|---|---|---|
| 1 | **Facts only** | Declarative names, dates, counts, third/terse-first person | Law, finance, B2B infra, consultancies |
| 2 | **Technical & dry** | Metric + verb-led mechanism steps + real CLI/UI strings | Devtools, APIs, databases, AI infra |
| 3 | **Founder's letter** | First person, named workflow enemy, customer's own pain words | Opinionated SaaS, challenger tools |
| 4 | **Self-aware playful** | Straight face on small product + literal spec right underneath | Drinks, snacks, indie studios, consumer apps |
| 5 | **Literary & formal** | Exact material/botanical nouns, zero exclamation marks | Skincare, fragrance, industrial design |
| 6 | **Proper nouns & restraint** | Geography, architecture, dates; never writes "luxury" | Heritage hotels, architecture, galleries |
| 7 | **Sensory 2nd-person** | Present-tense physical facts (oven hour, weight, room light) | Cafes, bakeries, spas, yoga, dining |
| 8 | **Historical scene** | Opens on a real dated event from the brief | Family trades, established venues |
| 9 | **Plain-spoken activist** | Measurable mission + honest admission of limits/impact | Circular/repair brands, non-profits |
| 10 | **Refusal & narrowness** | Positioned by what it refuses to do (spends the negation budget) | Specialists, repair benches, single-product makers |
| 11 | **Product as hero** | Product is sentence subject; zero "we"; spec follows every claim | Hardware, bikes, lamps, focused apps |
| 12 | **Hurried conversational** | Talks to one busy buyer, parenthetical asides, plain availability | Freelancers, small creative studios, portfolios |

*Tone shift rule:* Hero, story, and microcopy (404, empty state, form hints) carry the voice; **pricing, booking, and FAQ always drop to plain, literal facts**.

### Rhetorical Device Budget & `copy-lint.mjs` Tells
Run `node <skill>/scripts/copy-lint.mjs index.html --kind <kind>` (<1s, zero browser). Over budget = `WARN`; `≥ 2 × budget + 1` = blocking `FAIL`:

| Device / Tell | Cap | `copy-lint` ID & Rule |
|---|---|---|
| Slop adjectives (`seamless`, `elevate`, `unlock`, `delve`, `bespoke`, `cutting-edge`, `robust`, `powerful`, `supercharge`, `reimagine`, `tapestry`, `realm`) | **0** | `copy-slop-word` (FAIL unless literal trade term like *seamless knit* / *climbing harness*) |
| Stock phrases (`In today's fast-paced world`, `Say goodbye to`, `Trusted by teams worldwide`, `It's not just X, it's Y`, `at your fingertips`) | **0** | `copy-stock-phrase` (FAIL) |
| Template/chat residue (`Certainly!`, `[NEED]`, `{{var}}`, `lorem ipsum`, raw markdown) | **0** | `copy-residue` (FAIL) |
| Self-applied virtue words (`honest`, `calm`, `quiet`, `actually`, `simply`, `genuinely`, `thoughtful`, `intentional`) | **0** | `copy-virtue` (show via an admission or fact instead) |
| Default AI cast names (`Priya`, `Okafor`, `Fieldnote`, `Kestrel`, `Halcyon`, `Lumen`, `Nimbus`, `Brightloop`) | **0** | `copy-cast`, `copy-cast-company` |
| Two-fragment headings (`Twelve rooms. Three ways to stay.`) | **1** | `copy-two-fragment` |
| Number-pair headings (`Four X, one Y`) | **0–1** | `copy-number-pair` |
| Negation runs (`No X. No Y.`) | **1** | `copy-negation` (only verifiable buyer refusals) |
| Contrast frames (`X, not Y`, `rather than`, `instead of`, `without the`) | **2 total** | `copy-contrast` (state the positive fact directly) |
| Footer poetic sign-offs (`Made with care in...`) | **0** | `copy-footer-signoff` (footer holds legal/contact facts only) |
| Eyebrow labels above `<h2>` | **1–2** | `copy-eyebrows` (a clear noun heading needs no eyebrow) |
| Participial riders (`, ensuring...`), colon/question reveals (`The result?`), em-dash spam | **Avoid** | `copy-ing-rider`, `copy-reveal`, `copy-em-dash` |

**Rival-name test & over-correction check:** Swap a competitor's name into `<h1>` and every `<h2>` — if a line still reads true, rewrite it from concrete facts. After editing, check that banning em dashes or `"not X but Y"` did not breed comma splices, `"rather than"` spam, or choppy two-word fragments in every paragraph.
