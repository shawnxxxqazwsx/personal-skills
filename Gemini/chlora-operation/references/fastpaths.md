# Compose common Graph routes

Read one current summary and the needed schemas (`clara schema <id>` / `chlora_describe_tool`). Resolve processing widths, channel order, wrapped status, current wires and container membership before writing. Reuse returned binding/state and await async work. Detailed entity semantics are in [nodes.md](nodes.md); parameter/level decisions are in [controls-and-plugins.md](controls-and-plugins.md).

## Choose the smallest matching construction

| Request | Construction |
|---|---|
| One mono channel | Exact MAIN channel edges, mono-capable processor |
| Contiguous stereo/wider bus | `connect_bus` with `sourceChannel`, `destinationChannel`, and `channels` (never `sourceStart`/`destinationStart`) |
| Whole wrapped bus in sequence | Snake branches; prefer exact aggregate-wire splice |
| Parallel processors | Split (`Fanout`) → independent chains → `Merge`, explicit branch gains |
| Dry plus wet effect return | Parallel recipe with effect verified wet-only |
| Process selected channels and preserve others | Selected subset → processor/Stack → identity Router gather |
| Repeat independent mono/stereo processing | Stack N×1 or N×2; one instance per lane |
| Pack or reorder source channels | Bundle or ordered PortSnake plus explicit Router mapping |
| Shared parameter changes across copies | MultiLink (`set_multi_link`) or sync selection (`set_sync_selection`) |
| IR convolution / Reverb Bank | `add_ir` → `import_ir` (WAVs) or `ir_advanced(loadBankFile)` (Reverb Bank) |
| Parameter modulation | `add_builtin(kind="lfo")` → `expose_parameter` → `connect_lfo` |
| Reuse a saved region | [Preset recall](presets.md), not reconstructing its internals |
| Clean the drawing | [Layout](layout.md), preserving semantic routes |

## Serial insertion and replacement

For one channel, use `connect_channel(sourceNodeKey, destinationNodeKey, sourceChannel, destinationChannel, destinationRole?, replaceExisting?)` (`destinationRole`: `"main"` | `"sidechain"`, default `"main"`; sidechain exempts the MAIN-only Snake guard); for a contiguous bus use `connect_bus(sourceNodeKey, destinationNodeKey, sourceChannel, destinationChannel, channels, destinationRole?, replaceExisting?)` (zero-based offsets `sourceChannel`/`destinationChannel` + width `channels` — never `sourceStart`/`destinationStart`). A stereo processor operates on a pair; a multichannel processor must actually support the chosen width. Independent mono lanes can use Stack or distinct nodes according to user intent.

For already wrapped equal-width endpoints, load a detached processor at its path width, await it, confirm `mainIn/mainOut`, wrap it, then connect with `connect_snake` using current source/destination branches. When adding it on an existing aggregate wire, prefer `splice_snake_node`: retain exact width and branch IDs, and verify the replaced wire becomes two serial wires. For an ordinary supported MAIN wire:
- **`chlora_graph_insert_plugin_on_wire`** (async → poll `chlora_get_operation`; read created **`op.nodeKey`** from the top level of the terminal operation response) loads a new third-party plug-in (`pluginUid` OR `.vst3`/`.clap`/`.component`/`AudioUnit:...` `pluginPath`) directly in series onto `(sourceNodeKey, sourceChannel, destinationNodeKey, destinationChannel, channels, x, y, groupId?)`. Note: an inserted plug-in defaults to `snakeWrapped: true` (`"Snake lines cannot be split by a plug-in"` rejects calling `insert_plugin_on_wire` a second time directly on its new Snake output unless unwrapped first, or use `graph_plan.py` `insert_on_wire` with 2+ plugins).
- **`chlora_graph_node_advanced(action="insertNodeOnWire")`** inserts an existing detached node (`nodeKey`) onto `(sourceNodeKey, sourceChannel, destinationNodeKey, destinationChannel, x, y, groupId?)` (accepts `groupId: 0`).
- **`splice_node` / `detach_node`** splice an existing detached ordinary plug-in or bypass-and-bridge-detach it; **`chlora_graph_node_advanced(action="disconnectNodePorts", nodeKey, direction: "inputs"|"outputs"|"both")`** clears all incident single/Snake wires without auto-bridging passthrough.

