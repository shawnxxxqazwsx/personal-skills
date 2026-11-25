# Chlora Parallel Development & Deployment

## 1. Worker Domain Lease Block

Embed this 5-line contract in every parallel worker assignment:

```text
[Chlora Domain Lease]
- Branch / worktree: main (macOS) | windows (../chlora-win-<task>)
- Writable lease: <exact submodule dir(s), e.g. network-audio/avb/>
- Frozen contracts: <header/struct/JS-event/JSON schema signatures>
- Build lane: --lane <mod>-<task> --build-dir build-lane-<mod>-<task> (-j 4, offline _deps)
- Verification: --target <targets> | ctest -R '<regex>' | node --check / unittest
```

## 2. Serialized Hub Files & Hub Patch Spec (HPS)

Parallel workers edit only their leased submodule directory. These **15 shared
hub files** are edited serially by the coordinator:
- **CMake:** `CMakeLists.txt`, `cmake/ChloraModulePaths.cmake`,
  `cmake/HostFileGraphAdm.cmake` *(DarkRoom + AES67)*
- **ABI:** `shared/include/mc/*`
- **Host / RouteService:** `host/app/MainComponent.h`,
  `host/engine/PluginHostEngine.h`, `host/web-shell/HostWebChrome.h`
  *(coupled with `CMakeLists.txt`, `ChloraModulePaths.cmake`, `host-surface.html`)*,
  `host/web-shell/HostShell.h`, `audio-bridge/device-io/DeviceIoController.h`,
  `audio-bridge/route-service/ChloraRouteService.cpp`
- **WebUI / Control / Docs:** `host/web-shell/ui/host-surface.html`,
  `control/catalog/commands.v1.json`, `tools/chlora_mcp.py`, `README.md`,
  `docs/architecture.md`

*(Place new module test targets in a dedicated `cmake/Host<Module>.cmake` to
keep `CMakeLists.txt` edits minimal.)*

1. **Freeze:** Coordinator freezes cross-module signatures/schemas before
   dispatch.
2. **HPS return:** When a worker needs hub registration, it returns:
   `Hub Patch Spec: <target hub> | <anchor> | <minimal insertion> | <ordering dep>`.
3. **Scoped acceptance:** Audit and stage strictly by lease path:
   `git status --porcelain -- <lease> && git diff -- <lease>`, then apply HPS
   serially on the coordinator.

## 3. Parallel Build Lanes

