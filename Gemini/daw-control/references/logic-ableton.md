# Logic Pro and Ableton Live

---

## Part 1: Logic Pro (macOS)

### Orient and distinguish Logic-native concepts

- Confirm Logic Pro version, active `.logicx` project path and saved state,
  active **Project Alternative**, sample rate (`File -> Project Settings ->
  Audio`), audio device/buffer (`Logic Pro -> Settings -> Audio`), transport
  state, and focused window/pane (Main Window, Mixer, Inspector, Plug-in
  Manager, or floating AU editor).
- Keep these layers distinct:
  - **Project Settings** (`File -> Project Settings`): per-project (Sample
    Rate, Spatial Audio/Atmos, Sync, Tuning).
  - **Settings / Preferences** (`Logic Pro -> Settings`): global (Audio
    I/O device, Buffer Size, Plug-in Delay Compensation mode, Plug-in Manager).
  - **Track Stack**: **Folder Stack** is VCA-like control grouping only (no
    audio bus); **Summing Stack** creates an Aux summing bus with inserts and
    sends.
  - **Channel Strip vs Track**: Inspector shows two side-by-side channel strips
    (selected track on the left, its destination Aux/Output on the right); do
    not confuse them when editing inserts or faders.
  - **Take Folder** vs flattened comp vs track regions.

### Audio Unit (AU) validation and cache refresh

Logic Pro hosts ONLY **Audio Units (`.component`)**—not VST3 or AAX. System
install paths are `/Library/Audio/Plug-Ins/Components/` and
`~/Library/Audio/Plug-Ins/Components/`.

- **Read-only CLI checks (safe without mutating projects)**:
  - `auval -a` — lists every registered AU with its 4-character `TYPE SUBT
    MANU` triplet, version, and validation status.
  - `auval -v <TYPE> <SUBT> <MANU>` (add `-strict` for strict compliance) —
    validates a specific AU binary (`aufx` effect, `aumu` instrument, `aumf`
    MIDI-controlled effect, `augn` generator).
  - `lipo -archs /Library/Audio/Plug-Ins/Components/<Name>.component/Contents/MacOS/<Bin>`
    — verifies `arm64` vs `x86_64` slice architecture.
- **Cache refresh (`AudioComponentRegistrar` and AU cache)**:
  - Modern macOS caches AU component registration in the background
    `AudioComponentRegistrar` daemon, while Logic stores validation results in
    `~/Library/Caches/AudioUnitCache/com.apple.audiounits.cache`.
  - After installing or rebuilding a `.component`, `auval -a` and Logic may
    keep seeing the old binary or miss the update. When Logic is **closed** and
    maintenance is authorized:
    1. Run `killall -9 AudioComponentRegistrar` (re-triggers macOS component
       discovery; if still stale, clear `com.apple.audiounits.cache`).
    2. Re-run `auval -a` / `auval -v` to confirm the updated version registers.
    3. Relaunch Logic and check `Settings -> Plug-in Manager` (use `Reset &
       Rescan Selection` for targeted re-validation).
  - **Out-of-process XPC hosting on Apple Silicon**: Logic runs native AUs in
    `AUHostingServiceXPC` and Intel-only AUs under Rosetta in
    `AUHostingServiceXPC_arrow`. Check Activity Monitor or macOS crash logs for
    those XPC processes when an AU fails to open or crashes without taking down
    Logic itself.

### Integrated Dolby Atmos / Spatial Audio and Binaural monitoring

- Enabled via `File -> Project Settings -> Audio -> Spatial Audio -> Dolby
  Atmos` (requires **48 kHz** sample rate for ADM BWF delivery; switches Master
  routing to a 7.1.2 Bed + Object engine and inserts the built-in **Dolby
  Atmos** plug-in on the Master channel strip).
- **Bed vs 3D Object routing**:
  - Standard **Surround Panner** routes audio into the 7.1.2 Bed.
  - Switching a track's panner to **3D Object Panner** routes the track
    directly as an Object to the Atmos plug-in, bypassing Bed bus summing.
    Verify whether a track is in Surround (Bed) or 3D Object mode before
    troubleshooting missing Bed meters or Group processing.
- **Monitoring Mode selector in the Dolby Atmos plug-in**:
  - Check whether monitoring is set to `Apple Renderer` (with optional Head
    Tracking toggle), `Dolby Renderer` (using per-track `Off`/`Near`/`Mid`/
    `Far` metadata selectors), or a discrete speaker layout (`2.0`, `5.1`,
    `7.1`, `7.1.4`).
