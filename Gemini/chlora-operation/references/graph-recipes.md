# Advanced Graph combinations

Use [fastpaths.md](fastpaths.md) for common routes and [nodes.md](nodes.md) for
entity capabilities. These examples extend the same width, identity and scope
rules; they are not universal requirements or fixed project layouts.

## Sidechain feeds

Confirm the destination's actual `sidechainIn` and bus format. Keep MAIN and
SIDECHAIN roles distinct. `chlora_graph_connect_bus` with
`destinationRole: "sidechain"`, exact starts and width connects a contiguous
auxiliary feed without replacing the main path (including from a regular Group boundary Fanout with nonzero local width to an ordinary unwrapped non-Sum peer). For atomic inline Align insertion onto a sidechain or MAIN wire, use `chlora_graph_node_advanced(action="insertAlignOnWire", nodeKey, destinationNodeKey, sourceChannel, destinationChannel, destinationSidechain: true|false, isBundle, channelCount, sourceBranch, destinationBranch, x, y)`. `chlora_graph_set_bus_format` can request
supported input/output formats and sidechain width; inspect effective widths
before routing. A declared layout is not proof the plug-in accepted it.

`chlora_graph_disconnect_channel` accepts optional `destinationRole: "main" | "sidechain"` (default `"main"`) to remove one exact SIDECHAIN feed without disturbing MAIN connections. For batch or multi-wire cleanup of an existing SIDECHAIN feed, `chlora_graph_delete_selection` with its exact `fromRole/toRole/fromCh/toCh` wire identity and empty unused selection arrays also works; check neighboring MAIN feeds afterward. Preset insert-on-wire is MAIN-only; retaining internal sidechain edges does not make an external SIDECHAIN insertion supported.

## Sparse channels, channel reordering and unequal buses

Choose selected order deliberately. Both PortSnake and native Bundle packing
sort one owner's MAIN channels ascending; Bundle append merges existing lanes
and deduplicates. Appending from a different source owner is rejected. Neither
preserves an arbitrary input-array permutation.

For ordered source selection S, map source channel S[j] into output j of a
compatible detached Router, clearing unwanted default crosspoints. Then pack
its dense outputs 0..K-1, where K=|S|. The ascending pack now preserves the
deliberately mapped processing order. Verify every crosspoint and packed lane.
At a full-width gather, an input PortSnake for T=sorted(destination selection D)
places processed dense lane j into input T[j]. Map that input to requested output
D[j], replacing the corresponding default selected crosspoints; leave untouched
outputs on their intended identity mappings. This is the inverse/per-destination
mapping, not another guessed array order. A different destination order or width
must use its own D, input limits and output limits. Route multi-source assembly
through a supported explicit Router/mapping stage rather than one mixed-owner
Bundle append. Check the native endpoint capability before connecting.

For selection S in a W-channel path, the subset processor needs |S| channels.
A full-width identity Router can gather processed S plus preserved other lanes.
When source/destination widths differ, `chlora_graph_set_router_channels`
requests independent input/output widths; shrinking a connected port is
rejected until affected routes are resolved. Set explicit crosspoints with
`set_router_route` or batch crosspoints with `chlora_graph_node_advanced(action="setRouterRoutesBatch", routes, on)`; clear one output before replacing its mapping when needed.
`reset_router` restores identity and may overwrite intentionally remapped rows.
Do not confuse an intentional matrix fan-in with an exclusive channel route.
For per-branch internal cross-channel mapping inside a `Merge` (`sum`) node, use `chlora_graph_node_advanced(action="setMergeBranchRoute", nodeKey, branch, input, output, on)` and `resetMergeBranchRoutes(nodeKey, branch)`. Note also that Router output ports do not accept `bundle_append_channels` (use `chlora_graph_create_port_snake` on Router outputs).

For independent stereo pairs, a Stack preserves pair boundaries. For uneven
partitions (mono plus stereo plus a wider bus), use separately width-matched
processors and explicit gather mapping. One uniform Stack does not represent
a wider lane or every mixed partition. Restore unselected channels if their
aggregate wire had to be replaced. Validate exact lane ordering, not just a
matching total width.

## Native Multi-Mono wrapper control

When independent per-channel mono processing is needed on one wrapped Graph plug-in node instead of a Stack, use `chlora_graph_node_advanced`:
- `action: "setMultiMono"`, `nodeKey`, `channels: 1..128` — converts/resizes the node into N mono lanes (requires a mono-capable plug-in).
- `action: "syncMultiMonoState"`, `nodeKey` — copies visible/current lane parameter state across the Multi-Mono lanes.
- `action: "setMultiMonoAutoSync"`, `nodeKey`, `on: boolean` — enables/disables ongoing Multi-Mono auto-sync.
Read back `lanes` and `autoSync` in the command detail/state rather than substituting Stack or `set_multi_link`.

