# Discover exact Chlora MCP tools & native `clara` CLI

The current connection's schemas (`clara schema <id>` / `chlora_describe_tool`) and bound Host validation are authoritative. This reference maps CLI/MCP discovery, `mcpFamily` search, socket isolation, Host/System tools, and the MCP vs WebUI vs Computer Use decision tree without duplicating the full 198-command catalog.

> **Default tool surface & intentional boundaries**
> - **Tool surface (`compact` vs `full`)**: Native `clara mcp serve --stdio` defaults to the **`compact`** surface (`--profile compact`, 8 entrypoints; pass `--profile full` to expose all 198 commands), whereas `tools/chlora_mcp.py` defaults to **`full`** (pass `--profile compact` to switch).
> - **Intentional read-only / UI-only boundaries**:
>   1. Live `wire.bakedRoute` / `commitGraphBakedWireRoutes` remains WebView auto-debounced and **MCP read-only** (preset-stored `layout.wires` supports up to `4096` rows and `pts` `8..512` floats / `256` point pairs with `(pairs-1)%3 == 0`).
>   2. Level Meter left `Peak/RMS` display toggle (`TP max` is a right-side readout), `Jelly` `Clear` trail & `Angles…` dialog, IR re-import & companion Router wizard, Router one-click `FullPortSnakes`, Finder reveal, and Host MCP toggle remain **UI-only**.
>   3. Standalone VST3 **`CLR Router`** internal non-parameter ValueTree state is excluded from `clara` control; Multi-Mono non-primary lane independent parameter read/write is queued as low-priority follow-up.
>   4. **`CLR-EDGE-03`**: `CLR Router` numeric box out-of-range input strictly rejects and restores the previous value.

Before coordinate layout, call unbound `chlora_get_capabilities({})` (CLI: `clara capabilities get`, `clara capabilities`, or `clara invoke capabilities.get --args-json '{}'`; older Desktop helpers only accept `clara capabilities` without `get` or `clara invoke`) to check the native Host version, renderer readiness, supported mixed plan fields, quality modes and limits. A ready retained renderer can answer geometry while hidden. Canonical compact geometry uses `structuredContent` once and a short text summary; read the structured result for complete coordinates.

## Native `clara` CLI & stdio MCP

The bundled, code-signed native helper `Host.app/Contents/Helpers/clara` executes typed CLI commands and stdio JSON-RPC MCP against a running Chlora Host using the shared `shared/control/commands.v1.json` catalog (198-command surface). No Python/Node runtime or model API key is required.

### Binary lookup order

1. `which clara` (if on `PATH`)
2. `~/Desktop/Chlora*.app/Contents/Helpers/clara`
3. `/Applications/Chlora*.app/Contents/Helpers/clara`

### Core CLI commands

```sh
clara host list --json
clara commands --json
clara schema <command-id>
clara state --socket /tmp/chlora-mcp-<uid>/host-<pid>.sock --json
clara <group> <verb> [--field val ...] [--context-file state.json]
clara invoke <command-id> --args-file arguments.json
clara mcp serve --stdio [--profile compact|full] [--socket /tmp/chlora-mcp-<uid>/host-<pid>.sock]
```

### Key CLI & MCP contracts

- **Profiles**: Native `clara mcp serve --stdio` defaults to **`compact`** (8 entrypoints: 5 direct reads — `chlora_get_state`, `chlora_graph_get_summary`, `chlora_find_plugins`, `chlora_list_plugins`, `chlora_get_operation` — plus `chlora_discover_tools`, `chlora_describe_tool`, `chlora_invoke`). Pass `--profile full` to expose all 198 registered commands directly. The legacy Python adapter `tools/chlora_mcp.py` retains **`full`** as its default (pass `--profile compact` when a small client needs compact mode).
- **CLI vs MCP response envelope**: `clara` CLI returns `{"ok": true, "result": ...}` where command-specific details such as `nodeKey` or `exposedId` sit in `result.mcpResult` (when present). In MCP stdio (`structuredContent`):
  - **Full-state synchronous write tools** (e.g. `chlora_graph_add_builtin`, `chlora_graph_add_merge`, `chlora_graph_level_meter(action="add")`, `chlora_graph_create_group`, `chlora_graph_save_preset`) return the complete Host state in `structuredContent` and place command-specific receipts (`nodeKey`, `groupId`, `presetId`, `revisionToken`, `exposedId`) inside **`structuredContent.mcpResult`**.
  - Only **standalone query / async-status tools** (e.g. `chlora_get_operation`, `chlora_graph_get_preset`, `chlora_graph_list_presets`, `chlora_graph_get_summary`, `chlora_find_plugins`) return flat fields directly at the top level of `structuredContent`.