Only remove/replace the intended original feed. Read back that an old direct path did not survive as an accidental parallel path. Wrapping an already connected node clears its incident routes; include every affected edge in the reconstruction scope. A node removal, `disconnectNodePorts`, and a `detach_node` that restores continuity have different outcomes.

## Parallel processing and dry/wet returns

Split the same intended bus into branch paths; gather once at a Merge of the matching width. For a wrapped aggregate source, an explicit Fanout keeps one compact output and legible split. For ordinary channel/bus paths, use the native supported endpoints; don't create extra Graph IN sockets merely for fanout. A split can occur after any compatible source node, not only Graph IN.

On an existing MAIN wire, `insert_builtin_on_wire(kind="fanout")` and a downstream `kind="merge"` insertion can preserve the original route while adding boundaries. For detached construction, `add_builtin(kind="fanout")` and `add_merge(channels=W, inputs=N)` create them; establish the Fanout input before matching its output width. Inspect returned branch IDs before choosing Merge inputs. Native Merge may retain a spare empty bank; `sumBranches` count is not the active path count.

For ordinary parallel processing, branch outputs can intentionally contain full processed signal. For dry plus wet-only return, establish the effect's wet-only state from listed descriptors and readback before adding a separate dry branch. Do not infer “wet-only” from a name or a guessed normalized value. An unresolved wet-only setting blocks that particular return topology, not unrelated serial/parallel requests.

Write user-specified branch/output gains using `set_merge_gain`; output uses `branch: -1`. If balance is unspecified, preserve existing gains when meaningful; otherwise choose and report an explicit starting balance. Mute, Solo and polarity are separate Merge branch operations. Verify branch feeds, resulting gains and one intended gathered downstream feed; listening/level matching is separate.

## Selected-channel processing with an identity gather

Let W be the full destination width and S the ordered selected source channels. Resolve names from the current layout rather than fixed immersive numbering. An identity Router gather preserves the untouched channels and replaces only S with processed return lanes. Ensure the chosen processor widths sum to |S|.

For an ascending subset on compatible unwrapped ports, use output PortSnake on the source and input PortSnake on the Router, both using the same S order; route output sidecar → processor/Stack → input sidecar. PortSnake uses native ascending order. Arbitrary reordering uses explicit Bundle packing or Router crosspoints instead; see [advanced recipes](graph-recipes.md).

Before creating attached sidecars, remove exact authorized occupied edges at those ports. If a replaced aggregate overlaps unselected channels, disconnect it as a whole and explicitly restore those unselected channels. Native creation may convert an untouched Graph IO identity route; inspect returned wiring and restore all required passthrough lanes. A selected subset's own bus width is |S|, not W. Never delete its plug-in owner just to replace a sidecar partition.

## Plugin Stack and built-in insertion

Prefer **Stack v2** via `chlora_graph_stack_control`: `action="add"` (`x, y, channels?, groupId?`) → `loadPlugins` (`uids`, optional `slotIndex`, `replace`, `stereoPairs`, `channelList`, `groupId`) → `setStereoMode("autoPairs"|"mono")` / `setStereoPair` / `setChannelGains` / `setChannelToggle` / Armada groups (`createArmadaGroup`, `assignArmadaGroup`, `updateArmadaGroup`, `deleteArmadaGroup`, `syncArmadaGroup`). Classic container Stacks (`chlora_graph_create_stack(count=N,width=1|2)` → `chlora_graph_configure_stack` → `chlora_graph_load_stack` / `chlora_graph_load_stack_file` → `chlora_graph_split_stack_lane` / `chlora_graph_unload_stack`) remain for legacy compatibility; connect their left and right boundary Fanouts externally. See [nodes.md](nodes.md) for Stack v2 vs Classic details and nesting limits.

