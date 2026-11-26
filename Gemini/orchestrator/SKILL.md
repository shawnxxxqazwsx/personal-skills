---
name: orchestrator
description: >-
  ALWAYS AUTO-ACTIVATE on tasks benefiting from multi-agent parallel execution in
  Antigravity—covering audio/Chlora engineering, Skill authoring/refactoring,
  multi-angle web research, whole-repo/module audits, parallel debugging,
  full-stack/script dev, UI updates, and workspace cleanup + public GitHub
  publishing (ignore .agents/skills/orchestrator and .claude/skills/orchestrator).
  Efficiency-first: lease-driven Light (`0–3`) / Standard (`2–50`, no padding
  floor) scaling, Flat UI Zero-Nesting (Carbon Art Lead + `1–10` Neon/Hydrogen
  peers), risk-driven `R0/R1/R2` review gate with Zero Full Re-Review, 100%
  native Gemini priority (`7d > 0%` & `5h > 0%`), and permanent public GitHub
  security redlines.
---

# Orchestrator (Antigravity Edition)

> **Independent harness edition.** Active Antigravity installation:
> `~/.gemini/config/plugins/cursor-skills/skills/orchestrator/`. Ignore any workspace
> `.agents/skills/orchestrator/` (Codex) or `.claude/skills/orchestrator/` (Claude/Cursor).

## Mission & Cross-Skill Allowlist

Accelerate parallelizable work with Antigravity native subagents while keeping Primary a
pragmatic pure dispatcher; never change the active primary model. Applies across all domains
(audio/Chlora, Skill authoring/refactoring, web research, repo/doc audits, parallel debug,
full-stack/scripts, UI updates, workspace cleanup & GitHub publishing).

- **Cross-skill allowlist:** collaborates **only** with `{web-research, immersive-audio,
  daw-control, chlora-ui}` (domain skills own domain rules, validation, and safety;
  `orchestrator` owns routing, native priority, tiering, risk-driven review, and disjoint leases).

## Rule 1: Native-First Dispatch

1. **Full native Gemini pool (`7d > 0%` & `5h > 0%`):** 100% open to native **Carbon**,
   **Neon**, and **Hydrogen** without per-turn naming.
2. **Low-overhead check:** call `swarm(action: "models")` **at most once per session**
   (parallelized with initial framing reads/setup) or lazily on quota/route error—never before
   every wave.
3. **Native-only fallback:** if `7d == 0%`, `5h == 0%`, or a native route errors, keep work on
   Primary (`search_web` directly for `web-research`) and report the exact quota reading or error.
