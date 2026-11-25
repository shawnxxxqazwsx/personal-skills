---
name: pigora-eq
description: >-
  Research, fit, validate, and audit Pigora hardware-EQ modules across target
  extraction/completion, filter/control-law fitting, compiled audio-response
  verification, quantitative smoothness, dynamic automation, realtime
  acceptance, and post-deployment module audits. Use for Pigora EQ fitting,
  validation, post-deployment verification, or targeted rechecks of
  user-reported curve defects. Do not use for GUI-only work, Chlora host
  development or UI styling, generic DAW operation, or spatial-audio format
  standards.
---

# Pigora EQ Fitting, Validation & Audit Skill

Governs **hardware-EQ public/inference fitting & validation** and
**post-deployment / compiled module auditing** for Pigora EQ models. Root
`AGENTS.md` in the Pigora EQ repository is authoritative.

## Part 1: Fitting & Validation (5-Step Workflow)

Run every EQ fit as a direct, reproducible loop without multi-file ledger
bureaucracy or multi-reviewer approval chains:

1. **Source Search & Scope Inventory** ([references/training-contract.md](references/training-contract.md))
   - Collect the highest-ranked public sources (numeric/vector plots -> raster
     manual plots -> documented independent measurements), using live web lookup
     when needed to verify manufacturer material.
   - Bind native front-panel controls (frequencies, gain range, Bell/Shelf/Cut
     modes, Q/Slope). Mark unverified controls `withheld` and unseen axes
     (phase, THD, loading) `not publicly specified`.
2. **Freeze Target Grid Before Optimization**
   - Extract vector curves or calibrate raster plots (`>= 3` tick anchors/axis;
     log-Hz, linear-dB) and complete sparse plots deterministically (baseline,
     proportional gain scaling, log-frequency shift per `training-contract.md`).
   - Freeze `target.csv` (`control_state, frequency_hz, target_db, provenance,
     uncertainty_db`) and record its SHA-256 before running the optimizer.
   - **Pre-Fit Visual Gate (Mandatory):** render and show the user a visual
     overlay of the extracted target curves on the manufacturer's original plots
     for human inspection **before** starting model optimization.
3. **Fit & Screen Architecture** ([references/fit-efficiency.md](references/fit-efficiency.md))
   - Screen filter order/topology against the **Realtime Performance** gate
     first, then fit a representative subset (extremes, neutral, mid-gain,
     near-Nyquist) before expanding to the full control grid.
   - After 2 failed bounded correction attempts under one hypothesis, diagnose
     the residual floor or switch filter topology rather than stacking patches.
   - Consult [references/airwindows-eq-dsp.md](references/airwindows-eq-dsp.md)
     only as candidate DSP math when relevant.
4. **Verify via Compiled Production Audio** ([references/smoothness-and-probes.md](references/smoothness-and-probes.md))
   - Measure actual processed audio through the compiled C++ processor (impulse
     or sine sweep — never Python helper formulas) across `44.1, 48, 88.2, 96 kHz`
     against **Core Acceptance Gates Summary** below.
5. **Verify Realtime Envelope & Write Single Receipt**
   - Benchmark all 4 rate/channel/buffer corners in **Core Acceptance Gates
     Summary** with zero callback allocations/locks, and emit `target.csv`,
     `evaluation.csv`, and `fit-receipt.json` under
     `tests/fixtures/hardware_eq/<eq_slug>/`.
   - **Post-Fit Visual Gate (Mandatory):** render and show the user a visual
     overlay of the final trained C++ production curves (plus error residuals)
     against the manufacturer's original curves for human verification.

## Part 2: Deployed / Compiled Module Audit Workflow

Use for post-fit/post-deployment verification, module audits, or targeted
rechecks of user-reported curve defects ([references/audit-matrix.md](references/audit-matrix.md)):

1. **Scope & Binary Binding**
   - Audit only the user-requested EQ module(s) — never silently expand to the
     full catalog. Bind the exact VST3 (`/Library/Audio/Plug-Ins/VST3/pigora draft.vst3`)
     or build-lane verifier (`mc_silk_tape_response_verify`), recording SHA-256,
     sample rates, channel layout, and block size.
