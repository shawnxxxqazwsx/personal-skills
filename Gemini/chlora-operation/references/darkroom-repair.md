# DarkRoom Audio Repair (`chlora_repair_*`)

DarkRoom Audio Repair provides spectral editing, preview playback, Mono serial third-party effect chaining, offline rendering, render history, and DraftRoom re-import for a loaded Standalone FileGraph **File Source**. All 10 `chlora_repair_*` commands (`repair.*`) live in **`mcpFamily: "graph"`**.

## Required locks and argument gating

Target File Source must already have loaded audio (`sourceReady != false`) in an active Standalone FileGraph project (`chlora_file_graph_project(action="new"|"open")`). Note: although `loadSource` / `load` normalize macOS symlinks via `realpath` (`/tmp` → `/private/tmp`), synthesize test WAVs using canonical paths (or `os.path.realpath`) so local test assertions match `sources[].source.path` readback verbatim.

1. **Common 5 required fields** (on all 10 `chlora_repair_*` commands):
   - `bindingGeneration`: integer from `chlora_get_state`
   - `index`: integer `-2` (legacy IN) or `>= 0` (`-1` is rejected)
   - `nodeKey`: File Source node key (decimal string — read from `state.fileGraph.sources[i].key`, not `nodeKey`)
   - `sourceGraphLifetime`: decimal string (`state.fileGraph.sourceGraphLifetime`)
   - `expectedSourceGeneration`: decimal string (current source generation for that File Source)
2. **Command-group locks**:
   - `chlora_repair_open`: **forbids** `repairId` and `inputRevision`. Read `state.fileGraph.repairs[]` from the reply for `id` (`repairId`), `inputRevision`, `open`, `busy`, `renderHistory[]`, `activeStepId`, `plugins[]`, and `graph`.
   - `chlora_repair_close` / `chlora_repair_cancel`: **require** `repairId` (`1..128` chars); **forbid** `inputRevision`.
   - **Remaining 7 tools** (`set_selection`, `set_view`, `request_analysis`, `playback`, `history`, `graph`, `render`): **require both** `repairId` and `inputRevision` (decimal string).

## Selection, view, spectral analysis, and playback

- **`chlora_repair_set_selection`**:
  - `firstFrame`, `endFrame`: **16-digit max decimal strings** (`^(0|[1-9][0-9]{0,15})$`, `0 <= firstFrame < endFrame <= frames`).
  - `channels`: deduplicated integer array (`0..channels-1`, max 128).
  - Optional paired `lowHz` + `highHz` (`0 <= lowHz`, `highHz <= sampleRate/2`; if `highHz == 0`, `lowHz` must be `0`, else `highHz > lowHz`). Passing only one of `lowHz`/`highHz` is rejected.
- **`chlora_repair_set_view`**:
  - `firstFrame`, `endFrame` (16-digit max decimal strings `^(0|[1-9][0-9]{0,15})$`); optional `displayFftSize` (`0 | 2048`), `columns` (`1..2`), `trackHeight` (`160..600`), `canvasRatio` (`0.08..0.85`), `displayBlend` (`0..1`), `displayFloor` (`-140..-30`), `displayCeiling` (`-20..0`), `displayZoom` (`0.25..16`).
- **`chlora_repair_request_analysis`** (`readOnly: true` / `readOnlyHint: true`):
  - **All 8 payload fields are `required`** in the MCP schema: `firstFrame`, `endFrame` (16-digit max decimal strings `^(0|[1-9][0-9]{0,15})$`), `channels` (deduplicated int array), `bins` (**`64..4096`**), `columns` (**`32..4096`**), `rows` (**`64..1024`**, e.g. `256`), `referenceColumns` (**`64..1024`**, `>= 1`, e.g. `64`), and `requestId` (runtime **`1..96` chars**). Only `fixedFftSize` (`0 | 2048`) is optional.
  - Memory budget: `len(channels) * (bins * 8 + columns * rows) <= 64 MiB` (`64 * 1024 * 1024`).
  - Spectral packet metadata lives at **`repairs[].packet`** (`repairs[].packet.token`). The Host waits inline up to 250 ms for the packet and returns `mcpResult: {token, byteCount, encoding: "base64", packetData}` directly on first call; for oversized windows exceeding 250 ms, poll `chlora_get_state` until `repairs[].packet.token` is populated and re-call `chlora_repair_request_analysis` with the exact same arguments to fetch the bytes.
