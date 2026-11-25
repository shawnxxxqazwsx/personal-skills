# Nuendo and Cubase

These hosts share a core engine, but labels and available post-production or
immersive features differ by edition (Elements/Artist/Pro/Nuendo) and version.
Trust the currently visible workspace and project configuration over remembered
menu paths.

## Establish project and routing context

- Confirm the active project, project sample rate/bit depth, Control Room state
  when relevant, transport/record mode, selected track(s), and focused window
  (Project, MixConsole, Audio Connections, VST Plug-in Manager, or plug-in
  editor).
- Read `Studio -> Audio Connections` and channel/bus format before changing
  routing. Track output assignment, Direct Routing, sends, Cue/Control Room
  paths, and channel configuration can each explain an apparent missing return.
- For surround/immersive work, verify the bus format, speaker configuration,
  panner/rendering path, and plug-in I/O. Do not change a project to Stereo,
  alter a renderer, or reinterpret a bed/object path merely to make a plug-in
  appear active.

## Control Room monitoring and Cue / Talkback safety isolation

When **Control Room** (`Studio -> Audio Connections -> Control Room`) is
enabled, it owns physical monitoring independently of the mix export bus:

- **Prevent double-monitoring**: when Control Room is active, set the Main Mix
  bus ports in `Audio Connections -> Outputs` to **Not Connected**. Leaving
  both `Outputs` and `Control Room -> Monitor` patched to the same hardware
  outputs causes +6 dB summing, comb filtering, and bypasses Dim/Monitor Level.
- **Insert boundary (print vs monitor)**:
  - **Control Room Inserts** apply ONLY to monitoring (ideal for room EQ,
    headphone correction, loudness/metering, binaural preview) and NEVER print
    into Audio Mixdown.
  - **Main Mix Output Bus Inserts** DO print into Audio Mixdown—never place
    speaker calibration or headphone-only monitoring tools there.
- **Cue, Talkback, and Listen Bus isolation**:
  - **Cue 1–4** feed independent headphone/studio mixes; **Talkback** injects a
    mic into Cues (with auto-dim) without touching Main Mix.
  - **Listen Bus (AFL/PFL)** routes soloed channels separately from Main Mix.
    If soloing a track sounds dry or ignores bus processing, check whether
    `Listen` (`L`) or AFL/PFL mode is active instead of standard Solo (`S`).
- Never change Control Room Monitor Source (`Mix` / `Cue` / `External`), toggle
  Talkback, disengage `Dim`, or switch speaker sets without explicit authority
  and confirmed safe monitor levels.

## Group, FX, VCA channels, and Direct Routing

- **Group Channel**: real-time summing audio bus (mono through 7.1.4 / 9.1.6 /
  Ambisonics depending on edition) with full inserts, EQ, sends, and output
  routing.
- **FX Channel**: return bus fed by sends (typically 100% wet). Match the FX
  channel's speaker configuration to the sending bus; a Stereo FX channel
  silently collapses surround sends.
- **VCA Fader**: control-only link (no audio passes through; no inserts or
  sends). Scales linked channels' faders and send behavior together. Note that
  `Coalesce VCA Automation` destructively merges VCA curves into member tracks;
  confirm and snapshot before running it.
- **Direct Routing** (Nuendo & Cubase Pro, up to 8 output destinations per
  channel):
  - **Exclusive Mode**: only one slot active at a time (switchable/automatable).
  - **Summing Mode**: multiple slots active simultaneously (e.g., feeding Main
    Mix, Stem Bus, and M&E concurrently).
  - When a track remains audible after reassigning its primary output or
    double-sums into a bus, inspect all 8 Direct Routing slots in MixConsole.
- In MixConsole, distinguish Channel Strip, Insert slots (including pre/post
  fader divider—slots 1–6/1–12 depending on divider position), pre/post-fader
  Sends, Direct Routing, and Control Room. Confirm exact slot numbers before
  opening or replacing a plug-in.

## Make targeted edits

- Use track names plus visible type and output assignment; Folder, VCA, Group,
  FX, Instrument, and Audio tracks are not interchangeable audio paths.
- Verify automation's target parameter, Read (`R`) / Write (`W`), and
  Nuendo/Cubase automation modes (`Touch`, `Auto-Latch`, `Cross-Over`, `Trim`,
  `Fill` ranges) before enabling Write. Disarm `W` immediately after the
  requested pass; never leave global Write active.
- For Direct Offline Processing (DOP), Render in Place, Freeze, or Export,
  check source track/event selection, range, tail, channel layout, output
  location, and whether originals are muted, disabled, or replaced.
- Capture versioned backups (`File -> Back up Project` or `Save New Version`)
  before broad routing, workspace, profile, key-command, or device setup edits.

## Control surfaces: MIDI Remote API, Generic Remote, and EuCon

External control planes can alter selection, banking, faders, transport, or
automation independently of mouse/keyboard focus:

- **MIDI Remote API** (Cubase/Nuendo 12+): JavaScript driver scripts in
  `~/Documents/Steinberg/<Nuendo|Cubase>/MIDI Remote/Driver Scripts/Local/` and
  user mappings in `MIDI Remote/User Settings/*.json`. Inspect these read-only
  to confirm whether a controller page is bound to Selected Track, Mixer Bank,
  or Focused Quick Controls.
- **Generic Remote** (`Studio -> Studio Setup -> Legacy -> Generic Remote`):
  XML-based MIDI-to-command/mixer table. Check for stale mappings if unexpected
  solo/mute flips or transport jumps occur.
- **EuCon** (`Studio -> Studio Setup -> EuCon`): network control plane for Avid
  Artist/S1/S3/S4/S6 surfaces via EuControl. Operates outside macOS
  Accessibility and can hijack track focus or latch automation. Check active
  control surfaces before diagnosing erratic UI or parameter writes.

