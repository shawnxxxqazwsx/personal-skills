# Execution & Model Routing (Antigravity Single Source of Truth)

Inspect live Antigravity tool schemas (`swarm`, `invoke_subagent`,
`define_subagent`, `post_message`, `read_board`, `send_message`) and bridge
availability (`~/.local/bin/magpie-agent`, `cursor:magpie_agent`) at call time.
Single source of truth for model IDs, effort, routing, scale, quotas & receipts.

## Native Model IDs

All native Gemini models share the single Antigravity `Gemini · 7 days` /
`Gemini · 5 hours` pool:

| Model | Native Dispatch & Exact IDs | Primary Role |
|---|---|---|
| **Neon** | `swarm` `gemini-4-neon-low\|medium\|high\|xhigh` *(always `swarm`; `invoke_subagent` only exposes `flash`/`pro`/`inherit`)* | Default engineering worker: UI coding & GUI perf, backend/DSP/concurrency/protocols/tests, Skill authoring, parallel debug, deep audits, non-Neon independent review |
| **Carbon** | `swarm` `gemini-4-carbon-low\|medium\|high` *(UI `[Carbon-UI-Lead]` uses `medium\|high` only)* or `invoke_subagent(..., Model: "pro")` *(pure read-only single-path visual review only)* | Secondary UI Art Lead (`[Carbon-UI-Lead]`): visual direction, tokens/skeleton, aesthetic review & sign-off; non-author review of Neon diffs |
| **Hydrogen** | `swarm` `gemini-4-hydrogen-low\|medium\|high\|xhigh` *(`gemini-4-hydrogen-medium` + `tasks: [...]` mandatory for `>= 3`-way `web-research`)* or `invoke_subagent(..., Model: "flash")` *(single isolated lightweight task only; never `web-research`)* | Fast 1M-context worker: sharded file reading/inventory, repo/log sweeps, `>= 3`-way `web-research` (`swarm`), mechanical scripts/cleanup, volume/regex pre-scans, read-only/inventory `[Carbon-UI-Helper]` |
| **Argon** | `swarm` `gemini-4-argon-low\|medium\|high` | Default `medium`; **user-named only** (never proactively dispatched) |

- **Persona / anthropomorphic content:** native **Neon**
  (`gemini-4-neon-medium|high`); routine bot logic/adapters use standard routing.

## Reasoning Effort

| Model | Default | Same-Category Multi-Instance Sharding | Peer-to-Peer Direct Collaboration (`@<peer>` / `#seq`) |
|---|---|---|---|
| **Neon** | `medium` (`high` for reviews) | `low\|medium`: sharded UI/component coding, routine backend/CLI/Skill edits<br>`medium\|high`: GUI perf, substantive DSP/backend, parallel debug hypotheses, module audits<br>`high\|xhigh`: realtime/lock-free concurrency, **multi-way (`>= 2`) non-author reviews** & security/logic audits | Implementation peers (`low\|medium\|high`) ↔ `@ui-carbon` or read-only `verifier` (`high\|xhigh`) direct fix loops; escalate frozen interface/lease changes to `@coordinator` |
| **Carbon** | `medium` | `medium`: `[Carbon-UI-Lead]` visual review/sign-off, non-author review of Neon diffs<br>`high`: 0-to-1 visual design systems, major redesigns, heavy cross-surface aesthetic or Neon-diff audits | Acts as `@ui-carbon` peer hub (`medium\|high`) directing `2–10` Neon/Hydrogen UI peers and approving final diffs before `@coordinator [done]` |
| **Hydrogen** | `medium` | `medium`: directory-sharded file/style/asset inspection, `>= 3`-way `web-research` (`swarm` + `tasks: [...]`), workspace cleanup, pre-push secret/volume sweeps (never UI production code edits from Primary or Carbon) | Fast reader/scanner peers (`medium`) feeding findings directly to `@ui-carbon` or Neon auditors via `@<peer>` & `#seq` |

## General Scenario Lane Routing