- **`chlora_repair_playback`**:
  - `action`: `"play" | "stop" | "toggle" | "seek" | "loop" | "clearLoop"`. `seek` requires `seconds >= 0`; `loop` requires `enabled: bool`, `startSeconds`, and `endSeconds > startSeconds`.

## Effect chain Graph (`chlora_repair_graph`)

Repair processing supports **Mono (`width: 1`)** acyclic serial chains of third-party non-instrument VST3 effects (up to 32 plug-ins; built-in routing/analyzer nodes, instruments, parallel branches, and loops are rejected).

- **Surface-open rule**: Except `setProcessingWidth` and `addPlugin`, the other **17 actions** require the Repair workspace surface to be open (`repairSurfaceEngine(repairId)` non-null; otherwise rejected with `"Open the repair workspace first"`). `repairCanvasState` also exports `multiLink`, `sandboxed`, `workerState`, `workerRetryable`, `workerToken`, and `workerRevision`.
- **Exact field names**: Use **`effectNodeKey`** (`sourceEffectNodeKey` / `destinationEffectNodeKey` for wiring) and **`exposedId`** — not `nodeKey` or `id` (batch actions `setNodesBypass`, `setMultiLink`, and `moveSelection` use `nodeKeys`).

| `action` | Required / optional fields | Notes |
|---|---|---|
| `setProcessingWidth` | `width` (`1` only in both schema and runtime) | Must be called before adding effects (`repair.order` empty) |
| `addPlugin` | `pluginUid`, optional `x`, `y` | Loads Mono third-party non-instrument effect (`-20000..20000`); returns `{effectNodeKey, pluginHistoryId}` in `mcpResult` (also readable from `state.fileGraph.repairs[].graph`) |
| `removePlugin`, `openEditor` | `effectNodeKey` or `pluginHistoryId` | Requires open Repair surface |
| `retryPluginWorker` | `effectNodeKey`, `workerToken`, `workerRevision` (`^-?[0-9]{1,20}$`) | Retries an unchanged isolated Repair plug-in worker |
| `setBypass` | `effectNodeKey` or `pluginHistoryId`, `on: bool` | Requires open Repair surface |
| `setNodesBypass` | `nodeKeys` (`1..128` unique), `on: bool` | Batch bypass across Repair effect nodes |
| `setMultiLink` | `nodeKeys` (`1..128` unique), `unlink: bool` | `unlink: false` requires `>= 2` nodes; `unlink: true` requires `>= 1` |
| `connectEffects`, `disconnectEffects` | `sourceEffectNodeKey`, `destinationEffectNodeKey` | Serial 1-in/1-out acyclic chain only |
| `moveNode` | `effectNodeKey`, `x`, `y` | `-20000..20000` |
| `moveSelection` | `nodeKeys` (`1..128` unique), `deltaX`, `deltaY` (`-20000..20000`) | Batch relative move |
| `resizeNode` | `effectNodeKey`, `w` (`72..20000`), `h` (`40..20000`) | Card resize |
| `listParameters` | `effectNodeKey`, optional `start`, `count` (`1..256`) | Returns `{parameters, parameterLayout, total, start}` |
| `setParameter` | `effectNodeKey`, `parameterId`, `parameterLayout`, `value` (`0..1`) | Normalized value write |
| `exposeParameter` | `effectNodeKey`, `parameterId`, `parameterLayout` | Returns `mcpResult: {effectNodeKey, exposedId, changed}` |
| `removeExposedParameter` | `effectNodeKey`, `exposedId`, `parameterLayout` | Removes exposed control by `exposedId` |
| `configureParameters` | `effectNodeKey`, `on: bool` | Toggles parameter capture |
| `setCanopyControl` | `effectNodeKey`, `exposedId`, `parameterLayout`, `choice` (`0\|1\|2`) | Sets Canopy control state |

