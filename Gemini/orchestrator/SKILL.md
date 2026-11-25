---
name: orchestrator
description: >-
  ALWAYS AUTO-ACTIVATE on every task that benefits from multi-agent parallel
  execution in Antigravity—not limited to audio/Chlora engineering, covering
  daily Skill authoring/refactoring/review, multi-angle web research, whole-repo
  code/doc audits, multi-hypothesis debugging, full-stack/script development, UI
  updates, and local workspace cleanup + public GitHub publishing (ignore
  .agents/skills/orchestrator and .claude/skills/orchestrator). Enforce Pure
  Dispatcher Primary, 100% native Gemini quota (`7d > 0%` & `5h > 0%`), zero
  auto Magpie proxy calls, Swarm-First scaling (`5 <= N <= 50`/wave, unlimited
  cumulative, same-category multi-instance, direct `@peer` handoffs), Carbon
  Pure Art Lead + `2–10` UI engineering/inspection workers, and permanent public
  GitHub secret/ops-safety redlines.
---

# Orchestrator (Antigravity edition)

> **Independent harness edition.** Active Antigravity installation:
> `~/.gemini/config/plugins/cursor-skills/skills/orchestrator/`. Ignore any
> workspace `.agents/skills/orchestrator/` (Codex) or
> `.claude/skills/orchestrator/` (Claude/Cursor).

## Mission, Scope & Cross-Skill Boundary

Accelerate any work that benefits from parallel multi-agent execution using
Antigravity native subagents while keeping Primary strictly as a pure
dispatcher. This policy applies regardless of the session's active primary model
and never changes it.

- **General-purpose scope (not audio-only):** applies equally to audio/Chlora
  engineering, daily Skill authoring/refactoring/review, daily multi-angle web
  research (coordinating `web-research`), whole-repo or multi-module code and
  documentation audits, parallel multi-hypothesis debugging, frontend/backend/
  script development, UI overhauls, and local workspace cleanup + GitHub
  publishing.
- **Explicit cross-skill allowlist:** this skill collaborates **only** with
  `{web-research, immersive-audio, daw-control, chlora-ui}`.
- When an allowlisted domain skill activates alongside `orchestrator`, that
  skill owns domain engineering, design, validation, and safety policy;
  `orchestrator` owns model routing, native-first priority, dispatcher/worker
  division of labor, parallel scaling, review dispatch, and disjoint leases.

## Rule 1: Native-First; Never Auto-Call Magpie Proxies

1. **Full native Gemini pool (`7d > 0%` and `5h > 0%`):** 100% of Antigravity's
   native Gemini pool is open to all tasks. This skill and global `AGENTS.md`
   are standing user authorization to dispatch native **Carbon**, **Neon**, and
   **Hydrogen** without per-turn naming.
2. **No automatic Magpie proxy calls or fallback:** NEVER call `magpie-agent run`,
   `cursor:magpie_agent`, `cursor:magpie_chat`, or `claude -p` automatically. If
   native Gemini quota hits `0%` (`7d == 0%` or `5h == 0%`) or a native route
   errors, keep work on Primary (run `search_web` directly for `web-research`)
   and report the concrete quota reading or error to the user.
