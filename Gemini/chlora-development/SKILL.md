---
name: chlora-development
description: >-
  Develop, architect, debug, build, review, and deploy code in the Chlora
  repository across macOS (`main`) and Windows (`windows`), covering
  Host/Sandbox/WebShell, DraftRoom (Graph, Strip, IR Loader, Analyzers),
  DarkRoom (FileGraph, ADM, Spectral Repair), Audio Bridge (Chloe VST3/AU,
  Chlora Audio Bridge HAL, Windows Chlora Audio ASIO/WaveRT,
  ChloraRouteService, Device I/O), Network Audio (AVB/Milan, AES67), Meris
  MIMO calibration, and `chlora` CLI/MCP. Trigger on any code, CMake, test,
  multi-agent slice, or deployment task targeting Chlora; do not trigger for
  UI visual design specifications, generic DAW operation, Pigora hardware-EQ
  fitting, spatial-audio standards theory, standalone third-party audio
  plug-ins, or generic JUCE/VST3 questions.
---

# Chlora Development

```text
DAW <-> Chloe VST3/AU <-> POSIX SHM IPC <-> Chlora Host (DraftRoom / DarkRoom / Meris)
System / Network <-> Chlora Audio Bridge (macOS) / Chlora Audio (Win) / ChloraRouteService / AVB / AES67 <-> Device I/O
```

Start every task with `git branch --show-current && git status --short`.
`AGENTS.md`, `CMakeLists.txt`, `cmake/ChloraModulePaths.cmake`, and
`docs/architecture.md` are the source of truth.

## 1. Platform Branches

- **`main`** = macOS Chlora; **`windows`** = Windows Chlora (Meris client +
  `Chlora Audio` ASIO/WaveRT driver). Both keep the same module hierarchy.
- Push macOS changes to `main` and Windows changes to `windows`.
- Work on the other platform in a sibling `git worktree` (`../chlora-windows`
  or `../chlora-win-<task>`) and sync shared modules by cherry-picking pure
  shared commits.

## 2. Module Hierarchy & Naming

Place every file in its owning major/minor module directory:

| Major Module | Minor Submodules | Registration Hook for New Submodules |
|---|---|---|
| `host/` | `app`, `engine`, `sandbox`, `stub`, `web-shell` (+ `ui/`) | `cmake/ChloraModulePaths.cmake` (+ `HostWebChrome.h` if `ui/`) |
| `draftroom/` | `graph`, `strip`, `nodes`, `ir-loader`, `analyzers/{common,level-meter,nebula,spectrogram}` | Same + `cmake/Host<Module>.cmake` |
| `darkroom/` | `workspace`, `sources`, `playback-monitor`, `adm`, `repair`, `recovery` | Same + `cmake/HostFileGraph*.cmake` |
| `audio-bridge/` | `chloe-plugin`, `chloe-host`, `chlora-audio-bridge` *(macOS)*, `chlora-audio` & `chlora-mix` *(Win)*, `route-service`, `app-takeover`, `device-io` | Same + standalone driver `CMakeLists.txt` |
| `network-audio/` | `avb`, `aes67-core`, `aes67-host` *(macOS `main`)*, `aes67-bridge-win` | Same + `network-audio/aes67-core/CMakeLists.txt` |
| `meris/` | `measurement`, `ui`, `meris_mimo_server` *(macOS `main`)*, `docs` | Same + `CMakeLists.txt` (`mc_host_meris_sources`) |
| `control/` | `cli`, `catalog`, `host-service` | `cmake/ChloraControl.cmake` + `control/catalog/commands.v1.json` |
| `shared/` | `include/mc`, `third_party` (`clap/`, plus `asio/` on `windows`) | Header-only ABI (`mc/*.hpp`); version deliberately |

- **New sub-feature:** add a kebab-case submodule under its owning major module
  (with `ui/` for module WebUI assets) and wire its registration hook above.
- **New product domain:** add a top-level kebab-case major module with
  submodules, register it in `cmake/ChloraModulePaths.cmake`, and update
  `README.md` and `docs/architecture.md`.
- **Naming:** Use product names (`Chlora`, `Chloe`, `Chlora Audio Bridge`,
  `Chlora Audio`, `ChloraRouteService`, `chlora`, `DraftRoom`, `DarkRoom`,
  `Meris`) for modules, files, UI, and docs; existing CMake/IPC identifiers are
  `McHost`, `McBridge_{VST3,AU}`, `mc_deploy_*`, `MC_PATCHER_*`, and
  `/mc_patcher_<id>`.

## 3. Multi-Agent Parallel Development & Deployment

For `>= 2` parallel agents, shared hub edits, new build lanes, deployment, or
`main`↔`windows` sync, read
[references/parallel-development.md](references/parallel-development.md).

1. **Disjoint leases:** One writer per submodule, file, behavior, build lane,
   or live controller. Scope status, diffs, and staging to leased paths
   (`git status --porcelain -- <lease>` / `git diff -- <lease>`).
2. **Serialized hubs:** Parallel workers return a declarative **Hub Patch
   Spec** instead of editing shared hub files directly (15-hub list in
   `references/parallel-development.md`).
3. **Isolated build lanes & coalesced deploy:** Run all CMake/CTest through
   `tools/mc_build_lane.py` (`build-lane-<mod>-<task>` with offline
   `build-juce/_deps/` donors). Parallel workers validate in their own lane;
   the coordinator runs one coalesced deploy on `build-juce --shared` and
   verifies all affected resident processes.
4. **Unified behavior:** Apply node, DSP, state, and UI updates uniformly to loaded and newly created nodes (no legacy-node fallback shims).

## 4. Realtime Safety & Live Sessions

- On audio threads (`processBlock`, HAL IOProc, AVB/AES67/SHM rings,
  `ChloraRouteService`): preallocate for the negotiated multichannel width (up
  to 128 ch), zero allocations/locks/I/O/UI/logging/graph rebuilds, and publish
  control-thread graph updates via atomic snapshots or SPSC rings
  (`shared/include/mc/`).
- Keep `audio-bridge/chloe-plugin/` thin (bus negotiation, transport, state,
  full round-trip + hosted PDC latency) and keep hosted plug-in identity stable
  across shell versions.
- Allow at most one active controller globally for live Chlora/DAW/hardware
  sessions (Primary or the single leased computer-use worker). Run
  mutating tests on copied/scratch sessions; change system audio devices or
  `host/app/MC_HOST_BUILD` only when explicitly requested.

## 5. On-Demand References

| Need | Reference |
|---|---|
| Parallel leases, 15 hubs + HPS, offline donors, 3-tier resource isolation, coalesced deploy, `main`↔`windows` worktree | [references/parallel-development.md](references/parallel-development.md) |
| Zero-JUCE fast lanes, offline donor configure, exact `CMake --target` vs `CTest -R` matrix, Graph/UI gates, `mc_deploy_*` | [references/verification.md](references/verification.md) |
| Live DAW wet-return, plug-in loading, multi-instance state, analyzer/gesture evidence, AVB/RouteService & `lsof` binary identity | [references/runtime-self-verification.md](references/runtime-self-verification.md) |

Report verified layers, branch/module paths, deployed bundle/PID status, and untested DAW, hardware, or Windows MSVC layers.