- **ADM BWF export**: `File -> Export -> Project as ADM BWF...`. Verify 48 kHz,
  exact Cycle/Project End bounds, active Bed/Object assignments, and note that
  Master inserts placed *after* the Dolby Atmos plug-in do not print into the
  ADM BWF.

### `.logicx` package structure and save safety

- A `.logicx` project is a macOS **package directory** containing
  `Alternatives/000/ProjectData` (binary state), `ProjectInformation.plist`,
  `Alternatives/000/Project File Backups/`, and (in Package mode) `Media/Audio
  Files/`.
- Before major routing, Atmos, or destructive edits, create a reversible
  snapshot via `File -> Project Alternatives -> New Alternative...` (shares
  media without duplicating audio files).
- Never modify files inside an open `.logicx` bundle from shell/Finder, and
  avoid running live sessions from actively syncing cloud folders (risk of
  `ProjectData` corruption or broken asset references).

### macOS Accessibility and UI automation considerations

- Logic Pro provides no official scripting API (no ReaScript/PTSL/LOM).
  Automation relies on macOS Accessibility (AX), Control Surfaces (Mackie
  Control/OSC), or Key Commands.
- **Duplicate channel strips**: Inspector and Mixer can both display the same
  track's controls simultaneously. Bind AX lookups to explicit window titles
  and container hierarchy, never generic first-match faders/buttons.
- **Custom AU editors vs `Controls` view**: third-party AU graphical UIs often
  render via opaque Metal/OpenGL/WebView views hosted over XPC. Switching the
  Logic plug-in window header dropdown from `Editor` to `Controls` exposes
  standard AX-accessible parameter sliders directly when UI inspection or
  exact parameter readback is needed.
- **Plug-in Delay Compensation check**: inspect `Settings -> Audio -> General
  -> Plug-in Latency -> Compensation` (`All` vs `Audio and Software Instrument
  Tracks` vs `Off`). `All` is required for accurate Aux/Bus/Sidechain
  alignment; `Low Latency Monitoring Mode` temporarily bypasses high-latency
  plug-ins on armed/output paths—verify it is OFF during validation bounces.

---

## Part 2: Ableton Live

### Orient and distinguish Live-native concepts

- Confirm Live version, active `.als` Set path and saved state, audio device,
  sample rate, buffer size, transport state, and active view:
  - **Session View** (non-linear clip/scene launcher) overrides **Arrangement
    View** per track whenever a Session clip is triggered; watch for the lit
    **Back to Arrangement** button when Arrangement playback appears ignored.
  - Track types: **Audio**, **MIDI**, **Group Track** (sums child tracks),
    **Return Track** (`A`, `B`, ...; pre/post-fader toggle sits globally per
    Return in the Main/Master section), and **Main / Master Track** (named
    `Main` in Live 12).
- **Read-only `.als` inspection**: an `.als` file is **gzip-compressed XML**.
  On a closed Set (or copy), `gzip -dc Set.als` exposes track names, sample
  rate, routing, device lists, and plug-in identifiers without launching Live.
  Never overwrite an `.als` file that is open in Live.

### Live Object Model (LOM), Control Surface Remote Scripts, and OSC

- **Live Object Model (LOM)**: exposes Live's runtime hierarchy (`live_app`,
  `live_set`, `tracks`, `return_tracks`, `master_track`, `devices`,
  `parameters`, `clip_slots`, `mixer_device`, `view`).
- **Authorized automation planes**:
  1. **Max for Live (M4L)** (`live.path`, `live.object`, `live.observer`,
     `live.remote~`, Node for Max): runs inside the Live Set. Note that
     `live.remote~` modulates parameters in real time without writing Undo
     steps, whereas `live.object set` mutates project state.
  2. **Python Control Surface Remote Scripts** (`~/Music/Ableton/User
     Library/Remote Scripts/` or app bundle `MIDI Remote Scripts/`): loaded at
     Live launch and selected in `Settings -> Link, Tempo & MIDI -> Control
     Surface`. Used by hardware scripts and user-authorized OSC/API bridges
     (e.g., AbletonOSC).
- Verify which Control Surface script and UDP/OSC port are active before
  sending commands, and always read back state via LOM/UI afterward because not
  all Remote Script mutations map cleanly onto Live's single Undo stack.