`chlora_graph_insert_builtin_on_wire` supports `bundle`, `merge`, `fanout`, and `router` on an exact current MAIN wire identity (`chlora_graph_node_advanced(action="insertAlignOnWire")` atomically inserts Align `channel` on an exact wire); `chlora_graph_splice_existing_builtin` uses a compatible detached built-in. Use full channel/aggregate/branch fields; do not derive a wire from a screenshot. Group insertion similarly requires explicit supported boundary/internal routing.

## IR Loader import and routing fastpath

1. Create with `chlora_graph_add_ir(x, y)` (creates a Snake-wrapped 400×280 node at current linked width) and read `node.irLoader.waveformRevision` (`""` when unloaded).
2. **Import WAVs or load Reverb Bank**:
   - **WAVs (`chlora_graph_import_ir`)**: supply current Graph binding, `nodeKey`, `expectedRevision`, ordered absolute `files`, `mode` (`linked` | `mono` | `diagonal` | `matrix`), `convention` (`channels` | `ambix` | `n3d` | `fuma`), `matrixInputs`, `matrixOutputs` (plus `linkedChannels` when `linked`, optional `sourceHashes`, `decayPercent`, `sizePercent`, `decaySeconds`, `edits`). Poll `chlora_get_operation(operationId)` until terminal.
   - **Reverb Bank `.irmatrix.json` (`chlora_graph_ir_advanced`)**: use `action: "loadBankFile"` with `path` (see [ir-banks.md](ir-banks.md)).
3. Refresh Graph binding (`chlora_get_state` / `chlora_graph_get_summary`), verify `node.irLoader.status` and I/O widths, then wire upstream/downstream via `connect_snake` (or `set_snake(false)` + `connect_bus`).
4. Tune scalar controls with `chlora_graph_set_ir_controls(field: "wet"|"gainDb"|"preDelayMs", value)` and bank matrix/gains/distance with `chlora_graph_ir_advanced`.

## LFO parameter exposure and modulation fastpath

1. Create an LFO node with `chlora_graph_add_builtin(kind="lfo", x, y)` (omit `channels`; zero audio ports).
2. On the target node, call `chlora_graph_list_parameters` to find the writable `parameterId` and current `parameterLayout`.
3. Expose the parameter via `chlora_graph_expose_parameter(nodeKey=targetKey, parameterId, parameterLayout)` and capture the returned `exposedId` (or read `target.exposed.parameters[].id` from full state).
4. Connect the modulation edge using `chlora_graph_connect_lfo(nodeKey=lfoKey, targetNodeKey=targetKey, exposedParameterId=exposedId, parameterLayout)` — **do not substitute the raw `parameterId`**.
5. Adjust per-edge behavior with `chlora_graph_set_lfo_depth(depth: -1..1)` and `chlora_graph_set_lfo_mapping(mode: "modulate"|"remote", minimum, maximum)`, and adjust LFO wave/rate/curve with `chlora_graph_set_lfo_settings`. Verify readback in `graphModulations[]`. Remember that modulation-only edits do **not** advance `graphTopology`.

## WebUI drawers, node windows & view fastpath

