# Multichannel and Immersive Monitoring Calibration & Room Acoustics

Use this reference to specify loudspeaker geometry, studio monitoring calibration, bass management, electro-acoustic measurement, and room-correction boundaries. Separate physical acoustic principles (stable) from room-certification targets or vendor guidelines (verify current ITU, SMPTE, EBU, or Dolby revisions before formal certification).

## Contents

- Coordinate conventions and loudspeaker geometry
- Dolby Atmos Home vs. Theatrical room norms
- Pink-noise SPL calibration
- Bass management, LFE +10 dB in-band gain, and crossover phase
- Time alignment, ESS measurement, and room EQ / MIMO pitfalls
- Calibration verification checklist

## Coordinate conventions and loudspeaker geometry

Before entering angles into any renderer, decoder, or room-design sheet, confirm the sign convention:

- **ITU-R BS.2051 / Ambisonics standard:** Azimuth `0°` is straight ahead (Center); **positive (`+`) is left (counter-clockwise)**, negative (`-`) is right (clockwise). Elevation `0°` is ear height; positive (`+`) is upward, negative (`-`) is downward.
- **Some DAWs, cinema tools, and game engines** invert azimuth sign (clockwise positive) or use Cartesian box coordinates (`X` left-to-right, `Y` back-to-front, `Z` bottom-to-top). Never copy angle tables across tools without testing a known front-left-up direction.

### ITU-R BS.775 (5.1 horizontal baseline)

ITU-R BS.775 defines the classic five-channel horizontal reference layout on an equidistant circle around the listening position at ear height:

- `L / R`: `±30°` azimuth, `0°` elevation.
- `C`: `0°` azimuth, `0°` elevation.
- `Ls / Rs`: `±110°` nominal azimuth (allowable range `±100°` to `±120°`), `0°` elevation.
- `LFE`: band-limited low-frequency channel without a fixed directional coordinate.

### ITU-R BS.2051 (Advanced Sound System layouts)

ITU-R BS.2051 classifies 3D loudspeaker layouts as `U+M+B` (**Upper + Middle + Bottom** channel counts, excluding LFE). Label prefixes denote layer (`U` upper, `M` middle, `B` bottom, `T+000` zenith at `+90°`).

| Designation | `U+M+B` | Common name | Layer summary |
|---|---|---|---|
| System A | `0+2+0` | 2.0 Stereo | L, R (`M±030`) |
| System B | `0+5+0` | 5.1 (BS.775) | 5 horizontal + 1 LFE |
| System C | `2+5+0` | 5.1.2 | 5 horizontal + 2 upper front + 1 LFE |
| System D | `4+5+0` | 5.1.4 | 5 horizontal + 4 upper + 1 LFE |
| System G | `4+9+0` | 9.1.4 | 9 horizontal (adds wides/screen inner) + 4 upper + 1 LFE |
| System J | `4+7+0` | **7.1.4** | 7 horizontal + 4 upper + 1 LFE |
| System H | `9+10+3` | **22.2** | 9 upper (incl. zenith `T+000`) + 10 middle + 3 bottom + 2 LFE |
| Studio extension* | `6+9+0` | **9.1.6** | 9 horizontal (adds `M±060` wides) + 6 upper (adds `U±090` top middles) + 1 LFE |

*\*9.1.6 is widely deployed in Dolby Atmos mastering and home-entertainment rooms, extending the BS.2051 upper ring from 4 to 6 loudspeakers; verify exact renderer speaker labels for the target studio specification.*

### Representative nominal angles and tolerances (7.1.4 / 9.1.6 / 22.2)

Verify the latest ITU-R BS.2051 table for formal broadcast certification; the following summarizes the standard geometric structure:

