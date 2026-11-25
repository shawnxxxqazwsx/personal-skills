# Other DAWs and Shared Safety

Use the dedicated guides for [REAPER](reaper.md),
[Nuendo/Cubase](nuendo-cubase.md), [Pro Tools](pro-tools.md),
[Logic Pro and Ableton Live](logic-ableton.md), and
[multichannel routing and validation](multichannel-routing-and-validation.md).
Use this reference for other hosts (Studio One, Digital Performer, Bitwig
Studio, etc.) and the compact troubleshooting record template.

## Map comparable concepts, not menu names

For Studio One, Digital Performer, Bitwig Studio, Ardour, FL Studio, or another
host, locate the native equivalents of project/session, track type, channel
format, I/O/routing, insert/device chain, automation mode, transport/record
state, and render/bounce rather than substituting commands from another DAW.

- **Studio One**: Song vs Project (mastering) vs Show pages; Audio/Instrument/
  Bus/FX/VCA channels; Event vs Part; Console inserts/sends/post-fader inserts;
  Listen Bus; Transform to Audio vs Export Stems/Mixdown.
- **Digital Performer**: Track vs V-Rack vs Aux/Master Fader; Soundbite vs
  Clip; Bundle I/O assignments; Chunks (multiple sequences in one project);
  Bounce to Disk.
- **Bitwig Studio**: Arranger vs Clip Launcher; Hybrid Tracks; Group/Effect/
  Master tracks; device chains & modulators; Bounce vs Bounce in Place;
  per-plugin sandboxing modes (individual vs bit-bridge vs by vendor—critical
  when verifying plug-in reloads).
- **Cross-host invariants**: verify native track channel width (stereo-only vs
  surround/Atmos/discrete multichannel), supported plug-in formats
  (`VST3`/`AU`/`AAX`/`CLAP`), and whether external hardware/bridge loops
  require Real-Time export instead of Offline render.

## Live recording preflight (when authorized)

1. Confirm input/source, target path, monitoring destination, clock/sample
   rate/buffer, and current arm/transport state.
2. Arm only authorized tracks and enable only authorized outputs with feedback
   loops isolated and safe monitor gain.
3. Stop transport after capture, disarm tracks, and verify the recorded take
   file on disk.

## Compact troubleshooting record

When an issue persists, capture these 5 items for clean reproduction:

1. **Host & engine**: DAW edition/version, CPU arch (`arm64`/Rosetta/`x86_64`),
   sample rate, bit depth, buffer, audio device/clock, saved state.
2. **Routing**: target track/bus, channel layout/order, PDC & monitoring mode.
3. **Plug-in**: format (`VST3`/`AU`/`AAX`/`CLAP`), on-disk binary path, and
   loaded instance identity/version.
4. **Repro & output**: exact steps plus visible error/log excerpt.
5. **Verified layer**: what was actually observed (UI readback, meter, on-disk
   file audit, real-time playback, or human listening).
