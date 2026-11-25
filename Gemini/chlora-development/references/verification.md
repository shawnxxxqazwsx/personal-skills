# Chlora Verification & Target Matrix

Use `CMakeLists.txt`, `cmake/ChloraModulePaths.cmake`, and `ctest -N` in the
active build lane as the source of truth. Run only touched layers plus one
adjacent regression.

## 1. Zero-JUCE Fast Lanes (Run First)

| Scope | Command |
|---|---|
| `network-audio/aes67-core/` | `python3 tools/mc_build_lane.py run --lane aes67-TASK --build-dir build-lane-aes67-TASK -- cmake -S network-audio/aes67-core -B build-lane-aes67-TASK -DCMAKE_BUILD_TYPE=Release && python3 tools/mc_build_lane.py run --lane aes67-TASK --build-dir build-lane-aes67-TASK -- cmake --build build-lane-aes67-TASK -j 4 && python3 tools/mc_build_lane.py run --lane aes67-TASK --build-dir build-lane-aes67-TASK -- ctest --test-dir build-lane-aes67-TASK --output-on-failure` |
| `audio-bridge/chlora-audio-bridge/` | `python3 tools/mc_build_lane.py run --lane hal-TASK --build-dir build-lane-hal-TASK -- cmake -S audio-bridge/chlora-audio-bridge -B build-lane-hal-TASK -DCMAKE_BUILD_TYPE=Release && python3 tools/mc_build_lane.py run --lane hal-TASK --build-dir build-lane-hal-TASK -- cmake --build build-lane-hal-TASK -j 4 && python3 tools/chlora_audio_bridge_install.py "build-lane-hal-TASK/Chlora Audio Bridge.driver"` *(dry-run check; live install requires explicit authorization + `sudo ... --install --replace`)* |
| `meris/meris_mimo_server/` | `PYTHONPATH=meris python3 -B -m unittest meris/meris_mimo_server/test_free_mimo_server.py -v` |
| WebUI / Catalog / Portable Core | `node --check <changed>.js` · `tests/*.mjs` · `cmake -S . -B build-lane-core-TASK -DMC_PATCHER_BUILD_JUCE_BRIDGE=OFF` (via `mc_build_lane.py`) |

## 2. JUCE Build Lanes (Offline Donor Configure)

```bash
python3 tools/mc_build_lane.py run --lane host-TASK --build-dir build-lane-host-TASK -- \
  cmake -S . -B build-lane-host-TASK -DCMAKE_BUILD_TYPE=Release \
    -DMC_PATCHER_BUILD_JUCE_BRIDGE=ON -DMC_HOST_BUILD_X86_WORKER=OFF \
    -DFETCHCONTENT_FULLY_DISCONNECTED=ON \
    -DFETCHCONTENT_SOURCE_DIR_JUCE="$PWD/build-juce/_deps/mc_juce_framework_donor-src" \
    -DFETCHCONTENT_SOURCE_DIR_MC_FILEGRAPH_BOOST="$PWD/build-juce/_deps/mc_filegraph_boost-src" \
    -DFETCHCONTENT_SOURCE_DIR_MC_LIBADM="$PWD/build-juce/_deps/mc_libadm-src" \
    -DFETCHCONTENT_SOURCE_DIR_MC_LIBBW64="$PWD/build-juce/_deps/mc_libbw64-src"

python3 tools/mc_build_lane.py run --lane host-TASK --build-dir build-lane-host-TASK -- \
  cmake --build build-lane-host-TASK -j 4 --target McHost ChloraRouteService chlora
```

## 3. Exact `CMake --target` vs `CTest -R` / Direct Execution Matrix

Build `EXCLUDE_FROM_ALL` test targets explicitly via `--target` before running
`ctest -R` or executing the binary:

