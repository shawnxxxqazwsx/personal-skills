# Airwindows EQ DSP Reference (Candidate Math Only)

Consult only when an Airwindows structure is relevant to a Pigora EQ modeling or
runtime question. Reviewed source:
[Airwindows repository](https://github.com/airwindows/airwindows) commit
`d22a25b7f7c0c8c05e9f3ae480e7f1da9769f49d` (`plugins/LinuxVST/src/`). Airwindows
code documents *its own* DSP, not a measured target for any hardware unit; never
copy coefficients, nonlinear stages, or branding without independent evidence
and license review.

## Transferable Hypotheses

| Source file | Observed implementation | Pigora use and falsifier |
|---|---|---|
| [SmoothEQ3Proc.cpp](https://github.com/airwindows/airwindows/blob/d22a25b7f7c0c8c05e9f3ae480e7f1da9769f49d/plugins/LinuxVST/src/SmoothEQ3/SmoothEQ3Proc.cpp) | Cascaded crossover split forming residual bass/mid/treble bands with separate gains; sample-rate-dependent fixed-Q biquad. | Test low-order split/recombine when target curves support broad overlapping tone bands; verify unity reconstruction, crossover shoulders, and full target response. Never replace documented adjustable Q with fixed Q. |
| [PearEQProc.cpp](https://github.com/airwindows/airwindows/blob/d22a25b7f7c0c8c05e9f3ae480e7f1da9769f49d/plugins/LinuxVST/src/PearEQ/PearEQProc.cpp) | Nested residual-band subtraction and recombination with rate-dependent frequency factors. | Try when a serial Bell/shelf stack cannot express broad overlapping curves; check gain interaction, neutral state, exterior response, and CPU cost. Fixed band positions are not native hardware controls. |
| [Baxandall3Proc.cpp](https://github.com/airwindows/airwindows/blob/d22a25b7f7c0c8c05e9f3ae480e7f1da9769f49d/plugins/LinuxVST/src/Baxandall3/Baxandall3Proc.cpp) | Rate-normalized LP biquads, subtracted treble residual, gain-coupled frequency, plus nonlinear `sin`/`asin` wrapper. | Test gain-coupled frequency or parallel low/high paths only when source curves support that interaction. Evaluate linear magnitude separately; never infer nonlinear wrappers from magnitude plots. |

*Note:* `SmoothEQ3` updates coefficients at block entry — its name does not
imply click-free automation; test time-domain transitions independently.

## Evaluation Checklist

1. Name the Pigora section, frozen `target.csv` SHA-256, failing curve, and
   hypothesis; compare a cheap isolated prototype before touching production DSP
   while keeping native controls intact.
2. Screen boost, cut, neutral, midpoints, detent edges, near-Nyquist regions,
   and every required sample rate (including inside any interpolated rate bank,
   preserving stage identity).
3. Re-run unchanged magnitude, smoothness, compiled `processBlock`, and realtime
   gates; report fidelity vs CPU cost separately. Never add Airwindows rows to
   `target.csv`, relax a frozen tolerance, or upgrade a claim tier.