All CMake/CTest runs go through `tools/mc_build_lane.py` (`HostVst3Sdk.cmake`
requires `MC_PATCHER_BUILD_LANE_LOCK`). See [verification.md](verification.md#2-juce-build-lanes-offline-donor-configure)
for the full offline configure command.
- Point `FETCHCONTENT_SOURCE_DIR_JUCE` to `build-juce/_deps/mc_juce_framework_donor-src`
  (clean unpatched donor); CMake snapshots it read-only into the lane's `_deps/`
  without locking `build-juce`.
- Pass `-DMC_HOST_BUILD_X86_WORKER=OFF` in dev lanes unless changing x86_64
  sandbox workers.
- Cap parallelism across `K` active lanes at `min(6, floor(cores / K))`
  (typically `-j 4`).
- Exit code **`75`** means the lane is busy; inspect with
  `python3 tools/mc_build_lane.py status --build-dir <dir>`. Remove finished
  one-off `build-lane-*` directories after integration.

## 4. Three-Tier Resource Isolation Matrix

| Tier | Scope | Concurrency Rule |
|---|---|---|
| **Tier 1 — Parallel (No Lock)** | Separate `build-lane-*` builds (`-j 4`); read-only `build-juce/_deps/` donors; `network-audio/aes67-core` 5 CTests; `audio-bridge/chlora-audio-bridge` build + dry-run check; `meris/meris_mimo_server` Python `unittest`; `node --check` & `tests/*.mjs`; PID-scoped offline CTests; user audio-router lanes | Run freely in parallel across agents. |
| **Tier 2 — Offset-Isolated** | `chlora_aes67_cli` loopback (`--ptp-event-port 43190+N --ptp-general-port 43200+N --sap-port 49875+N --rtsp-port 48554+N`); test scratch artifacts (`build-lane-<id>/artifacts/`); `chlora_control_*_verify` temp Unix sockets | Assign disjoint port offsets and scratch paths per lane. |
| **Tier 3 — Serialized (Single Owner)** | `build-juce --shared` & all `mc_deploy_*`; **11 `MC_PATCHER_FIXED_SHM_TESTS`** (`shm_roundtrip`, `bridge_offline_pacing`, `bridge_pdc_hostfx`, `shm_multi_instance`, `instance_latency_alignment`, `shm_multich`, `wet_return_wantret`, `chloe_tap_passthrough_verify`, `click_softness`, `strip_remove_still_audible`, `fanout_wet_correlation` — they `shm_unlink` fixed global SHM names across lanes); physical AVB NIC (`en19`), `avbdeviced`, `avbutil`; `coreaudiod` restart & `sudo` HAL install; UDP `319/320`, `9875`, `5004`, `5353`; live `Chlora`/`ChloraRouteService`/DAW/MCP socket/GUI/`~/Library/Application Support/MC Host/` | Queue strictly on the coordinator or the single live controller; run the 11 fixed-SHM tests in one serialized pass. |

## 5. Coalesced Deployment & Runtime Bundle Topology

| Tier | Deployed Artifacts & Destinations | Owner |
|---|---|---|
| **Independent** | `chlora_aes67_cli`, Python `meris/meris_mimo_server`, build-tree `chlora` CLI, dry-run `chlora_audio_bridge_install.py` check | Any lane |
| **User-space (`build-juce --shared`)** | `mc_deploy_host` → `~/Desktop/Chlora <ver>.<build>.app` *(embeds `Contents/Helpers/{ChloraRouteService,ChloraPluginWorker,ChloraPluginWorkerX86}.app` + `chlora`; WebUI `<submodule>/ui/` flattened into `McHostWebAssets` + `Contents/Resources/`, verified by `McHostWebAssetIdentity.cmake`, dev lookup via `HostWebChrome.h` `kModuleUiDirs[]`)*; `mc_deploy_bridge` → `/Library/Audio/Plug-Ins/VST3/Chloe.vst3`; `mc_deploy_bridge_au` → `~/Library/Audio/Plug-Ins/Components/Chloe.component`; `mc_deploy_theme_lab` → `~/Desktop/MC Host Theme Lab.app`; Windows `cmake/deploy_host_win.py` → `%LOCALAPPDATA%\Programs\Chlora` | Coordinator only |
| **System drivers** | macOS HAL (`audio.chlora.AudioBridge*`): `sudo python3 tools/chlora_audio_bridge_install.py --install --replace "<bundle>"` + authorized `coreaudiod` restart; Windows ASIO/WaveRT: `audio-bridge/chlora-audio/scripts/install_chlora_drivers.ps1` | Explicit user authorization |

**Coalesced deployment workflow:** Workers validate in their own `build-lane-*`
and return a **Deployment Ticket** (affected deploy target, helpers needing
restart, unique visible/symbol marker). The coordinator runs **one** coalesced
deploy on `build-juce --shared`, then verifies:
1. Stdout contains `Installed <dest>` with zero `skipped`/`failed` warnings
   (`McHostInstallDesktop.cmake` and `McBridgeInstallUser.cmake` can warn and
   exit `0`) and `McHostWebAssetIdentity.cmake` passes.
2. `codesign --verify --deep --strict "<bundle>"` and binary `shasum`/`strings`.
3. Restart `Chlora` **and** `ChloraRouteService` (plus `ChloraPluginWorker`/DAW
   when affected) and verify fresh PIDs/inodes per
   [runtime-self-verification.md](runtime-self-verification.md#binary-identity).

## 6. Cross-Platform `main` ↔ `windows` Sync

- Use sibling worktrees (`../chlora-windows` or `../chlora-win-<task>`) for
  Windows branch work.
- Isolate edits to shared layers (`shared/include/mc/`,
  `network-audio/aes67-core/`, `meris/{measurement,ui}/`, `control/catalog/`)
  in pure shared commits and `git cherry-pick <sha>` across platform worktrees.
- Before `git push origin main`, confirm `git diff --name-only origin/main..HEAD`
  contains only macOS/shared paths (zero `audio-bridge/chlora-audio/`,
  `audio-bridge/chlora-mix/`, `shared/third_party/asio/`,
  `cmake/deploy_host_win.py`). State clearly when Windows MSVC/WDK builds or
  `deploy_host_win.py` were not run on macOS.