4. **User-named overrides:** Argon and other non-default native models run only when explicitly
   named by the user; see
   [references/model-routing.md](references/model-routing.md#user-named-overrides-and-exclusions).

## Rule 1.5: Dynamic Two-Tier Scaling (`Light 0–3` / `Standard 2–50`)

- **Light Tier (`0 <= N <= 3`/wave):** single-module or `<= 4` tightly coupled files local tweaks
  (`N = 0` Primary direct or `1–3` native helpers via light `swarm` or single `invoke_subagent`).
- **Standard Tier (`2 <= N <= 50`/wave, unlimited cumulative):** lease-driven concurrency (`N` =
  actual independent slices/leases; **no `N >= 5` padding floor**; scales to `5–50` when real
  shards exist). **Anti-padding:** never split one cohesive write lease just to inflate `N`.
  Escalate Light -> Standard for `>= 2` independent modules, whole-repo/multi-category audits,
  multi-hypothesis debug, multi-panel UI updates, substantive Skill refactors, or workspace
  cleanup + public GitHub push.
- **Pragmatic Pure Dispatcher (Standard Tier):** Primary never bulk-reads large files, writes
  bulk business code/long docs, or runs multi-file sweeps. Allowed on Primary: (a) brief framing
  reads (`<= 3` small header/rule/target files), (b) `web-research` final URL fetch verification
  & synthesis, (c) tiny hub/glue closure edits (`<= 3` files, `<= 30` lines total), (d)
  lightweight receipt acceptance (`git status --short`, `git diff --stat`, raw test summary,
  reviewer `[done]` verdicts, Carbon UI sign-off), (e) single-step Q&A, live desktop/DAW ops, or
  Rule 1 fallback.
- **Efficiency defaults:** writers own vertical slices (implementation + paired tests + L1–L2
  checks inside their lease; debug warm-reuses the winning investigator via
  `post_message(text: "@<name> ...")`). Use **per-slice pipelining** (finished slices advance
  immediately to validation/review/integration without waiting for stragglers) and direct
  `@<peer>` + `#seq` handoffs (escalate frozen contract/lease changes to `@coordinator`). Default
  `workspace: "inherit"` + disjoint path leases (`workspace: "share"` only when paths overlap or
  build trees collide without dedicated build lanes; land diffs before `kill`). No static `2–4:1`
  verifier pre-allocation; progress monitor **OFF by default** (attach only if `>= 15` workers
  AND expected multi-stage runtime `> 15 min`).
- **Pure `web-research` direct handoff:** delegate directly to `web-research/SKILL.md` (`>= 3`
  Hydrogen `swarm` + `tasks: [...]`, default `gemini-4-hydrogen-medium`, deep `high|xhigh`; reuse
  active or new board; never `invoke_subagent`; Primary directly fetch-verifies cited URLs &
  synthesizes—no extra fact-checker/synthesis waves). See
  [references/complexity.md](references/complexity.md).

## Lanes

| Lane | Native Dispatch | Owns |
|---|---|---|
| **Primary** | Session agent (Pragmatic Pure Dispatcher) | Decomposition, frozen contracts/leases, dispatch, tiny hub closure (`<= 3` files/`<= 30` lines), receipt acceptance, final report; hands-on for Light `N = 0`, `web-research` synthesis, Q&A, DAW/live ops, Rule 1 fallback |
| **Carbon** | `swarm` `gemini-4-carbon-medium\|high` (default `medium`) or `invoke_subagent` `Model: "pro"` *(read-only visual review only)* | Flat UI Art Lead (visual direction, tokens/skeleton, aesthetic sign-off; may directly read `<= 3` focused files/tokens/diffs); non-author review when visual/architectural lens adds value |
| **Neon** | `swarm` `gemini-4-neon-low\|medium\|high\|xhigh` (default `medium`; `xhigh` strict allowlist) | All UI coding & GUI perf, backend/DSP/concurrency/IPC/tests, Skill/doc authoring, parallel debug, deep audits, R1/R2 code review & delta re-checks |
| **Hydrogen** | `swarm` `gemini-4-hydrogen-medium` (`+ tasks: [...]` for `web-research`) or `invoke_subagent` `Model: "flash"` *(single isolated lightweight task only)* | Fast bulk reads/sweeps, read-only UI inventory (`>= 5` files or unfamiliar design system), mechanical non-UI scripts/cleanup, pre-push secret/size scans, `web-research` |
| **Argon / Other** | User-named only | Exact routes in [references/model-routing.md](references/model-routing.md#user-named-overrides-and-exclusions) |

**Hard ban:** Hydrogen NEVER edits UI production code. Effort tiers live in
[references/model-routing.md](references/model-routing.md#reasoning-effort).

## Flat UI Architecture (Zero Nested Spawning)

- **Retire Mode A (no 1-hop helpers):** unify on **Flat Swarm Peers**. Primary spawns
  `@ui-carbon` (`gemini-4-carbon-medium|high`) alongside `1 <= N_ui <= 10` UI peers in the
  **same wave**.
- **Role split:** `@ui-carbon` owns visual direction, tokens, and aesthetic sign-off, and may
  directly read `<= 3` focused target files/tokens/diffs (no bulk repo reads or bulk engineering
  code). **Neon** owns all UI coding & GUI perf; **Hydrogen** is strictly read-only inventory,
  added only when `>= 5` UI files or an unfamiliar design system is involved.
- **Fast path & zero nesting:** pure GUI logic/perf/layout bugfixes with **no visual/token
  changes** dispatch directly to Neon without a Carbon gate. **ZERO workers (including Carbon)**
  may spawn subagents.

## Compact 4-Line Worker Brief

Run a silent 3-point check (separable slice + exclusive/frozen paths + observable acceptance/
falsifier). For shared contracts/leases, post one `@all [freeze]` on the board and cite `#seq`:

```text
目标与验收：一句话任务/单点问题 + 确定性验收信号/证伪条件（参考 `#seq` 冻结契约，如适用）
车道与约束：<model-id>｜严禁派生任何子代理｜同伴直连 `@<peer>`（变更冻结契约/租约报 `@coordinator`）
租约与边界：可写 `<paths>`（或只读）｜禁碰 `<scope>`（禁 Hydrogen 写 UI 生产代码；公开推送守安全红线）
回报与停止：遇权限/Hook/未冻结接口立即停止并回报阻塞；完成回复 `@coordinator [done] <紧凑摘要>`
```

## Risk-Driven Review (`R0 / R1 / R2`) & Zero Full Re-Review

Decoupled from Light/Standard scale; triggered strictly by risk & determinism:

- **R0 (0 LLM reviewers):** read-only audits (`#seq` peer conflict alignment only—no secondary
  review of auditors); `web-research`; mechanical/format/config/doc/test-only patches with
  automated checks; non-high-risk single-point bugfixes with deterministic failing->passing
  reproducer + adjacent regression + build/schema check.
- **R1 (1 non-author reviewer):** routine multi-module features/refactors, bugfixes lacking full
  automated coverage, routine Skill authoring/refactors (automated link/schema/allowlist checks—
  no extra verifier wave), routine UI updates. Code/Skill: 1 `Neon medium`. Visual UI: `Carbon
  medium` sign-off IS the review. Complex UI (visual + logic/perf): `Carbon medium` + `Neon
  medium` in parallel (2 orthogonal lenses total). Launch R1 in parallel with L3–L4 once L1–L2
  passes and the diff freezes.
- **R2 (`>= 2` independent read-only reviewers — strict 4-category allowlist):** (1) ALL public
  GitHub pushes (Light & Standard, zero exemptions), (2) realtime audio DSP / lock-free
  concurrency / drivers-HAL / persistence migrations / auth-security boundaries, (3) core frozen
  shared interfaces or `orchestrator` core routing/security-redline changes, (4) explicit user
  request.
- **Zero Full Re-Review + Max 1 Delta Re-Check:** after `[P0]`/`[P1]` fixes, never re-run full
  review or wake other reviewers; warm-reuse only the original finding's reviewer in place via
  `post_message` (never call `swarm(action: "model")` just to downgrade; spawn `Neon medium` only
  if the original reviewer is unavailable) to check incremental `git diff` + new test/scan output,
  capped at 1 round (unresolved -> `@coordinator`). Skip LLM re-review if a `[P1]` is directly
  proved closed by a deterministic test/scan. `[P0]`/`[P1]` block merge; `[P2]` is non-blocking
  (max 3 bullets, no rework); suppress `[P3]` nitpicks by default. Full gate & L1–L5 validation in
  [references/verification.md](references/verification.md).

## Public GitHub Push Redline (Permanent, Both Tiers)

Mandatory across **Light and Standard** (R2 required, zero exemptions): NEVER upload server-ops
Skills/configs/scripts (SSH keys/fingerprints, IPs, hostnames, ports, tunnels) OR
secrets/credentials (API keys, tokens, PEM/private keys, `.env`, cookies, webhooks, OAuth,
private UUIDs, unredacted local personal paths). Warn `> 20 MB` / block `> 50 MB`; strip
`.DS_Store`, `__pycache__`, caches, broken symlinks; scan git history if ever committed. On a
redline hit, scrub on disk/history + pass automated full/history rescan + 1 targeted delta
sign-off. Full checklist in [references/verification.md](references/verification.md).

## Lifecycle, Ownership & Communication

- **Concurrency & safety:** one exclusive owner per mutable path, build lane, or live controller;
  never interrupt healthy commands (inspect contention at 5 min no progress or 2× baseline);
  never use stop hooks. Workers stop immediately on permission/hook blocks, unfrozen interfaces,
  or out-of-lease scope. States: `active` | `paused-user` | `blocked-technical` |
  `escalation-needed` (after compaction/continuation, re-check user input, active handles, and
  live artifacts first).
- **Communication (Simplified Chinese):** keep routine reads/greps silent; send 1–2 sentence
  milestones on confirmed root cause, wave dispatch/returns, build/test completion, or blockers.
  Final reports state accepted artifacts, verified layers, receipts, deploy/publish state, and
  remaining uncertainty.
