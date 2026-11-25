# Chlora Runtime Self-Verification

Select only the section matching the reported runtime behavior.

## Audio, Wet Return, & Manual DAW Path

- Record DAW & version, deployed Chloe build + restart/rescan status, sample
  rate, block size, negotiated channel layout, instance ID, Chlora build, and
  hosted plug-in identity.
- Verify Chlora wet-return and PDC alignment across the reported realtime or
  offline path: align gain, latency, and channel order before measuring
  discontinuities, dropped/repeated blocks, timing offsets, PDC transitions,
  dry/wet mount, steady state, editor open/close, and teardown.

## Hosted Plug-in Loading & Channel Capability

- Identify the exact bundle, architecture, format, shell child, and binary.
- Instantiate the negotiated layouts and process audio far enough to separate
  accepted-but-silent layouts from working layouts; keep one working plug-in as
  an adjacent regression.
- Verify UI refresh, audio continuity, editor lifecycle, failure cleanup, and
  crash containment separately.

## State, Multi-Instance, & Graph

- Reproduce with the reported instance count and ordering on a copied or
  scratch session. Verify stable instance ID, plug-in state, routes, channel
  counts, mixer values, route-specific parallel PDC, and per-instance undo.

## WebUI, Gestures, & Analyzers

- Trace gesture defects (drag, click, wheel, keyboard) through the native
  bridge and execute the real physical gesture in the deployed Chlora/DAW
  session, restoring any fixture afterward.
- For analyzer fidelity (Level Meter, Jelly (formerly Nebula), Spectrogram,
  Meris plots), freeze
  an observation contract (binary ID, routing, material/window, SR/block,
  physical plot rectangle, display scale), test mid/high tone pairs or harmonic
  combs plus a low-frequency regression, and verify both renderer data arrays
  and native-scale onset/steady/release crops.
- Verify third-party editor focus, close/reopen, fullscreen, and drag/pan/undo
  latency against a repeatable baseline under the single active live
  controller.

## Network Audio & RouteService

- Physical AVB (`en19`, `avbdeviced`, `avbutil`) is globally exclusive; request
  explicit authorization before `coreaudiod` / `avbdeviced` restarts or
  disruptive rate/clock-master switches.
- Run local AES67 loopback checks on non-privileged port offsets
  (`--ptp-event-port 43190+N` etc.) without `sudo`.
- After any `ChloraRouteService` / AVB / Device I/O deploy, confirm both
  `Chlora` and `ChloraRouteService` restarted to the new bundle PID.

## Binary Identity

- Confirm `McHostWebAssetIdentity.cmake` (Mach-O embedded `BinaryData` vs
  `Contents/Resources/`) passed with zero deployment warnings.
- Verify executable timestamp, `shasum`, or `strings` symbol markers on every
  deployed bundle (`Chlora.app`, `Chloe.vst3`/`.component`,
  `Chlora Audio Bridge.driver`).
- Inspect running processes with `ps` and `lsof -p <pid>` (`Chlora`,
  `ChloraRouteService`, `ChloraPluginWorker`, DAW) to confirm no pre-deploy
  inode remains mapped before accepting live evidence.
