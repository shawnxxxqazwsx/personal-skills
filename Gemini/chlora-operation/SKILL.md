---
name: chlora-operation
description: >-
  Operate a running Chlora (Clara/Klora) through MCP, the native `clara` CLI, or
  bounded UI/computer-use fallbacks for built-in Graph nodes, routing and layout,
  presets, Strip slots, mixer gain/mute/solo, hosted plug-in parameters, LFO
  modulation, IR Loader / Reverb Banks, Analyzers (Level Meter, Jelly / Nebula,
  Spectrogram, LFE Spectrum), Standalone FileGraph / Device I/O / Monitor Bus,
  and DarkRoom Audio Repair.
---

# Chlora operation

Use MCP state, the bundled native `clara` CLI (`Host.app/Contents/Helpers/clara`),
and supported UI/computer-use fallbacks to carry out the user's requested change.
Clara / Klora in conversational requests refers to this Chlora operation skill.
Native UI controls alone do not prove MCP support. Existing task authorization
covers its necessary operations; do not request approval again for a generated plan.

> **Default tool surface & intentional boundaries**
> - **Tool surface defaults**: `clara mcp serve --stdio` defaults to the **`compact`** surface (`--profile compact`, 8 entrypoints; pass `--profile full` for all 198 commands), whereas `tools/chlora_mcp.py` defaults to **`full`** (pass `--profile compact` to switch).
> - **Intentional read-only / UI-only boundaries**:
>   1. Live `wire.bakedRoute` / `commitGraphBakedWireRoutes` remains WebView auto-debounced and **MCP read-only**.
>   2. Level Meter left `Peak/RMS` display toggle (`TP max` is a right-side readout), `Jelly` `Clear` trail & `Angles…` dialog, IR re-import & companion Router wizard, Router one-click `FullPortSnakes`, Finder reveal, and Host MCP toggle remain **UI-only**.
>   3. Standalone VST3 **`CLR Router`** internal non-parameter ValueTree state is excluded from `clara` control; Multi-Mono non-primary lane independent parameter read/write is queued as low-priority follow-up.
>   4. **`CLR-EDGE-03`**: `CLR Router` numeric box out-of-range input strictly rejects and restores the previous value.

For **Reverb Bank / IR matrix creation, conversion, validation or loading**, read
[IR Bank specification and reproduction](references/ir-banks.md) completely
before authoring a manifest. This reference is self-contained: channel order,
WAV format, complete JSON schema, physical-source reuse, internal chunk budgets,
generator, examples, matching node presets, loading and acceptance. Start offline
authoring with the supplied IR inventory; a live Host connection is needed only
for requested loading or live verification.

## Read only the relevant workflow

| User intent | Reference |
|---|---|
| Create, convert, validate, share or load an IR Loader Reverb Bank; Stereo/9.1.6 matrix reverb from any IR library | [ir-banks.md](references/ir-banks.md) — read fully, then use [ir_bank.py](scripts/ir_bank.py) and the complete [recipe example](assets/ir-bank-recipe.example.json) |
| Choose or manipulate an internal Node (Snake, Merge, Fanout, Router/Matrix, Align, Stack, IR Loader, LFO, Level Meter, Jelly / Nebula, Spectrogram, LFE Spectrum, File Source, Device I/O, Monitor Bus, Chloe/App Input), wrapper, container or link | [nodes.md](references/nodes.md) |
| Serial, parallel, subset, repeated-lane, LFO modulation or IR Loader routing | [fastpaths.md](references/fastpaths.md) |
| Sidechain, sparse/reordered channels, Multi-Mono wrappers, linked copies, uneven widths | [graph-recipes.md](references/graph-recipes.md) |
| Faders, input trim, Merge/Router/Align/IR/Stack/FileGraph controls, Solo/Mute/Polarity, node/slot Bypass and plug-in controls | [controls-and-plugins.md](references/controls-and-plugins.md) |
| Save, find, recall, repeat, insert, update or delete a preset; configure library folders | [presets.md](references/presets.md) |
| Arrange nodes, keep Graph operations/setups readable, simplify wires, Pins, Comments, UI drawers/windows, camera or port alignment | [layout.md](references/layout.md) |
| DarkRoom Audio Repair (`chlora_repair_*` locks, Mono effect graph, UI presentation commit gate, render & DraftRoom import) | [darkroom-repair.md](references/darkroom-repair.md) |
| Native `clara` CLI vs MCP setup, multi-instance `--socket` isolation, 198-command discovery (`graph.ui_control`, `graph.level_meter`, `graph.stack_control`, `graph.insert_plugin_on_wire`, `graph.rename_preset`, `patchbay.control`), Standalone FileGraph, or MCP vs UI vs Computer Use decision tree | [mcp-tool-reference.md](references/mcp-tool-reference.md) |

