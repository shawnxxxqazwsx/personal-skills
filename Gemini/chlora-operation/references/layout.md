# Arrange the Graph and simplify wiring

Use this when the request includes 整理线路, 简洁排版, fewer visible jumps,
alignment, Comments, Pins, or camera changes; also apply it while an authorized
Graph operation or test setup creates or changes any Graph element. This is a
mandatory construction rule for user projects, QA, reproductions, temporary
probes and presentation captures. New work must remain orderly, free of node
overlap, easy to trace and as visually simple as the required routing permits.
For a current project or production Graph, preserve its intentional arrangement
outside the authorized change. Do not change signal routes, add/remove
processing stages, or alter Group membership solely for appearance. A simpler
drawing must not merge independent processors, sum channels accidentally, or
replace a sidechain.

## Keep every addition readable

- Plan free space before creating or pasting an element; do not stack objects
  at a default origin and defer cleanup until the end. Apply the same rule to
  nodes, inserted plug-ins, Router/Snake/Merge objects, Group/Stack regions,
  boundary ports, Pins and Comments. A container may enclose its owned members;
  that intended containment does not permit cards, headers or controls to
  obscure one another.
- Arrange signal stages left to right, parallel paths in consistent rows, and
  returns/sidechains in separate legible lanes. Keep related ports close and
  connection corridors clear. Use enough spacing for actual intrinsic controls,
  attachment rails and expanded content, rather than just stored anchors.
- After an asynchronous load or insertion, check the new rendered envelope
  before adding the next element. Reserve clear space for unknown sizes and
  adjust only the authorized region. Paste or preset insertion must fit clear
  of existing content; preserve internal geometry when translating a region.
  Reopening a saved project still restores its exact geometry, not a new layout.
- Use the minimum necessary visible jumps, crossings, bends and Pins for the
  requested topology. Tests obey this standard too: if discrete cables are the
  failure signal, keep them neatly ordered and visible until that behavior is
  tested; do not aggregate away the condition under investigation.
- Creating a Group can already establish MAIN boundary Fanouts. Read the
  returned Group `fanouts` before adding another port; reuse the matching
  boundary when it represents the intended route. Place any necessary extra
  port at a distinct side position with enough rendered spacing, rather than
  adding it on top of the existing midpoint port.
- Verify both unobstructed controls and traceable cables in the rendered
  result. Bounds/quality metrics support this check but do not replace visual
  inspection. If native rendering is unavailable, record that evidence limit;
  do not claim visual acceptance from coordinates alone.

## Choose a layout from the topology

| Shape | Arrangement decision |
|---|---|
| Serial bus | Left-to-right stages, ports near a shared horizontal axis |
| Parallel branches | Split at one point; one row per branch; gather once downstream |
| Dry/wet return | Short wet chain; dry bypass outside node bounds, Pins only if needed |
| Selected-channel processing | Dense aggregate connections around a subset processor/Stack; preserved channels remain legible |
| Repeated mono/stereo lanes | Stack if that is the requested independent processing unit; do not convert existing nodes just to reduce lines |
| Sparse or remapped channels | Ordered Bundle/PortSnake and explicit Router mapping; annotate the mapping when helpful |
| Group or nested region | Move containers and their owned contents as a unit; show boundary ports clearly |
| Feedback/sidechain | Separate return/auxiliary lane and explicit role; retain intended junctions |

Order stages from the actual directed routes, not current x coordinates. Keep
parallel branches aligned and enough room for intrinsic node dimensions. Minimize
unnecessary crossings, node obstacles and detours. Do not overlap ordinary node
envelopes or route a cable through unrelated controls. Intended fanout junctions,
shared cable paths and container/member containment are different from obstructing
nodes. Do not require zero total `wireIntersections`: retain necessary junctions
and crossings without adding avoidable clutter. No fixed coordinate grid or
piano layout applies.

