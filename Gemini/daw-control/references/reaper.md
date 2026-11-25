# REAPER

## Orient before editing

- Confirm the active project tab and its saved path. REAPER can have several
  project tabs and open FX windows; a title or plug-in name alone is not a
  unique target.
- Inspect the Track Control Panel, Mixer, Routing window/Matrix, and FX chain
  needed for the request. Check record arm, input, monitoring, mute/solo,
  parent send, receives/sends, hardware outputs, and track channel count.
- For media edits, distinguish the source file, take, item, active take,
  take FX, item FX, track FX, and render target. They are separate layers.

## Operate with REAPER-native semantics

- Use stable GUIDs (`TrackGUID`, `FXGUID`) and visible action outcomes rather
  than numeric track indexes or screen coordinates: reordering and folder
  nesting change indexes. Avoid global actions when a selected-item or
  selected-track action is available.
- Inspect the Routing window or Matrix for both ends of a send/receive. Confirm
  source and destination channel pairs, send mode (`Post-Fader`, `Pre-FX`,
  `Pre-Fader (Post-FX)`), sidechain target channels, and whether Parent Send is
  deliberately enabled or disabled.
- In the FX chain, distinguish bypass, offline, wet/dry, parameter automation,
  and preset state. For a plug-in replacement, preserve routing/pins and record
  the old/new instance state before removal.
- When changing envelopes, reveal the correct lane and verify the time range,
  point shape, and target parameter. Avoid moving underlying items unless the
  task says to ripple or move them.

## 64-channel (and 128-channel) track routing and Pin Connector matrix

REAPER supports up to 64 channels per track in REAPER 6 and up to 128 channels
per track in REAPER 7, but tracks default to 2 channels until widened.

- **End-to-end channel width**: inserting a multichannel plug-in (e.g., 7.1.4 =
  12 ch, 3rd-order HOA = 16 ch, 64 ch bridge) does not automatically expand
  parent folders or Master. Verify `Track Channels` (`I_NCHAN`) on the source
  track, every parent folder track, receiving bus tracks, and the Master track
  (`MASTER_NCH`). Any narrower intermediate track silently drops upper channels.
- **Pin Connector matrix (`N in M out` button in FX window)**:
  - Verify both input pins (track channels -> plug-in inputs) and output pins
    (plug-in outputs -> track channels). Never infer multichannel processing
    from a stereo track meter.
  - Check **Zero out unmapped output channels** vs pass-through behavior: on a
    wide track (e.g., 12 ch or 64 ch), a stereo plug-in passes unmapped
    channels `3..N` through dry by default unless explicitly zeroed or mapped.
  - Check **VST3 bus size** (right-click the `in/out` pin button -> `VST3 bus
    size` -> `Auto` vs explicit channel count such as `2`, `6`, `8`, `12`,
    `16`, `64`). Some VST3 plug-ins negotiate Stereo if inserted before the
    track was widened or when `Auto` does not match the intended bus layout.
- **Sidechain routing**: route the key source to destination channels `3/4`
  (auto-widening a stereo track to 4 ch) and confirm the plug-in's auxiliary
  input pins map to channels `3/4`, not main inputs `1/2`.
- **Send/receive bit encoding** (relevant in ReaScript and `.RPP` audits):
  `I_SRCCHAN` / `I_DSTCHAN` encode 0-based channel offset in the low 10 bits,
  `1024` (`0x400`) for mono, `((width / 2) << 10)` for multichannel width > 2,
  and `-1` for audio disabled (MIDI-only send).

## ReaScript (Lua / Python) API patterns

Prefer **Lua** over Python for portable readback and controlled automation: Lua
is built into REAPER, whereas Python requires an explicitly configured Python
shared library under `Preferences -> Plug-ins -> ReaScript`.

### Read-only inspection primitives

- **Project & transport**: `EnumProjects(-1)` (active project handle & path),
  `IsProjectDirty(0)`, `GetPlayState()` (`0` stop, `1` play, `2` pause, `4`
  record), `GetSetProjectInfo(0, "PROJECT_SRATE", 0, false)` and
  `"PROJECT_SRATE_USE"`.
- **Audio device**: `GetAudioDeviceInfo("SRATE")`, `GetAudioDeviceInfo("BSIZE")`,
  `GetAudioDeviceInfo("IDENT_IN")`, `GetAudioDeviceInfo("IDENT_OUT")`.
- **Tracks & routing**: `CountTracks(0)`, `GetTrack(0, i)`, `GetTrackGUID(tr)`,
  `GetTrackName(tr)`, `GetMediaTrackInfo_Value(tr, parm)` (`"I_NCHAN"`,
  `"B_MAINSEND"`, `"I_RECARM"`, `"I_RECMON"`, `"B_MUTE"`, `"I_SOLO"`),
  `GetTrackNumSends(tr, cat)` (`-1` receive, `0` send, `1` hardware out), and
  `GetTrackSendInfo_Value(tr, cat, idx, parm)` (`"I_SRCCHAN"`, `"I_DSTCHAN"`,
  `"I_SENDMODE"`, `"D_VOL"`, `"B_MUTE"`).
