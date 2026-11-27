# Decomposition, Vertical Slices & Lease Isolation

On-demand reference for complex decomposition, vertical-slice templates, flat UI
peer coordination, and lease isolation. See [../SKILL.md](../SKILL.md) for
two-tier rules/briefs, [model-routing.md](model-routing.md#reasoning-effort) for
model IDs/effort, and [verification.md](verification.md) for `R0`/`R1`/`R2`
review and push security.

## Lease-Driven Scaling, Pipelining & Hard Boundaries

- **Hard Mid-Session Escalation Thresholds:** Light `N = 0` is strictly capped at
  `<= 4` edited files AND `<= 5` **Primary self-read** business-source files
  (`Light N = 1–3` single-module helpers reading files do not trigger Standard
  escalation). Mid-session, the moment **Primary self-reads** exceed `> 5`
  business-source files, pending edits exceed `> 4` files, or `>= 2` independent
  hypotheses/modules emerge, **stop immediately and escalate**: if the whole task
  has only **1 non-splittable cohesive write lease**, dispatch an `N = 1` writer
  Swarm (Anti-Padding overrides the `N >= 2` Standard floor); otherwise escalate
  to Standard Swarm (`2 <= N <= 50`). Small visual UI tweaks (`<= 4` files) may
  skip a full coding swarm (dispatching `1–3` single-module helpers such as
  `@ui-carbon` as needed), and any visible visual/typography/sizing/token change
  still requires `@ui-carbon` visual sign-off (pure logic/perf bugfixes exempt).
- **Anti-Padding Rule (no `N >= 5` floor):** in Standard Tier (`2 <= N <= 50`/wave,
  unlimited cumulative), set `N` to actual independent slices/leases (or `N = 1`
  when only one cohesive write lease exists after leaving `Light N = 0`). Never
  split one cohesive write lease just to inflate `N`; scale to `5–50` (via
  `tasks: [...]`) only when independent shards exist.
- **Vertical slices, warm reuse cap & atomic retirement:** writers own
  implementation + paired unit/focused tests + L1–L2 checks inside their lease
  (no separate reader, test-author, or verifier waterfall waves). Never casually
  `kill` healthy `waiting` workers between waves (zero idle cost); reuse via
  `post_message(text: "@<name> ...")`. Workers may tag `[compacted]` in summaries.
  **Retirement cap:** once a worker hits `>= 3` context compactions (`CHECKPOINT`),
  spans `>= 4` major waves, or repeatedly re-reads the same files post-compaction,
  retire it via an **atomic two-step loop**: (1) outgoing worker lands diffs (if
  `workspace: "share"`) and posts a `<= 20`-line structured handover (`#seq`) to
  **`@coordinator`**; (2) on wakeup, Primary runs `swarm(action: "kill", old)` +
  `swarm(action: "add", new, brief: "...citing #seq...")` in the **same turn**.
- **Long-session anti-drift:** Primary's Pure Dispatcher boundary (`<= 3` focused
  reads; `<= 3` files / `<= 30` lines hub closure) holds across **all waves without
  decay**. When a worker stalls, diagnose, wake, or hand over to a fresh worker—never
  pull Primary into writing business code.
- **Per-Slice Pipelining:** advance each finished independent slice straight to
  validation, review, or integration without waiting for slower slices.
- **Zero-Nesting hard boundary:** ZERO workers (including Carbon) may spawn
  subagents; every brief must include `严禁派生任何子代理`. Static `2–4 : 1`
  verifier ratios are abolished; progress monitor stays OFF unless `>= 15`
  workers AND `> 15 min` expected multi-stage runtime.
- **Direct peer handoffs:** pass peer `@name`s in briefs so adjacent owners align
  findings and bounded fix loops via `@<peer>` + `#seq`; escalate frozen interface
  or write-lease changes to `@coordinator`.

## Vertical-Slice Scenario Templates

Combine templates for hybrid work under the cross-skill allowlist
`{web-research, immersive-audio, daw-control, chlora-ui}`:

1. **Audio / Systems Engineering** *(+ `immersive-audio`, `daw-control`)*:
   disjoint vertical writers (`Neon medium|high`; `xhigh` strictly allowlisted for
   lock-free concurrency/memory ordering) owning code + paired tests + L1–L2;
   optional `Hydrogen medium` only for heavy log/fixture sweeps. Review: `R1`
   routine; `R2` for realtime DSP, lock-free, HAL/drivers, or persistence.
2. **Skill Authoring & Refactoring**:
   optional `Hydrogen medium` sweep for large inventories; disjoint writers (`Neon
   medium`, `Carbon medium` for craft/structure) owning edits + automated
   link/schema/allowlist checks. Review: `R1` routine; `R2` only for core
   `orchestrator` routing/security-redline changes.
