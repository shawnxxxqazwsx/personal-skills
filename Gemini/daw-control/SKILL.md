---
name: daw-control
description: Safely inspect, operate, troubleshoot, and verify common DAWs (REAPER, Nuendo/Cubase, Pro Tools, Logic Pro, Ableton Live, and other hosts). Use for live host control, track/bus/multichannel routing, plug-in reload, scripting/control-plane operation, transport, rendering, and on-disk signal verification; not for editing source code, modeling hardware DSP, or analyzing spatial-audio acoustics/delivery standards.
---

# DAW Control

Use the DAW as the live host, not as an assumed state. Favor the application's
current semantic UI, user-authorized scripts/APIs, and observable readback over
coordinates, memorized menu paths, or file-name guesses.

## Scope boundary

- **In scope**: live DAW inspection and operation, track/bus/I/O and multichannel
  Pin Connector routing, host-side plug-in scanning/reload, authorized scripting
  or control-surface planes, transport/recording preflight, export execution,
  and objective on-disk signal integrity verification.
- **Out of scope**: modifying plug-in or host source code, modeling hardware
  DSP, spatial-audio acoustics/psychoacoustics or binaural/speaker rendering
  algorithms, room/loudspeaker calibration theory, and normative codec/metadata
  delivery-standard analysis (handle only the host's UI switches, routing slots,
  and export settings here).

## Reference index

Load only the reference guide(s) matching the active DAW and task:

| Reference | When to read |
|---|---|
| [REAPER](references/reaper.md) | REAPER projects, ReaScript (Lua/Python), Web Control HTTP API, `reaper.ini`/`.RPP` audits, 64/128-ch routing & Pin Connector, headless `-renderproject`, SWS/ReaPack, VST3/AU cache & force-rescan |
| [Nuendo & Cubase](references/nuendo-cubase.md) | Nuendo/Cubase Control Room & Cue/Talkback isolation, Group/FX/VCA & Direct Routing, MIDI Remote/Generic Remote/EuCon, built-in Dolby Atmos & ADM BWF switches, VST Plug-in Manager/Blocklist, batch Audio Mixdown, macOS AX/blank-editor checks |
| [Pro Tools](references/pro-tools.md) | Pro Tools Studio/Ultimate, PTSL (gRPC) read/write boundaries, I/O Setup & Film-vs-SMPTE Path Order, Routing Folders/Aux/Master/VCA, AAX cache & rescan, Playback Engine/ADC/Video Engine, Bounce/Commit/Freeze & Atmos ADM BWF switches |
| [Logic Pro & Ableton Live](references/logic-ableton.md) | Logic Pro (`auval`, `AudioComponentRegistrar`, Integrated Dolby Atmos switches, `.logicx` packages, macOS AX) and Ableton Live (LOM/Remote Scripts/OSC, Max for Live stereo-vs-multichannel boundaries, Collect All and Save, Track Delay/Reduced Latency When Monitoring, Export/Freeze/Flatten) |
| [Multichannel Routing & Validation](references/multichannel-routing-and-validation.md) | Host PCM channel layouts & ordering (5.1 Film/SMPTE, 7.1.2, 7.1.4, 9.1.6, HOA AmbiX 1st–7th, discrete 64 ch), PDC & bypass latency traps, loopback/wet-return test signals & level safety, macOS CoreAudio/Aggregate Device clocks, objective render file verification |
| [Other DAWs & Shared Safety](references/common-daws.md) | Studio One, Digital Performer, Bitwig Studio, and other hosts; compact troubleshooting record template |

## Establish the live state first

Before changing anything, identify and report only what matters to the request:

- DAW edition/version, CPU architecture (`arm64` native vs Rosetta / `x86_64`),
  foreground project path and saved state, active project tab/alternative,
  transport state, sample rate, bit depth, and audio device/clock.
- Selected track(s), bus/routing context, channel layout/order, PDC/monitoring
  mode, and whether any armed/input-monitored/record-enabled path is active.
- Exact target plug-in/clip/marker/automation lane, including visible instance
  name, format (`VST3`/`AU`/`AAX`/`CLAP`), and on-disk binary path when
  diagnosing reloads.
- Target acceptance layer: UI readback, signal/routing proof, objective on-disk
  render audit, or human listening decision.

Refresh the relevant surface after each mutation. Bind UI automation to visible
application/window/element identity, not a stale window ID, fixed coordinate,
or merely the first similarly named plug-in. If another task may be driving a
DAW window, stop on ambiguity rather than stealing focus or sending blind keys.

