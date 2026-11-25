# Pro Tools (Studio and Ultimate)

Pro Tools uses a binary `.ptx` session format, strict AAX plug-in architecture,
and explicit session-level I/O routing. Always confirm the exact edition
(**Intro**, **Artist**, **Studio**, or **Ultimate**), audio engine
(**Native** vs **HDX / HD Native**), and whether surround/Atmos capabilities
are licensed in the running instance.

## Establish session state safely

- Confirm session name, saved state, `.ptx` path, sample rate, bit depth,
  timecode frame rate, Playback Engine, transport state, active window (`Edit`
  vs `Mix` vs `MIDI Editor` vs `I/O Setup`), and selected track(s).
- **Read-only text audit**: because `.ptx` files are binary and cannot be
  grepped directly, use `File -> Export -> Session Info as Text...` (or PTSL
  `ExportSessionInfoAsText`) when you need a complete offline inventory of
  tracks, channel widths, plug-in inserts, file paths, clip lists, and memory
  locations without touching session routing.

## PTSL (Pro Tools Scripting Library, gRPC)

Pro Tools (2022.12+ with expanding command coverage in 2023–2025 releases)
exposes an official local gRPC control plane (`localhost:31416` by default).
Clients must authenticate/register with `RegisterConnection` before issuing
commands.

### Read-only inspection RPCs

- **Session & transport**: `GetSessionName`, `GetSessionPath`,
  `GetSessionSampleRate`, `GetSessionBitDepth`, `GetSessionAudioFormat`,
  `GetSessionLength`, `GetSessionStartTime`, `GetSessionTimeCodeRate`,
  `GetTransportState`, `GetTransportArmed`, `GetPlaybackMode`, `GetRecordMode`,
  `GetDynamicTransportState`, `GetMainCounterFormat`.
- **Track & timeline inventory**: `GetTrackList` (returns track name, ID, type,
  format/width, and mute/solo/record-arm/input-monitor/hidden/inactive flags),
  `GetTimelineSelection`, `GetMemoryLocations`, `GetFileLocation`,
  `GetEditMode`, `GetEditTool`, `ExportSessionInfoAsText`.

### Controlled mutation RPCs and hard boundaries

- **Supported controlled mutations** (varies by Pro Tools / PTSL version):
  `CreateNewTracks`, `SelectTracksByName`, `SetTrackMuteState`,
  `SetTrackSoloState`, `SetTrackRecordEnableState`,
  `SetTrackInputMonitorState`, `SetTrackFrozenState`, `CreateMemoryLocation`,
  `Import`, `ExportMix`, `SaveSession`, `SaveSessionAs`, `OpenSession`,
  `CloseSession`, `TogglePlayState`, `ToggleRecordEnable`.
- **Hard boundaries**: PTSL does NOT provide general-purpose arbitrary plug-in
  DSP parameter editing, full I/O Setup matrix re-patching, pin/bus inspection,
  or arbitrary automation breakpoint authoring. Do not assume a UI or plug-in
  parameter task can be completed via PTSL alone; check the running host's
  supported PTSL command list first.
- **Safety rules**: never invoke `CloseSession` with `save_on_close=false` on a
  dirty session, never overwrite via `SaveSession` when destination/version is
  ambiguous, and always re-query `GetTrackList` / `GetTransportState` after a
  mutating RPC to verify the resulting state.

## I/O Setup (Input, Output, Bus, Insert, and Path Order)

Open `Setup -> I/O...` to audit routing across its dedicated tabs (**Input**,
**Output**, **Bus**, **Insert**, **Mic Preamps**, **H/W Insert Delay**,
**Dolby Atmos**):

- **Session I/O vs System I/O**: each `.ptx` embeds its own I/O Setup. Opening
  a session from another rig commonly leaves paths *italicized* (inactive or
  unmapped). Never click `Default` blindly—it wipes custom stem, bus, and
  sub-path assignments.
- **Bus-to-Output mapping**: in the **Bus** tab, verify whether an Output bus
  has `Mapping to Output` enabled and pointing to the intended physical/virtual
  output. Meters moving with no audible return often trace to an unmapped bus
  or an inactive output path.
