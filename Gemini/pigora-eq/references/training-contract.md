# Pigora EQ Training Contract

Single source of truth for target construction, magnitude/rate/smoothness/realtime
acceptance gates, and the `fit-receipt.json` schema. Root `AGENTS.md` in the
Pigora EQ repository remains authoritative.

## 1. Evidence & Claim Tiers

- **Never claim unqualified "100% hardware fit".** Every fit covers magnitude
  response over a finite declared grid; phase, THD, impedance loading, and unit
  tolerances remain `not publicly specified` unless separately measured.
- **Target provenances:**
  - `measured` / `image-digitized` -> supports `public-source fit`.
  - `inference-derived` (proportional gain scaling, log-frequency shift, or
    inferred midpoint/flat baseline) -> supports `product-selectable —
    inference-derived` without upgrading `public_fit_state`.
- **Public-fit states:** `public-fit passed`, `public-fit partial`,
  `public-fit failed/withheld`, `not publicly specified`.

## 2. Target Extraction & Sparse Completion

1. **Freeze before fitting:** finish digitization and sparse completion before
   optimization, and record the SHA-256 of `target.csv`.
2. **Plot digitization:** prefer vector paths or numeric tables; for raster
   plots calibrate `>= 3` tick anchors per axis (log-Hz, linear-dB), preserve
   real resonant peaks/steep cutoffs without smoothing away extrema, and record
   calibration residual plus trace uncertainty (`<= 0.50 dB`; `<= 0.20 dB` for
   primary public tier).
3. **Deterministic sparse completion (standing authorization):**
   - **Baseline:** (1) measured bypass/0-setting trace; else (2) pointwise
     midpoint `0.5 * (boost_db + cut_db)` of symmetric `+G/-G` traces; else (3)
     declared `0 dB` flat baseline.
   - **Gain scaling:** `target_delta_db(f) = donor_delta_db(f) * |req_gain_db| / |donor_gain_db|`
     for `0 <= |req_gain_db| <= |donor_gain_db|`, keeping boost/cut separate and
     neutral at `0 dB`.
   - **Frequency transfer:** shift donor curve across documented native panel
     positions by log-frequency ratio `f_recipient / f_donor`.

## 3. Magnitude Residual & Sample-Rate Gates

Evaluate on actual compiled C++ processor output (never Python helper formulas):

- **44.1 & 48 kHz primary:** `max |predicted_db - target_db| <= 0.20 dB` across
  all in-band rows (reference `RMS <= 0.08 dB`).
- **Pragmatic `fallback-0.5`:** if digitization resolution or realtime filter
  order prevents `0.20 dB` after **>= 2 bounded correction attempts**, record
  the `0.20 dB` worst row and technical residual-floor diagnosis in
  `fit-receipt.json`, then judge `max |error| <= 0.50 dB` (ref `RMS <= 0.15 dB`).
- **88.2 & 96 kHz (`sample-rate-engineering-0.5`):** once 48 kHz passes, verify
  the frozen target over `f < Nyquist` at `max |error| <= 0.50 dB` (ref
  `RMS <= 0.15 dB`). `176.4 / 192 kHz` are optional extension checks.

## 4. Production Audio, Extrema & Smoothness Gate

Mandatory at **both** `0.20 dB` and `0.50 dB` tiers via compiled C++ audio
(see [smoothness-and-probes.md](smoothness-and-probes.md) for probe matrices and
formulas):

- **Compact extrema:** per Bell / Low Shelf / High Shelf / HPF / LPF unit, cover
  max boost & max cut × `{low, mid, high}` freq × `{min, mid, max}` Q/Slope,
  neutral (`0 dB`/`Off`) + adjacent active step, and one 9-point single-axis
  track per continuous axis including interpolation-knot neighbors.
- **Smoothness:** `0` NaN/Inf/unstable states; unintended extra peak/dip/shoulder
  prominence `<= 0.15 dB`; local 3-point chord departure and knot seam jump
  `<= 0.20 dB` (legitimate source resonance and discrete switches preserved).

## 5. Realtime Support Matrix

Test 1 complete active native EQ module per instance (all concurrent bands
active, steady state + control transitions, zero audio-thread allocations/locks):

- **44.1 kHz:** 64 ch @ 128 samples (`<= 2.902 ms`)
- **48.0 kHz:** 64 ch @ 128 samples (`<= 2.667 ms`)
- **88.2 kHz:** 32 ch @ 256 samples (`<= 2.902 ms`)
- **96.0 kHz:** 32 ch @ 256 samples (`<= 2.667 ms`)

## 6. Minimal Deliverable Schema (`fit-receipt.json`)

Store `target.csv`, `evaluation.csv`, and `fit-receipt.json` under
`tests/fixtures/hardware_eq/<eq_slug>/` (historical receipts remain valid
without retroactive schema migration):

```json
{
  "schema": "pigora-eq-fit-receipt-v2",
  "module_type": "exampleEq",
  "model_name": "Brand Model",
  "product_display_name": "Pigment Display Name",
  "product_short_name": "SHORT BADGE",
  "claim_tier": "public-source fit | inference-derived/source-informed approximation",
  "public_fit_state": "public-fit passed | partial | failed/withheld | not publicly specified",
  "in_scope_units": ["LF Shelf", "LMF Bell", "HMF Bell", "HF Shelf", "HPF"],
  "withheld_or_excluded": [],
  "not_publicly_specified": ["phase", "thd", "impedance_loading", "unit_tolerance"],
  "target_csv_sha256": "<sha256>",
  "rates": {
    "44100": {"gate": "primary-0.2", "max_abs_error_db": 0.14, "rms_db": 0.04, "status": "PASS"},
    "48000": {"gate": "primary-0.2", "max_abs_error_db": 0.13, "rms_db": 0.04, "status": "PASS"},
    "88200": {"gate": "sample-rate-engineering-0.5", "max_abs_error_db": 0.28, "rms_db": 0.07, "status": "PASS"},
    "96000": {"gate": "sample-rate-engineering-0.5", "max_abs_error_db": 0.31, "rms_db": 0.08, "status": "PASS"}
  },
  "compact_extrema_status": "PASS",
  "smoothness": {"max_extra_prominence_db": 0.03, "max_knot_or_chord_jump_db": 0.06, "status": "PASS"},
  "realtime_matrix": {
    "44100_64ch_128": {"p99_ms": 0.85, "max_ms": 1.12, "deadline_ms": 2.902, "allocs": 0, "status": "PASS"},
    "48000_64ch_128": {"p99_ms": 0.84, "max_ms": 1.10, "deadline_ms": 2.667, "allocs": 0, "status": "PASS"},
    "88200_32ch_256": {"p99_ms": 0.91, "max_ms": 1.18, "deadline_ms": 2.902, "allocs": 0, "status": "PASS"},
    "96000_32ch_256": {"p99_ms": 0.90, "max_ms": 1.16, "deadline_ms": 2.667, "allocs": 0, "status": "PASS"}
  }
}
```