- **FX chain & pins**: `TrackFX_GetCount(tr)`, `TrackFX_GetFXName(tr, fx)`,
  `TrackFX_GetFXGUID(tr, fx)`, `TrackFX_GetEnabled(tr, fx)`,
  `TrackFX_GetOffline(tr, fx)`, `TrackFX_GetIOSize(tr, fx)`,
  `TrackFX_GetPinMappings(tr, fx, isOutput, pin)` (returns low32/high32 masks
  for ch 1–64; add `0x1000000` for ch 65–128 in REAPER 7), and
  `TrackFX_GetNamedConfigParm(tr, fx, key)` (`"fx_ident"`, `"fx_type"`,
  `"pdc"`, `"vst_chunk"`).
- **Items & takes**: `CountTrackMediaItems(tr)`, `GetActiveTake(item)`,
  `GetMediaItemTake_Source(take)` + `GetMediaSourceFileName(src)`,
  `TakeFX_GetCount(take)`.

### Controlled mutation safety

- Treat ReaScript as a mutating control plane; run mutating scripts only within
  explicit task authorization.
- Resolve targets by `TrackGUID` / `FXGUID` (not transient selection or index).
- Wrap all edits in `Undo_BeginBlock()` ... `Undo_EndBlock("desc", -1)` so the
  mutation enters REAPER's undo history cleanly; use `PreventUIRefresh(1/-1)`
  and `UpdateArrange()` / `TrackList_AdjustWindows(false)` when changing layout.
- Look up non-native action IDs dynamically via `NamedCommandLookup("_SWS_...")`
  or `NamedCommandLookup("_RS...")` and invoke via `Main_OnCommandEx(cmd, 0,
  proj)`. Never hardcode dynamic numeric IDs for scripts or extensions.
- Re-read mutated state after execution; a zero error code from a script does
  not prove the expected routing or audio result.

## REAPER Web Control (HTTP) interface

Configured under `Preferences -> Control/OSC/web -> Add -> Web browser
interface` (default local port e.g. `8080`, optional username/password).

- **Endpoint pattern**: `GET /_/<CMD>` (semicolon-separated batch commands).
- **Read-only queries**:
  - `GET /_/TRANSPORT` — play state, cursor seconds, repeat flag, beat/time string.
  - `GET /_/NTRACK` and `GET /_/TRACK` (or `GET /_/TRACK/<1-based-idx>`) — track
    name, bit flags (folder/selected/muted/soloed/armed), volume, pan, peak
    meters, send/receive counts.
  - `GET /_/MARKER`, `GET /_/REGION`, `GET /_/GET/<cmd_id>` (toggle state),
    `GET /_/GET/PROJEXTSTATE/<section>/<key>`.
- **Mutating endpoints (require explicit authority)**:
  - Transport actions: `1007` (Play), `1016` (Stop), `1008` (Pause). Never send
    `1013` (Record) without explicit recording authority.
  - Track controls: `SET/TRACK/<idx>/MUTE/<0|1|-1>`,
    `SET/TRACK/<idx>/SOLO/<0|1|-1>`, `SET/TRACK/<idx>/VOL/<val>`, or
    `_<named_action_id>`.
- **Safety boundaries**: Web Control uses plaintext HTTP without TLS and can
  trigger arbitrary REAPER actions. Confirm bind interface/auth before relying
  on it, never issue mutating `GET` calls speculatively, and re-query
  `TRANSPORT` / `TRACK/<idx>` to verify state changes.

## `reaper.ini` and `.RPP` text structure forensics

REAPER's resource directory is typically `~/Library/Application Support/REAPER`
(macOS), `%APPDATA%\REAPER` (Windows), or the portable install folder.

- **`reaper.ini`**: plain INI holding global preferences (`[REAPER]` keys such
  as `vstpath64`, `audiodevice*`, `lastprojs`, `renderclosewhendone`). Inspect
  read-only; never edit while REAPER is running because REAPER overwrites
  `reaper.ini` on exit.
- **`.RPP` project files**: plain-text chunked hierarchy (`<REAPER_PROJECT ...>`
  to closing `>`), safe to audit read-only on closed files or copies:
  - Project header: `SAMPLERATE <hz> <use_flag> <bpm_flag>`, `MASTER_NCH <ch>`,
    `RENDER_FILE`, `RENDER_PATTERN`, `RENDER_FMT`, `RENDER_RANGE <mode> <start>
    <end> <tail_flag> <tail_ms>`, `RENDER_SETTINGS`.
  - Track blocks `<TRACK {GUID}>`: `NAME`, `NCHAN`, `MAINSEND <flag>
    <dst_offset>`, `VOLPAN`, `MUTESOLO`, `REC <arm> <in> <mon> ...`, `HWOUT`.
  - **Receives (`AUXRECV`)**: stored on the *destination* track as
    `AUXRECV <0-based-src-idx> <mode> <vol> <pan> <mute> <mono_sum> <phase>
    <src_ch> <dst_ch> ...` — always check destination tracks when auditing sends.
  - FX blocks `<FXCHAIN>`: `<VST ...>`, `<AU ...>`, `<JS ...>`, `<CLAP ...>`,
    `BYPASS <bypass> <offline> <delta>`, `WAK`, plus base64 state chunks.