- **Multichannel Path Order & Sub-paths (critical)**:
  - Pro Tools defaults to **Film order** for 5.1 (`L C R Ls Rs LFE`), NOT
    SMPTE/ITU order (`L R C LFE Ls Rs`)! Inspect the exact channel order in
    `Setup -> I/O -> Output / Bus` (and `5.1` / `7.1.2` / `7.1.4` path headers)
    before comparing renders or patching external bridges/renderers.
  - Multichannel paths expose nested stereo/mono **sub-paths**. Confirm a track
    output targets the full multichannel path rather than a stereo sub-path.
- **Hardware Inserts**: require symmetrical I/O numbering (e.g., Out 3–4 paired
  with In 3–4 on the **Insert** tab). Check **H/W Insert Delay** compensation
  values when diagnosing comb filtering or misalignment on external hardware
  inserts.

## Routing Folders, Aux Inputs, Master Faders, and VCAs

| Track type | Passes audio | Insert point | Key operational rule |
|---|---|---|---|
| **Basic Folder** | No | None | Visual/edit grouping only; zero routing effect. |
| **Routing Folder** | Yes | Pre-fader | Combines folder grouping with an audio summing bus (mono up to 7.1.4/9.1.6); dragging tracks in can reassign their outputs to the folder bus. |
| **Aux Input** | Yes | Pre-fader | Real-time return/stem bus; use **Solo Safe** (`Command-click` / `Ctrl-click` Solo) so soloing sources does not mute returns. |
| **Master Fader** | Controls bus level | **Post-fader** | Inserts sit *after* the fader—moving a Master Fader changes drive into master limiters/dither. No Sends or Solo Safe. |
| **VCA Master** | No | None | Control-only fader/mute/solo/automation link via an assigned Mix/Edit Group. Coalescing VCA automation is destructive—snapshot first. |

- Distinguish **Audio Track Input Monitoring (`I`)** vs **Record Enable**:
  input-monitored tracks pass live input and suppress timeline playback unless
  configured for TrackInput/AutoInput monitoring appropriately.
- Distinguish **Multi-Channel** vs **Multi-Mono** plug-in instances on wide
  tracks: multi-mono inserts separate mono processors per channel (with
  optional link toggle) and does not perform cross-channel spatial or linked
  sidechain processing the way a true multi-channel AAX plug-in does.

## AAX plug-in format, cache, and rescan paths

Pro Tools natively loads ONLY **64-bit AAX** (AAX Native, AAX DSP on HDX, and
AAX AudioSuite offline). It does not load VST3 or AU natively.