“Fewer wires” means fewer necessary visible cables, with the complete audio
lanes, endpoints, bus roles, branches and mappings preserved. Prefer compatible
Snake/Bundle/PortSnake boundaries and supported preserving conversion of existing
discrete lanes when it simplifies the requested work. Check Pins, geometry,
history and persistence as well as expanded endpoint equivalence. Legacy wrap
operations may clear incident edges; do not delete and rebuild established
routing merely to obtain a cleaner picture. If safe aggregation is unsupported,
retain the routes and improve their geometric arrangement instead. Do not
introduce Group/Stack conversions solely for decoration.

## Use actual renderer geometry

**Scope note**: The renderer Layout API (`chlora_get_capabilities`, `chlora_graph_get_layout_geometry`, `chlora_graph_preview_layout`, `chlora_graph_validate_layout`, `chlora_graph_apply_layout`, `chlora_graph_align_ports`, `chlora_graph_set_group_port_position`, and `graph_layout.py`) supports **ordinary sessions (`instanceId >= 1`) and Standalone FileGraph (`instanceId = 0`)**. It does **not** support Background Patchbay (`state.patchbay == true`); in Patchbay, move nodes/Groups/Comments through `chlora_patchbay_control(action="graphCommand")` with `chlora_graph_move_node`, `chlora_graph_move_group`, or `chlora_graph_move_comment`.

1. Begin with `chlora_get_capabilities({})`: require schema2, a ready renderer,
   supported plan fields/quality/projection and sufficient limits. This unbound
   native preflight establishes connected Host support; static schemas do not.
2. Request `chlora_graph_get_layout_geometry` with `detail: "nodes",
   representation: "compact", includePorts: false`. Follow every continuation
   with the same binding/projection/revision until null. Validate offsets,
   returned counts, totalItems and unique identities before planning; pages may
   shrink to fit 1 MiB. Inventory covers up to 4096 committed objects/128 Groups.
   `items` records nodes, Group/Stack, Comment and Pin ownership. Hidden routing
   nodes have no visible footprint. Await pending loads before collecting. Optional
   `observer: "read" | "calibrate"` (plus `observerPixels: boolean` only with
   `calibrate`) enables opt-in real-page RAF/Nebula timing diagnostics before
   layout work; neither measures physical compositor/GPU presentation latency.
3. Positions/bounds use native Graph world units, **3× world CSS**. `position`
   is the move anchor; `bodyBounds` is actual card size; `bounds` includes Snake
   extensions. Place the next anchor using its envelope-to-anchor offset as well
   as the preceding right edge and gap. Node `size:{wCss,hCss}` is stored CSS
   sizing; intrinsic controls may enlarge its actual body. Group `position` and
   `frameSize`, and Comment `position` and `size`, are stored native geometry.
   The 66-unit grid/fractional cells are metadata; preserve free dragging.
4. Build a mixed plan with loose `nodes`, frame edits `groups`, boundary
   `groupPorts`, absolute saved Group origins `containers`, `comments`, `pins`
   and CSS `nodeSizes`. Container translation moves owned descendants once;
   exclude independent descendant position rows and nested moved containers.
   Hidden/attached/Stack-owned nodes and boundary ports are not independent
   moves/resizes. Stack boundary sides are fixed. Containers need a saved frame.
   A saved container frame that cannot contain its rendered contents must be
   updated before translation; preview rejects that mismatch before any write.
5. Preview once with `quality: "bounds"`, then apply its exact normalized delta
   and observed revision with `quality: "none"` (or use read-only
   `chlora_graph_validate_layout` with optional `layout` to score current or
   proposed geometry). All layout operations validate identity,
   ownership, ranges and revisions; a mixed commit adds one undo snapshot and
   does not publish audio topology. Bounds compares affected ordinary node
   envelopes against all ordinary visible obstacles, with 250000 pair-test
   budget and explicit partial status. It does not score wires. `full` remains
   the default and retains global 256-visible-node/512-wire and path budgets;
   a small proposal does not bypass those limits. Use full only when its
   wire-quality scope and budget are appropriate.