| Module | CMake `--target` | CTest (`ctest -R`) / Direct Run |
|---|---|---|
| `shared/` SHM/IPC | `mc_ipc_smoke`, `mc_shm_audio_tests` | `ipc_smoke`, `instance_claim` *(serialize the 11 `MC_PATCHER_FIXED_SHM_TESTS` — see `parallel-development.md` §4)* |
| `host/` app, sandbox, perf | `McHost`, `McHostPluginWorkerNative`, `mc_host` | `host_.*perf_verify\|bridge_session_snapshot\|bridge_host_claim\|host_graph_wire_` |
| `draftroom/` IR, Stack, Analyzers | `mc_host_ir_loader_dsp_verify`, `mc_host_level_meter_verify`, `mc_host_nebula_core_verify`, `mc_host_spectrogram_verify` *(plus static libs `mc_host_{ir_loader,stack,level_meter,nebula,spectrogram}`)* | `host_ir_\|advanced_stack_\|host_level_meter_\|host_nebula_\|host_spectrogram\|spectrum_` |
| `darkroom/` FileGraph, ADM, Repair | `mc_file_graph_audio`, `mc_host_file_*` | `host_file_(graph\|repair)\|adm_static_monitor\|host_file_graph_adm` |
| `audio-bridge/` Chloe & Device I/O | `McBridge_VST3`, `McBridge_AU`, `ChloraRouteService`, `mc_host_device_io_verify` *(`EXCLUDE_FROM_ALL`)* | `^host_device_io$` (+ PluginVal `>= 5` for VST3 lifecycle changes) |
| `network-audio/` AVB & AES67 | `chlora_avb_device_io_verify`, `chlora_aes67_device_io_verify` *(`EXCLUDE_FROM_ALL`)* | `^chlora_(avb\|aes67)_device_io$` (+ standalone `aes67-core` 5 CTests) |
| `meris/` measurement & calibration | `mc_host_meris_pure_fr_verify` *(`EXCLUDE_FROM_ALL`)*; direct-only (`EXCLUDE_FROM_ALL`, no CTest): `mc_host_measurement_mimo_e2e_verify`, `mc_host_meris_pink_noise_graph_verify`, `mc_host_meris_ir_verify`, `mc_host_meris_device_io_routing_verify`, `mc_host_mic_input_verify` | CTest: `^host_meris_pure_fr_verify$`; run direct-only binaries from `<build-dir>/<target>` |
| `control/` CLI & MCP | `chlora`, `mc_chlora_control_service_verify` | `^chlora_control_` (`service`, `cli`, `parity`, `catalog`, `mcp`, graph/analyzer control) |

- Local plug-in probes (`mc_host_load_smoke`, `mc_host_engine_verify`) are
  opt-in via `-DMC_PATCHER_ENABLE_LOCAL_PLUGIN_TESTS=ON`; report missing local
  plug-ins as an unavailable prerequisite.
- Run large multi-engine native verifiers directly under the default shell
  stack limit in addition to CTest (heap-allocate engines if hitting
  `___chkstk_darwin`).

## 4. Graph & WebUI Interaction Gates

- Separate logical port count from edge multiplicity (e.g. Fanout = 1 output
  port with N edges; Merge = 1 input port with N internal branches) and verify
  simultaneous routes, reconnect, round-trip, and single-edge removal.
- Verify full Frame/Group/Comment lifecycle (create, edit, move, 4-corner
  resize without shrinking user bounds, undo/redo, restore, attached wire
  tracking, atomic container vs content deletion).
- Share one endpoint-geometry function across paint, hit-test, marquee,
  reroute, and drag preview; test real hit-test/drag-finish calls with emitted
  branch identities and channel range.

## 5. Serialized Deployment Command (Coordinator Only)

```bash
python3 tools/mc_build_lane.py run --shared --lane integration-TASK --build-dir build-juce -- \
  cmake --build build-juce --target <mc_deploy_host|mc_deploy_bridge|mc_deploy_bridge_au|mc_deploy_theme_lab|mc_deploy_products>
```