| Channel role | BS.2051 label | Nominal azimuth | Typical tolerance | Nominal elevation | Notes |
|---|---|---|---|---|---|
| Center | `M+000` | `0°` | `±5°` | `0°` | Acoustic axis at ear height (`~1.2 m` seated) |
| Left / Right | `M±030` | `±30°` | `±22°..±35°` (layout-dependent) | `0°` | `±30°` standard for music/broadcast; cinema screens may narrow slightly |
| Left / Right Wide (9.1.6 / System G/H) | `M±060` | `±60°` | `±50°..±70°` | `0°` | Bridges front-to-side panning gap in larger rooms |
| Side Surround (7.1.4 / 9.1.6) | `M±090` (or `M±110`) | `±90°` (`±90°..±100°` in Atmos Home) | `±85°..±110°` | `0°` | Keep strictly horizontal in small rooms to preserve vertical separation |
| Rear Surround (7.1.4 / 9.1.6) | `M±135` (or `M±150`) | `±135°` to `±150°` | `±135°..±150°` | `0°` | System J allows `±110°..±150°` depending on room geometry |
| Top Front | `U±030` / `U±045` | `±30°` to `±45°` | `±30°..±60°` | `+30°` to `+45°` | BS.2051 nominal `+30°` (`+20°..+45°`); Dolby Home targets `~+45°` |
| Top Middle (9.1.6 / System H) | `U±090` | `±90°` | `±80°..±100°` | `+30°` to `+45°` | Placed directly lateral to MLP in 6-overhead rooms |
| Top Back / Rear | `U±135` (or `U±110`) | `±135°` | `±100°..±150°` | `+30°` to `+45°` | Symmetric front-to-back relative to Top Front improves overhead panning |
| Zenith (22.2 System H) | `T+000` | `0°` | — | `+90°` | Directly overhead; unique to 22.2 / dome rigs |
| Bottom Front (22.2 System H) | `B+000`, `B±045` | `0°`, `±45°` | — | `-15°` to `-30°` | Below screen plane |

## Dolby Atmos Home vs. Theatrical room norms

Home-entertainment / music Atmos rooms and theatrical dubbing stages differ in loudspeaker topology, acoustic target curves, and reference levels. Never copy theatrical stage rules directly into a small control room or vice versa.

| Parameter | Dolby Atmos Home Entertainment / Music Studio | Dolby Atmos Theatrical / Dubbing Stage |
|---|---|---|
| Typical layout | Discrete point-source `7.1.4`, `9.1.4`, or `9.1.6` | Screen channels (`L/C/R`, optional `Lc/Rc`) behind perforated screen + surround arrays (`Ls/Rs/Lrs/Rrs` + individual addressable surrounds) + overhead array lanes |
| Horizontal ear plane | `0°` elevation at seated ear height; if screen monitors sit above a display, keep elevation `≤ 20°` to preserve separation from heights | Screen acoustic center near `~2/3` screen height; surround arrays elevated along side/rear walls with downward tilt toward audience |
| Overhead elevation & alignment | Target `~45°` elevation (typical acceptable range `30°–55°` based on ceiling height); aligned on radial sphere or parallel to `L/R` width | Two overhead array rows spanning front-to-back aligned laterally with `L/R` screen width (`~45°` lateral elevation from reference seat), covering multiple audience rows |
| Target in-room frequency response | Nominally flat in-room target (often slight natural HF tilt in larger rooms; verify current Dolby Home Studio Technical Guidelines / DARDT) | Historically SMPTE ST 202 (X-curve) HF roll-off above `2 kHz` (subject to modern ongoing SMPTE/cinema calibration updates—verify room spec) |
| Reference SPL per channel | **`79 dBC`** preferred baseline (range `79–85 dBC` depending on room volume) | **`85 dBC`** per screen channel (`82 dBC` per surround zone array sum in classic 5.1/7.1 cinema procedures; verify current Atmos Cinema calibration spec) |
| Bass management | Standard when using compact satellites/heights (`80 Hz` typical crossover to sub(s)) plus discrete LFE | Full-range screen channels and high-output bass-managed surrounds/overheads; dedicated high-SPL LFE subwoofer array (`115 dBC` peak capability) |