- **CLI group-name spelling & `--help` / `--context-file`**: `file_graph.control`, `file_graph.project`, and `file_graph.output` all use the unified `file_graph` CLI group (`clara file_graph control`, `clara file_graph project`, `clara file_graph output`). `--help` / `-h` (including `--help -h`) work on `host list`, `commands`, and `schema` as well as typed verbs. `--args-file`, `--args-json`, `--context-file`, and `--profile` can appear before or after the subcommand and reject empty string values `""` (as do `--socket` and `--timeout-ms`). `--context-file state.json` (or `--context-file -` for stdin) is applied after explicit `--field` flags, skips empty string values `""` (so detached/attaching `patchbayStatus.serviceId == ""` is not injected and empty `fileGraph.sourceGraphLifetime == ""` falls back cleanly to top-level `sourceGraphLifetime` or `graphLifetime`), and fills missing `instanceId`/`bindingGeneration`/`graphTopology`/`graphLifetime` AND `sourceGraphLifetime`/`serviceId`/`documentRevision` from a saved state snapshot (on `file_graph.control`, `sourceGraphLifetime` is injected only for source/device commands and scoped `load` — not `new|open|save|show|close|stop|seek`; on `file_graph.project`, `sourceGraphLifetime` is injected only for source/device/automation actions and for `loadSource` only when explicit non-`-2` `index`, `nodeKey`, or `expectedSourceGeneration` is supplied; `instanceId: 0` is skipped when a target command schema requires `minimum >= 1`).
- **Flag spelling**: Typed CLI flags accept both `--field value` and `--field=value` (including negative numbers such as `--target-level-db -18` or `--target-level-db=-18`), as well as exact schema camelCase (`--instanceId`) and generated kebab-case (`--instance-id`; underscores map to hyphens). **Never mix both spellings in one invocation** (rejected as duplicate). Strings pass as text; arrays, objects, booleans (`true`/`false`), and numbers use JSON values. `--args-file -` and `--context-file -` read UTF-8 JSON from stdin (4 MiB local parse limit).
- **Transport limits & timeouts**: Host Unix IPC allows a **64 KiB** request and **4 MiB** reply; global `--timeout-ms` defaults to `5000` (range `1..120000`).
- **Exit codes**:
  - `0`: success
  - `1`: local usage / input / schema error (`clara` runs `Service::validateArguments()` locally before opening the Host socket)
  - `2`: Host rejection
  - `3`: known transport failure
  - **`4`: outcome unknown (`outcome_unknown`) — the request may have reached the Host; NEVER replay a mutating write. Inspect state/operations first (`clara state --json`, `clara operation get --operation-id <id>`).**
- **Per-action strict parameter allowlists (13 umbrella tools / 172 actions)**: All 13 umbrella commands (`repair.playback`, `repair.history`, `repair.graph`, `file_graph.project`, `file_graph.output`, `graph.node_advanced`, `graph.analyzer_control`, `graph.ir_advanced`, `host.manage_system`, `graph.level_meter`, `graph.stack_control`, `graph.ui_control`, `patchbay.control`) enforce symmetric strict per-action required/allowed field validation across C++ Host, `clara` CLI (exit `1`), and `tools/chlora_mcp.py` (JSON-RPC `-32602` before Host dispatch). Mismatched arguments for the chosen `action` are rejected immediately rather than silently ignored.

### Multi-instance socket pinning & isolated QA Hosts