## LFO modulation edges

1. Create an LFO (`chlora_graph_add_builtin(kind="lfo", x, y)`, no `channels`).
2. List target parameters (`chlora_graph_list_parameters`, reading `parameterLayout` from the response top level) and expose the intended writable `parameterId` via `chlora_graph_expose_parameter`, which returns **`mcpResult.exposedId`** (also stored in `target.exposed.parameters[].id`).
3. Connect with `chlora_graph_connect_lfo(nodeKey=lfoKey, targetNodeKey, exposedParameterId=exposedId, parameterLayout)`. **One target parameter can be driven by at most 1 LFO at a time** — connecting a second LFO driver to the same exposed parameter conflicts.
4. Tune edge depth (`chlora_graph_set_lfo_depth`, `-1..1`) and range (`chlora_graph_set_lfo_mapping`, `mode: "modulate" | "remote"`, `0 <= minimum <= maximum <= 1`).
5. Read back `graphModulations[]` for `source`, `target`, `id`, `layout`, `base`, `depth`, `mode`, `minimum`, `maximum`, and `active`.
   - `chlora_graph_disconnect_lfo` requires matching the stored `layout` from **`state.graphModulations[].layout`** (plus `exposedParameterId = graphModulations[].id`), and restores `base` only when the target remains resolvable under that stored layout.
   - **Field-name mapping across tools**: `chlora_graph_expose_parameter` returns `mcpResult.exposedId` (stored as `node.exposed.parameters[].id`); LFO edge tools (`connect_lfo`, `disconnect_lfo`, `set_lfo_depth`, `set_lfo_mapping`) pass **`exposedParameterId`**; whereas `chlora_graph_remove_exposed_parameter` takes **`id`** (matching `exposedId`).
   - Modulation-only edits do **not** advance `graphTopology`.

## Parameter-linked processing and independent copies

Graph `chlora_graph_set_multi_link` requires compatible hosted plug-ins; link
at least two explicit keys, or `unlink: true` for specified memberships.
Inspect returned `multiLink` IDs before assuming propagation. Persistent
MultiLink and temporary `chlora_graph_set_sync_selection` are distinct.
Clearing temporary selection uses `nodeKeys: []` and leaves persistent links.
They share parameters/state according to native semantics, not audio wires.

For Stack v2 per-channel gains, toggles, slot bypass, and Armada group sync (`syncArmadaGroup`), use `chlora_graph_stack_control`. For a Stack macro, list the first member's parameters, retain its layout and current normalized value, and call `chlora_graph_set_stack_macro` with matching `groupId` (Armada group or Stack `nodeKey`/parent group), `nodeKey`, `parameterId`/`parameterLayout`, `gesture`, `sourceStart`, `value`, and `absolute` (`false` applies relative delta preserving lane offsets within native clamps; `true` requests the same value across compatible members). Always read back each member's resulting quantized value; Stack membership alone does not mean every direct member parameter write propagates.

Copy/duplicate/recall can allocate new keys and asynchronous workers. Do not
reuse old member IDs. Use current native state to determine which link/sync
memberships survive an import rather than inferring from matching names.

## Named subsets in any layout

If current names identify a subset of adjacent stereo pairs, an N-lane stereo
Stack can process those 2N channels within a wider bus. Resolve N, indices and
pair order from the current layout. An odd leftover mono channel needs its own
mono lane or processor; do not silently discard it or pair it with an unrelated
channel. Sparse/nonadjacent pairs need explicit packing/mapping.

One possible composition is full-width parallel dry/wet return, then a
full-width serial processor, then selected pair processing with a Router
gather. Another puts the subset inside the wet branch. Follow the user's
requested ordering, since those topologies have different signal behavior.
The Stack width is the selected lane total, independent of session width. Names
availability follows actual incoming channel identity, including subsets and
Router permutations. Read the view preference after routing; annotate the branch
when its incoming identities remain unresolved. Nothing in this example requires a named third-party
model or a particular session's node keys.

## Recovery after partial edits

Multi-step recipes can stop after a successful earlier mutation. Read current
state, identify changed edges/parameters/containers and the last confirmed
operation, then choose bounded recovery within the requested scope. `chlora_undo` / `chlora_redo` accepts
one history operation and restoration can remain in flight: if `stateRestoreInFlight` is `true`, poll `chlora_get_state` until `stateRestoreInFlight == false`
before reading new `nodeKey`s, binding tokens, or issuing any write. Never
replay a timed-out paste/load or CLI exit-code `4` (`outcome_unknown`) write to “finish” an uncertain outcome. Keep the user's
unrelated routes and saved-state boundaries intact.