3. **Multi-Dimensional Web Research** *(direct `web-research/SKILL.md`)*:
   mandatory native `swarm` with `>= 3` parallel `Hydrogen` hunters
   (`gemini-4-hydrogen-medium` default, `high|xhigh` for deep dives) via
   `tasks: [...]` (reuse active or new board; never `invoke_subagent`). Primary
   directly fetch-verifies cited URLs and synthesizes (`R0`; no extra fact-checker
   or synthesis sub-waves).
4. **Whole-Repo / Multi-Module Audit**:
   `>= 1` read-only worker per major category (`Neon medium|high`; `Hydrogen medium`
   for large directory sweeps), sharded inside large categories. Peers align
   conflicts via `#seq` (`R0`; no secondary review of auditors).
5. **Parallel Multi-Hypothesis Debugging**:
   1 read-only investigator per live hypothesis (`H1..Hk`, `Neon medium|high`;
   optional `Hydrogen medium` for heavy log sweeps). On winning hypothesis, reassess
   immediately and **warm-reuse the winning investigator directly as fix writer**
   via `post_message` (fix + reproducer + regression + L1–L2). Review: `R0` if
   deterministic repro+regression covers it, else `R1`/`R2`.
6. **UI Overhaul / Update (Flat Peer Only; Mode A Retired)** *(+ `chlora-ui`)*:
   Primary spawns `@ui-carbon` (`gemini-4-carbon-medium`, `high` only for 0-to-1
   design systems/major redesigns; may read `<= 3` focused target files/tokens/diffs,
   never bulk-reads or bulk-codes) alongside `1 <= N_ui <= 10` UI peers in the
   **same wave**: `Neon` (`low|medium|high`) owns all UI coding, GUI perf & tests;
   `Hydrogen` (`medium`) is strictly read-only inventory, added **only** when
   `>= 5` UI files or unfamiliar design systems (never edits UI production code).
   **Zero UI serial ping-pong:** when `@ui-carbon` and `Neon` dispatch in the same
   wave, `Neon` starts immediately in parallel on skeleton/DOM inventory, test
   stubs, or non-visual wiring against a lightweight structural freeze—never sit
   idle waiting for Carbon's visual spec. Small visual UI tweaks (`<= 4` files)
   may skip a full coding swarm but still require `@ui-carbon` visual sign-off
   for any visible visual/typography/sizing/token change; pure GUI logic/perf/layout
   bugfixes with no visual/token changes dispatch directly to `Neon` without a
   Carbon gate. Review: Carbon visual sign-off (plus parallel `Neon medium` code
   review on complex visual + logic/perf UI).
7. **Workspace Cleanup & Public GitHub Push**:
   merge cleanup + doc/link/index updates into disjoint writers (`Hydrogen medium` /
   `Neon medium`), followed by automated secret/size/tree scan (`> 20 MB` warn,
   `> 50 MB` block) and mandatory **`>= 2` independent read-only security
   reviewers** (`R2`, zero exemptions across Light & Standard; see
   [verification.md](verification.md)).

## Read/Write Lease Isolation & Pre-Dispatch Check

Run a **silent 3-point check** before dispatching (no manifest boilerplate): (1)
bounded deliverable + observable acceptance/falsifier; (2) exclusive writable
paths + frozen shared interfaces (`@all [freeze]` when shared); (3) non-colliding
build/execution lane + peer `@name` handoff targets.

- **Single Reusable Build Lane (1 holder at a time):** each task strictly reuses
  a single dedicated `build-lane-<product>-<suffix>` directory across waves
  (never create a fresh `cmake -S` build directory per round) with **at most 1
  holder at any moment**. When `>= 2` compiling writers run in the same wave,
  freeze code and pass the build token serially via `@<peer>` to run compiled
  L1–L2 (or use `workspace: "share"` if concurrent edits touch a shared target
  graph); report `blocked` only for external/unresolvable lock contention (use a
  single delayed `schedule` retry or `blocked-technical`). If new module/test
  registrations wait for Primary's end-of-wave Hub closure (`<= 3` files /
  `<= 30` lines) without pre-staged stubs, writers pass in-lease syntax/standalone
  L1 (and runnable L2) and flag pending Hub items in `[done]`; Primary runs
  link-stage L1–L2 immediately after Hub closure.
- **Default `workspace: "inherit"`:** keep readers and disjoint writers on
  `workspace: "inherit"` with exclusive path leases (+ the task's reused build
  lane). Use `workspace: "share"` **only** when paths overlap or build trees
  collide without dedicated lanes; always land diffs before `kill`.
- **Read/write concurrency & hub serialization:** readers safely share an
  immutable revision or frozen interface; writes conflict with any read/write
  sharing mutable state, transitive deps, build trees, generated artifacts, or
  live controllers. Never mutate shared inputs mid-flight or interrupt healthy
  workers. Keep one exclusive owner per path/build/controller; serialize shared
  hub files on Primary (defer only colliding phases). Reassess on diagnosis,
  interface freeze, first green slice, or repeated failures; verify disk diffs
  and raw outputs per [verification.md](verification.md).
