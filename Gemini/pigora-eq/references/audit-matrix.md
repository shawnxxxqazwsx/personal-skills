# Post-Deployment EQ Audit Matrix & Defect Patterns

## 1. Units & Control Sampling

Count each `module × band × filter_type × native_mode` independently (Bell,
Low Shelf, High Shelf, HPF, LPF; Constant/Prop Q; discrete dB/oct slopes).

| Axis | Audit Sample Set |
|---|---|
| **Gain** | `0 dB`, `±3 dB`, `±6 dB`, and exact native max boost / max cut |
| **Continuous Frequency** | Native shaft `0, 0.25, 0.5, 0.75, 1.0` (report actual Hz) |
| **Discrete Frequency / Q / Slope** | Every legal native detent |
| **Continuous Q / Slope** | Native shaft `0, 0.25, 0.5, 0.75, 1.0` |
| **Tracks** | 9–17 equally spaced positions per continuous axis + interpolation-knot neighbors |

Use pairwise planes (`Gain × Q` at `F_mid`, `Freq × Q` at `G_max`, `Gain × Freq`
at `Q_mid`) plus the 8 extreme corners rather than an exploding 3D Cartesian
cube.

## 2. Verification Layers

1. **Static magnitude:** compare measured audio against frozen `target.csv` per
   [training-contract.md](training-contract.md).
2. **Smoothness (`>= 48–96 points/octave`):** apply the formulas and limits in
   [smoothness-and-probes.md](smoothness-and-probes.md).
3. **Dynamic automation (`48 kHz`):** `2 s` slow and `100 ms` fast sweeps across
   zero and authored knots at block sizes `64` and `512` — zero nonfinite
   samples, zero unbounded transients/clicks, accurate final settled state.
4. **Routing & state:** neutral/bypass comparison, Stereo L/R & M/S isolation,
   and preset/state save-restore round-trip.
5. **Realtime envelope (when in scope):** verify the 4 rate/channel/buffer
   corners in [training-contract §5](training-contract.md#5-realtime-support-matrix)
   with zero audio-thread allocations/locks.

## 3. Recurring Hardware-EQ Defect Patterns

Use one representative probe per failure mechanism and expand only where
recorded dependencies warrant it; never copy historic thresholds into a new
acceptance contract.

| Defect pattern | Required audit check |
|---|---|
| **Prop-Q shoulders/folds at high Q** *(e.g. LF Prop Q detents)* | Inspect slope/curvature across every implicated detent even when magnitude stays bounded and monotone |
| **Narrow inter-anchor pole spikes** *(MID/HF/LF siblings)* | Probe pole neighborhoods and actual audio at localized extrema; dense gain grids cannot hide sparse frequency sampling |
| **Extreme cut tail staircase** *(negative extremes)* | Check max-cut exterior slope separately from boost; do not chase raster texture as a product feature |
| **Ineffective Q mode or bumpy gain travel** | Verify non-neutral switch separation, gain-dependent Q tracks, and intermediate responses |
| **HF Shelf plateau/inflection seams** *(e.g. 11–24 kHz)* | Test shelf plateau/transition, frequency tracks, and HF mapping seams independently; never inherit Bell acceptance |
| **Shared rack near-Nyquist roll-off/phase** | Compare empty/neutral/bypass complex response across each shared rack processing route |
| **Single-node fit vs cell-interior / runtime gap** | Probe continuous cell interiors and collect separate realtime/installed evidence; fitting progress is not deployment acceptance |

## 4. Required Audit Outputs

- `audit-receipt.json`: binary SHA-256, state counts, per-rate worst & RMS
  errors, smoothness metrics, dynamic/routing status, and exact reproducer for
  any failure.
- Visualization PNGs (`>= 1600 px` wide, plotted directly from measured audio):
  `overview.png` (unit × rate/layer summary), per-unit 48 kHz curve slices &
  control-track heatmaps/overlays, and magnified detail plots for any failure.