6. Await operations and collect fresh compact pages. Verify original requested
   anchors/sizes, effective envelopes/ownership, unchanged unrelated objects and
   semantic wire multiset including hidden routes. Scoped replies may omit
   large container descendants with explicit affected/returned/omitted counts
   and `readbackRequired`; fresh pages complete verification. Stale revisions
   require recomputation. A timeout has unknown outcome: retain transcript and
   operation ID; never blindly replay a write.

The deterministic helper provides the complete coordinate workflow:

```bash
python3 "$SKILL_DIR/scripts/graph_layout.py" collect --socket /absolute/verified.sock --socket-identity DEVICE:INODE --transcript collect.jsonl --output inventory.json
python3 "$SKILL_DIR/scripts/graph_layout.py" plan --inventory inventory.json --spec spec.json --output plan.json
python3 "$SKILL_DIR/scripts/graph_layout.py" execute --socket /absolute/verified.sock --socket-identity DEVICE:INODE --transcript execute.jsonl --plan plan.json --output result.json
```

Derive DEVICE:INODE from the verified intended Host socket; do not pick the
newest socket or create a session automatically. Use new output/transcript paths.
`spec.json` uses a top-level `"mode"` key:
- `row`: `{"mode": "row", "nodeKeys": ["10", "11"], "origin": [400, 1200], "gap": 240}` (do **not** wrap in `{"row": {...}}`; do not include fixed auto-snapped FileGraph boundary nodes such as the default `File Output` in `nodeKeys`, and ensure `origin` clears any unmoved existing nodes on the canvas so Host anti-overlap pushback after `commit` does not shift anchors and cause `verify_readback` to fail with `geometry readback differs`).
- `parallel`: `{"mode": "parallel", "lanes": [["10", "11"], ["12"]], "origin": [400, 800], "gap": 240, "rowGap": 240}`
- `topology`: `{"mode": "topology", "nodeKeys": [...], "origin": [400, 800], "gap": 240, "rowGap": 240}` (visible MAIN DAG only; requires `--state`)
- `explicit`: `{"mode": "explicit", "layout": {...}}` (mixed layout)
Cycles, sidechains, dependent/owned nodes
and ambiguous layouts need an explicit plan. Finite planners do not establish
optimal readability for arbitrary graphs. The helper keeps one stdio connection,
validates complete pagination and readback, and preserves audit evidence. A truncated pure-container preview can be
projected from complete before geometry and checked after apply; a truncated
nonlinear mixed resize/relative edit stops before writing and needs a smaller
proposal. Independent card sizing applies to ordinary plugin nodes as well as Align (`isChannel`), Merge (`isSum`), and Router (`isRouter`) (`chlora_graph_resize_node(nodeKey, w, h, x?, y?)` in CSS pixels, `w: 72..20000`, `h: 40..20000`, optional paired `x`/`y` `-20000..20000` with `has(x) == has(y)` in one atomic undo snapshot), including internal
processors; IO, Bundle, Fanout, and PortSnake sidecars are rejected by `chlora_graph_resize_node`.

`chlora_graph_align_ports` aligns current port descriptors to a reference on
x or y; request ports explicitly and use rendered ordinals 0..255, distinct
from Snake branch indices 0..63. `chlora_graph_set_group_port_position` places one current boundary port
on its side; both use the observed renderer revision. Topology-level
`chlora_graph_move_group_fanout` updates the native boundary position without
that renderer API. Keep Stack left/right boundary alignment where helpful;
do not invent extra Stack boundary Fanouts.

## Pins, Comments and exact presentation scope