- **Install locations**:
  - macOS: `/Library/Application Support/Avid/Audio/Plug-Ins/` (quarantined or
    disabled plug-ins live in `Plug-Ins (Unused)/`).
  - Windows: `C:\Program Files\Common Files\Avid\Audio\Plug-Ins\`.
- **Cache & preference paths**:
  - macOS: `~/Library/Preferences/Avid/Pro Tools/InstalledAAXPlugIns` (alongside
    `DAE Prefs`, `Pro Tools Prefs`).
  - Windows: `%APPDATA%\Avid\Pro Tools\InstalledAAXPlugIns`.
- **Reload & force-rescan workflow**:
  - Pro Tools scans AAX binaries ONLY at startup (no live hot-rescan).
  - With Pro Tools closed, delete `InstalledAAXPlugIns` to force a full AAX
    rescan, or move a suspect `.aaxplugin` to `Plug-Ins (Unused)/` for
    isolation, then relaunch.
  - On Apple Silicon macOS, verify whether Pro Tools is launching **Native
    (`arm64`)** or **Open using Rosetta (`x86_64`)** (Finder `Get Info`).
    Intel-only AAX binaries are silently skipped in native `arm64` mode.
  - After relaunch, verify the newly loaded plug-in instance, format
    (Multi-Channel vs Multi-Mono, Native vs DSP), and version inside the
    session.

## Playback Engine, Delay Compensation, and Video Engine

Open `Setup -> Playback Engine...`:

- **Session reload warning**: changing the active Playback Engine closes and
  reopens the current session. Always save before changing engines.
- **H/W Buffer Size**: use low buffers (64–128 samples) for live tracking and
  higher buffers (512–1024+) for heavy multichannel mixing/rendering.
- **Ignore Errors During Playback/Record**: keep **OFF** during audio
  verification—enabling it suppresses error alerts while allowing silent
  dropouts/clicks into playback or captures.
- **Delay Compensation (ADC)** (`Options -> Delay Compensation`):
  - Expose Mix window rows via `View -> Mix Window Views -> Delay
    Compensation` (`dly` = plug-in/track latency, `+/-` user offset, `cmp` =
    applied compensation).
  - Color states: **green** = healthy compensation; **orange** = channel
    exceeds ADC ceiling (16,383 samples @ 48 kHz, 32,767 @ 96 kHz, 65,535 @
    192 kHz); **red** = longest path or broken/bypassed compensation.
  - Note: HDX **DSP Safe** / Low Latency Monitoring and bypassed vs inactive
    plug-ins change latency differently—verify sample alignment after toggling.
- **Dynamic Plug-in Processing**: suspends idle plug-ins to save CPU. Check
  whether it causes first-transient clicks or missed tail decay on short test
  bursts; disable during deterministic null/latency validation if authorized.
- **Video Engine (`Avid Video Engine`)**: disable when running audio-only
  sessions if it causes transport stalls or memory pressure.

## Offline Bounce, Commit / Freeze, and Dolby Atmos / ADM BWF

### Bounce Mix (`File -> Bounce Mix...`)

- Confirm **Bounce Source** (physical Output, Bus, or Internal Atmos Renderer),
  **File Type** (`WAV`, `AIFF`, `Dolby Atmos (ADM BWF)`), **File Format**
  (`Interleaved` vs `Multiple Mono`), **Bit Depth**, **Sample Rate**, and
  exact destination folder/filename.
- **Offline vs Real-Time trap**: uncheck **Offline** (force Real-Time Bounce)
  whenever the bounce path includes **Hardware Inserts**, **Live Inputs**,
  external audio bridges, or an **External Dolby Atmos Renderer** over
  CoreAudio/MADI/Dante. Offline bounce will render silence or un-returned audio
  on external real-time loops.

### Track Freeze vs Track Commit

- **Track Freeze**: reversible, non-destructive temporary render up to a chosen
  insert; preserves underlying clips and plug-ins.
- **Track Commit**: renders audio to new clips/track with selectable scope
  (`Commit Up to This Insert`, `Volume & Mute`, `Sends`, `Consolidate Clips`)
  and source disposition (`Do Nothing`, `Hide and Make Inactive`, `Delete`).
  Always prefer `Do Nothing` or `Hide and Make Inactive`; never choose `Delete`
  without explicit user authorization.

### Dolby Atmos Renderer and ADM BWF linkage

- **Internal vs External Renderer**: Pro Tools Studio and Ultimate (2023.12+)
  include an **Internal Dolby Atmos Renderer** alongside legacy **External
  Renderer** linkage (via Dolby Audio Bridge / MADI / Dante + LTC sync). Check
  `Setup -> Peripherals -> Dolby Atmos` to confirm which mode is active.
- **Routing audit** (`Setup -> I/O -> Dolby Atmos` + Mix window Output/Bus
  assignment):
  - Verify **Beds** (up to 7.1.2 per bed) and **Objects** (<= 128 total
    channels; Object tracks have the orange Object toggle engaged in Mix/Edit).
  - Check host-side **Trim & Downmix**, per-bed/object **Binaural Render Mode**
    selector (`Off`/`Near`/`Mid`/`Far`), and **Renderer Monitoring Format**
    (`7.1.4` / `5.1` / `2.0` / `Binaural`).
- **ADM BWF export**: verify **48 kHz / 24-bit**, exact timeline selection,
  matching frame rate, and no unintended Solo/Mute states before bouncing
  `Dolby Atmos (ADM BWF)` (or recording into an External DAR), then run an
  objective on-disk file check.