- Never hand-edit an `.RPP` that is open in REAPER; saving in REAPER will
  clobber disk edits, and reopening discards unsaved UI state.

## Headless / CLI batch rendering (`reaper -renderproject`)

- **Command**:
  - macOS: `/Applications/REAPER.app/Contents/MacOS/REAPER -renderproject /abs/path/to/project.rpp`
  - Windows/Linux: `reaper -renderproject /abs/path/to/project.rpp`
- **Useful flags**: `-nosplash`, `-newinst` (separate instance; avoid concurrent
  writes to shared `reaper.ini`), `-ignoreerrors`, `-batchconvert <list.txt>`.
- **Mandatory preflight & caveats**:
  - `-renderproject` executes the **exact render settings saved in the `.RPP`**
    (`RENDER_FILE`, `RENDER_PATTERN`, `RENDER_RANGE`, `RENDER_FMT`,
    `RENDER_SETTINGS`). Audit those lines first so you do not overwrite an
    existing deliverable or render unintended bounds/stems.
  - On macOS, REAPER still requires an active GUI/WindowServer session for many
    third-party plug-ins and can stall on modal dialogs (missing media, license
    prompts). Enforce a timeout and check exit status plus output file metadata.
  - Offline `-renderproject` will NOT capture live hardware inserts or external
    real-time audio bridges unless the project is configured for Online Render
    and the external path is active.

## SWS and ReaPack extension detection

- **On disk**: inspect `<resource_path>/UserPlugins/` for
  `reaper_sws-*.dylib`/`.dll` and `reaper_reapack-*.dylib`/`.dll`.
- **In ReaScript**: check `reaper.APIExists("CF_GetSWSVersion")` (or
  `NamedCommandLookup("_SWS_...") ~= 0`) for SWS, and
  `reaper.APIExists("ReaPack_BrowsePackages")` for ReaPack.
- Never assume SWS (`_SWS_*`, `_BR_*`, `_XENAKIOS_*`) or ReaPack scripts exist;
  probe first and fall back to native REAPER APIs/actions when absent.

## VST3 / AU cache, reload, and force-rescan

- **Cache files in `<resource_path>/`**:
  - `reaper-vstplugins_arm64.ini` (Apple Silicon macOS) /
    `reaper-vstplugins64.ini` (Intel macOS & Windows x64). Format:
    `<filename>=<timestamp_hex>,<uid>,<display_name>`. An entry missing the
    display name after the comma marks a failed or skipped scan.
  - `reaper-auplugins_arm64.ini` / `reaper-auplugins64.ini` (macOS AU cache).
  - `reaper-clap-arm64.ini` / `reaper-clap-win64.ini` (CLAP cache).
- **Rescan modes** (`Preferences -> Plug-ins -> VST -> Re-scan`):
  1. `Re-scan VST paths for new/modified plug-ins`: fast mtime-based check; can
     miss rebuilt `.vst3` bundles whose outer directory mtime did not change.
  2. `Plug-ins that failed to scan`: targeted retry of previously failed
     binaries without clearing the full cache.
  3. `Clear cache and re-scan VST paths for all plug-ins`: full rescan (slow).
  4. Targeted cache eviction (when REAPER is closed): delete only the single
     plug-in's line from `reaper-vstplugins_*.ini`, then relaunch REAPER.
- **Reload discipline**: on macOS, a full REAPER process restart is required to
  guarantee `dlopen` maps a freshly replaced `.vst3`/`.component` binary. After
  reload, verify a fresh instance in the FX chain, its architecture/version,
  and its live I/O pin arrangement.

## Rendering and verification

- Before interactive rendering, read the Render dialog's source (`Master mix`,
  `Stems`, `Selected tracks`, `Selected media items`, `Region render matrix`),
  bounds, tail, sample rate, channels, format, output location, and filename
  policy (`Silently increment` vs `Overwrite`).
- Verify rendered files objectively on disk (see
  [multichannel routing and validation](multichannel-routing-and-validation.md)).

## Useful diagnostic split

When a plug-in or route "does nothing," separately test whether it is:

1. Not receiving audio (source, arm/monitor, item/take, mute/solo, send).
2. Receiving but bypassed/offline/at zero wet gain.
3. Processing into the wrong channels, narrowed folder/Master bus, or unmapped
   Pin Connector outputs.
4. Running an old in-memory binary/instance.
5. Producing signal that requires listening or a real-time meter to judge.
