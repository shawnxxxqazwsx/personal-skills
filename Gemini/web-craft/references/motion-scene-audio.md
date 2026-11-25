# Track B (`showcase`) — Real-Time WebAudio Scene Mixing & Oracles

Mixing music beds, environmental ambience, and visitor-triggered interaction SFX for interactive web scenes without muddying the low-mid band or mistaking hand feedback for background noise.

---

## 1. Three Separate Buses (`bgm` / `hand` / `world`)

Never hang ambience and visitor interactions off a single master fader — lowering wind will bury the visitor's own touch feedback. Route every WebAudio source into one of three GainNode buses:

| Bus | Carries | Control Law |
|---|---|---|
| `bgm` | Musical score / bed (cut losslessly via `ffmpeg -c copy -map_metadata -1`, trimmed against whole-piece LUFS/LRA, all fades in `GainNode`) | Per-act gain curve (§2) × hand-triggered ducking (§3) |
| `hand` | Every sound **caused by the visitor's input** (even if spatially distant and wet with reverb) | Single group trim; re-trim sustained low-frequency layers individually whenever raising the bus so impulses get clearer without turning drones into a hum |
| `world` | Autonomous environment (wind, sand, birds, falling glyphs) | Per-act ambience curve; streamed in/out via `volumeIn * volumeOut` audibility lifecycle (`30 Hz` gain updates) |

---

## 2. Inverse Per-Act Curves & Single-Variable Iteration

Thick music beds (strings/pads) and environmental wind share the exact same `200–900 Hz` band. Make their per-act curves **inverse**:
- **Interactive / spatial acts:** Raise `world` (`1.00`), pull `bgm` underneath (`0.46`, `~ -36 LUFS`) so hand sounds have headroom.
- **Narrative / passive acts:** Drop `world` (`0.16`), hand the emotional arc to `bgm` (`0.86`, `~ -31 LUFS`).
- **Tuning discipline:** Balance is the *ratio* between buses. **Move only one bus per iteration and print per-act integrated LUFS** — raising `bgm` `+9 dB` while cutting `world` `-6 dB` in one edit swings relative balance by `15 dB` and destroys attribution.

---

## 3. Asymmetric Hand Ducking (`Fast Down, Slow Up`)

In acts where `bgm` peaks (`~ -30 LUFS`), delicate interaction sounds (`-35 dB` glyph brush) get masked unless the score steps aside **exclusively on `hand` events** (never trigger ducking from `world` ambience, which causes audible pumping):

```js
// Target gain multiplier on bgm duck node: 1.0 at rest, 0.45 (~ -7 dB) while hand acts
const target = handActive ? 0.45 : 1.0;
const tau = handActive ? 0.05 : 0.70; // 50ms grab, 700ms invisible release
duckGain += (target - duckGain) * (1 - Math.exp(-dt / tau));
```

---

## 4. Discrete World Events Over Louder Noise Beds

A continuous low-passed noise bed has **no gain setting between "inaudible floor" and "annoying hiss"** because human hearing tracks *change*, not steady-state RMS. Keep the continuous bed quiet and hook **discrete Poisson/state-edge micro-events** to visual events already happening in the scene:
- Sand ticks driven by gust squared (`rate = (0.12 + gust * gust * 1.7) * 26` grains/sec — `4.6/s` in calm air, `20+/s` in gusts; check **event density** separately from peak dB!).
- Rising-edge triggers on visual flips, startled creatures, or per-column/per-glyph step increments.
- *Measured effect:* Overall RMS rises `+0.1 dB` (no louder) while zero-crossing rate rises `+156 Hz` (crisper, unmistakably alive).

---

## 5. Hand-Sound Causality, Filter-Q Loss & Mandatory REST Oracle

### 5.1 Feed Frame Deltas, Never Persistent Visual State
Feeding a slow-drying visual field (`wetDensity`) into an interaction synth keeps the sound running after the pointer stops — the ear immediately reclassifies it as background hiss.
1. **Drive hand sounds with per-frame pointer travel `hypot(dx, dy)`** accumulated into fast-decaying momentum (`energy *= 0.62` per frame for paper wash, `0.72` for scrub).
2. **Shape with band-pass, not wide low-pass, and separate neighbouring timbres:** A `900 Hz` low-pass sounds like broadband static; an `820 Hz` band-pass (`Q = 0.8`) reads as tactile paper scuff, distinct from an adjacent act's crisp `1150–2000 Hz` erase scrape.
3. **Mandatory REST Oracle (assert on every hand sound):**
   - Drive hand input for `0.60s`, stop pointer completely at `T0 + 0.60s`, and measure RMS in `[T0 + 0.85s, T0 + 1.10s]`.
   - **Pass condition:** Level must drop **`≥ 15 dB`** within `0.25s` of stopping (if fast decay lowers active RMS too much, raise the layer's input gain — never lengthen the decay).

### 5.2 Inspect Filter `Q` Before Copying Gains & Subtract Deterministically
- **Narrower `Q` eats `10–20 dB`:** Copying `gain = 0.05` from a `Q = 1.1` impulse onto a `Q = 2.4` band-pass (`46%` bandwidth) drops output by `~7 dB` into silence. Always inspect the filter chain before choosing gain.
- **Sample-by-sample offline subtraction:** Aggregate RMS hides quiet layers inside a `14 dB` crest-factor wind bed. Render `OfflineAudioContext` twice with one layer muted (`__noSand = true`), using a **per-event golden-ratio deterministic phaser** (`start[i] = (start[i] + 0.618034 * 4) % 4` — never `Math.random()`) so all other layers stay bit-identical, then subtract sample-by-sample and print layer `RMS`, `peak`, `ZCR`, and `events/s`.
