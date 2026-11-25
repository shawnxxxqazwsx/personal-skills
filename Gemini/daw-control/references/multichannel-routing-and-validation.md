# Multichannel Routing, Timing, and Render Validation

Cross-DAW engineering reference for verifying channel layouts, Plug-in Delay
Compensation (PDC), loopback/wet-return tests, macOS CoreAudio clocks, and
objective render outputs.

## Standard channel layouts and channel ordering

Channel permutation between Film order, SMPTE/ITU order, and Ambisonics
conventions is one of the most common silent failures in multichannel DAW work.
Always verify the host's actual bus order rather than assuming a label matches.

| Layout | Ch | Standard / Host Convention | Exact 1-based Channel Order |
|---|---:|---|---|
| **5.1 (SMPTE / ITU)** | 6 | WAV (`WAVEFORMATEXTENSIBLE`), VST3, Nuendo/Cubase, Logic Pro, REAPER default | `1:L, 2:R, 3:C, 4:LFE, 5:Ls, 6:Rs` |
| **5.1 (Film)** | 6 | **Pro Tools default**, cinema stems | `1:L, 2:C, 3:R, 4:Ls, 5:Rs, 6:LFE` |
| **5.1 (DTS)** | 6 | Legacy DTS layouts | `1:L, 2:R, 3:Ls, 4:Rs, 5:C, 6:LFE` |
| **7.1 (SMPTE / ITU)** | 8 | WAV, VST3, Nuendo/Cubase, Logic Pro | `1:L, 2:R, 3:C, 4:LFE, 5:Lss (Ls), 6:Rss (Rs), 7:Lrs (Lb), 8:Rrs (Rb)` |
| **7.1.2 (Atmos Bed, SMPTE)** | 10 | Nuendo/Cubase, Logic Pro, ADM BWF | `1:L, 2:R, 3:C, 4:LFE, 5:Lss, 6:Rss, 7:Lrs, 8:Rrs, 9:Ltm, 10:Rtm` |
| **7.1.4 (SMPTE / ITU)** | 12 | VST3, Nuendo/Cubase, Logic Pro, Atmos speaker bus | `1:L, 2:R, 3:C, 4:LFE, 5:Lss, 6:Rss, 7:Lrs, 8:Rrs, 9:Ltf, 10:Rtf, 11:Ltr, 12:Rtr` |
| **9.1.6 (SMPTE / ITU)** | 16 | Nuendo, Pro Tools SMPTE, Atmos 9.1.6 | `1:L, 2:R, 3:C, 4:LFE, 5:Lss, 6:Rss, 7:Lrs, 8:Rrs, 9:Lw, 10:Rw, 11:Ltf, 12:Rtf, 13:Ltm, 14:Rtm, 15:Ltr, 16:Rtr` |
| **HOA AmbiX (ACN / SN3D)** | `(N+1)^2` | 1st=4, 2nd=9, 3rd=16, 4th=25, 5th=36, 6th=49, 7th=64 | `ACN 0..((N+1)^2 - 1)` (1st order: `0:W, 1:Y, 2:Z, 3:X` — **not** FuMa `W,X,Y,Z`) |
| **Discrete Multichannel** | 1–64+ | REAPER tracks, audio bridges (e.g. Chlora/Chloe), MADI/Dante/AVB | Linear unlabelled channels `Ch 1..N`; verify mapping explicitly |

### Layout verification pitfalls

- **Pro Tools Film vs SMPTE**: Pro Tools 5.1/7.1/7.1.2/7.1.4 paths often place
  `C` at ch 2 and `LFE` after surrounds/heights depending on `Setup -> I/O`
  path order. Check I/O Setup before exporting stems or feeding external
  bridges.
- **9.1.6 Wide placement**: some renderers/plug-ins place `Lw/Rw` at ch 9–10
  (before heights) while others append them after heights; confirm with a
  channel-walk test.
- **HOA AmbiX integrity**: never apply independent per-channel dynamics
  (unlinked compressors/limiters), channel-only EQ, or stereo bus inserts to
  ACN/SN3D buses—doing so corrupts spatial directionality and energy balance.