Confirm exact certification tolerances (RT60 targets across `125 Hz–8 kHz`, speaker directivity, maximum SPL headroom, and room dimensions) with the current Dolby Atmos Home Entertainment Studio Technical Guidelines or Dolby Audio Room Design Tool (DARDT).

## Pink-noise SPL calibration

### Meter setup

- **Weighting:** `C`-weighted (`dBC`), because `A`-weighting attenuates bass heavily and misrepresents full-range and subwoofer energy.
- **Ballistics:** `Slow` (`1 s` time constant) for stable integration of random pink noise.
- **Microphone position:** Calibrated omnidirectional measurement capsule at the Main Listening Position (MLP) ear height, oriented per its calibration file (`90°` vertical for diffuse-field/random-incidence calibration; `0°` on-axis only when measuring a single speaker with a free-field calibration file).

### Full-band vs. 500 Hz–2 kHz band-limited pink noise

- **Full-band pink noise (`20 Hz–20 kHz`):** Equal energy per octave. Sensitive to room modes below `~300 Hz` and loudspeaker LF roll-off differences (e.g., larger LCR monitors vs. smaller ceiling monitors), causing inconsistent channel-to-channel level reads unless room EQ is already complete.
- **Band-limited pink noise (`500 Hz–2 kHz`):** Widely preferred for repeatable channel-to-channel trim alignment in studio rooms (used in Dolby Home, ITU, and EBU small-room workflows). It avoids low-frequency room-mode variance and high-frequency off-axis beaming, matching the direct-field sensitivity of heterogeneous speakers accurately.
- **RMS normalization pitfall:** Band-limiting a `-20 dBFS` full-band pink-noise file to `500 Hz–2 kHz` without re-normalizing reduces its electrical RMS by `~6–7 dB` (2 octaves out of ~10). Always check whether your reference generator outputs `-20 dBFS RMS` **after** band-limiting (the standard calibration convention) or merely applies a filter to a `-20 dBFS` broadband source.

### 79 dBC vs. 85 dBC reference levels

| Reference level (per channel, `-20 dBFS RMS` pink noise) | Typical use | Peak headroom implication (0 dBFS) |
|---|---|---|
| **`85 dBC`** | Theatrical dubbing stages, large film/scoring rooms (SMPTE RP 200) | `105 dBC` per main channel, `115 dBC` LFE |
| **`79 dBC`** | Nearfield / midfield broadcast, music, and Dolby Atmos Home studios (ITU-R BS.1116 / EBU Tech 3276 / Dolby Home) | `99 dBC` per main channel, `109 dBC` LFE (at `-6 dB` monitor trim below cinema reference) |

Calibrate **one channel at a time** at the nominal monitor-controller reference position (0 dB / CAL detent). Afterward, verify stereo/multichannel summing with uncorrelated pink noise (each doubling of uncorrelated equal-level channels adds `+3 dB` SPL) and check phantom center stability with correlated mono pink noise across `L+R`.

## Bass management, LFE +10 dB in-band gain, and crossover phase

### LFE `+10 dB` in-band gain (common measurement mistake)

The LFE (`.1`) channel is defined with **`+10 dB` higher acoustic in-band gain** (equal spectral power density `+10 dB` within its passband, nominally up to `~120 Hz`) than a single main channel driven at the same digital level.

