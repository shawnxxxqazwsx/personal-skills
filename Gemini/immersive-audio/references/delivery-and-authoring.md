# Immersive Audio Authoring, Metadata Exchange, and Delivery

Use this reference to navigate ADM XML structure, real-time S-ADM and cinema IAB interchange, the AOM IAMF open delivery architecture, Dolby Atmos master delivery gates, and ITU-R BS.1770 multichannel/immersive loudness standards. Always verify mutable platform delivery specifications and current standard revisions before final mastering or broadcast submission.

## Contents

- ITU-R BS.2076 ADM XML hierarchy
- Real-time broadcast and cinema exchange: S-ADM and IAB
- AOM IAMF (Immersive Audio Model and Formats)
- Dolby Atmos Master (ADM BWF) and streaming delivery gates
- Multichannel loudness weighting and regional standards
- Pre-delivery QC checklist

## ITU-R BS.2076 ADM XML hierarchy

The **Audio Definition Model (ITU-R BS.2076)** is an open XML metadata model describing channel-based, object-based, HOA, matrix, and binaural audio. In file-based workflows, ADM XML lives in the `axml` chunk of a **BW64** (64-bit Broadcast Wave, ITU-R BS.2088) or RF64 `.wav` file alongside a `chna` chunk that binds XML IDs to physical PCM tracks.

### Core structural hierarchy

```text
audioProgramme (top-level mix, language, loudness metadata)
 └─ audioContent (semantic group: dialogue, music, effects, accessibility)
     └─ audioObject (timed element: gain, interactivity, head-lock, track refs)
         ├─ audioTrackUID ──► links via `chna` chunk to physical PCM track
         └─ audioPackFormat (spatial format type: DirectSpeakers / Objects / HOA / Matrix / Binaural)
             └─ audioChannelFormat (single logical channel within the pack)
                 └─ audioBlockFormat (time-segmented spatial/gain/extent/HOA parameters)
```

| ADM Element | Primary responsibility | Key attributes / cautions |
|---|---|---|
| `audioProgramme` | Defines a complete playable presentation (e.g., Main English, Audio Description) | Carries `loudnessMetadata`, `start`/`end`, `audioProgrammeLanguage`; one file can declare multiple programmes sharing underlying audio tracks |
| `audioContent` | Groups semantically related elements (Dialogue, Music, Effects) | Carries `dialogue` content-kind flags and content-level loudness metadata |
| `audioObject` | Binds timed PCM audio to spatial formatting and user-interactivity rules | Controls `start`/`duration`, `gain`, `mute`, `interact` bounds (`gainInteract`, `positionInteract`), `complementary` groups (e.g., alternative languages) |
| `audioPackFormat` | Groups channels into one spatial paradigm via `typeLabel` / `typeDefinition` | `0001 DirectSpeakers`, `0002 Matrix`, `0003 Objects`, `0004 HOA`, `0005 Binaural`; common speaker layouts use Common Definitions (`ITU-R BS.2094`) |
| `audioChannelFormat` | Represents one logical channel (e.g., `M+030`, one object, or one HOA component) | Contains ordered `audioBlockFormat` elements covering its active timeline |
| `audioBlockFormat` | Atomic time-varying metadata snapshot (`rtime`, `duration`) | Carries polar (`azimuth`/`elevation`/`distance`) or Cartesian (`X`/`Y`/`Z`, requires `cartesian="1"`) coordinates, `gain`, `width`/`height`/`depth` extent, `diffuse`, `jumpPosition`, `headLocked`; for HOA carries `order`, `degree`, `normalization` (defaults to `SN3D` if omitted), and `nfcRefDist` |

*Note on track linkage:* Full BS.2076 also defines `audioStreamFormat` and `audioTrackFormat` between `audioChannelFormat` and `audioTrackUID`; simplified/common-definition profiles allow `audioTrackUID` to reference `audioChannelFormat` and `audioPackFormat` directly.

### Frequent ADM authoring failure modes

- **Coordinate flag omission:** Writing `X`/`Y`/`Z` without `cartesian="1"` causes compliant BS.2127 renderers to misinterpret coordinates as polar.
- **Timeline gaps or overlaps:** Non-contiguous `rtime` + `duration` values across `audioBlockFormat` blocks can trigger silent dropouts or interpolation jumps.
- **Profile mismatch:** Full ITU-R BS.2076 permits features (e.g., nested packs, arbitrary HOA orders, complex interactivity) rejected by vendor-constrained profiles such as the **Dolby Atmos Master ADM Profile** or **ITU-R BS.2168** Emission Profile. Validate against the exact target profile schema.