When the Graph WebUI is loaded and visible:
- **Drawers, dialogs, node windows & Add palette (`chlora_graph_ui_control`)** (async `viewOperation` → poll `chlora_get_operation` and read snapshot at **`op.result.ui`**, unlike async plug-in loads where `op.nodeKey` sits at the top level):
  - `getUiState` (Strip-safe along with `setConsoleWidth`, `setDialog`, `setPluginDrawer` — all 4 allow omitting both `graphTopology` and `graphLifetime` together; supplying only one is rejected, and Graph mode runtime still requires both): read current UI state (`pluginDrawerOpen`, `pluginFilter`, `pluginFormat`, `nodeDrawerOpen`, `nodeDrawerPage`, `nodeDrawerFamily`, `activeDialog`, `cheatView`, `cheatModule`, `cheatFilter`, `addPaletteOpen`, `addPaletteQuery`, `openRouterKeys`, `openStackGroupId`, `openSpectrogramKeys`, `openNebulaKeys`, `openIrEditorKey`, `openIrDistanceKey`, `openNebulaRampKey`, `nebulaRampOpen`, `openPresetEditorId`, `presetEditorOpen`, `playbackOpen`, `darkroomOpen`, `consoleWidth`).
  - `setPluginDrawer(open, filter?, format?)` / `setNodeDrawer(open, page?: "nodes"|"presets", family?: "routing"|"sound-design"|"analyzer")`: open/close Plug-in Browser (`format`: `"all"|"VST3"|"AudioUnit"|"CLAP"`) or Node Lens drawer and filter/switch tabs.
  - `setDialog(dialog: "none"|"cheatSheet"|"settings", cheatView?, cheatModule?, cheatFilter?)`: open/close Cheat Sheet or Settings and jump to module/search.
  - `setNodeWindow(kind: "router"|"stack"|"spectrogram"|"nebula"|"ir"|"playback"|"darkroom"|"irDistance"|"nebulaRamp"|"presetEditor", open, nodeKey?, groupId?, presetId?)`: open/close expanded node panels (`nebula` toggles inline **Detail** [`detailsEnabled`, persisting project state] rather than opening a separate floating window, while `nebulaRamp` opens the ramp modal; `router`/`spectrogram`/`nebula`/`ir`/`irDistance`/`nebulaRamp` require `nodeKey` when `open: true` and allow omitting it when `open: false`; `stack` requires `groupId` or `nodeKey` when `open: true` and allows omitting both when `open: false`; `darkroom` asynchronously triggers `fileGraphRepairOpen`; `presetEditor` forbids `nodeKey`/`groupId` and accepts optional `presetId` `1..128`).
  - `openAddPalette(open, query?, x?, y?)`: open/close `Shift+A` canvas add palette and filter by query.
- **Camera & view preferences**: `chlora_graph_get_view_preferences`, `chlora_graph_set_viewport(zoomScale, panX, panY)`, `chlora_graph_set_spatial_meter(target, on)`, `chlora_graph_set_cable_dead_zone(pixels)`, `chlora_graph_set_stack_names`, `chlora_set_zoom(percent)`, `chlora_graph_analyzer_control(action="setNebulaViewing" | "setSpectrogramViewing")` (`setNebulaViewing` also accepts `detailsVisible`).

## Nebula Details + Phase, Storage & Patchbay fastpaths

- **Nebula Details + Phase**:
  1. Create or locate Nebula (`chlora_graph_add_builtin(kind="nebula", channels=...)`, defaults to `snakeWrapped: true`).
  2. Configure via `chlora_graph_analyzer_control(action="setNebulaSettings", nodeKey, settings={...})`: enable `detailsEnabled: true`, `phaseMode: true`, and `phaseAllLinks: false` (Adjacent pairs) or `true` (All pairs). Use `phaseColorStops` (2..9 ascending `-1..1` stops with `#RRGGBB`) **or** legacy `phaseNegativeMax`/`phasePositiveMin` (mutually exclusive); likewise `speakerAngles` cannot be combined with `mapping` or `inputSource`.
  3. Toggle observation lease with `setNebulaViewing(visible=true, detailsVisible=true)` and read frames via `getNebulaFrame`.
- **FileGraph Storage cleanup** (unbound):
  1. Call `chlora_manage_system(action="storageInspect")` to get current disk inventory and a fresh `token`.
  2. Call `chlora_manage_system(action="storageClean", token=..., mode="rebuildableCache")` (cache-only; do not pass `selection`) or `mode="trash"` with `projectIds` / `selection: [{id, version}]`.
- **Background Patchbay hardware & clock setup**:
  1. Isolate QA with `CHLORA_ROUTE_HOME=/tmp/<id>/route-home`, call `chlora_patchbay_control(action="attach", bindingGeneration=...)`, and poll `chlora_get_state` until `state.patchbayStatus.serviceId` is nonempty.
  2. Configure hardware via `chlora_patchbay_control(action="deviceConfigure", bindingGeneration, serviceId, documentRevision, graphTopology, graphLifetime, nodeKey, deviceId)` (or `inputId`/`outputId`) and audio clock via `setAudioSettings(..., sampleRate, bufferSize)` (`0` = `"Device default"`), polling `chlora_get_operation` for each returned `operationId`.

