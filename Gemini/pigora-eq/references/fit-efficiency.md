# Efficient Fitting Without Weaker Evidence

Use these checkpoints for new model families, control laws, and DSP rewrites.
They speed up exploration without weakening the frozen evidence contract in
[training-contract.md](training-contract.md). Reuse compatible passing receipts
rather than restarting completed stages.

## 1. Preflight the Actual Optimizer Input

Before spending optimizer time, verify the loaded input matches the frozen
`target.csv` SHA-256 and check identity, controls, frequencies, values,
provenance, and row coverage. Reject missing, duplicate, extra, or mismatched
rows upfront — matching row counts alone does not confirm identical targets.

## 2. Run a Bounded Representative Pilot First

- Start on a representative subset covering each distinct topology, boost/cut
  family, neutral and gain extremes, frequency/control boundaries, interior
  control states (endpoints alone cannot identify control laws), and the
  near-Nyquist region. This subset is a fast falsifier, never reduced acceptance.
- Measure residual/Jacobian cost on the pilot; prefer vectorized evaluation,
  cached invariant terms, bounded stable parameterizations, and a small local
  solve or justified warm start. Set a finite evaluation/time budget from the
  pilot rather than an arbitrary universal duration.
- Escalate to multistart, differential evolution, or Powell only when pilot
  evidence points to local minima rather than target, capacity, conditioning, or
  control-law defects. After `>= 2` bounded correction attempts fail to reach
  `0.20 dB`, diagnose the residual floor or switch topology; if practical limits
  prevent `0.20 dB`, document the diagnosis and apply `fallback-0.5` per
  [training-contract.md](training-contract.md) without relaxing smoothness limits.

## 3. Validate the Control Law Before C++ Integration

- Once pilot capacity passes, evaluate the mathematical candidate over the full
  declared domain and continuous-control probes (intermediate gains, anchor
  crossings, neutral state, dense inter-anchor shape, intended knob direction)
  using `scripts/curve_coverage.py` ([smoothness-and-probes.md](smoothness-and-probes.md)).
- Separate target-to-control-law error from control-law-to-runtime error before
  touching C++ serialization or runtime wiring. If a shared model family shows a
  shape defect, run one cheap scan on sibling bands using that structure without
  auto-refitting passing unrelated bands. Mathematical checks remain diagnostic
  and never replace compiled C++ audio verification.

## 4. Screen Realtime Feasibility & Arithmetic Early

- Bind the rate/channel/buffer envelope from
  [training-contract §5](training-contract.md#5-realtime-support-matrix) during
  inventory before committing to a filter topology. Estimate filter order/taps,
  memory, latency, and operations for 1 complete active native EQ per instance;
  if feasibility is uncertain, run a bounded kernel benchmark before full fitting.
- Check serialized coefficients and actual runtime float precision early,
  including low-frequency conditioning and parameter transitions. Stable
  double-precision poles do not prove float runtime accuracy, and one passing
  rate bank does not validate rate transforms or newly visible high-rate bands.