- **Why a broadband SPL meter does NOT read `+10 dBC`:** If you feed full-band `-20 dBFS` pink noise into a main speaker (`20 Hz–20 kHz`, ~10 octaves) and into an LFE channel low-passed at `120 Hz` (~2.5 octaves), the LFE receives roughly one-quarter of the broadband power (`~-6 dB`) before the `+10 dB` boost. Consequently, a properly calibrated LFE channel reads only about **`+4 dBC` broadband** above a single main speaker on a C-weighted SPL meter (and varies slightly with sub LF cutoff, low-pass slope, and C-weighting roll-off below `~31.5 Hz`). Setting LFE to read `+10 dBC` on a broadband meter using full-band pink noise makes the subwoofer **`~6 dB` too loud**.
- **Correct calibration methods:**
  1. **RTA / FFT comparison (preferred):** Measure a main speaker's acoustic level across `30–80 Hz` on a 1/3-octave RTA or FFT, then adjust the LFE channel until its trace sits **`+10 dB`** above the main channel's trace across that overlapping band.
  2. **Identically band-limited noise:** Feed the exact same narrowband pink noise (e.g., `40–80 Hz`, well inside both speakers' passbands) to a full-range main speaker and to the LFE channel; here, the SPL meter *should* read `+10 dBC` higher on LFE.

### Bass management and crossover phase alignment

- **Signal flow separation:** Main, surround, and height channels pass through a high-pass filter (commonly `80 Hz`, `LR4` 24 dB/oct or `BW2` 12 dB/oct), while their complementary low-pass outputs sum into the subwoofer bus **at unity acoustic in-band gain (`0 dB` relative to the mains)**—never apply the `+10 dB` LFE gain to bass-managed main channels. The discrete LFE channel (with its `+10 dB` in-band gain and `~120 Hz` LPF) sums into the subwoofer after the bass-management crossover.
- **Summing headroom:** Redirecting low frequencies from 11–15 channels into a single subwoofer can produce up to `20 log10(N)` dB of correlated peak summation in the bass-management summing node. Verify digital headroom before the DAC and amplifier peak-SPL capability.
- **Acoustic phase alignment at crossover (`f_c`):**
  - Geometric distance delay alone rarely achieves phase alignment at `80 Hz` because cabinet acoustic roll-off (ported/sealed box phase), electrical HPF/LPF phase shift, and internal subwoofer DSP latency add group delay.
  - Align the acoustic arrival and phase slope of the subwoofer to the mains at `f_c` using subwoofer delay (and polarity or all-pass alignment if needed).
  - **Gold-standard verification:** Measure `Main (HPF) + Sub (LPF)` combined at MLP:
    1. In normal polarity, the summed response should track `+6 dB` at `f_c` (for aligned `LR4` slopes) with smooth magnitude through the crossover band.
    2. **Invert subwoofer polarity temporarily:** a properly phase-aligned crossover produces a **deep, sharp, symmetrical cancellation notch** centered right at `f_c`. If the notch is shallow or shifted far from `f_c`, refine subwoofer delay.

## Time alignment, ESS measurement, and room EQ / MIMO pitfalls

### Time alignment

- Measure acoustic time-of-flight (`t = d / c`, with `c ≈ 343 m/s` at `20 °C`) from every loudspeaker to the MLP using an acoustic impulse measurement with a fixed timing reference.
- Delay closer loudspeakers so all ear-level and height speakers arrive simultaneously at the MLP (target mismatch **`≤ 0.1 ms`**, roughly `3.4 cm`, to avoid Haas/precedence pulling and comb-filtered phantom images).
- Account for **heterogeneous monitor DSP latency**: active DSP monitors often introduce `0.5–4 ms` of internal conversion/filtering delay compared to analog monitors or passive ceiling speakers. Never calculate delays purely with a laser tape measure when speaker models differ.

### Electro-acoustic measurement with Exponential Sine Sweep (ESS)

The **Exponential Sine Sweep** (Farina method) is the standard electro-acoustic measurement excitation for control rooms:

- **Distortion separation:** Deconvolving an ESS with its inverse filter packs all harmonic distortion products (`2nd`, `3rd`, ...) into causal echoes at **negative time lags** before the linear impulse peak, leaving the linear Room Impulse Response (RIR) clean.
- **High LF SNR:** Pink-like energy distribution devotes longer dwell time to low frequencies, improving signal-to-noise ratio in modal regions compared to white MLS or impulses.
- **Timing reference:** Use a wired electrical loopback reference channel (or an acoustic reference chirp on a fixed speaker when measuring across separate playback/capture clocks) to preserve exact relative arrival times across channels.

### Windowing and reflection separation

- **Reflection-free direct windowing:** Placing a right-hand window (e.g., half-Hann or Tukey taper) just before the first strong reflection (desk/console bounce or floor reflection at `Δt = Δd / c`) isolates the loudspeaker's quasi-anechoic direct field.
- **Time-frequency resolution limit:** A window of duration `T_w` yields valid spectral resolution only above roughly `f_min ≈ 1 / T_w` (a `5 ms` window cannot resolve features below `~200 Hz`).
- **Frequency-Dependent Windowing (FDW):** Applies a constant number of cycles (e.g., `6–15 cycles`) per frequency, combining a short, reflection-free window at high frequencies with a longer steady-state window at low frequencies. Use FDW to distinguish direct speaker voicing from room-boundary interference before touching any EQ.

### Room EQ and MIMO calibration pitfalls

| Pitfall | Acoustic cause | Engineering remedy |
|---|---|---|
| **Boosting deep narrow nulls** | Boundary interference (SBIR) and standing-wave cancellation notches are **non-minimum-phase**; adding `+12 dB` of boost cannot cancel destructive arrival, eats headroom, raises distortion, and creates huge peaks inches away | Cut modal peaks only; solve nulls via speaker/sub repositioning, acoustic treatment, or multi-sub optimization |
| **Overfitting single-point HF measurements** | Desk, monitor, and ceiling comb filtering varies dramatically over a few centimeters | Restrict tight EQ primarily below the room's **Schroeder frequency** (`f_s ≈ 2000 * sqrt(RT60 / V)`). Above `f_s`, use spatial multi-point averaging around the MLP with ERB or `1/6–1/3` octave smoothing and trust the monitor's anechoic directivity |
| **Aggressive full-band FIR excess-phase inversion** | Attempting to invert room reflections across the full band causes audible **pre-ringing**, high latency, and a tiny millimeter sweet spot | Limit excess-phase / phase-linearization correction to smooth loudspeaker crossover phase and low-frequency minimum-phase regions; verify impulse pre-ringing and off-axis seats |
| **Ignoring off-axis and adjacent seats in MIMO / multi-sub EQ** | Independent per-sub EQ ignores inter-sub interference across the listening area | Optimize multi-sub or MIMO modal controllers jointly across multiple spatial measurement points (e.g., MLP + left/right/front/back seats), minimizing seat-to-seat variance rather than flattening one point |
| **Corrupting LFE vs. bass-management gain in matrix DSP** | Applying room-EQ trim or MIMO matrix normalization indiscriminately across both LFE and redirected main bass | Verify LFE `+10 dB` in-band gain and redirected `0 dB` bass-management gain independently after any MIMO or room-EQ preset update (see [reference.md](reference.md) for MIMO IR matrix verification) |

## Calibration verification checklist

```text
[ ] Confirm coordinate convention and physical speaker angles (azimuth, elevation, symmetry)
[ ] Measure true acoustic arrival time per speaker (including monitor DSP latency) and time-align to ≤ 0.1 ms
[ ] Verify polarity of every speaker and subwoofer (impulse peak direction / polarity pulse)
[ ] Match all ear-level and height channels with 500 Hz–2 kHz band-limited pink noise (-20 dBFS RMS) to target dBC Slow (79 or 85 dBC)
[ ] Align bass-management crossover phase at f_c and confirm deep polarity-flip cancellation notch
[ ] Verify LFE +10 dB in-band acoustic gain via RTA/FFT or matched narrowband noise (not broadband SPL alone)
[ ] Confirm room EQ cuts peaks below Schroeder frequency without boosting non-minimum-phase nulls or introducing FIR pre-ringing
[ ] Validate across MLP and off-axis seats: phantom center stability, 360°/overhead pan smoothness, and downmix translation
```