| Scenario | Primary Lanes & Multi-Instance Split | Mandatory Review / Gate |
|---|---|---|
| **Light Tier (`0 <= N <= 5`)** *(ultra-simple local feature or small Skill tweak: 1–3 tightly coupled files ONLY)* | `N = 0`: Primary edits & verifies directly; `1 <= N <= 5`: `<= 5` concurrent native workers (light `swarm` or single `invoke_subagent`; Neon `low\|medium` for small code/Skill tweaks, Hydrogen `medium` for quick checks; no auto-Magpie; no Hydrogen UI edits) | Primary self-check or 1 read-only check; **must escalate to Standard Tier** for `>= 2` independent modules, audits, parallel debug, UI overhauls, large Skill refactors, `>= 3`-way `web-research`, or workspace push (public GitHub security gate never relaxes) |
| **Audio / Backend / Systems** *(Standard Tier; + `immersive-audio` / `daw-control` when active)* | Neon (`medium\|high\|xhigh`) for DSP/realtime/host/bridge/tests + Hydrogen (`medium`) for repo/log sweeps & fixtures | `>= 2` non-author reviewers (Neon `high\|xhigh` / Carbon `medium\|high`) |
| **Skill Authoring & Review** | Hydrogen (`medium`) for cross-file inventory/link checks + Neon (`low\|medium`) for Skill/reference edits | `>= 2` independent read-only reviewers (Neon `high` / Carbon `medium`) |
| **Multi-Way Retrieval** *(+ `web-research`)* | Mandatory native `swarm`: `>= 3` parallel Hydrogen (`gemini-4-hydrogen-medium` + `tasks: [...]`, reusing active or starting new board) + Neon (`medium`) or Primary synthesis *(never `invoke_subagent`)* | Live URL/source cross-check before citing |
| **Repo / Multi-Module Audit** | Directory-sharded Hydrogen (`medium`) sweeps + category-split Neon (`medium\|high`) deep audits | `>= 2` independent reviewers cross-checking findings (Neon `high` / Carbon `medium\|high`) |
| **Multi-Hypothesis Parallel Debug** | `>= 2` parallel Neon (`medium\|high`) hypothesis investigators + Hydrogen (`medium`) log/code/git sweeps + Neon (`high\|xhigh`) fix | `>= 2` independent reviewers (Neon `high` / Carbon `medium`) re-checking failure signal & regression |
| **UI Updates** *(+ `chlora-ui` when active)* | Carbon (`medium\|high`, `[Carbon-UI-Lead]`) art lead + `2–10` workers: Hydrogen (`medium`) read-only file reading/inventory + Neon (`low\|medium\|high`) UI coding & GUI perf | Carbon visual sign-off + `>= 1` non-author code reviewer (`>= 2` independent reviewers total on core/large UI overhauls) |
| **Workspace Cleanup & Public GitHub Push** | Hydrogen (`medium`) cleanup/junk/volume/doc-index workers + Neon (`medium`) structural/manifest updates | `>= 2` independent read-only security/privacy reviewers (Hydrogen `medium` pre-scan + Neon `high` / Carbon `medium`): **permanent ban** on uploading server-ops configs/scripts/SSH/IPs or keys/tokens/`.env` |

## Parallel Scale & UI Dual-Mode Routing

- **Light Tier (`0 <= N <= 5`, strict local scope):** reserved exclusively for
  ultra-simple, ultra-lightweight local changes (single file or 1–3 tightly
  coupled files, small copy/config/local Skill tweaks). Allows **`N = 0`** on
  Primary (explicitly exempt from the Standard Tier pure-scheduler ban) or
  **`1 <= N <= 5`** concurrent native subagents (cap 5/wave; Neon `low|medium`
  for edits, Hydrogen `medium` for quick checks; never auto-Magpie, never
  Hydrogen editing UI code). **Escalation gate:** any task involving `>= 2`
  independent modules, repo/multi-category audits, parallel debug, UI
  visual+engineering updates, large Skill overhauls, workspace cleanup/public
  GitHub push, or `>= 3`-way `web-research` (always native `swarm`) **must**
  enter Standard Tier.
- **Standard Tier (`5 <= N <= 50`/wave, cumulative unlimited):** standard
  orchestration dispatches **5–50** parallel workers per main wave (cap 50/wave,
  unlimited cumulative), split by category with **same-category multi-instance
  sharding** (`>= 2` independent reviewers, directory-sharded inspection,
  parallel debug hypotheses). Single-writer convergence fix/verify sub-waves
  bound by exclusive write leases, UI Mode A (whose `2–10` helpers count toward
  total scale), and `>= 3`-way `web-research` (mandatory native `swarm`
  `gemini-4-hydrogen-medium` + `tasks: [...]`, reusing active or new board)
  dispatch per actual lease scope. Primary (`coordinator`) is **pure scheduler**
  and does not occupy a business read/write slot.