- **Mandatory `--socket` pinning**: Every Chlora process listens on `/tmp/chlora-mcp-<uid>/host-<pid>.sock` (directory `0700`, socket `0600`, same UID). Without `--socket`, `clara` and `tools/chlora_mcp.py` connect **only** when exactly one live Host exists. Whenever `> 1` Host is running, **always pass `--socket /tmp/chlora-mcp-<uid>/host-<pid>.sock`** and verify filesystem identity (`stat -f '%d:%i' /tmp/chlora-mcp-<uid>/host-<pid>.sock` on macOS). Never touch another user or agent session's socket.
- **Isolated background QA Host**: To rehearse or test without disturbing running Hosts, launch a private copy with isolated support/workspace directories using **`Contents/MacOS/Chlora`** (not `McHost`):
  ```sh
  MC_HOST_SUPPORT_DIR=/tmp/<id>/support \
  MC_FILE_GRAPH_WORKSPACE_HOME=/tmp/<id>/workspace \
  CHLORA_ROUTE_HOME=/tmp/<id>/route-home \
  MC_HOST_FILE_GRAPH_ONLY=1 \
    "/path/to/Chlora.app/Contents/MacOS/Chlora" &
  ```
  (`ChloraRouteClient::defaultHome()` reads **`CHLORA_ROUTE_HOME`**, defaulting to `~/Library/Application Support/Chlora Route Service` when unset — always set `CHLORA_ROUTE_HOME` or an isolated `HOME` before exercising Patchbay so you never touch the user's live `ChloraRouteService` daemon.)
  Record its spawned PID, bind exclusively to `/tmp/chlora-mcp-<uid>/host-<spawned-pid>.sock`, and terminate **only** that exact PID when finished. Never use broad `killall` or name-pattern kills. On macOS, CUA app selection or post-quit window observation can relaunch an app; verify the exact PID exited and check `clara host list --json` without re-selecting the closed app.
  **Important startup state & initial endpoints**: Even with `MC_HOST_FILE_GRAPH_ONLY=1`, a freshly started Host opens in `mode: "strip", fileGraph: null`. Call `chlora_file_graph_project(action="new")` or `chlora_file_graph_project(action="open", path="/abs/project.filegraph")` (which auto-detaches Patchbay, normalizes `path` via `realpath`, and opens directly without a chooser) first to enter Standalone FileGraph Graph mode (`instanceId: 0`, `state.mode == "graph"`). Note that `file_graph.project(action="new")` pre-populates **2 default endpoint nodes** (`Chloe Input` + `File Output`), and a fresh Background Patchbay under a new `CHLORA_ROUTE_HOME` likewise starts with **2 default endpoint nodes** (`Device Input` + `Device Output`) — always assert topology by **incremental delta nodes/wires** rather than assuming an empty 0-node canvas. Standalone projects automatically maintain a managed project file at `state.fileGraph.projectFile`; calling `chlora_file_graph(command="save", path="/abs/export.filegraph")` flushes the managed autosave and exports a copy to `path` (which can later be imported/opened via `chlora_file_graph_project(action="open", path=...)`). Also prefer canonical paths (e.g. `os.path.realpath` rather than `/tmp` symlink aliases vs `/private/tmp`) when generating test WAV files so local assertions match `sources[].source.path` readback verbatim (even though `loadSource`/`load` normalize via `realpath` server-side).
- **`chlora_get_state` vs `chlora_graph_get_summary` shape**: `chlora_get_state` exposes `graphNodes[]` and `graphWires[]` whose wire endpoints (`from` / `to`) are integer node `index` values, whereas `chlora_graph_get_summary` exposes `nodes[]` and `wires[]` whose wire endpoints are stable decimal-string `sourceNodeKey` / `destinationNodeKey` values. Both `graphWires[]` (`state.get`) and `graph.get_summary`'s `wires[]` carry optional `bakedRoute: {sig, pts}` when WebView has baked an obstacle-avoiding Bézier path (`commitGraphBakedWireRoutes` is a WebView-only debounced cache, read-only from MCP, and automatically invalidated by C++ when nodes or topology change). `chlora_graph_get_summary` also exposes top-level `sourceGraphLifetime` (when present), `patchbay`, `patchbayStatus`, `graphModulations`, and per-node `isStack`, `stack`, `isLevelMeter`, `levelMeter`, `meterChannels`, `pluginFormatName`/`format`/`formatBadge`, `routerAdvanced`/`routerMatrix`, `channelMasterGainDb`, `isDeviceInput`/`isDeviceOutput`/`deviceIo`/`isChloeInput`/`chloeInput`/`isFileSource`/`isFileMonitor`.
- **macOS sandbox `unix_sockets` rule** (for read-only sandboxed CLI clients):
  ```toml
  default_permissions = "clara_local"

  [features.network_proxy]
  enabled = true

  [permissions.clara_local]
  extends = ":read-only"

  [permissions.clara_local.network]
  enabled = true
  mode = "limited"
  domains = {}
  unix_sockets = { "/tmp/chlora-mcp-<uid>/host-<pid>.sock" = "allow" }
  ```

## `mcpFamily` search mapping (`compact` profile)

In `compact` profile, pass `family` to `chlora_discover_tools({"query": "...", "family": "..."})` to avoid truncated or missed results across the 198-command catalog:

| `mcpFamily` | Included command domains |
|---|---|
| `graph` | All `chlora_graph_*` tools (plug-ins including `chlora_graph_insert_plugin_on_wire`, built-ins, routing, LFO, IR Loader + `chlora_graph_ir_advanced`, Analyzers + `chlora_graph_analyzer_control` [`setSpectrogramMeterTarget`, `Jelly`/`nebula`, etc.] / `chlora_graph_level_meter` [`setTargetLevel`, etc.] / `chlora_graph_set_spectrogram_*` / `chlora_graph_get_spectrogram_frame`, `chlora_graph_node_advanced`, `chlora_graph_stack_control`, `chlora_graph_ui_control`, Stack, Group, Comment, Cable Pins, Layout, Presets, View preferences) **AND all 10 DarkRoom Audio Repair commands (`chlora_repair_*`, `repair.*` belongs to `mcpFamily: "graph"`)** |
| `session` | Capabilities/state/operation (`chlora_get_capabilities`, `chlora_get_state`, `chlora_get_operation`), session lifecycle (`select`/`open`/`close`), mixer gain/mute/solo/bypass/layout/undo/redo, Host preferences (`chlora_get_host_preferences`, `chlora_set_host_preferences`), `chlora_manage_system`, Standalone FileGraph (`chlora_file_graph`, `chlora_file_graph_project`, `chlora_file_graph_output`), and Background Patchbay (`chlora_patchbay_control`) |
| `strip` | All 16 `chlora_strip_*` commands (Multi Channel / Multi Mono slot load/remove/move/bypass/span/layer/retry/open_editor/parameters/Q-Link/Strip routes) |
| `catalog` | `chlora_list_plugins`, `chlora_find_plugins`, `chlora_rescan_plugins`, `chlora_set_plugin_grouping`, `chlora_set_plugin_favorite`, `chlora_set_plugin_preferred_channels` |

Workflow in `compact` mode:
1. `chlora_discover_tools` with a concise `query` and matching `family` (`graph` | `session` | `strip` | `catalog`).
2. `chlora_describe_tool({"action": "chlora_..."})` to inspect the exact schema.
3. `chlora_invoke({"action": "chlora_...", "arguments": {...}})` to execute.

Do not treat a truncated `compact` discovery list as a missing capability; conversely, a native UI feature without a registered command in `clara commands --json` / `commands.v1.json` remains unsupported through MCP.

## Operation owners

- Built-in nodes, containers, analyzers, LFO, IR Loader, FileGraph overview: [nodes.md](nodes.md).
- DarkRoom Audio Repair (`chlora_repair_*`, locks, Mono graph, presentation commit gate, render/import): [darkroom-repair.md](darkroom-repair.md).
- Serial/parallel/subset/Stack/IR/LFO routing fastpaths & `graph_plan.py`: [fastpaths.md](fastpaths.md).
- Sidechain, sparse reordering, Multi-Mono wrappers, LFO modulation edges, recovery: [graph-recipes.md](graph-recipes.md).
- Gain, Solo/Mute/Polarity, Bypass, Strip, hosted parameters, Q-Link, system/editor actions: [controls-and-plugins.md](controls-and-plugins.md).
- Preset revisions, library folder config, stored vs live identities: [presets.md](presets.md).
- Renderer geometry, wire Pins, view settings & `graph_layout.py`: [layout.md](layout.md).
- Reverb Bank `.irmatrix.json` specification, `ir_bank.py`, `chlora_graph_ir_advanced`: [ir-banks.md](ir-banks.md).

## Session, Catalog, System & Preferences controls

### Session, Undo/Redo, and Layout tokens
- `chlora_open_session(instanceId)`, `chlora_select_session(instanceId)`, `chlora_close_session(session binding)`: open/select require a live Chloe producer and refresh `bindingGeneration`. Closing persists that session and stops Host processing.
- `chlora_set_mode(session binding, mode: "graph"|"multiChannel"|"multiMono", allowPluginLoss?)`: `allowPluginLoss: true` can discard processing/undo history; use only when explicitly requested.
- `chlora_clear_all(session binding, confirm: "clear")`: resets session plug-ins and processing.
- `chlora_set_channel_layout(mode: "native"|"unified"|"immersive"|"auro")`, `chlora_set_speaker_adaptation(enabled)`, `chlora_set_insert_channels(channels)`, `chlora_set_output_channels(channels)`, `chlora_set_input_channel_name(channel, text)`, `chlora_reset_input_channel_names`: all require `session binding` + current `channelLayoutToken`. Multi Mono locks Insert to Output; a linked Bridge can republish Output width.
- `chlora_undo` / `chlora_redo(session binding)`: accepts `instanceId >= 0` (hosted sessions and Standalone FileGraph `0`). History restoration is asynchronous: if the reply has `stateRestoreInFlight: true`, **poll `chlora_get_state` until `stateRestoreInFlight` becomes `false`** before reading new node keys, tokens, or issuing any write. In Standalone FileGraph (`instanceId: 0`), `chlora_file_graph(command="undo"|"redo")` rolls back File Source / UI history rather than direct MCP graph node additions.

### Host, Catalog, and System tools
- **Catalog**: `chlora_list_plugins({})` (cached catalog), `chlora_find_plugins(query, limit?, format?: "all"|"VST3"|"AudioUnit"|"CLAP")` (CLI ID **`plugins.find`**, `clara plugins find --query EQ` — never `plugins.search`; searches installed plug-ins directly on current Host and preserves `format`/`formatBadge`/`path`), `chlora_rescan_plugins(scope: "new"|"full")` (poll `chlora_list_plugins` until `scanning` is `false`), `chlora_set_plugin_grouping(groupBy: "vendor"|"channels")`, `chlora_set_plugin_favorite(pluginUid, on)`, `chlora_set_plugin_preferred_channels(pluginUid, channels: 0..128)`.
- **Host / Session runtime**: `chlora_set_meter_mode(target: "mixer"|"master", mode: "peak"|"rms")`, `chlora_set_worker_threads(threads: 1..maxWorkerThreads)`, `chlora_reset_perf_max`, `chlora_set_zoom(percent: 75|100|125|150|175)`, `chlora_dismiss_failed_load(loadId)`, `chlora_close_editors`, `chlora_clear_channel_flags(scope: "input"|"output", flag: "mute"|"solo")`, `chlora_clear_channel_selection`. The 11 Standalone-capable `host.*` commands (`clear_all`, `close_editors`, `set_meter_mode`, `set_worker_threads`, `reset_perf_max`, `set_zoom`, `set_plugin_grouping`, `set_plugin_favorite`, `set_plugin_preferred_channels`, `undo`, `redo`) all accept `instanceId: 0` in Standalone FileGraph across both C++ and schema validation.
- **Global Host preferences** (unbound, uses `preferencesToken`):
  - `chlora_get_host_preferences({})` → returns current preferences (including `renderScale`, default `2.0`) and `preferencesToken`.
  - `chlora_set_host_preferences(preferencesToken, ...)`: at least one field among:
    - `themeMode`: `"light" | "dark"`
    - `darkPalette`: `"graphite" | "slate" | "carbon"`
    - `titleFont`: `"charm" | "caveat" | "kalam" | "courgette" | "merienda" | "fraunces" | "lora" | "manrope" | "space" | "barlow-condensed" | "system" | "mono"`
    - `bodyFont`: same 12 values plus `"original"`
    - `alwaysOnTop`: `boolean`
    - `renderScale`: `0.5 | 0.75 | 1 | 1.5 | 2 | 3` (default `2.0`; also included in `preferencesToken` hash)
    - `unifiedChannelSettings`: `{enabled: bool, family: "atmos"|"auro", atmos16: [{role, label?}] (16 items), auro14: [{role, label?}] (14 items)}`
  - Rejected during busy restore/load or stale `preferencesToken`.
- **System, Libraries, Batch Strip & Storage (`chlora_manage_system`)**:
  - Library folders & blocked plug-ins (unbound; optional `instanceId` accepts Standalone `0` and `bindingGeneration` is optional):
    - `action: "getLibraries"` → returns `pluginFolders`, `auPluginFolders`, `clapPluginFolders`, `auSupport`, `clapSupport`, `pluginBlacklist`, `irBankFolder`, `irBankFolders`, `graphPresetFolder`, `instances`.
    - `action: "addPluginFolder" | "removePluginFolder" | "unblockPlugin" | "setIrBankFolder" | "addIrBankFolder" | "removeIrBankFolder" | "setGraphPresetFolder"`, with absolute `path` (plugin folder actions accept optional `format`: `"VST3" | "AU" | "AudioUnit" | "CLAP"`). Changes to plug-in, IR Bank, and Graph Preset folders automatically persist to Host preferences (and the first `addIrBankFolder` tolerates an uncreated default empty folder).
    - `action: "findBridges"` → refreshes Bridge discovery and returns state.
  - Batch Strip helpers (requires Strip session `instanceId >= 1` + `bindingGeneration`):
    - `action: "selectAllChannels"` → selects all active output/MonoLink channels.
    - `action: "setStripRoutesBatch"`, `stage: "input"|"post"`, `routes: [{input, output}]`, `on: bool` → batch Strip routing in Strip mode.
  - FileGraph Storage cleanup (unbound):
    - `action: "storageInspect"` → returns inventory and fresh `token`.
    - `action: "storageClean"`, `token` (from `storageInspect`), optional `mode: "rebuildableCache"|"trash"` (default `"trash"`), optional `projectIds: [...]`, optional `selection: [{id, version}]` (`mode: "rebuildableCache"` rejects `selection`).

## 3-layer operation decision tree (MCP/`clara` vs WebUI View Tools vs Computer Use)

Always pick the lowest-layer tool that owns the requested operation:

1. **Layer 1 — Data / Topology / Parameters (works headless or hidden via `clara` CLI / MCP)**:
   - Graph creation, wiring, Bundle/Merge/Fanout/Router/Align/Stack (`chlora_graph_stack_control`)/Group/Comment/Pin (`chlora_graph_node_advanced(removeCablePins)`)/LFO/IR Loader/Level Meter (`chlora_graph_level_meter`)/Spectrogram/Nebula, plug-in loading & inline wire insertion (`chlora_graph_insert_plugin_on_wire` / `insertNodeOnWire`) & parameter read/write/expose/bypass, Preset CRUD, offline/geometry layout (`chlora_graph_get_layout_geometry` with ready retained WebUI even while hidden), Strip slots & routing, `chlora_file_graph*`, `chlora_patchbay_control`, `chlora_repair_*`, `chlora_manage_system`, `chlora_get/set_host_preferences`.
   - **Background Patchbay (`chlora_patchbay_control`, CLI `clara patchbay control`)**:
     - Attach & detach: call `chlora_patchbay_control(action="attach", bindingGeneration=...)`, then poll `chlora_get_state` until `state.patchbayStatus.serviceId` is nonempty (top-level `canUndo`/`canRedo` also reflect live Patchbay history). Never call `attach` on a shared machine without `CHLORA_ROUTE_HOME` isolation. A fresh Background Patchbay under an empty `CHLORA_ROUTE_HOME` starts with **2 default endpoint nodes** (`Device Input` + `Device Output`) — verify incremental nodes/wires rather than assuming an empty 0-node graph. Use **`action: "detach"`** (needs only `bindingGeneration`) to exit `routeActive` cleanly back to the local Session or Standalone FileGraph (`bindingGeneration` increments, `graphPresetScope` returns to `"ordinary"`); calling `chlora_select_session`, `chlora_open_session`, `chlora_file_graph(new|open|show)`, or `chlora_file_graph_project(new|select)` also auto-detaches from Patchbay.
     - **Important boundary while attached (`state.patchbay == true`)**: regular `chlora_graph_*` / `chlora_undo` / `chlora_redo` still target the Host's local session, **not** Patchbay. To edit Patchbay topology, undo/redo, or manage Patchbay-scoped presets, use `chlora_patchbay_control`:
       - `action: "graphCommand"`: requires `bindingGeneration`, `serviceId`, `documentRevision` (from `state.patchbayStatus`), `graphLifetime`, `graphTopology`, `operation`, and optional `graphArgs` (do not repeat `instanceId`/`bindingGeneration`/`graphLifetime`/`graphTopology` inside `graphArgs` — the server injects bindings and enforces `(serviceId, documentRevision, persistenceEpoch)` + Takeover guards). Supported `operation`s cover `ChloraRouteGraph`/`ChloraPatchbayEndpoints` `chlora_graph_*` commands (`chlora_graph_add_builtin`, `chlora_graph_add_merge`, `chlora_graph_remove_node`, `chlora_graph_connect_channel`, `chlora_graph_disconnect_channel`, `chlora_graph_connect_bus`, `chlora_graph_connect_snake`, `chlora_graph_disconnect_snake`, `chlora_graph_set_snake`, `chlora_graph_set_wire_style`, `chlora_graph_move_node`, `chlora_graph_resize_node`, `chlora_graph_set_router_*`, `chlora_graph_set_merge_*`, `chlora_graph_set_lfo_*`, `chlora_graph_delete_selection`, plus **Group & Comment** ops: `chlora_graph_create_group`, `chlora_graph_detach_group`, `chlora_graph_set_group_parent`, `chlora_graph_move_group`, `chlora_graph_resize_group`, `chlora_graph_remove_group`, `chlora_graph_set_group_comment`, `chlora_graph_create_comment`, `chlora_graph_set_comment_text`, `chlora_graph_move_comment`, `chlora_graph_resize_comment`, `chlora_graph_remove_comment`) and Patchbay-specific & unified routing ops (`route_graph_unified` covering 88 unified node actions in `ChloraGraphCommands.h`, `route_patchbay_level_meter` [incl. `setGraphLevelMeterTargetLevel`], `route_patchbay_spectrogram_settings` [incl. `setGraphSpectrogramMeterTarget`], `route_patchbay_nebula_settings`, `route_graph_add_io` with `kind: "chloe"|"deviceInput"|"deviceOutput"|"appInput"|"fileSource"|"monitorBus"` + `x, y, channels`, `route_graph_set_io`, `route_patchbay_add_level_meter`, `route_graph_connect_wires`, `route_patchbay_load_plugin` [supports VST3 / AudioUnit / CLAP], `loadGraphStack`, `loadGraphStackPlugins`, etc.; `graphCommand` auto-registers plug-ins into `PluginCatalog.xml` for `route_patchbay_load_plugin` and `loadGraphStack*`; `route_graph_clipboard` is rejected).
       - **Common `graphCommand` pitfalls**:
         - Creating a `Router` via `operation: "chlora_graph_add_builtin"` requires explicit `channels` inside `graphArgs` (e.g. `{"kind": "router", "channels": 2, "x": 750, "y": 400}`; omitting `channels` fails with `"Router requires channels"`).
         - `Level Meter` nodes added by `operation: "route_patchbay_add_level_meter"` (matching `chlora_graph_level_meter(action="add")` in ordinary Graph/FileGraph) default to **`snakeWrapped: true`**. Before wiring one via `"chlora_graph_connect_bus"`, unwrap it first with `"chlora_graph_set_snake"` (`{"nodeKey": "...", "wrapped": false}`); otherwise `connect_bus` rejects with `"Graph bus endpoints do not support an explicit range"`. Conversely, unwrapped (`snakeWrapped: false`) `Router` and `Merge (Sum)` nodes do not support `chlora_graph_connect_bus` explicit ranges either — use `chlora_graph_connect_channel` per channel or wrap/branch with `chlora_graph_connect_snake`.
       - `action: "undo"` / `action: "redo"`: requires `bindingGeneration`, `serviceId`, `documentRevision`, `graphLifetime`, `graphTopology`.
       - **Patchbay clipboard** (all return async `operationId` → poll `chlora_get_operation`):
         - `copySelection` (`bindingGeneration, serviceId, documentRevision, graphTopology, graphLifetime`, nonempty `nodeKeys` or `groupIds`)
         - `pasteSelection` (`bindingGeneration, serviceId, documentRevision, graphTopology, graphLifetime, x, y`)
         - `duplicateSelection` (`bindingGeneration, serviceId, documentRevision, graphTopology, graphLifetime`, nonempty `nodeKeys` or `groupIds`)
         - After `pasteSelection` / `duplicateSelection`, `op.result` automatically passes the `snapshot` sync barrier and returns `detail.nodeKeys`, `detail.groupIds`, and updated `{serviceId, documentRevision, graphLifetime, graphTopology, canUndo, canRedo}`.
       - **Patchbay-scoped preset lifecycle** (all return async `operationId` → poll `chlora_get_operation`):
         - `listPresets` (`bindingGeneration`) → `op.result.detail.presets`
         - `getPreset` (`bindingGeneration, presetId`) → `op.result.detail` (`revisionToken`, `thumbnailDataUrl`, `nodes`, `groups`, `wires` with optional `bakedRoute`)
         - `savePreset` (`bindingGeneration, serviceId, documentRevision, graphTopology, graphLifetime, name, nodeKeys`, optional `groupIds`) → `op.result.detail` (`presetId`, `revisionToken`)
         - `loadPreset` (`bindingGeneration, serviceId, documentRevision, graphTopology, graphLifetime, presetId, x, y`, optional `revisionToken, nodeKeys, groupIds, layout`) → `nodeKeys` accepts **0-based preset-local indices (`"0".."2147483647"`)** matching `getPreset` (unlike `savePreset`/`copySelection`/`duplicateSelection`, which require live keys `"1".."4294967295"`); `insertWire` is not exposed on Patchbay `loadPreset` (ordinary sessions use `chlora_graph_load_preset`). Auto-completes snapshot sync barrier; `op.result` returns `detail.pastedNodeKeys` + updated `{serviceId, documentRevision, graphLifetime, graphTopology, canUndo, canRedo}`
         - `updatePreset` (`bindingGeneration, presetId, revisionToken, layout` [supports `wires`]) → updates Patchbay preset geometry/baked routes and returns new `revisionToken`
         - `renamePreset` (`bindingGeneration, presetId, revisionToken, name`)
         - `deletePreset` (`bindingGeneration, presetId, revisionToken`)
       - **Async receipt contract**: `graphCommand` / `undo` / `redo` return `{operationId, status: "pending", instanceId: 0}`. Poll `chlora_get_operation(operationId)` until `status == "succeeded"`, then read `op.nodeKey` (when a node was created) and `op.result` (`detail` plus updated `serviceId`, `documentRevision`, `graphLifetime`, `graphTopology`, `canUndo`, `canRedo`) for the next chained call.
     - Other actions: `deviceConfigure(serviceId, documentRevision, graphTopology, graphLifetime, nodeKey+deviceId | inputId+outputId)`, `setAudioSettings(graphTopology, graphLifetime, sampleRate, bufferSize)` (`0` = `"Device default"`), `status`, `refreshDevices`, `save`, `load`, `patchApplicationToBridge`, `startTakeover`, and `stopTakeover` (which enforces `serviceId`/`documentRevision` and validates any provided `graphLifetime`/`graphTopology` tokens, rejecting stale tokens) all return async `operationId` (poll `chlora_get_operation`). Only `attach` / `detach` remain synchronous state transitions without `operationId`.
2. **Layer 2 — Visible WebUI Drawers, Windows & View Tools (requires WebUI loaded and visible)**:
   - **`chlora_graph_ui_control`** (`clara graph ui-control`, async `viewOperation` → poll `chlora_get_operation` for `op.result.ui`; note the contrast with async plug-in loads such as `add_plugin` / `insert_plugin_on_wire`, where the newly created `nodeKey` sits at the top level **`op.nodeKey`** of the `chlora_get_operation` reply):
     - `getUiState` (Strip-safe along with `setConsoleWidth`, `setDialog`, `setPluginDrawer` — all 4 allow omitting both `graphTopology` and `graphLifetime` together; supplying only one is rejected, and Graph mode runtime still requires both): read full UI snapshot (`pluginDrawerOpen`, `pluginFilter`, `pluginFormat`, `nodeDrawerOpen`, `nodeDrawerPage` [`nodes|presets`], `nodeDrawerFamily` [`routing|sound-design|analyzer`], `activeDialog` [`none|cheatSheet|settings`], `cheatView`, `cheatModule`, `cheatFilter`, `addPaletteOpen`, `addPaletteQuery`, `openRouterKeys`, `openStackGroupId`, `openSpectrogramKeys`, `openNebulaKeys`, `openIrEditorKey`, `openIrDistanceKey`, `openNebulaRampKey`, `nebulaRampOpen`, `openPresetEditorId`, `presetEditorOpen`, `playbackOpen`, `darkroomOpen`, `consoleWidth`).
     - `setPluginDrawer(open, filter?, format?)`: toggle left Plug-in Browser, live filter query, and optional format filter (`"all"|"VST3"|"AudioUnit"|"CLAP"`).
     - `setNodeDrawer(open, page?, family?)`: toggle right Node Lens drawer, switch `nodes`/`presets` page or `routing`/`sound-design`/`analyzer` category.
     - `setDialog(dialog: "none"|"cheatSheet"|"settings", cheatView?: "overview"|"details", cheatModule?, cheatFilter?)`: open/close Cheat Sheet or Settings dialog and jump to module/search.
     - `setConsoleWidth(width: 48|56|64|80|96|112)`: set Settings Strip track width (`ui.consoleWidth`; persisted in WebKit local storage across launches within the same system WebView storage domain).
     - `setNodeWindow(kind: "router"|"stack"|"spectrogram"|"nebula"|"ir"|"playback"|"darkroom"|"irDistance"|"nebulaRamp"|"presetEditor", open, nodeKey?, groupId?, presetId?)`: open/close expanded node window/editor (`nebula` toggles inline **Detail** [`detailsEnabled`, persisting project state] rather than opening a separate floating window, while `nebulaRamp` opens the **`Jelly`** ramp modal; `router`/`spectrogram`/`nebula`/`ir`/`irDistance`/`nebulaRamp` require `nodeKey` when `open: true` and allow omitting it when `open: false`; `stack` requires `groupId` or `nodeKey` when `open: true` and allows omitting both when `open: false`; when `state.fileGraph.nodePlaybackEnabled == false` [`sourcePlaybackOnly == true`], `playback` opens from `nodeKey=<fileSourceKey>` and `addPlayback` rejects with `"Open Playback from its File Source"`; `darkroom` takes optional `nodeKey` and asynchronously sends `fileGraphRepairOpen` via `ChloraRepairUI.open()`, so `op.result.ui.darkroomOpen` may initially still be `false` — poll `chlora_get_state` until `state.fileGraph.repairs[]` shows `open == true` and `analysis.ready == true` before reading `id`/`inputRevision` or running E2E `chlora_repair_render`; `presetEditor` forbids `nodeKey`/`groupId` and accepts optional `presetId` `1..128`).
     - `openAddPalette(open, query?, x?, y?)`: open/close `Shift+A` canvas add-node palette and set search query.
   - Other view/preference commands: `chlora_graph_get_view_preferences`, `chlora_graph_set_viewport(zoomScale, panX, panY)`, `chlora_graph_set_spatial_meter(target, on)`, `chlora_graph_set_cable_dead_zone(pixels)`, `chlora_graph_set_stack_names(groupId | nodeKey, on)` (`groupId` and `nodeKey` are mutually exclusive XOR), `chlora_set_zoom(percent)`, `chlora_graph_analyzer_control(action="setNebulaViewing" | "setSpectrogramViewing")`.
3. **Layer 3 — Computer Use / Native GUI mouse & keyboard (last resort, multi-instance PID-isolated on macOS)**:
   - Use **only** when operating third-party VST3 native editor controls not exposed as automatable VST parameters (e.g. proprietary preset menus/buttons inside a plugin window), verifying native OS file choosers, or confirming real DAW host/window presentation.
   - **PID + sandboxed worker `CGWindowID` lookup**: Third-party VST3 native editors opened by `chlora_graph_open_editor` / `chlora_strip_open_editor` / `chlora_graph_stack_control(openSlotEditor)` run inside sandboxed child processes (`ChloraPluginWorker`, `ChloraCompatibilityWorker`, `ChloraPluginWorkerX86`) whose `PPID == <bound_host_pid>`. Also, when `alwaysOnTop` is enabled, windows use `kCGFloatingWindowLevelKey` (not `0`) — **never hardcode `kCGWindowLayer == 0`**. Always build `allowed_pids = {bound_pid} | child_pids_of(bound_pid)` first, then enumerate on-screen windows with zero-dependency native `swift -e 'import CoreGraphics; import Foundation; ...'` (since macOS system Python does not preinstall `pyobjc`/`Quartz`):
     ```python
     import json, subprocess

     def allowed_pids(host_pid: int) -> set[int]:
         out = subprocess.check_output(['ps', '-ax', '-o', 'pid=,ppid=,comm='], text=True)
         pids = {host_pid}
         for line in out.splitlines():
             parts = line.strip().split(None, 2)
             if len(parts) >= 2 and int(parts[1]) == host_pid:
                 pids.add(int(parts[0]))
         return pids

     swift_code = '''
     import CoreGraphics; import Foundation
     let rows = (CGWindowListCopyWindowInfo([.optionOnScreenOnly, .excludeDesktopElements], kCGNullWindowID) as? [[String: Any]] ?? []).compactMap { w -> [String: Any]? in
         guard (w[kCGWindowIsOnscreen as String] as? Bool) == true,
               let num = w[kCGWindowNumber as String] as? Int,
               let pid = w[kCGWindowOwnerPID as String] as? Int,
               let bounds = w[kCGWindowBounds as String] as? [String: Any] else { return nil }
         return [
             "windowId": num,
             "pid": pid,
             "owner": (w[kCGWindowOwnerName as String] as? String) ?? "",
             "title": (w[kCGWindowName as String] as? String) ?? "",
             "layer": (w[kCGWindowLayer as String] as? Int) ?? 0,
             "bounds": bounds,
         ]
     }
     let data = try JSONSerialization.data(withJSONObject: rows)
     print(String(data: data, encoding: .utf8)!)
     '''
     pids = allowed_pids(BOUND_HOST_PID)
     all_wins = json.loads(subprocess.check_output(['swift', '-e', swift_code], text=True))
     wins = [w for w in all_wins if w['pid'] in pids]
     ```
   - **Focusless silent single-window capture**: Always capture the exact window by ID without stealing focus or picking up overlapping Chlora instances:
     ```sh
     screencapture -x -o -l <CGWindowID> /tmp/chlora-win.png
     ```
     (`-x` mutes shutter sound; `-o` strips window drop shadow so PNG dimensions align strictly with `kCGWindowBounds`.) If `screencapture` fails with `could not create image from window`, the current terminal/host app has not been granted macOS Screen Recording TCC permission (**System Settings → Privacy & Security → Screen & System Audio Recording**) — report the permission block honestly instead of guessing coordinates.
   - **Retina 2× pixel → Quartz logical point conversion & click guardrails**:
     `kCGWindowBounds` and macOS `CGEvent` / Computer Use clicks use **Quartz logical points**, whereas `screencapture -o -l` produces **2× physical pixels** on Retina displays (1× on non-HiDPI). Compute exact click coordinates from PNG `(px_x, px_y)` and image size `(png_width, png_height)`:
     ```python
     pt_x = bounds['X'] + (px_x / png_width) * bounds['Width']
     pt_y = bounds['Y'] + (px_y / png_height) * bounds['Height']
     ```
     **Safety rules**:
     1. When multiple Chlora instances coexist, **never** activate windows by app name `"Chlora"`; if bringing a window to front is strictly required, target the exact `pid` via `AppKit.NSRunningApplication.runningApplicationWithProcessIdentifier_(pid)`.
     2. Before dispatching any click, **assert** `bounds['X'] <= pt_x < bounds['X'] + bounds['Width']` and `bounds['Y'] <= pt_y < bounds['Y'] + bounds['Height']` for a window owned by `allowed_pids`.

### Native input evidence alongside MCP

An AX click on a native text field can succeed without giving it keyboard focus. Before unscoped Select All, paste or typing, confirm that the intended editable field actually owns focus. Before Return submits a path or value, verify its complete intended contents and retained focus. If AX activation leaves focus elsewhere, withhold text keys, inspect the current screenshot and establish focus with a bounded coordinate action. Keep failed setup attempts separate from the product behavior being verified.

Committed text entry, physical letter keys, paste, native menu actions and keyboard shortcuts are distinct verification paths. Record the exact input API and resulting field value/focus. Validate shortcuts against a known responding editor in the same bound QA; do not replace an unexplained failing variant with a passing one in the acceptance record.