- **Discrete 64-channel integrity**: confirm width at *every* hop (source track
  -> plug-in bus/pin connector -> bridge/host -> return track/bus -> Master ->
  render channel count). A single 2-channel folder, FX return, or host pin
  setting silently collapses or truncates upper channels.

## PDC (Plug-in Delay Compensation) traps and verification

Hosts align parallel audio paths using each plug-in's reported latency in
samples. Common failure modes:

1. **Dynamic latency updates mid-playback**: switching oversampling,
   linear-phase EQ, lookahead, or internal bridge buffers changes latency. Many
   hosts do not rebuild the full PDC graph cleanly during live playback—stop
   and restart transport (or toggle the track/plug-in) and re-measure.
2. **Soft bypass vs host bypass vs offline/inactive**:
   - A plug-in's internal bypass normally preserves reported latency (safe for
     parallel nulling/wet-dry A/B).
   - Host hard-bypass or Inactive/Offline state can drop reported latency to
     `0` depending on DAW, causing comb filtering or time shifts on parallel
     buses. Always verify whether both A and B paths share identical latency.
3. **Sidechain, Aux, and monitoring-mode exceptions**:
   - Logic Pro: confirm `Compensation = All` (not `Audio and Software
     Instrument Tracks`) and `Low Latency Monitoring Mode = OFF`.
   - Ableton Live: confirm `Delay Compensation = ON`, `Reduced Latency When
     Monitoring = OFF`, and `Track Delay = 0 ms`.
   - Pro Tools: check Mix window `dly`/`cmp` indicators for orange (ceiling
     exceeded) or red (uncompensated/broken).
4. **Block-size quantization**: REAPER pads track PDC to multiples of the audio
   buffer block size in several live/playback scenarios; never assume displayed
   plug-in latency equals exact end-to-end sample offset without measuring.
5. **External bridges and virtual loopback**: DAWs cannot automatically
   compensate audio routed out through virtual audio drivers/HAL/hardware and
   back onto another track unless the bridge plug-in explicitly reports total
   round-trip latency or the DAW's Hardware Insert Delay offset is calibrated.

### Measuring exact latency and polarity

- Route a 1-sample impulse (at `-12 dBFS`) or short band-limited sweep through
  a clean reference path and the target path in parallel.
- Render or capture both paths, then compute peak cross-correlation offset
  (`Δsamples`) and polarity sign (`+1` in-phase vs `-1` inverted `180°`).
- For unity-gain transparent paths, align by `-Δsamples` and check the
  difference signal (null depth in dB).

## Loopback and wet-return testing: signals and safety boundaries

Automated or scripted signal tests must never risk hearing damage, transducer
failure, or runaway feedback.

### Safety preflight

1. **Isolate physical monitors**: mute physical speaker outputs, engage Control
   Room Dim, or route tests strictly through muted/offline/virtual buses unless
   explicitly authorized for human listening at a known calibrated level.
2. **Conservative test headroom**: keep generated test signals at **`-18 dBFS`
   to `-12 dBFS`** (`-18 dBFS` RMS for continuous sine/pink noise; `-12 dBFS`
   peak for impulses/sweeps). Never inject `0 dBFS` continuous tones or
   unfiltered impulses—downstream filter boost or inter-sample peaks will clip.
3. **Feedback loop prevention**: before enabling any virtual audio bridge,
   Aggregate Device loopback, or `Monitor = In`, verify the return track does
   NOT route back to the send bus or Master output feeding the loopback input.
   Verify with fader down or muted first.

### Diagnostic signal toolbox

| Test signal | Recommended level | What it proves |
|---|---|---|
| **Channel-walk staggered impulses / distinct-frequency multitone** | `-12 dBFS` peak / `-18 dBFS` per tone | End-to-end channel mapping, ordering, crosstalk, and absence of stereo fold-down across 6–64 channels in one pass. |
| **1-sample Dirac impulse / short chirp** | `-12 dBFS` peak | Exact round-trip sample latency (`Δsamples`), polarity inversion, and linear impulse response. |
| **Pure sine tone (e.g., 1 kHz)** | `-18 dBFS` peak/RMS | Unity gain accuracy, clipping, harmonic distortion/aliasing, and buffer dropouts/clicks. |
| **Pink noise / log sine sweep (ESS)** | `-18 dBFS` RMS / `-12 dBFS` peak | Broadband frequency response, filter/EQ curve behavior, and inter-channel balance. |
| **Digital silence (`-∞ dBFS`)** | `-∞ dBFS` | Self-noise floor, DC offset, denormal spikes, or unintended crosstalk/bleed from other tracks. |