- **UI Dual-Mode (`[Carbon-UI-Lead]` + `2–10` Engineering Subagents):**
  - **Carbon (`gemini-4-carbon-medium|high`, `[Carbon-UI-Lead]`)** is strictly
    secondary **UI Art Lead** (visual direction, design tokens/skeleton,
    aesthetic review & final sign-off); never bulk-reads large files or writes
    bulk engineering code.
  - All file reading, UI coding, component engineering, and GUI perf dispatch to
    **`2 <= N_ui <= 10`** subagents via `swarm`: **Neon** (`low|medium|high`)
    owns all UI code & GUI perf; **Hydrogen** (`medium`) is strictly read-only
    file reading/inventory. Neither Primary nor Carbon may ever dispatch
    Hydrogen or external models to edit UI production code.
  - **Mode A (Carbon 1-hop helpers):** Primary spawns `[Carbon-UI-Lead]` via
    `swarm` -> Carbon spawns `2–10` `[Carbon-UI-Helper]` workers and **must**
    pass explicit `model: "gemini-4-neon-low|medium|high"` or
    `"gemini-4-hydrogen-medium"` (overriding parent-model inheritance; forbid
    further spawning; report to `@<carbon-name>`) -> Carbon visually reviews disk
    diffs, integrates helper work, and `kill`s its own helpers before
    `@coordinator [done]`.
  - **Mode B (Flat Swarm peers):** Primary directly dispatches `@ui-carbon`
    (`[Carbon-UI-Lead]`) alongside `2–10` Neon/Hydrogen Swarm peers in the same
    wave; peers coordinate directly with `@ui-carbon` via `@<peer>` & `#seq`
    (read findings -> art spec -> UI coding/perf -> Carbon visual sign-off ->
    `@coordinator [done]`).

## Quota Eligibility (`used` vs `remaining`)

Check the turn-start quota banner (or `swarm(action: "models")` /
`~/.local/bin/magpie-agent quotas`) before each **new** dispatch batch (skip for
warm follow-ups):

- **`used` vs `remaining` formula:** plain-text `magpie quota` output (e.g.
  `Gemini 7d 13%`) and `~/.config/magpie/quotas.json` `"used"` fields report
  **USED** %, **not** remaining %: `remaining = 100 - used` (`13%` used = `87%`
  remaining, fraction `0.87`). Across accounts, pick the largest 7-day
  `remaining` whose 5-hour `remaining > 0`.
- **Active pool (`7d remaining > 0%` and `5h remaining > 0%`):** 100% open to
  native Carbon, Neon, and Hydrogen.
- **Exhausted (`7d == 0%` or `5h == 0%`) or native route failure:** NEVER
  auto-fallback to Magpie proxies. Keep the package on Primary (run `search_web`
  directly for `web-research`) and report the exact quota reading or error.

## User-Named Overrides and Exclusions

- **Permanent hard ban:** NEVER reverse-proxy Antigravity/Vertex Gemini through
  Magpie (`agy-cli/gemini-*`, `antigravity/gemini-*`, `google-vertex*/gemini-*`,
  `magpie-gemini*`) even if user-named; Grok is permanently fixed to `@256k`
  Ultra Fast (`fast: true`, `tier: "priority"`, `high|xhigh` only—never
  `low`/`medium` or `@500k`).
- **Default rule:** every external Magpie route and native Argon are **excluded
  from automatic dispatch** and invoked **only** when the user explicitly names
  that model (and/or effort) in the current request:

| User-Named Target | Dispatch Route & Exact Model IDs | Notes |
|---|---|---|
| **Gemini (Carbon / Neon / Hydrogen / Argon)** | Antigravity native `swarm` / `invoke_subagent` | Always native unless user explicitly specifies `ai-studio` |
| **Google AI Studio (`ai-studio` / `AI Studio`)** | `cursor:magpie_agent` / `cursor:magpie_chat` / `magpie-agent`: `ai-studio/gemini-4-neon\|carbon\|hydrogen\|argon` (aliases `ai-studio-neon\|carbon\|hydrogen\|argon`) | Explicit user-named exception only; defaults: neon/carbon `high`, hydrogen/argon `medium` |
| **Claude (Opus 5.5 / Sonnet 5.5 / Haiku / Fable)** | **Native first:** `swarm` `claude-opus-5-5-low\|medium\|high`, `claude-sonnet-5-5-low\|medium\|high` while `Claude & GPT` pool > 0 | Use `magpie-agent` (`claude/claude-*`, `claude-haiku-5-5`, `claude-fable-5-2`) only if user requests `xhigh\|max`, Haiku/Fable, or Magpie |
| **Grok 4.7 256k Ultra Fast** | `magpie-agent` / `cursor:magpie_agent`: `group/grok-4.7-256k-high` or `group/grok-4.7-256k-xhigh` (`--model magpie-grok --effort high\|xhigh`) | Fixed `@256k` + `priority`; `high\|xhigh` only; never frontend UI |
| **DeepSeek** | `magpie-agent` / `cursor:magpie_agent`: `magpie-deepseek` -> `deepseek/deepseek-flash` | Default effort `high`; never frontend UI |
| **Sol 6.2 / Astra 6.2 / Terra 6.1** | `magpie-agent` / `cursor:magpie_agent`: `magpie-codex-sol` (`group/sol-6.2-xhigh\|high` / `codex/gpt-6.2-sol`), `magpie-codex-astra` (`group/astra-6.2-xhigh\|high` / `codex/gpt-6.2-astra`), `magpie-codex-terra` (`group/terra-6.1-xhigh\|high` / `codex/gpt-6.1-terra`) | Explicit user request only |

## Antigravity Dispatch Mechanics, Nesting & Warm Reuse

1. **Swarm (`swarm`):** call `swarm(action: "title", ...)` + parallel
   `swarm(action: "add", name: "<role>", model: "gemini-4-*", workspace:
   "inherit"|"share", brief: "<中文任务包>")` (use `tasks: [...]` for sharded
   homogeneous slices). `post_message`, `read_board`, and `swarm_wait` unlock on
   the turn after the first `add`.
2. **`define_subagent` / `invoke_subagent` (single isolated lightweight task or
   pure read-only single-path visual review ONLY — NEVER `web-research`):**
   - Ordinary single-path lightweight worker: define once per session via
     `define_subagent(Name: "agy-worker-rw" | "agy-worker-ro", EnableWriteTools:
     true | false, EnableSubagentTools: false, ...)` so nested spawning is
     physically blocked. All `>= 3`-way `web-research` **must** use native
     `swarm` (`gemini-4-hydrogen-medium` + `tasks: [...]`, reusing active or
     starting a new board).
   - UI tasks: any task with UI code or GUI performance changes **must** use
     `swarm` (so Neon handles coding/perf alongside Carbon Art Lead);
     `invoke_subagent(..., Model: "pro")` is restricted to pure read-only
     single-path visual review.
3. **Read-only & write isolation:** read-only reviewers/diagnosticians use
   `workspace: "inherit"` with explicit read-only rules. Concurrent writers use
   disjoint path leases (+ dedicated repo build lanes where required) or
   `workspace: "share"` (land diffs before `swarm(action: "kill", ...)`).
4. **Warm reuse:** `swarm` via `post_message(text: "@<name> <续跑指令>")`
   (`waiting` workers cost zero idle tokens and retain full context);
   `invoke_subagent` via `send_message(Recipient: "<conversationId>", Message:
   "...")`; authorized external Magpie via `magpie-agent run --resume
   <session_id>` or `cursor:magpie_agent(session_id: "...")`.
5. **Escalation:** workers stop immediately on unfrozen interfaces, ownership
   conflicts, external mutations outside lease, or permission/hook denials—never
   repairing hooks or spawning unauthorized subagents.

## Route Receipts

Verify execution after every delegated worker returns:

- **Antigravity native (`invoke_subagent` and `swarm`):** verify returned
  `conversationId` or `swarm(action: "status")` / `read_board` `[done]` posts
  plus real file diffs and raw command outputs on disk.
- **User-named external Magpie routes (including `ai-studio/gemini-4-*`, via
  `~/.local/bin/magpie-agent` / `cursor:magpie_agent`):** verify
  `receipt.status == "verified"` in the returned JSON reconciled against
  `~/.config/magpie/usage.jsonl` (`req`, `served`, `effort`,
  `http_status == 200`; for Grok also `served == "grok-4.7@256k"` and
  `tier_sent == "priority"`).