## End-to-end render and DraftRoom import loop

`chlora_repair_render(nodeKeys=[...])` connects and freezes the serial effect chain (ending in a single sink) and renders the selected time/channel/frequency region.

**Critical presentation commit gate & headless `commit` alternative**: After offline audio rendering and FFT preparation complete, `repair.refresh.phase` enters **`"prepared"`** and waits for the WebUI DarkRoom view to acknowledge presentation (`fileGraphRepairPresented`). Only after that acknowledgement (or an explicit headless `chlora_repair_history(action="commit")`) is the rendered audio committed to `renderHistory[]` and `inputRevision` incremented! If no DarkRoom view acknowledges presentation within **30 seconds** (and no headless `commit` is issued), the candidate render times out and cancels (`"Rendered spectrogram presentation timed out"`).

Follow this exact end-to-end sequence:

1. **Open the visible/WebKit DarkRoom Repair window first** (this opens the Repair workspace/surface and automatically handles `fileGraphRepairOpen` + `fileGraphRepairPresented`), **or** for headless automation use `chlora_repair_open` + `chlora_repair_history(action="commit")` after `render`:
   ```text
   chlora_graph_ui_control(action="setNodeWindow", kind="darkroom", open=true, nodeKey="<fileSourceNodeKey>", ...)
   ```
   **Async open timing**: Because the WebUI's `ChloraRepairUI.open()` sends `fileGraphRepairOpen` asynchronously to C++, the immediate `op.result.ui.darkroomOpen` returned by `setNodeWindow` may still be `false`. Poll `chlora_get_state` until the matching source entry in `state.fileGraph.repairs[]` reports `open == true` and `analysis.ready == true` (read `id` as `repairId` and `inputRevision` as the optimistic lock from that entry; a subsequent `getUiState` call will now show `darkroomOpen == true`).
2. Configure selection (`chlora_repair_set_selection`), build/adjust the Mono serial chain (`chlora_repair_graph`), and trigger `chlora_repair_render(nodeKeys=["<sinkEffectNodeKey>"])`.
3. Poll `chlora_get_state` until `repair.busy == false` and either `repair.renderHistory[]` contains the new committed step (WebUI presented) or `repair.refresh.phase == "prepared"` (headless flow). In the headless flow, call **`chlora_repair_history(action="commit")`** (**omit `stepId`**, which is forbidden for `commit` and `import`) to commit the prepared candidate (`phase == "prepared"`, `status.ready`, `completedFftLevels == 6`) directly into `renderHistory[]` and increment `inputRevision` (returns `{committed, repairId, inputRevision, activeStepId}`).
4. Call **`chlora_repair_history(action="import")`** using the new `inputRevision` (**omit `stepId`**) to import the current `activeStep` back into DraftRoom as a new **File Source** node. (Use `chlora_repair_history(action="select", stepId="<id>")` to switch `activeStep` between steps before importing or re-rendering.)

Authority: [ChloraMcpExtended.h](../../../../../../Projects/mc-patcher/apps/host/juce/ChloraMcpExtended.h), [MainComponent.h](../../../../../../Projects/mc-patcher/apps/host/juce/MainComponent.h), [FileGraphRepairWorkspace.inc](../../../../../../Projects/mc-patcher/apps/host/juce/FileGraphRepairWorkspace.inc), [FileGraphRepairRefresh.inc](../../../../../../Projects/mc-patcher/apps/host/juce/FileGraphRepairRefresh.inc), [FileGraphRepairHistory.inc](../../../../../../Projects/mc-patcher/apps/host/juce/FileGraphRepairHistory.inc), [FileGraphRepairCanvas.inc](../../../../../../Projects/mc-patcher/apps/host/juce/FileGraphRepairCanvas.inc).