## macOS CoreAudio, Aggregate Devices, sample rate, and clock checks

### Read-only CLI inspection (macOS)

- **Enumerate all CoreAudio devices, UIDs, channel counts, and sample rates**:
  ```sh
  system_profiler SPAudioDataType
  ```
- **Inspect installed virtual HAL audio drivers** (e.g., Chlora Audio Bridge,
  BlackHole, Dolby Audio Bridge, Dante Virtual Soundcard):
  ```sh
  ls -la /Library/Audio/Plug-Ins/HAL/
  ```
- **Inspect recent `coreaudiod` errors without restarting the daemon**:
  ```sh
  log show --predicate 'process == "coreaudiod"' --last 5m --style compact
  ```
  Never run `killall coreaudiod` while a DAW has an active or unsaved session
  without explicit user authorization.

### Sample rate and clock pitfalls

- **Sample-rate mismatch**: confirm DAW project sample rate, CoreAudio device
  nominal rate (`Audio MIDI Setup`), and any external bridge/host rate match
  exactly (e.g., all `48000 Hz`). A `44.1 kHz` vs `48 kHz` mismatch causes
  ~8.8% pitch/speed shifts, silent virtual bridges, or unintended OS sample
  rate conversion.
- **Aggregate Device clocking**:
  - Select exactly **one** sub-device as the **Clock Source**.
  - Enable **Drift Correction** on every *other* sub-device that does NOT share
    hardware Word Clock, ADAT, PTP, or AVB/Milan sync with the Clock Source.
  - Do NOT enable Drift Correction on devices already externally clock-locked
    (adds unnecessary SRC), and do NOT leave it OFF on unsynced devices (causes
    periodic clicks/buffer slips).
  - Sub-device ordering inside an Aggregate Device defines logical channel
    numbers `1..N`; adding or reordering a sub-device shifts downstream DAW
    I/O assignments.

## Objective render output verification checklist

A DAW showing "Render complete" proves only that export finished—not that the
file is valid. Verify the rendered file on disk with objective tools (`afinfo`
on macOS, `ffprobe`, `soxi`, or Python `soundfile`/`numpy`) before reporting
success:

1. **Identity & freshness**: verify exact absolute path, non-zero size, and
   modification timestamp matching the current run (not a stale file from an
   earlier render).
2. **Container & header integrity**:
   - Container (`WAV`, `RF64` required for >4 GB multichannel WAV renders,
     `AIFF`, `CAF`), sample rate, bit depth/encoding (`PCM 24-bit`, `IEEE Float
     32-bit`, etc.), and exact channel count (e.g., `12` for 7.1.4, `64` for
     64-channel discrete).
   - For ADM BWF deliveries, confirm `axml` and `chna` RIFF chunks are present
     and sample rate is 48 kHz / 24-bit.
3. **Duration & bounds**: confirm exact sample count / duration matches the
   intended locator/selection range plus any expected tail (catches inverted
   locators, 0-length exports, or truncated tails).
4. **Per-channel activity & silence audit**: measure RMS and peak dBFS *per
   individual channel*. Confirm every expected active channel contains signal,
   unused channels have no bleed, and no upper surround/height/Ambisonics
   channel was silently zeroed.
5. **Peak, True Peak, clipping, and float hygiene**:
   - Measure **Sample Peak (`dBFS`)** and **True Peak (`dBTP`)** (e.g.,
     `ffmpeg -i file.wav -af ebur128=peak=true -f null -`).
   - Count clipped samples (`>= 0 dBFS`), check **DC offset**, and on 32-bit
     float renders explicitly check for `NaN`, `Inf`, or `> 0 dBFS` overs that
     float containers store without hard-clipping.
6. **Boundary & discontinuity check**: inspect start and end samples for clicks,
   abrupt mid-waveform truncation, or unintended silence padding.