## Real-time broadcast and cinema exchange: S-ADM and IAB

Do not conflate file-based ADM, serial S-ADM, and cinema IAB—they serve distinct carriage layers.

### ITU-R BS.2125 S-ADM (Serial ADM)

- **Design:** Slices ADM metadata into video-frame-synchronous XML frames (`frameHeader` + `audioFormatExtended`) so live broadcast switchers, encoders, and Next-Generation Audio (NGA) playout chains can stream dynamic objects and personalization metadata in real time.
- **Frame types:** `full` (complete scene in one frame), `divided` / `intermediate` (split across frames when payload exceeds one frame budget), `all`, and `header`, paired with `changedIDs` to let receivers skip unchanged static declarations.
- **Baseband carriage (AES3):** **SMPTE ST 2116** maps S-ADM XML into SMPTE ST 337 non-PCM data bursts carried over an AES3 digital audio pair (including MADI-embedded AES3). Verify per-frame payload limits and optional gzip compression support at high frame rates (`50/59.94 fps`) or large object counts.
- **IP carriage (SMPTE ST 2110):** **SMPTE ST 2110-41** (Fast Metadata / FMX over RTP, with **SMPTE ST 2127-2** defining Metadata-Guided Audio / S-ADM payload mapping) carries S-ADM as an independent IP essence stream synchronized via PTP (IEEE 1588) to ST 2110-30 (uncompressed PCM) or ST 2110-31 (AES3) audio streams.
- **Emission constraints:** **ITU-R BS.2168** defines emission-profile bounds for ADM and S-ADM in broadcast distribution.

### SMPTE ST 2098-2 IAB (Immersive Audio Bitstream)

- **Scope:** Open SMPTE standard for **theatrical cinema** immersive audio exchange (e.g., SMPTE DCP / IMF cinema workflows).
- **Structure:** Binary, frame-synchronous bitstream (`IAFrame`s) carrying channel beds plus dynamic audio objects and spatial metadata alongside uncompressed PCM (typically `48 kHz` or `96 kHz`, 24-bit).
- **Boundary rule:** IAB is not ADM XML in a different wrapper. Converting between ADM BWF and IAB requires a dedicated authoring/rendering transcoder that respects theatrical bed/object constraints and cinema loudness/headroom conventions.

## AOM IAMF (Immersive Audio Model and Formats)

