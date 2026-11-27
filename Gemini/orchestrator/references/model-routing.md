# Model Routing & Dispatch Primitives (Antigravity SSoT)

On-demand single source of truth for Antigravity native model IDs, reasoning
effort, quota checks, dispatch primitives, and route receipts. For scaling
tiers and Flat Swarm topology see `complexity.md`; for `R0/R1/R2` review gates
and security redlines see `verification.md`.

## Native Model IDs

All native Gemini models share the single Antigravity `Gemini · 7 days` /
`Gemini · 5 hours` pool:

| Model | Native Dispatch & Exact IDs | Primary Role |
|---|---|---|
| **Neon** | `swarm` `gemini-4-neon-low\|medium\|high\|xhigh` *(always `swarm`; `invoke_subagent` only exposes `flash`/`pro`/`inherit`)* | Default engineering worker: UI coding & GUI perf, backend/DSP/concurrency/protocols/tests, Skill edits, parallel debug, deep audits, non-author reviews, persona content (`medium\|high`) |
| **Carbon** | `swarm` `gemini-4-carbon-low\|medium\|high` *(UI `@ui-carbon` uses `medium\|high` only)* or `invoke_subagent(..., Model: "pro")` *(pure read-only single-path visual review only)* | Secondary UI Art Lead (`@ui-carbon`): visual direction, tokens/skeleton, aesthetic sign-off (may read `<= 3` focused target files/tokens/diffs; never bulk-reads or writes bulk code); optional non-author R2 lens |
| **Hydrogen** | `swarm` `gemini-4-hydrogen-low\|medium\|high\|xhigh` *(`web-research` defaults to `gemini-4-hydrogen-medium` + `tasks: [...]`, optional `high\|xhigh` for deep dives; **never** `invoke_subagent`)* or `invoke_subagent(..., Model: "flash")` *(single isolated lightweight task only)* | Fast 1M-context worker: sharded file reading/inventory, repo/log sweeps, `>= 3`-way `web-research` (`swarm`), mechanical scripts/cleanup, volume/secret pre-scans. **Hard ban:** never edits UI production code |
| **Argon** | `swarm` `gemini-4-argon-low\|medium\|high` | Default `medium`; **user-named only** (never proactively dispatched) |

## Reasoning Effort

Default to the lowest effort that cleanly solves the slice; downgrade
aggressively for routine execution and all delta re-checks:

| Model | Effort Tier | Allowed Scope |
|---|---|---|
| **Neon** | `low` | Mechanical edits, formatting, simple config/copy/rename patches |
| **Neon** | `medium` *(default)* | Routine implementation, paired unit/focused tests, Skill authoring, GUI perf, **R1 reviews**, and **delta re-checks** (warm-reuse R2 reviewers in place via `post_message`; use `medium` for R1 or any freshly spawned delta checker) |
| **Neon** | `high` | **R2 reviews**, hard root-cause diagnosis, substantive DSP/realtime/architecture audits |
| **Neon** | `xhigh` *(strict allowlist)* | **ONLY** lock-free concurrency, memory-ordering, crypto/security-boundary proofs, or deadlocked root causes |
| **Carbon** | `medium` *(default)* | `@ui-carbon` visual direction, tokens/review/sign-off, routine UI updates, non-author reviews |
| **Carbon** | `high` | Strictly 0-to-1 visual design systems or major multi-surface redesigns |
| **Hydrogen** | `medium` *(default)* | Sharded reading/inventory, repo/log sweeps, cleanup, pre-push scans, default `web-research` (`swarm` + `tasks: [...]`) |
| **Hydrogen** | `high\|xhigh` | Deep-dive `web-research` slices only |

## Quota Eligibility

- Call `swarm(action: "models")` **at most once per session** (piggybacked in
  parallel with initial framing reads/setup) or **lazily only on quota/route
  error**—**never** re-query before every wave or follow-up.
- **Active pool (`7d remaining > 0%` and `5h remaining > 0%`):** 100% open to
  native Neon, Carbon, and Hydrogen.
- **Exhausted (`7d == 0%` or `5h == 0%`) or native route failure:** keep the
  slice on Primary (run `search_web` directly for `web-research`) and report
  the exact quota reading or error to the user.

## User-Named Overrides and Exclusions

Native **Argon** and any non-default native model returned by
`swarm(action: "models", all: true)` are **excluded from automatic dispatch**
and invoked **only** when the user explicitly names that model (and/or effort)
in the current request:

| User-Named Target | Dispatch Route & Exact Model IDs | Notes |
|---|---|---|
| **Gemini (Carbon / Neon / Hydrogen / Argon)** | Antigravity native `swarm` / `invoke_subagent` | Always native; Neon/Carbon/Hydrogen are default lanes, Argon is user-named only |
| **Other Native Models (e.g. Claude Opus / Sonnet)** | Antigravity native `swarm` (`swarm(action: "models", all: true)` for exact IDs) | Explicit user request only when available in the active Antigravity model list |

## Antigravity Dispatch Primitives, Zero Nesting & Warm Reuse

1. **`swarm` (primary multi-worker & engineering primitive):** call
   `swarm(action: "title", ...)` + parallel `swarm(action: "add", name, model,
   workspace, brief)` (use `tasks: [...]` for sharded homogeneous slices).
   `post_message`, `read_board`, and `swarm_wait` unlock on the turn after the
   first `add`. Mandatory for all Neon work, all UI coding/GUI perf, and all
   `>= 3`-way `web-research` (`gemini-4-hydrogen-medium` + `tasks: [...]`,
   reusing active or starting a new board; **never** `invoke_subagent`).
2. **`define_subagent` / `invoke_subagent` (single isolated task ONLY):**
   restricted to one lightweight non-UI task (`Model: "flash"`, defined once
   per session with `EnableSubagentTools: false`) or pure read-only single-path
   visual review (`Model: "pro"`). Never use for `web-research` or UI code.
3. **Zero nesting across ALL workers:** no worker—including `@ui-carbon`, Neon,
   Hydrogen, or `invoke_subagent` helpers—may ever spawn subagents. Every brief
   carries `严禁派生任何子代理`; `define_subagent` sets `EnableSubagentTools: false`.
4. **Workspace isolation:** default `workspace: "inherit"` with disjoint path
   leases (+ dedicated build lanes when compiling/testing). Use
   `workspace: "share"` only when paths overlap or build trees collide without
   dedicated lanes (land diffs before `swarm(action: "kill", ...)`).
5. **Warm reuse cap vs. no inter-wave premature kills:** never casually `kill`
   healthy `waiting` `swarm` workers between waves (zero idle tokens, full
   context retained—e.g. winning debug investigator -> fix writer); reuse via
   `post_message(text: "@<name> <续跑指令>")` and `invoke_subagent` via
   `send_message(Recipient: "<conversationId>", Message: "...")`. Workers may
   self-report `[compacted]` in summaries. **Atomic two-step retirement:** once
   a worker accumulates `>= 3` context compactions (`CHECKPOINT`), spans `>= 4`
   major waves, or repeatedly re-reads the same files post-compaction: (1) the
   outgoing worker lands diffs (if `share`) and posts a `<= 20`-line structured
   handover (`#seq`) to **`@coordinator`**; (2) on wakeup, Primary runs
   `swarm(action: "kill", old)` + `swarm(action: "add", new, brief: "...citing #seq...")`
   in the **same turn** (preventing dual-writer overlap or missed wakeups).
   Workers stop immediately on unfrozen interfaces, lease conflicts, external
   edits, or permission/hook denials.
6. **No-polling anti-pattern & long async watchdog:** Primary and all workers
   are strictly forbidden from loop-polling `manage_task(status)` /
   `swarm(action: "status")` / `read_board` / `tail -n`; rely exclusively on
   reactive async wakeups (`swarm_wait`, task notifications), reserving
   `swarm(action: "status")` for anomaly troubleshooting or final receipt checks
   (for external non-swarm lock `blocked`, use a single delayed `schedule` retry
   or `blocked-technical`). For any external/cloud job expected to exceed
   `> 10 min` (Colab, long builds, external CI), Primary must confirm an active
   `schedule` watchdog before entering `swarm_wait` and attach any replacement
   timer **before** cancelling the old one.

## Route Receipts

Verify native Antigravity execution before slice/wave integration (without
polling loops):

- **`swarm`:** verify `read_board` `[done]` posts (use `swarm(action: "status")`
  only for final receipt or anomaly troubleshooting; read-only workers require
  only `[done]` verdicts); for writers, also check real disk diffs
  (`git status --short`, `git diff --stat`) and raw L1–L2 exit codes/summaries.
- **`invoke_subagent`:** verify returned `conversationId` completion message
  (plus disk diffs and raw outputs for write tasks).
- **Long async jobs (`> 10 min`):** verify a `schedule` watchdog was active
  across `swarm_wait` windows and handoffs replaced timers before cancellation.