Pins bend one exact visible wire. `chlora_graph_add_cable_pin` needs live endpoint
keys, channels, destination role, and for an aggregate the width and both branch
numbers. Keep returned `pinId`; move/remove with `chlora_graph_move_cable_pin` /
`chlora_graph_remove_cable_pin`, or batch-remove multiple Pins via **`chlora_graph_node_advanced(action="removeCablePins", pinIds: [...])`** (no `nodeKey` needed; `delete_selection` does not remove Pins). Set `curve` or `straight` using
`chlora_graph_set_wire_style` on the same exact identity (also supported in Background Patchbay via `chlora_patchbay_control(action="graphCommand", operation="chlora_graph_set_wire_style")`). Re-read after topology
changes, since a former wire/pin identity may no longer exist. Live `wire.bakedRoute` (`{sig, pts}` in `state.get` `graphWires[]` and `graph.get_summary` `wires[]`) is a WebView-only debounced Bézier obstacle-avoidance cache committed internally via `commitGraphBakedWireRoutes` after render idle: it is **read-only from MCP** and automatically invalidated by C++ when nodes move or topology changes (for preset-stored baked routes, use `get_preset` `wires[].bakedRoute` and `layout.wires` on `update_preset`/`load_preset`).

Use `chlora_graph_create_comment`, `chlora_graph_set_comment_text`,
`chlora_graph_move_comment`, `chlora_graph_resize_comment` and
`chlora_graph_remove_comment` for independent annotations. A Comment can label a
branch or encompass a region; keep its header/control affordances away from
processor controls. `chlora_graph_set_group_comment` edits a Group's title.
Stack labels are not a routing operation; use a separate Comment if the desired
annotation is not rendered on that container. Optional `parentGroupId` attaches
an annotation to an allowed ordinary Group; do not assume Stack nesting support.

For mixed removal, `chlora_graph_delete_selection` takes explicit nodeKeys,
groupIds, commentIds and exact wires (unused arrays empty). Group removal and
node deletion have different native semantics; inspect membership/owned routes
before choosing a cleanup operation. Never delete an audio node to remove its
annotation. Prefer exact MCP identities for removal. If an authorized native/UI
fallback uses Delete or Backspace, establish and inspect the complete intended
selection across nodes, containers, annotations, endpoints, cables and Pins
before pressing it. A highlighted cable alone does not establish that other
categories are deselected. Verify preserved objects and routing after removal;
refresh full state after any recovery Undo before continuing.
`chlora_graph_move_selection` shifts `nodeKeys` and optionally one Comment by a
delta; container moves use Group tools.

## Camera and display preferences

`chlora_graph_ui_control` (drawers, dialogs, node windows including `irDistance`/`nebulaRamp`/`presetEditor`, and `Shift+A` add-palette; Strip-safe actions `getUiState`/`setConsoleWidth`/`setDialog`/`setPluginDrawer` allow omitting both `graphTopology` and `graphLifetime` together), `chlora_graph_get_view_preferences`, `chlora_graph_set_viewport`,
`chlora_graph_set_spatial_meter`, `chlora_graph_set_cable_dead_zone`,
`chlora_graph_set_stack_names`, `chlora_set_zoom` (`percent`: `75|100|125|150|175`), and
`chlora_graph_analyzer_control` (`setNebulaViewing` / `setSpectrogramViewing`) operate through the visible WebUI. `chlora_graph_ui_control` and the Graph view preference commands are
asynchronous; poll `chlora_get_operation` and read back `result.ui` or the preference afterward. Stack Names requires the
incoming channel identity; see [nodes.md](nodes.md). Spatial meters require an available
speaker layout on that side. Camera pan is in CSS units, separate from node
native coordinates; `(zoomScale: 0.7, panX: 0, panY: 0)` resets the view to 100%.
Preserve the camera during unrelated edits; frame/reset only as requested or
when needed to show the result. Keep the changed path within a readable viewport
when the authorized operation permits it, and read back any camera change.
Extreme zoom, cropping or dumping new objects far from the coherent layout is
not a substitute for fixing clutter or overlap. Keep every added element
discoverable and the affected signal path inspectable at a useful scale.

Visual quality and unchanged semantic routing are separate checks. Inspect the
rendered result when available; stored anchors, sizes, counts and metrics do not
prove actual cable readability. If geometry omits an owned/attached visible
endpoint or jack, use an already-authorized rendered UI/fallback inspection
path; otherwise record that exact element as unverified. Do not invent ports or
detach an owner to make it appear covered.