### Max for Live and multichannel routing constraints

- **Strict 2-channel native mixer**: Ableton Live's Audio, MIDI, Group, Return,
  and Main tracks are **stereo (2-channel) only**. Live does NOT natively route
  5.1, 7.1.4, Ambisonics, or 64-channel buses through standard mixer tracks.
- Inserting a multichannel VST3/AU on a standard Live track connects only
  channels `1–2` (plus optional stereo sidechain input on supported plug-ins).
  True multichannel/spatial audio in Live requires **Max for Live** routing
  (e.g., `mc.*`, `adoutput~`, Envelop for Live, or parallel paired stereo
  tracks routed to discrete hardware/bridge outputs).
- Audit **Audio From / Audio To** tap points (`Pre FX`, `Post FX`, `Post
  Mixer`) and each track's **Monitor** switch (`In`, `Auto`, `Off`). Setting
  `Monitor = In` forces live input monitoring and silences Arrangement/Session
  clips on that track.

### Collect All and Save

- `File -> Collect All and Save` copies referenced external audio files,
  imported samples, and selected library assets into the Set's Project Folder
  (`Samples/Imported/`, `Samples/Processed/`).
- Before archiving, moving a Set, or handing off a diagnostic repro project,
  confirm the `.als` lives in a dedicated Project Folder and run `Collect All
  and Save` (when authorized) to prevent `Media Files Are Missing` failures.

### Track Delay, Delay Compensation, and Reduced Latency When Monitoring

Three timing controls frequently explain unexpected phase/alignment shifts in
Live:

1. **`Options -> Delay Compensation`**: keep **ON** for accurate multi-track
   and parallel processing alignment.
2. **`Options -> Reduced Latency When Monitoring`**: bypasses delay
   compensation on tracks that are actively monitoring (`In`, or `Auto` while
   record-armed) to minimize live performance latency. **Critical validation
   trap**: if left ON during loopback or wet-return testing through an armed
   track, that track shifts out of time relative to unmonitored tracks. Check
   and record this setting explicitly.
3. **Track Delay** (`D` toggle in the bottom-right mixer section): per-track
   positive or negative ms/sample offset. Verify Track Delay is `0 ms` on all
   involved tracks before diagnosing PDC bugs.

### Audio Export and Freeze / Flatten boundaries

- **Export Audio/Video** (`File -> Export Audio/Video...`):
  - **Rendered Track**: `Master`/`Main`, `All Individual Tracks`, `Selected
    Tracks Only`, or a single named track.
  - **Include Return and Master Effects**: useful for quick stems, but running
    each track solo through a nonlinear Master limiter/compressor changes gain
    reduction compared to the full mix.
  - **Technical validation flags**: keep **Normalize = OFF**, **Convert to
    Mono = OFF** (unless mono is explicitly requested), **Dither Options = No
    Dither** for 24/32-bit float intermediate or null-test renders, and verify
    exact Sample Rate, Bit Depth, and Render Start/Length bounds.
  - **Real-Time Export**: Live automatically switches to real-time rendering
    when an active **External Audio Effect** or **External Instrument** device
    is in the rendered path, but offline export will NOT capture arbitrary
    external loopback routing patched outside those devices.
- **Freeze Track vs Flatten**:
  - **Freeze Track**: reversible temporary render of track clips and device
    chain. Cannot freeze tracks containing External Audio Effects/Instruments
    or certain external sidechain dependencies.
  - **Flatten**: **destructive** replacement of the frozen track's devices and
    MIDI with baked audio clips (undoable only within the current session
    history). Duplicate the track or save a new Set version before Flattening.

### Plug-in scanning and logs (VST2 / VST3 / AU)

- Check `Settings -> Plug-Ins` toggles (`Use Audio Units`, `Use VST2 Plug-In
  System/Custom Folder`, `Use VST3 Plug-In System/Custom Folder`).
- **Force deep rescan**: hold **`Option` (macOS)** or **`Alt` (Windows)** while
  clicking **Rescan** to bypass cached skip/mtime entries and rescan all
  plug-ins.
- **Forensic scan logs**: inspect `~/Library/Preferences/Ableton/Live
  <ver>/Log.txt` (macOS) or `%APPDATA%\Ableton\Live <ver>\Preferences\Log.txt`
  (Windows) when a VST3/AU fails to appear or crashes during scan—Live logs
  exact binary paths, scan exclusions, and plugin load failures there.