These workflows compose. For “parallel reverb, then selected-channel delay and
clean layout,” combine routing, controls and layout; do not restart discovery
for each stage or read every reference by default.

Apply the mandatory Graph presentation baseline to user work, tests,
reproductions and temporary probes alike. Before adding, loading, pasting or
inserting any node, routing object, container, Pin or Comment, plan a clear place
using current rendered bounds. Keep nodes free of overlap or obscured controls,
order paths source-to-processing-to-sink, and align parallel lanes so a person
can follow the signal at a glance. Use the fewest necessary visible cables,
crossings and detours while preserving every required audio lane and mapping.
Read [layout.md](references/layout.md) from the first addition; maintain this
standard throughout construction, not just for the final screenshot. Preserve
unrelated user layout and routing.

## Bind once, reuse current state

1. **Locate the control binary & pin the exact socket first:**
   - When an MCP server is already connected, call `chlora_get_state`.
   - When using the CLI, resolve `clara` via `which clara` or the installed app bundle (`~/Desktop/Chlora*.app/Contents/Helpers/clara` or `/Applications/Chlora*.app/Contents/Helpers/clara`), run `clara host list --json` (or `python3 tools/chlora_mcp.py --list-hosts`), and **always pass `--socket /tmp/chlora-mcp-<uid>/host-<pid>.sock`** whenever more than one Host or QA instance exists. Never touch another user/agent session's socket.
   - For isolated QA/rehearsal runs without disturbing running sessions, launch a private Host copy with `MC_HOST_SUPPORT_DIR=/tmp/<unique>/support MC_FILE_GRAPH_WORKSPACE_HOME=/tmp/<unique>/workspace MC_HOST_FILE_GRAPH_ONLY=1` (and when exercising Background Patchbay, also set **`CHLORA_ROUTE_HOME=/tmp/<unique>/route-home`** so `ChloraRouteClient::defaultHome()` isolates `ChloraRouteService` away from the user's real daemon) using `Chlora.app/Contents/MacOS/Chlora`, record its spawned PID, bind exclusively to `/tmp/chlora-mcp-<uid>/host-<spawned-pid>.sock`, and terminate only that exact PID afterward. Note: even with `MC_HOST_FILE_GRAPH_ONLY=1`, a freshly launched Host starts in `mode: "strip", fileGraph: null` — call `chlora_file_graph_project(action="new" | "open")` first to enter Standalone FileGraph Graph mode (`state.mode == "graph"`).
2. Session tools require `instanceId` (state's `activeInstanceId`; `0` in standalone FileGraph, supported by the 11 Standalone-capable `host.*` commands: `clear_all`, `close_editors`, `set_meter_mode`, `set_worker_threads`, `reset_perf_max`, `set_zoom`, `set_plugin_grouping`, `set_plugin_favorite`, `set_plugin_preferred_channels`, `undo`, `redo`, as well as the 11 non-Strip `host.manage_system` actions) and `bindingGeneration`. When using `clara --context-file state.json` (or `--context-file -`), explicit `--field` flags (accepting both `--field value` and `--field=value`) take precedence; empty string values `""` are skipped (so detached/attaching `patchbayStatus.serviceId == ""` is not injected and empty `fileGraph.sourceGraphLifetime == ""` falls back cleanly to `sourceGraphLifetime` / `graphLifetime`); `sourceGraphLifetime` is injected only for source/device `file_graph.control` commands (not `new|open|save|show|close|stop|seek`) and `file_graph.project` source/device/automation actions (`loadSource` only when explicit non-`-2` `index`, `nodeKey`, or `expectedSourceGeneration` is passed), and `instanceId: 0` is skipped when a target command schema requires `instanceId >= 1`. Bound Graph tools additionally require `graphTopology` and `graphLifetime` as **decimal strings** (note: LFO modulation-only edits do not advance `graphTopology`). While attached to Background Patchbay (`state.patchbay == true`), regular `chlora_graph_*` / `chlora_undo` / `chlora_redo` remain bound to the Host local session — edit Patchbay topology, clipboard (`copySelection`/`pasteSelection`/`duplicateSelection`), presets, and undo/redo via `chlora_patchbay_control` using `(serviceId, documentRevision, graphLifetime, graphTopology)` and poll `chlora_get_operation` (use `action: "detach"` or switch session/FileGraph to exit Patchbay). Domain sub-systems enforce optimistic tokens: IR operations split tokens strictly — `setInternalRoute`/`resetInternalRoutes`/`setDistance`/`clearDistancePreview` require nonempty `node.irLoader.internalRouting.topologyRevision`, whereas `chlora_graph_set_ir_*`, `setGains`, `audition`, `getWaveform` use `node.irLoader.waveformRevision` (`""` allowed on unloaded `import_ir`; `loadBankFile` omits `expectedRevision`, returns no `operationId`, and polls `chlora_get_state` until `preparing == false && busy == false && status == "Ready"`; `listBanks` and `cancelImport` allow omitting `nodeKey`); FileGraph source/device/output edits require `sourceGraphLifetime` (and `expectedSourceGeneration` for source loads/playback/automation); DarkRoom Repair requires `repairId` + `inputRevision` (see [darkroom-repair.md](references/darkroom-repair.md)); Graph presets reflect `state.graphPresetScope` (`"ordinary"` vs `"patchbay"`).
3. `chlora_graph_get_summary` is unbound. Preset list/get/update/rename/delete, `chlora_manage_system` library/storage calls, and `chlora_get_host_preferences` / `chlora_set_host_preferences` (`preferencesToken`) are also unbound. Layout/name/Insert/Output changes require current `channelLayoutToken` from full state.
4. Poll `chlora_get_operation` (`clara operation get --operation-id <id>`) for async loads (`add_plugin*`, `load_stack*`, `insert_plugin_on_wire`), paste, IR import/kernel rebuilds, renderer/layout and view/UI operations (including `chlora_graph_ui_control`; its Strip-safe actions `getUiState`, `setConsoleWidth`, `setDialog`, and `setPluginDrawer` allow omitting both `graphTopology` and `graphLifetime` together — supplying only one is rejected, and Graph mode runtime still requires both). After `chlora_undo` / `chlora_redo` (accepts `instanceId >= 0`, including Standalone `0`; note `file_graph.control(command="undo")` rolls back File Source/UI history rather than direct MCP graph additions), if `stateRestoreInFlight` is `true`, poll `chlora_get_state` until `stateRestoreInFlight` becomes `false` before reading new node keys or issuing writes. Timeout or `clara` CLI exit code `4` (`outcome_unknown`) means an unknown outcome: inspect state first and **never blindly replay a mutating call**.
5. Cache needed schemas for the current connection (`clara schema <id>` or `chlora_describe_tool`). Native `clara mcp serve --stdio` defaults to `compact` profile (8 tools: 5 direct reads + `chlora_discover_tools`, `chlora_describe_tool`, `chlora_invoke`); `tools/chlora_mcp.py` defaults to `full`. See [mcp-tool-reference.md](references/mcp-tool-reference.md) for `mcpFamily` search mapping and the MCP vs WebUI vs Computer Use decision tree.

## Choose the signal operation before writing

- Work at any channel count supported by the current session and processor.
  Derive source width, destination width and each path/subset width separately;
  never infer one from the other. Use current channel names or explicit indices,
  validate each offset/span, and preserve mapping order. Unequal widths, odd
  counts and mixed mono/stereo/wider partitions need explicit routing, not
  padding to an immersive format or silently dropping leftover channels.
- Resolve the affected channel names/order, MAIN or SIDECHAIN role, branch
  identity and actual bus widths. Mono, stereo and wider buses use the same
  decision process; no fixed immersive channel numbering is assumed.
- Serial insertion replaces one path; parallel splitting duplicates a signal;
  Merge sums; Bundle packs; Router maps. Visual grouping, a Strip layer or a
  plug-in Stack does not itself establish parallel summing or an external wire.
- Distinguish parallel processing from a **dry plus wet-only return**. Only the
  latter requires establishing the effect's wet-only parameter state before
  connecting it beside an independent dry path. Use explicit gains if requested;
  any chosen starting balance must be reported.
- Preserve unrelated feeds and state. Copy exact replaced wire identities from
  current state. `replaceExisting: true` applies only to an intended exclusive
  destination. An aggregate Snake must be disconnected/replaced as a whole;
  restore any unselected channels that shared the replaced aggregate.
- Snake wrapping changes incident wiring. Record all affected edges before
  wrapping an already connected node. Prefer native exact-wire splice/insert
  operations when they express the change without reconstruction.
- Use an isolated capability probe only for an unfamiliar or unverified bus or
  endpoint combination that the current schema/state cannot establish. Ordinary
  supported routing does not require a disconnected test graph first.

## Scope controls and verify the requested result

Resolve a volume/solo/mute request to input, output, master, Merge branch, Strip
slot or hosted parameter before selecting a tool. Set explicit values and flag
states rather than toggling. Account for selection/Q-Link/Multi Link before
writes so unrelated channels or copies are not changed. Hosted parameters use
listed IDs, layout tokens and normalized values; display units are not a linear
normalization rule. Read the controls reference when making these changes.

Verify the affected topology, widths, effective parameters/flags, preserved
neighboring routes and identities. For layout, use the paged coordinate planner/executor in layout.md: native
capability preflight, lightweight inventory, one bounded preview, atomic delta
apply and complete coordinate/semantic-wire readback. Renderer quality coverage
and actual rendered bounds remain distinct from stored anchors/sizes. MCP state alone does not
prove listening, realtime performance, native-editor visibility or DAW acceptance.
For partial failure, inspect the last confirmed state and choose a bounded
recovery; undo/redo requires fresh identities and tokens afterward.

## Deterministic Graph planning

Resolve the skill directory once (`SKILL_DIR` = directory containing this `SKILL.md`, e.g. `~/.config/magpie/library/skills/chlora-operation`):

```sh
python3 "$SKILL_DIR/scripts/graph_plan.py" --state current.json --spec recipe.json --output plan.json
python3 "$SKILL_DIR/scripts/graph_plan.py" --apply plan.json --socket /absolute/current-host.sock --socket-identity DEV:INO --transcript unique.jsonl --output receipt.json
```

`graph_plan.py` and `graph_layout.py` auto-discover `CHLORA_MCP_ADAPTER`, `tools/chlora_mcp.py`, or the bundled native `clara` helper (`clara mcp serve --stdio --profile full`), or accept an explicit `--adapter`. The second form performs authorized writes against the verified current Host socket (`stat -f '%d:%i' /path/to/host.sock` on macOS). The helper rejects a changed initial binding, checks schemas, waits for `stateRestoreInFlight` on undo/redo, stops at failure and does not replay writes. Its finite templates (`subset`, `stack` with `pluginUid`/`pluginPath`, `builtin` including analyzers/Align/LFO/IR/LevelMeter/Stack v2, `series` with `pluginUids`/`pluginPaths`, `insert_on_wire`, `group`, `steps`) are described in [fastpaths.md](references/fastpaths.md). Standalone Strip/FileGraph/Repair workflows use `clara` CLI or MCP directly rather than this Graph-centered planner. For multi-instance macOS Computer Use against native plug-in editors, follow the bound-`PID` + sandboxed-worker `CGWindowID` isolation rules in [mcp-tool-reference.md](references/mcp-tool-reference.md).