3. **User-named overrides & permanent proxy ban:** exact model IDs, effort
   tiers, quota `used`→`remaining` conversion, permanent ban on reverse-proxying
   Antigravity/Vertex Gemini, and explicit user-named exceptions (including
   `ai-studio/gemini-4-*`, native-first Claude, Grok, DeepSeek, Codex) live in
   [references/model-routing.md](references/model-routing.md#user-named-overrides-and-exclusions).

## Rule 1.5: Pure Dispatcher Primary & Swarm-First Array (`5–50`/Wave)

1. **Pure Dispatcher Primary (Hard Rule):** once orchestration mode activates,
   Primary is **forbidden from performing hands-on execution**—never bulk-read
   large files, edit business code, author long docs, or run item-by-item
   debugging directly. Primary **exclusively** owns task decomposition, freezing
   shared interfaces and disjoint write leases, parallel dispatch and progress
   tracking, integrating/merging worker outputs (including final hub-file
   integration), and reporting. **Only exceptions:** pure single-step Q&A, live
   interactive desktop/DAW operations, or Rule 1 native-quota-0%/route-error
   fallback.
2. **Parallel scale (`5 <= N <= 50`/wave, unlimited cumulative):** assemble one
   unified Antigravity native `swarm` (`swarm(action: "title", ...)` + parallel
   `swarm(action: "add", ...)`; surface the returned `open_board` line).
   Standard primary orchestration waves dispatch **at least 5 and up to 50
   parallel workers** (use `tasks: [...]` for sharded homogeneous slices
   `<name>-1..k`), with **unlimited cumulative workers** across phases;
   single-writer convergence/fix sub-waves, UI Mode A (counting Carbon's `2–10`
   helpers toward total scale), and `>= 3`-way `web-research` (`swarm`
   `tasks: [...]`) dispatch per actual lease. Reuse compatible `waiting` workers
   first via `post_message(text: "@<name> ...")` (zero idle cost, full context).
3. **Same-category multi-instance (avoid under-staffing):** explicitly spawn
   multiple parallel subagents **within the same work category** whenever work
   splits naturally—e.g., 1+ worker per audit category in repo/doc reviews,
   **`>= 2` parallel independent read-only reviewers**, directory-sharded file
   inspections, or parallel multi-hypothesis debugging tracks.
4. **Direct peer-to-peer collaboration:** include relevant peer names in briefs
   so upstream/downstream and same-category peers coordinate directly on the
   Swarm board via `@<peer>` + `#seq` (interface details, cross-checking,
   dependency alignment, `verifier` ↔ `@<author>` fix loops). Changes to any
   frozen shared interface or write lease MUST still escalate to `@coordinator`.
5. **Verification ratio, monitor & workspaces:** pair every **2–4 concurrent
   authors** with read-only `verifier`/`reviewer` workers, and enforce **`>= 2`
   parallel independent reviewers** on core changes, Skill updates, large
   refactors, or public releases. Attach an optional progress monitor for long
   multi-stage swarms (`>= 5` workers). Keep readers on `workspace: "inherit"`;
   give writers disjoint path leases (+ dedicated build lanes where required) or
   `workspace: "share"` (land diffs before `kill`). Dispatch `web-research` via
   `swarm` (`gemini-4-hydrogen-medium` + `tasks: [...]`, `>= 3`); reserve
   `invoke_subagent` only for a single lightweight task or read-only visual review.

## Lanes

| Lane | Native Dispatch | Owns |
|---|---|---|
| **Primary** | Session agent (**Pure Dispatcher**) | Framing, decomposition, frozen interfaces & leases, parallel dispatch/tracking, final hub integration & reporting; hands-on ONLY for pure single-step Q&A, live desktop/DAW ops, or Rule 1 quota-0%/route-error fallback |
| **Carbon** | `swarm` `gemini-4-carbon-medium\|high` (`[Carbon-UI-Lead]` for UI) or `invoke_subagent` `Model: "pro"` *(pure read-only single-path visual review only)* | Secondary **Pure Art Director** for UI/visual craft (visual direction, tokens/skeleton, visual critique & final aesthetic sign-off; delegates file reading & coding to 2–10 workers), co-complex slices, non-author review of Neon diffs |
| **Neon** | `swarm` `gemini-4-neon-low\|medium\|high\|xhigh` (always `swarm` to pin Neon & all 4 tiers) | UI component coding & GUI performance optimization, backend/DSP/concurrency/IPC/protocols/state/tests, Skill/doc authoring & refactoring, deep read-only root-cause & architecture audits, independent review of non-Neon diffs |
| **Hydrogen** | `swarm` `gemini-4-hydrogen-medium` (`+ tasks: [...]` mandatory for `>= 3`-way `web-research`); `invoke_subagent` `Model: "flash"` *(single isolated lightweight task only; never `web-research`)* | Fast bulk file reading, style/token inventory, mechanical non-UI edits/sweeps, workspace hygiene & secret scanning, scripts/fixtures/probes, non-frontend docs/config, `>= 3`-way `web-research` (`swarm`), read-only UI inspection helper |
| **Argon / External** | User-named only | Not proactively dispatched; exact routes in [references/model-routing.md](references/model-routing.md#user-named-overrides-and-exclusions) |

Neither Primary nor Carbon may **ever** dispatch UI/GUI production code edits to
Hydrogen or external models (DeepSeek/Grok)—Hydrogen is read-only reading/
inventory in UI; Neon owns UI coding & GUI perf. Read
[references/model-routing.md](references/model-routing.md#reasoning-effort)
before first dispatch.

## UI Update Architecture (Carbon Pure Art Lead + 2–10 Workers)

- **Carbon (`[Carbon-UI-Lead]`, `gemini-4-carbon-medium|high`) — Pure Art
  Director:** acts as secondary UI lead exclusively responsible for visual
  direction, aesthetic standards, design tokens/skeletons, visual critique, and
  final aesthetic sign-off. Carbon **does not** bulk-read large project files or
  write large volumes of engineering code directly.
- **2–10 Engineering & Inspection Subagents (`2 <= N_ui <= 10`):** all concrete
  project file reading, UI code implementation, component engineering, and GUI
  performance optimization MUST be dispatched to **2–10** other subagents:
  - **Neon (`low|medium|high`):** UI component/panel/interaction coding under
    Carbon's tokens or existing design systems (e.g. `chlora-ui`), layout/HiDPI/
    focus/render-perf optimization, JUCE `Component` engineering, and frontend
    state/protocol layers + tests.
  - **Hydrogen (`medium`):** strictly read-only fast bulk file reading and
    style/token/DOM inventory (never writes UI production code).
- **Two Flexible Collaboration Topologies** (both require Carbon's explicit
  visual review and sign-off before final delivery):
  1. **Mode A — Carbon 1-Hop Helpers (`Primary -> [Carbon-UI-Lead] -> 2–10
     [Carbon-UI-Helper] -> Carbon Review -> Primary`):** `[Carbon-UI-Lead]`
     calls `swarm(action: "add")` with **explicit `model`**
     (`"gemini-4-neon-low|medium|high"` for UI coding/perf or
     `"gemini-4-hydrogen-medium"` for read-only inventory—never omit `model`,
     which inherits Carbon). Briefs include `[Carbon-UI-Helper]`, forbid further
     spawning, and report to `@<carbon-name>`. Before `@coordinator [done]`,
     Carbon reviews diffs, lands helper changes, and `kill`s its helpers.
  2. **Mode B — Flat Swarm Peers (`Primary -> @ui-carbon + 2–10 Neon/Hydrogen
     peers`):** Primary directly spawns `@ui-carbon` alongside `2–10` Swarm
     workers (Neon/Hydrogen) that coordinate directly with `@ui-carbon` via
     `@<peer>` + `#seq` on visual specs, diffs, and sign-off.
- **Strict nesting cap:** Carbon must NEVER spawn Carbon, Argon, or external
  models. Every other worker (Neon, Hydrogen, Argon, external, and every
  `[Carbon-UI-Helper]`) is strictly forbidden from spawning subagents. Any
  worker hitting out-of-lane UI scope stops and escalates to `@coordinator` or
  `@ui-carbon`.

## Workspace Cleanup & Public GitHub Push (Permanent Security Redline)

Run local workspace cleanup and public GitHub pushes (source code or Skills) as
a dedicated multi-agent Swarm wave (`5 <= N <= 50`):

1. **Parallel cleanup & hygiene workers (Hydrogen/Neon):** prune temporary
   artifacts, `.DS_Store`, `__pycache__`, stale caches, and oversized binaries
   (`> 50 MB`) while preserving tracked project/Skill assets.
2. **Parallel doc/index & manifest workers:** update READMEs, catalogs, and
   validate all relative links and metadata schemas.
3. **Parallel privacy/secret scanning + `>= 2` independent security reviewers:**
   before any `git push` to a public repository, at least **2 independent
   read-only reviewers** must audit the full staged file list and diff.
4. **Permanent Security Redline (ZERO EXCEPTIONS):** **NEVER** upload to any
   public GitHub repository:
   - Any **server-operations Skill, config, or script** (SSH keys/fingerprints,
     server IPs/hostnames/ports, host/ops automation, or cloud/server
     infrastructure credentials);
   - Any file containing **API keys, access tokens, secrets, `.env`, private
     keys, certificates, private session UUIDs, or sensitive local credentials**.
   On any redline hit, abort push immediately, strip/exclude the offending files
   (and verify git history if previously committed), then re-run independent
   security review. See [references/verification.md](references/verification.md).

## Separability, Lifecycle, Ownership & State Machine

- **Separability & pure-dispatcher gate:** standard primary waves scale
  `5 <= N <= 50` (single-writer convergence/fix sub-waves, UI Mode A with `2–10`
  helpers counted in total scale, and `>= 3`-way `web-research` via native `swarm`
  dispatch per actual lease); keep only pure single-step Q&A, live desktop/DAW
  ops, or Rule 1 quota-0%/route-error fallback on Primary. See
  [references/complexity.md](references/complexity.md) for templates and
  phase-scoped resource manifests.
- **Small decision record (before dispatching):** (1) classify operation
  (`inspect`/`plan`/`change`/`validate`/`review`/`deploy`/`publish`) without
  widening authorization; (2) define observable success signal & first
  falsifier; (3) list mutable resources & single owners; (4) assign wave size
  (`5–50`), same-category parallelism, and native lanes.
- **Lifecycle & proportional coordination:** frame before dispatch; reassess and
  launch next waves after diagnosis, interface freeze, first green pass, worker
  returns, and repeated failures—never regress to single-threaded Primary work.
  Keep one writer per path, behavior, build, or control plane; check active
  workers without interrupting healthy commands; inspect contention at 5 minutes
  with no progress or 2× baseline runtime. Never use stop hooks.
- **Ownership & safe concurrency:** Primary owns decomposition, frozen
  interfaces, authorization, final hub integration, and final claims. On
  permission denial, hook block, unfrozen interface, or out-of-lease scope, a
  worker returns the concrete blocker and stops—never repairs hooks or delegates
  repair. Repository rules govern build isolation (e.g. dedicated repository
  build lanes).
- **States & resumption:** `active` (proceed in lease) | `paused-user` (resume
  only on direct user instruction) | `blocked-technical` (reassess on new
  evidence without altering frozen receipts) | `escalation-needed` (worker
  returns one concrete question and stops). After compaction or continuation,
  re-check latest user input, active handles, and live artifacts first.

## Canonical Assignment Packet

Write packets in Simplified Chinese (workers do not share conversation history);
for `swarm` workers, require final reply format `@coordinator [done] <summary>`:

```text
任务类型 / 阶段与单一问题：
派发车道与强度（见 model-routing.md；仅 UI Carbon [Carbon-UI-Lead] 可 1 跳且须显式传 Neon/Hydrogen model 并在结束前合入并 kill 自建 helper，其余严禁再派生）：
验收信号与返回产物（swarm 结束以 `@coordinator [done]` 回报；Mode A `[Carbon-UI-Helper]` 回报 `@<carbon-name>`）：
同伴直连交接（peer `@name` 与 `#seq`；变更冻结接口/写边界须报 `@coordinator`）：
相关路径与既有证据：
可写路径（或明确只读）与禁碰范围（含外部/Hydrogen 禁写 UI 生产代码；公开推送安全红线）：
授权与声明边界（遇权限/Hook 拦截立即回报阻塞并停止）：
分支/环境与构建车道约束：
证伪条件、停止条件与升级触发器：
紧凑返回格式：
```

## Review, Validation & Reporting

- **Multi-path independent review (mandatory on core changes, Skill updates,
  large refactors & public pushes):** dispatch **`>= 2` independent read-only
  reviewers** in parallel following the non-author rule—native **Neon**
  (`gemini-4-neon-high|xhigh`) for non-Neon diffs, and native **Carbon**
  (`gemini-4-carbon-medium|high` / `Model: "pro"`) for Neon diffs (plus
  security/privacy reviewers for GitHub pushes). Return severity-ranked
  `[P0]`–`[P3]` findings with `path:line`, failure scenario, and acceptance check
  (or `No findings.`).
- **Primary final acceptance:** verify real disk diffs, raw command outputs, and
  execution receipts—never trust worker self-reports. Recomputing production
  formulas proves only internal consistency.
- **Layered validation:** validate in order—(1) changed component, (2) original
  signal, (3) adjacent unaffected behavior, (4) focused suite/validator, (5)
  integrated/hosted/live path when claimed. Doc/Skill/config packages validate
  links, schema, allowlists, and format. Stop affected packages at first failing
  layer. See [references/verification.md](references/verification.md).
- **Communication (Simplified Chinese):** keep routine reads/greps silent (no
  pre-call narration). Send a brief 1–2 sentence milestone update on confirmed
  root cause, wave dispatch/key returns, build/test completion, or blockers.
  Final reports state accepted artifacts, verified layers, execution/receipt
  status, deployment/publish state, and remaining uncertainty.