2. **Static Audio Matrix & Smoothness (`48 kHz` full + `44.1 / 88.2 / 96 kHz` corners)**
   - Measure compiled processed audio across each supported unit (Bell, Low/High
     Shelf, HPF, LPF; Constant/Prop Q; discrete slopes) and judge residuals and
     smoothness against **Core Acceptance Gates Summary**.
3. **Dynamic Automation & State/Routing Probes**
   - Run slow (`2 s`) and fast (`100 ms`) parameter sweeps across zero/knots at
     `64` and `512` buffers for clicks, spikes, or dropped updates; verify
     neutral insertion (`0 dB`/`Off` vs bypass), Stereo vs M/S routing, and
     preset/state round-trip.
4. **Concise Report & Plots**
   - Emit `audit-receipt.json` and measured PNG plots (`overview.png` + per-unit
     overlays, `>= 1600 px` wide) and embed key plot paths in the summary.
   - Report `PASS` / `FAIL` / `PENDING` per layer (`target-fit`,
     `audio-smoothness`, `dynamic-automation`, `realtime-envelope`,
     `state-routing`). Do not modify DSP or loosen thresholds in audit-only runs.

## Precise Pigment / Colorimetric Naming Contract

Enforce strict dual-track naming separation across internal evidence and product UI:

- **Internal provenance (`eq_slug` & frozen fixtures):** `tests/fixtures/hardware_eq/<eq_slug>/` (`target.csv`, `evaluation.csv`, `fit-receipt.json`) retains the exact real-world manufacturer and model name so source audits and frozen SHA-256 hashes never change.
- **User-facing product surfaces (`moduleDisplayName`, `moduleDisplayShortName`, faceplates, `Alternatives`, active EQ rack & module search browser):** never display raw manufacturer brand names, sound-alike parody names (e.g. `DAX EQ`, `BUS XFORMER`), or vague generic color words (`Red`, `Blue`, `Black`, `Grey`). Register a unique artist-pigment or colorimetric proper name anchored to the unit's dominant palette upon release:
  - `dangerousBax` -> `Alizarin Crimson` / `ALIZARIN CRIMSON`
  - `rndMbtEq` -> `Indanthrene Blue` / `INDANTHRENE BLUE`
  - `rndShelfordEq` -> `Payne's Grey` / `PAYNE'S GREY`
  - `neumannW492` -> `Buff Titanium` / `BUFF TITANIUM`

## Core Acceptance Gates Summary

| Dimension | Primary Target | Pragmatic Fallback / High-Rate Rule |
|---|---|---|
| **Magnitude @ 44.1 & 48 kHz** | `max \|error\| <= 0.20 dB` (ref `RMS <= 0.08 dB`) | `fallback-0.5`: `max \|error\| <= 0.50 dB` (ref `RMS <= 0.15 dB`) after >= 2 bounded attempts with documented residual-floor diagnosis |
| **Magnitude @ 88.2 & 96 kHz** | `max \|error\| <= 0.50 dB` (`f < Nyquist`) | `sample-rate-engineering-0.5` once 48 kHz baseline passes (`176.4 / 192 kHz` optional extension) |
| **Compact Extrema Matrix** | All supported units (Bell / Low Shelf / High Shelf / HPF / LPF) | Max boost & max cut × low/mid/high freq × min/mid/max Q or Slope + neutral + one 9-point track per continuous axis |
| **Curve Smoothness** | Finite output (`0` NaN/Inf) at all states | Unintended extra peak/dip prominence `<= 0.15 dB`; local 3-point chord / knot seam jump `<= 0.20 dB` |
| **Realtime Performance** | 1 full active native EQ per instance, 0 alloc/lock | `44.1/48 kHz`: 64 ch @ 128 (`2.90 / 2.67 ms`); `88.2/96 kHz`: 32 ch @ 256 (`2.90 / 2.67 ms`) |

## Optional Helper Scripts

- `scripts/curve_coverage.py` — pole-aware frequency probes & local extremum
  refinement ([references/smoothness-and-probes.md](references/smoothness-and-probes.md)).
- `scripts/validate_public_fit.py`, `scripts/validate_inference_fit.py`,
  `scripts/validate_withheld_points.py` — legacy strict CSV validators for
  historical receipts ([references/legacy-validators.md](references/legacy-validators.md)).
