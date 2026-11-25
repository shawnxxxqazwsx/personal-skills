---
name: memory
description: >-
  Read and write persistent cross-model developer preferences (procedural),
  project-level milestones and durable conclusions (episodic), and stable
  architecture/domain facts (semantic/resource) in ~/.mnemon-mcp/memory.db.
  Use when the user states a preference or workflow rule, asks about recent
  project milestones, or asks to remember, update, or recall durable facts
  across sessions and models.
---

# Cross-Model Long-Term Memory (`mnemon`)

Persistent SQLite + FTS5 store at `~/.mnemon-mcp/memory.db`, shared across models and sessions via two paths:

1. **Active MCP Tools (`mnemon` / `user-mnemon`)** — available in `antigravity`, `claude`, `claude-desktop`, `codex`, `cursor`, and `dsh`.
   - **Antigravity native sessions** bypass the Magpie gateway: always call `memory_search` / `memory_add` / `memory_update` directly. If MCP is unavailable in a native session, tell the user honestly that nothing was auto-persisted instead of emitting hook tags.
2. **Magpie Gateway Auto-Hook (`http://127.0.0.1:3425`, external models only)**:
   - Applies **only** to external models routed through Magpie (`/v1/chat/completions`, `/v1/messages`, `/v1/responses`). `onRequest` injects `<magpie_shared_memory>`; `onResponse` persists `<magpie_memory_write layer="..." scope="..." title="...">...</magpie_memory_write>`.

## Cognitive Layers & Scope Boundary

| Layer | `entity_type` | `scope` | What to store |
|---|---|---|---|
| `procedural` | `rule` | `global` or `<project>` | Developer preferences, reporting style, coding & routing rules |
| `episodic` | `project` | `<project>` (e.g. `mc-patcher`) | Project-level high-level milestones and cross-session durable conclusions |
| `semantic` | `project` / `concept` | `global` or `<project>` | Project catalog, architecture contracts, hardware-fit thresholds, environment paths |
| `resource` | `file` / `tool` | `global` or `<project>` | Key file paths, external documentation links, device/LAN endpoints |

- **Do NOT store** single-session stopping points, uncommitted diff details, dirty-tree status, or first continuation instructions for a fresh window (those belong in temporary task-switch handoff notes, not long-term memory).

## When to Write or Update

1. **New or updated preference** ("以后都这样…", "记住我喜欢…", "不要再…"):
   - Search first with `memory_search`; update via `memory_update(id=..., supersede=true, new_content=...)` or create via `memory_add(layer="procedural", scope="global", entity_type="rule", importance=0.95, title=..., content=...)`.
2. **Project-level milestone or durable cross-session conclusion**:
   - Update the project's `episodic` entry (`scope="<project>"`, `entity_type="project"`, `entity_name="<project>"`).
3. **Magpie-routed fallback (when MCP is unavailable on a gateway-routed model)**:
   - Append `<magpie_memory_write layer="procedural|episodic|semantic" scope="global|<project>" title="...">...</magpie_memory_write>` at the end of the response.