## Act in a reversible, narrow scope

The user's task authorizes only its necessary DAW actions. Prefer one visible,
reversible change, then inspect its resulting state before batching equivalent
changes. Preserve unrelated selection, routing, plug-in chains, automation,
media, project preferences, and global DAW settings.

Do not describe an action as reversible until it has actually entered the
project's undo history. Before destructive operations (replacing source media,
deleting tracks/plug-ins, flattening/commit, overwriting a render, changing
session-wide rate/tempo, or saving over another version), resolve the exact
targets and create a recoverable copy/version when authorized; ask if ambiguous.

Never start recording, playback through an unknown physical path, loudness
calibration, hardware control, audio-device/clock/routing changes, or external
export/upload merely because a DAW is open. Explicit scope must cover the
affected device, monitoring state, destination, and program; a stopped
transport does not prove hardware monitoring is safe.

## Plug-ins, reloads, and multichannel paths

Record the in-host instance and track/bus/channel layout before editing a
plug-in. Preserve host pin/bus mapping and never silently collapse surround,
Atmos, Ambisonics, sidechain, or discrete channels to stereo; verify via
host-visible I/O/pin info rather than the plug-in's own labels.

An installed VST3/AU/AAX build, file hash, scan result, or offline host test
does not prove that a running DAW loaded it. If the project is untitled or has
unsaved changes, ask the user to save it and resolve the Save As destination
before closing, restarting, or rescanning the DAW. After reload, verify the
fresh instance's identity/version and keep old in-memory vs reloaded instances
distinct in the report.

For an external audio bridge or hosted graph (e.g., Chlora/Chloe), verify both
DAW-side bus negotiation and the bridge/graph's wet return separately.

## Validate the requested claim

Choose the smallest evidence that actually addresses the task:

| Claim | Minimum observation |
|---|---|
| UI/control operation | Visible control readback and intended target identity |
| Track/bus routing | Both sending and receiving endpoints, channel mapping/order, and meter/signal observation when safe |
| Plug-in load/reload | Host-visible instance after rescan/restart, with active format, architecture, and channel layout |
| Automation/edit | Affected lane/item and changed point/range readback; untouched regions preserved |
| Offline render/export | Exact output path, bounds/source, format, completion status, and objective on-disk file audit; no silent overwrite |
| Audio behavior | Controlled signal measurement or an explicitly stated human listening observation |
| Recording/hardware path | Explicit device authority, armed source/destination, safe monitoring, take/file receipt, and post-stop disarm state |

Never promote screenshots, menu state, meters, automation writes, or an offline
render to an unperformed listening, DAW reload, physical-device, or release
claim; state any unverified layer plainly.

## Recovery and reporting

If live state diverges, stop issuing actions, capture the visible error and
last confirmed state, and use the narrowest DAW-native recovery (cancel dialog,
undo known op, disable failing target, or reopen a saved version). Never
discard unsaved changes without direction. Report host/project context, exact
targets/actions, verified result, and any unperformed acceptance layer (plus
repro steps, logs, and next safe diagnostic on failure).

## Live verification (`web-research`) and knowledge-base updates

1. **When to invoke `web-research`**: call `web-research` whenever local
   `references/` cannot answer the task or may be stale—such as new DAW
   versions, changed UI/menu paths, updated scripting APIs (ReaScript/PTSL/MIDI
   Remote/LOM), plug-in scan/cache changes, or an uncovered host. Prefer
   primary sources (official vendor/DAW manuals, SDK/API docs, official repos);
   label paywalled/undocumented behavior honestly and never treat unverified
   forum posts as normative truth.
2. **Closed-loop write-back**: after task verification succeeds, merge
   reusable, verified facts into the matching `references/<topic>.md` in place
   (replace outdated rows rather than appending chronological logs). Create a
   new kebab-case `references/<topic>.md` only for a genuinely uncovered DAW
   host or major domain, updating the **Reference index** above in the same
   edit, and attach the primary-source URL + verification date (`YYYY-MM-DD`).
3. **Anti-pollution guardrails**: persist only reusable facts/workflows (API
   signatures, cache paths, version limits, verified flags). Never write
   one-off session logs, local user paths/project names, unverified guesses, or
   paragraphs duplicated across files (cross-link instead), and keep
   version-mutable quirks separate from stable host-safety invariants.