## Offline plan helper (`graph_plan.py`)

`"$SKILL_DIR/scripts/graph_plan.py"` composes:
- `series`: accepts either **`pluginUids`** or **`pluginPaths`** (wrapped serial chain between already-wrapped endpoints).
- `subset`: ascending `channels` PortSnakes between unwrapped compatible owners.
- `stack`: `count`×`width` (`1` or `2`, ≤128) with optional **`pluginUid`** or **`pluginPath`**.
- `builtin`: supports `bundle`, `fanout`, `router`, `channel`, `lfo`, `nebula`, `spectrogram`, `lfespectrum`, `merge` (`add_merge`), `ir` (`add_ir`), **`levelmeter`** (`chlora_graph_level_meter(action="add", ...)`), and **`stack` / `stack_v2`** (`chlora_graph_stack_control(action="add", x, y, channels?, groupId?)`).
- `insert_on_wire`: inline series splice onto an existing MAIN wire (`source`, `sourceChannel=0`, `destination`, `destinationChannel=0`):
  - **New plug-ins** (`plugins: [{"name"?: str, "pluginUid"?: str, "pluginPath"?: str, "channels": int, "x": float, "y": float, "groupId"?: int}, ...]`):
    - When `len(plugins) == 1`: emits a single `chlora_graph_insert_plugin_on_wire` (resulting node has `snakeWrapped: true`).
    - When `len(plugins) >= 2`: because `insert_plugin_on_wire` creates `snakeWrapped: true` nodes whose Snake outputs cannot be re-split by a second `insert_plugin_on_wire` (and single-output sources like `Router` require freeing source lanes before reconnecting), the planner emits `add_plugin` / `add_plugin_file` + `set_snake(wrapped=False)` (+ optional `set_node_group`) for each plug-in first, then emits `disconnect_channel` for the original `source -> destination` span, and finally wires `connect_bus(..., replaceExisting=True)` across `source -> $p0 -> ... -> $p_{n-1} -> destination`.
  - **Existing detached node**: supply `nodeKey` (plus `x`, `y`, optional `groupId`) — emits `chlora_graph_node_advanced(action="insertNodeOnWire", ...)`.
- `group`: `create_group` (rejects nesting a Stack inside a regular Group).
- `steps`: arbitrary explicit `chlora_graph_*` tool steps.

`replaceEdges` now disconnects MAIN channel wires (`disconnect_channel`), aggregate Snake wires (`disconnect_snake`), **and `sidechain`/non-MAIN wires (`delete_selection`)** before creating new steps. `graph_plan.py` auto-discovers `CHLORA_MCP_ADAPTER`, `tools/chlora_mcp.py`, or native `clara` (`clara mcp serve --stdio --profile full`), rejects changed initial bindings, checks schemas, waits for `stateRestoreInFlight` on `chlora_undo`/`chlora_redo`, stops at first failure, and never replays writes.

Example detached Stack component:

```json
{"replaceEdges": [], "components": [
  {"recipe":"stack","name":"lanes","count":2,"width":2,"x":1800,"y":600,
   "pluginPath":"/absolute/ExactInstalledPlugin.vst3"}
]}
```

This creates components, not a fully connected route. Capture references such as `$lanes.groupId`, `$lanes.leftNodeKey` and `$lanes.rightNodeKey` use actual returned state; missing boundaries stop execution. Explicit step shape:

```json
{"tool":"chlora_graph_connect_snake","arguments":{
  "sourceNodeKey":"CURRENT_SOURCE_KEY","destinationNodeKey":"$lanes.leftNodeKey",
  "sourceBranch":0,"destinationBranch":0},"capture":"optionalResult"}
```

`graph_plan.py --apply` writes `receipt.json` with top-level **`captures.<name>`** (containing created `nodeKey` / `groupId` / `leftNodeKey` / `rightNodeKey`) and **`verification`** (`"readback available; assess requested topology"`), alongside `state` and `plannedChecks`. For scoped offline placement, `layout(geometry,node_keys,origin,gap)` calculates one loose-node row from actual native bounds. Containers use the native layout workflow in [layout.md](layout.md).