## Built-in Dolby Atmos Renderer and ADM BWF verification

Available in Nuendo and Cubase Pro (check edition feature set for 9.1.6 /
external renderer / advanced post tools):

1. **Project prerequisites**: confirm **48 kHz** sample rate (or 96 kHz where
   supported by the host's renderer version; 48 kHz is standard Atmos delivery)
   and verify project frame rate (`Project -> Project Setup`) matches delivery.
2. **Renderer routing**: in `Audio Connections -> Outputs`, verify the
   multichannel Main Mix bus (typically **7.1.4**) carries the **Renderer for
   Dolby Atmos** insert. Any plug-in placed *after* the Renderer on that bus
   affects local monitoring only—it does NOT print into the exported ADM BWF.
3. **ADM Authoring (`Project -> ADM Authoring for Dolby Atmos`)**:
   - Inspect **Beds** (up to 7.1.2 max per bed) vs **Objects** (mono/stereo
     source tracks switched to **VST MultiPanner** in Object mode). Objects
     bypass Group/Main Mix summing and feed the Renderer directly—check the
     Renderer's Object meter when an Object track is absent from a Group meter.
   - Verify host-side **Trim & Downmix** presets, per-Bed/Object **Binaural
     Render Mode** selector (`Off`/`Near`/`Mid`/`Far`), and the Renderer's
     **Monitoring** output selector (`7.1.4` / `5.1` / `2.0` / `Binaural`)
     match the active playback setup.
4. **ADM BWF export**: verify Left–Right Locator range, 48 kHz / 24-bit output,
   no stray Solo/Mute states, and target path without overwriting an existing
   master unless authorized.

## VST Plug-in Manager: blocklist, paths, and rescan cache

- **Preferences & scan cache directories**:
  - macOS: `~/Library/Preferences/Nuendo <ver>/` or `~/Library/Preferences/Cubase <ver>/`
  - Windows: `%APPDATA%\Steinberg\Nuendo <ver>_64\` or `Cubase <ver>_64\`
- **Key cache & config files**:
  - `Vst2xPlugin Blacklist Nuendo.xml` / `Vst2xPlugin Blacklist Cubase.xml` and
    `Vst2xPlugin SearchPaths *.xml` (note: Cubase/Nuendo 13+ native Apple
    Silicon skips VST2; Cubase/Nuendo 14 removes VST2 support by default).
  - VST3 scan cache XMLs (e.g., `VstPlugInfoV3.xml` / plug-in cache database in
    the preferences directory).
  - Standard VST3 paths: `/Library/Audio/Plug-Ins/VST3` and
    `~/Library/Audio/Plug-Ins/VST3` (macOS); `C:\Program Files\Common
    Files\VST3` (Windows).
- **Rescan & reload workflow**:
  1. Open `Studio -> VST Plug-in Manager` and check the **Blocklist** tab first
     (note: reactivating a blocked plug-in can crash the host—ensure the
     project is saved first). Inspect the bottom **Plug-in Information** pane
     for exact binary path, version/SDK string, and architecture (`arm64` vs
     `x86_64`).
  2. Use the circular **Rescan All** button for newly added plug-ins. If an
     already-loaded `.vst3` binary was rebuilt on disk, **full quit + relaunch**
     is required to map the updated binary into memory; if stale metadata
     persists while closed, clear only the relevant scan cache entry before
     relaunching.
  3. Verify a fresh in-project instance, its visible version/build, active bus
     layout, and sidechain/pin routing after reload.

## Multitrack Audio Mixdown Batch Export boundaries

Before executing `File -> Export -> Audio Mixdown` (`Single` vs `Multiple`
Channel Batch Export):

- **Locator sanity**: verify Left and Right locators are in normal order (red
  cycle bar indicates inverted locators and will fail or produce invalid range).
- **Effects mode in Multiple Export**: check the **Effects** selector (`Dry
  (Transfer Channel Settings)` vs `Channel Settings` vs `Groups and Sends` vs
  `Master/Groups/Sends`). Exporting channel-only stems omits Group/FX/Master
  processing; exporting multiple stems individually through a shared nonlinear
  Group/Master compressor alters compression response compared to the full mix.
- **Channel format traps**: confirm `Interleaved` vs `Split Channels` vs
  `Mono Downmix` (never leave `Mono Downmix` checked accidentally on stereo or
  surround stems).
- **Real-Time Export**: mandatory whenever External FX, External Instruments,
  or real-time audio bridges/network loops are in the signal path; offline
  export skips live external returns.
- **Export Queue & conflict policy**: inspect the Export Queue for stale jobs
  from earlier sessions, verify Naming Scheme and destination folder, and avoid
  `Overwrite` unless explicitly authorized.

## macOS input and blank-editor checks

- **Hit-test before retrying clicks**: if a click or AX action fails to change
  a control, run a read-only system-wide AX hit test to verify the actual hit
  PID, window title, and frame rather than relying on CG window rectangles.
- **Calibrate coordinate space**: confirm whether the input tool already
  applies Retina scaling or global window offsets; verify one visible,
  reversible control with readback before attempting drags.
- **Separate submission from delivery**: successful native event dispatch
  proves only submission—re-read the target control after a single event.
- **Blank embedded editors**: distinguish window occlusion or lack of app
  activation from a plug-in rendering failure; verify foreground activation,
  confirm no overlapping window covers the editor rect, and check load or
  presentation logs before diagnosing a plug-in bug.
- **Presentation checks**: exercise a visibly changing control on the same
  editor instance and geometry instead of inferring refresh failure from static
  frames or a simultaneous move+resize.
