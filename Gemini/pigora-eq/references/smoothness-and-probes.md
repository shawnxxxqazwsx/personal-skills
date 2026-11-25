# Compiled Audio Probes & Quantitative Smoothness

Verify every fit on actual processed audio through the compiled C++ processor
(`mc_silk_tape_response_verify` or plugin binary) — never rely solely on Python
helper formulas or UI plot paths. Magnitude residual gates are defined in
[training-contract.md](training-contract.md).

## 1. Audio Capture & Acceptance Units

- Render impulses or stepped/swept sines across `44.1, 48, 88.2, 96 kHz`
  (`176.4 / 192 kHz` optional) with sufficient FFT/capture length to resolve
  low-frequency and narrow high-Q features.
- Count each supported `band × filter_type × native_mode` separately:
  - **Bell** (Constant Q and Proportional Q separately if switchable)
  - **Low Shelf** / **High Shelf** (separate units)
  - **HPF** / **LPF** (each discrete dB/oct slope covered)
- Skip excluded or `withheld` controls and list them in `fit-receipt.json`.

## 2. Compact Extrema & Single-Axis Control-Track Matrix

Run this probe set at **48 kHz** (record executed state count and worst metrics
directly in `fit-receipt.json`; no multi-hash preflight ceremony needed):

1. **Bell & Shelf extrema corners:** exact native **max boost** and **max cut**
   × `{low, mid, high}` native frequency × `{min, mid, max}` native Q or Slope
   (`<= 9` states per gain sign; deduplicate fixed/absent axes).
2. **HPF & LPF corners:** `{low, mid, high}` active cutoff × every discrete
   slope × `{min, mid, max}` adjustable Q/resonance (when present), plus `Off`
   vs adjacent active limit.
3. **Neutral & near-zero:** `0 dB` neutral (flat `0 dB` within numerical
   precision unless source specifies non-flat insertion) + nearest active
   positive/negative step at mid frequency/Q.
4. **Single-axis continuous tracks (9 equally spaced points + authored
   interpolation-knot neighbors):**
   - **Gain track:** full gain range at mid frequency & mid Q/Slope.
   - **Frequency track:** full frequency range at max boost (or max cut for
     cut-only bands) & narrowest Q.
   - **Q / Slope track:** full Q/Slope range at max boost & mid frequency (also
     max cut if boost and cut use distinct topologies or tables).
5. **Other required rates (`44.1, 88.2, 96 kHz`):** evaluate the full frozen
   target plus `{low, high}` frequency × `{min, max}` Q/Slope corners at max
   boost and max cut to confirm near-Nyquist stability and zero rate-mapping
   kinks.

## 3. Quantitative Smoothness Formulas

Mandatory at both `0.20 dB` and `0.50 dB` magnitude tiers on unsmoothed measured
magnitude `m_i` (dB):

### Frequency-direction metrics

Let `x_i = log2(f_i / 1 Hz)` for strictly increasing `f_i < Nyquist`, with
`h_L = x_i - x_(i-1)` and `h_R = x_(i+1) - x_i`:

```text
s_L = (m_i - m_(i-1)) / h_L                                # left slope (dB/octave)
s_R = (m_(i+1) - m_i) / h_R                                # right slope (dB/octave)
c_i = 2 * (s_R - s_L) / (h_L + h_R)                        # curvature (dB/octave^2)
d_i = m_i - (h_R * m_(i-1) + h_L * m_(i+1)) / (h_L + h_R)  # local chord departure (dB)
```

- **Finite & bounded:** all `m_i`, `s`, `c`, `d` finite (`0` NaN/Inf).
- **No unsupported lobes/kinks:** any extra peak, dip, or monotone fold not
  backed by source topology has prominence `<= 0.15 dB`.
- **Seam / chord continuity:** at dense probe spacing (`>= 24–48 points/octave`)
  and around runtime frequency joins, `|d_i| <= 0.20 dB` unless caused by a
  legitimate narrow source resonance peak.

### Continuous control-track metrics

Along each 9-point continuous track (Gain, Frequency, Q/Slope) plus
interpolation-knot neighbors, let `t_i` be the normalized or physical control
coordinate (`k_L = t_i - t_(i-1)`, `k_R = t_(i+1) - t_i`):

```text
d_ctrl(f) = m_i(f) - (k_R * m_(i-1)(f) + k_L * m_(i+1)(f)) / (k_L + k_R)
```

- Verify monotonic peak/cutoff progression in the intended knob direction and
  knot-neighbor seam jump `<= 0.20 dB` (preserving legitimate source asymmetry).
- Check discrete hardware switches (Bell/Shelf, discrete dB/oct slopes,
  Bypass/Off) per switch state rather than as continuous derivatives.

## 4. Pole-Aware Probing & Effective States (`scripts/curve_coverage.py`)

Use `scripts/curve_coverage.py` (standard-library Python) to place dense
pole-aware probes between sparse manual anchors, refine inter-anchor extrema via
bounded golden-section search, and verify neighboring controls do not collapse
to identical coefficients via `summarize_effective_states`:

```python
from curve_coverage import (
    PoleHint, build_frequency_probes, make_coverage_report, refine_local_extrema,
)

plan = build_frequency_probes(
    frozen_anchor_frequencies_hz, sample_rate_hz=48_000.0,
    subdivisions_per_interval=3,
    pole_hints=[PoleHint(center_hz=center, bandwidth_hz=bandwidth)],
)
refinement = refine_local_extrema(
    model_adapter.magnitude_db, plan.frequencies_hz,
    interval_hz=plan.bounds_hz, max_evaluations=512, frequency_tolerance_hz=1e-4,
)
report = make_coverage_report(plan, refinement=refinement)
```

Self-test:

```bash
python3 scripts/curve_coverage.py --self-test
python3 scripts/test_curve_coverage.py
```