**IAMF** (developed by the Alliance for Open Media, [aomediacodec.github.io/iamf](https://aomediacodec.github.io/iamf/); also seen in consumer ecosystems under brands such as Eclipsa Audio) is an open, royalty-free spatial audio container and rendering model designed for web, streaming, mobile, and home playback.

### Bitstream architecture (Open Bitstream Units — OBUs)

IAMF is **codec-agnostic**: it wraps compressed or lossless substreams encoded with **Opus**, **AAC-LC**, **FLAC**, or **LPCM** inside **OBUs** divided into:

1. **Descriptors:** `IA Sequence Header`, `Codec Config`, `Audio Element`, and `Mix Presentation` OBUs establishing static stream topology and decoding setup.
2. **IA Data (Temporal Units):** Frame-synchronous Audio Frame OBUs paired with Parameter Block OBUs (time-varying mix gain, demixing mode, and reconstruction gain).

### Audio Elements (`audio_element_type`)

| Element type | Bitstream config | How it works |
|---|---|---|
| **Scalable Channel-based** (`CHANNEL_BASED`) | `ScalableChannelLayoutConfig` | Encodes layered speaker layouts hierarchically (e.g., `2.0 -> 5.1 -> 7.1.4`) using **demixing parameters** and **recon gain**, allowing an artist-controlled downmix or direct extraction of lower layouts without simulcasting redundant audio |
| **Scene-based** (`SCENE_BASED`) | `AmbisonicsConfig` | Carries HOA (`ACN` / `SN3D`) using either mono-channel coding or a projection matrix coding mode (check current spec order limits, e.g., up to 4th order in IAMF v1.x) |
| **Object-based extensions** | Extended `audio_element_type` | Check exact specification version and target player profile (IAMF v1.0/v1.1 standardized Scalable Channel and Scene-based elements; later IAMF v2.x extensions add discrete `OBJECT_BASED` elements) |

### Mix Presentations and Reference Rendering

- A **Mix Presentation** combines one or more Audio Elements into **Sub-Mixes**, attaching layout-specific rendering rules, loudness metadata (integrated loudness, digital peak, optional true peak and anchored loudness), language tags, and accessibility/personalization overrides (e.g., dialogue enhancement).
- Playback adaptation to physical speaker layouts or binaural headphones is defined through the open reference **Open Audio Renderer (OAR)** model. Always check browser/platform MSE/codec profile support before choosing Opus vs. AAC-LC vs. FLAC inside IAMF.

## Dolby Atmos Master (ADM BWF) and streaming delivery gates

Keep the **mastering file** (ADM BWF / DAMF), **distribution encode** (E-AC-3 JOC, AC-4, TrueHD), and **endpoint renderer** (AVR, soundbar, Dolby Binaural, Apple Spatial Audio) strictly separate.

### Typical Atmos Music master and streaming QC gates

Verify current label/DSP technical specifications before delivery; standard baseline gates include:

- **Master container:** ADM BWF (`.wav` / BW64), `48 kHz / 24-bit` PCM, compliant with the current Dolby Atmos Master ADM Profile, with exact start/end length matching the companion stereo release master when required for seamless DSP format switching.
- **Integrated loudness ceiling:** **`≤ -18 LKFS`** measured across the full track per ITU-R BS.1770 (this is a **maximum ceiling**, not a mandatory target—intimate/dynamic acoustic mixes may legitimately sit at `-22` to `-26 LKFS`).
- **True Peak ceiling:** **`≤ -1.0 dBTP`** (4× oversampled true peak) to prevent inter-sample distortion during lossy E-AC-3 JOC / AC-4 / platform spatial encoding.
- **Downmix / trim validation:** Explicitly audition and configure `5.1` and `2.0` downmix trim metadata (`Lo/Ro`, `Standard`, `Direct Render`, surround/height trim offsets) inside the renderer rather than leaving defaults unchecked.

### Binaural Render Mode metadata (`Off` / `Near` / `Mid` / `Far`) and Apple Spatial Audio divergence

Dolby Atmos ADM metadata carries a per-bed-channel and per-object **Binaural Render Mode** tag (`Off`, `Near`, `Mid`, `Far`) intended for the **Dolby Binaural Renderer**:

| Mode | Dolby Binaural Renderer behavior | Typical authoring intent |
|---|---|---|
| `Off` | Bypasses binaural HRTF/room processing (direct L/R feed) | LFE, sub-bass anchors, or elements intentionally kept dry/non-externalized (overuse collapses spatial depth) |
| `Near` | Tight virtual-room early reflections, intimate proximity | Lead vocals, dry close-miked percussion, foreground focus |
| `Mid` | Moderate virtual room reflections and distance | General instruments, harmonies, stereo beds |
| `Far` | Higher virtual room reflection energy and perceived distance | Ambience, orchestral halls, reverb returns, distant pads |

**Critical cross-platform divergence (Apple Spatial Audio):**

- **Apple Spatial Audio** (Apple Music on iOS/macOS/tvOS/AirPods) decodes the delivered Atmos stream through **Apple's proprietary spatial renderer**, **not** the Dolby Binaural Renderer.
- Apple's renderer applies its own HRTF, virtual-room model, and optional Dynamic Head Tracking, and **does not reproduce Dolby Binaural Render Mode (`Off`/`Near`/`Mid`/`Far`) behavior identically** (for instance, elements marked `Off` may still be spatialized differently than in Dolby's headphone monitor, and tonal/reverb balance can shift noticeably).
- **Mandatory workflow rule:** Never sign off an Atmos music master solely on Dolby Binaural monitoring. Audition across (1) a calibrated `7.1.4` / `9.1.6` loudspeaker room, (2) Dolby Binaural, (3) an actual Apple Spatial Audio playback path (both Fixed and Head-Tracked), and (4) the stereo fold-down.

## Multichannel loudness weighting and regional standards

### ITU-R BS.1770 multichannel and 3D channel weighting

ITU-R BS.1770 (current revision **BS.1770-5**, extending the 3D Annex 3 weighting introduced in BS.1770-4 for BS.2051 layouts) filters each non-LFE channel through a two-stage **K-weighting** filter (high-shelf head-diffraction model + RLB high-pass), computes mean-square energy in `400 ms` blocks (`75%` overlap) with absolute (`-70 LKFS`) and relative (`-10 LU`) gating, and sums channels using position-dependent power weights $G_i$:

| Elevation ($\varphi$) | Azimuth ($\theta$) | Weight $G_i$ | Equivalent gain | Typical channels |
|---|---|---|---|---|
| $|\varphi| < 30^\circ$ | $|\theta| < 60^\circ$ | **`1.00`** | `0.0 dB` | `L`, `R`, `C`, `Lc`, `Rc`, `Lw`, `Rw` |
| $|\varphi| < 30^\circ$ | $60^\circ \le |\theta| \le 120^\circ$ | **`1.41`** | **`+1.5 dB`** | `Ls`/`Rs` (5.1), `Lss`/`Rss` (7.1.4 / 9.1.6) |
| $|\varphi| < 30^\circ$ | $120^\circ < |\theta| \le 180^\circ$ | **`1.00`** | `0.0 dB` | `Lrs`/`Rrs` (`±135°..±150°`), `Cb` (`180°`) |
| $|\varphi| \ge 30^\circ$ *(Upper & Bottom)* | All azimuths | **`1.00`** | `0.0 dB` | `Ltf`, `Rtf`, `Ltm`, `Rtm`, `Ltb`, `Rtb`, `T+000`, Bottom layer |
| LFE (`.1` / `.2`) | N/A | **`0`** | Excluded | `LFE1`, `LFE2` |

**Practical mixing consequence:** Horizontal side surrounds (`60° ≤ |θ| ≤ 120°`) carry a `+1.5 dB` loudness weight, whereas rear surrounds (`±135°..±150°`) and **all height/overhead channels (`|φ| ≥ 30°`)** carry unity weight (`1.00`). Moving loud elements between side surrounds and height/rear speakers shifts measured BS.1770 integrated loudness even at identical electrical level. Always verify which rendered loudspeaker layout (`5.1` vs. `7.1.4` vs. object-renderer internal meter) a delivery spec mandates for loudness compliance.

### Regional broadcast and streaming loudness targets

Verify current broadcaster/platform delivery documents before final export:

| Specification / Region | Integrated target | Tolerance | Max True Peak | Measurement basis & notes |
|---|---|---|---|---|
| **EBU R128** (Europe / EBU) | **`-23.0 LUFS`** | `±0.5 LU` (`±1.0 LU` live) | **`-1.0 dBTP`** | Whole-program ITU-R BS.1770; pairs with Loudness Range (`LRA`, EBU Tech 3342) and max momentary/short-term checks where specified |
| **ATSC A/85** (North America / CALM) | **`-24.0 LKFS`** | `±2.0 LU` (often `±1.0 LU` in delivery specs) | **`-2.0 dBTP`** | Anchor-element / **dialogue-gated** (commonly paired with `dialnorm` metadata in AC-3 / E-AC-3 / AC-4); confirm whether full-mix or dialogue-gated applies |
| **ARIB TR-B32** (Japan) | **`-24.0 LKFS`** | Per broadcaster | **`-1.0 dBTP`** | ITU-R BS.1770 whole-program or anchor rules per broadcast tier |
| **Immersive Music Streaming** *(e.g., Dolby Atmos Music)* | **`≤ -18.0 LKFS`** *(ceiling)* | Do not exceed ceiling | **`-1.0 dBTP`** | Full-program ITU-R BS.1770-4/-5 rendered loudness; confirm exact DSP rules (Apple Music, Tidal, Amazon Music, etc.) |

## Pre-delivery QC checklist

```text
[ ] Verify target deliverable layer: ADM BWF master vs. S-ADM live stream vs. IAB cinema vs. IAMF / codec encode
[ ] Confirm sample rate (48 kHz standard for Atmos/broadcast/IAB), bit depth (24-bit), frame rate, and start/duration sync
[ ] Validate ADM XML / chna integrity against the exact target profile (BS.2076, BS.2168 Emission, or Dolby Atmos ADM Profile)
[ ] Check integrated loudness (correct BS.1770 layout weights and gating mode) and True Peak ceiling
[ ] Audit LFE low-pass bandwidth, zero unintended DC/ultrasonic energy, and absence of hard clipping on beds and objects
[ ] Audition loudspeaker render, Dolby Binaural, Apple Spatial Audio (Fixed + Head-Tracked), and 5.1 / 2.0 downmixes
```
