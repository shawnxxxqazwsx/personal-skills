# Task Decomposition, Swarm Scale & Resource Leases

Use this reference to decompose work into parallel native subagent swarms and
protect concurrent write/build lanes. For model IDs, effort tiers, and quota
math, see [model-routing.md](model-routing.md); for multi-reviewer and security
gates, see [verification.md](verification.md).

## Orchestration Scale & Primary Role Boundary

1. **Swarm sizing (`5 <= N <= 50` main parallel scale):** standard orchestrated
   main parallel waves dispatch **5–50** subagents (`50`/wave ceiling; unlimited
   cumulative workers across phases—prefer warm reuse via `@<name>` over
   kill/respawn churn, and use `tasks: [...]` for sharded sweeps `<name>-1..k`).
   Convergent fix/re-check sub-waves constrained by an exclusive single-writer
   lease, UI Mode A (where Carbon's `2–10` helpers count toward total scale),
   and standalone `>= 3`-way `web-research` dispatch per their actual leases.
2. **Primary is a pure dispatcher:** in orchestrated tasks, Primary MUST NOT
   bulk-read large project files, perform bulk code edits, run log forensics, or
   execute multi-file inspections (keeping only lightweight rule/shared-interface
   header reads, final acceptance diff/receipt checks, pure single-step Q&A,
   live desktop/DAW ops, or Rule 1 native-quota-0%/route-error fallback).
   Primary owns framing, decomposition, frozen interfaces/write leases,
   escalations, and final integration.
3. **Same-category multi-spawn (encouraged):** spawn multiple workers **within
   the same category** whenever scope benefits from parallel depth or sharding:
   - `>= 2` independent read-only reviewers per core change/refactor/release;
   - directory- or module-sharded file/codebase readers;
   - 1 dedicated read-only worker per live debugging hypothesis;
   - concurrent disjoint writers across non-overlapping files/modules.
4. **Direct peer handoffs:** provide peer names in briefs so adjacent owners
   exchange findings, specs, and reviewer↔author fixes directly on the board via
   `@<peer>` + `#seq`. Only changes to frozen interfaces or write leases
   escalate to `@coordinator`.

## Scenario Decomposition Templates

Pick the matching template (combine for hybrid tasks) and scale to
`5 <= N <= 50` workers while preserving the strict cross-skill allowlist
`{web-research, immersive-audio, daw-control, chlora-ui}`:

1. **Audio / Systems Engineering** *(domain rules: `immersive-audio`, `daw-control`)*:
   1–2 interface/architecture readers + `>= 2` disjoint DSP/backend/IPC writers
   + 1 test/fixture author + `>= 2` read-only reviewers (realtime-safety +
   contract/regression). Lanes: Neon `medium|high|xhigh` (DSP/concurrency/tests/
   review), Carbon `medium|high` (non-author review of Neon), Hydrogen `medium`
   (fixtures/log sweeps).
2. **Skill Authoring & Refactoring**:
   `>= 2` sharded file/reference/script auditors + `>= 2` disjoint writers
   (`SKILL.md`, `references/*`, `scripts/*`) + 1 link/schema/allowlist verifier
   + `>= 2` read-only reviewers. Lanes: Hydrogen `medium` (sweeps/checks), Neon
   `medium|high` (specs/scripts/review), Carbon `medium|high` (craft/structure).
3. **Multi-Dimensional Web Research** *(with `web-research`)*:
   `3–6+` parallel angle hunters (official docs, papers/specs, compare/pricing,
   edge cases, counter-evidence) + 1 URL/claim fact-checker + 1 synthesis writer.
   Lanes: Hydrogen `medium` (`flash` / `gemini-4-hydrogen-medium`) for
   fetch-before-cite; Neon `medium|high` for deep technical verification.
4. **Whole-Repo / Multi-Module Code Audit**:
   **`>= 1` read-only worker per major category** (architecture/correctness,
   concurrency/realtime, security/privacy, perf/memory, UI/UX, build/tests);
   multi-spawn inside large categories by subsystem/directory shard. Lanes: Neon
   `high|xhigh` (deep audit), Hydrogen `medium` (sweeps); peers align via `#seq`.
5. **Parallel Multi-Hypothesis Debugging**:
   1 read-only investigator per live hypothesis (`H1..Hk`) + 1 log/artifact
   sweeper + 1 isolated reproducer; post-diagnosis: exclusive fix writer +
   `>= 2` independent reviewers. Lanes: Neon `medium|high` (trace/fix), Hydrogen
   `medium` (sweeps); reassess immediately when any hypothesis resolves.
6. **UI Overhaul / Update** *(design rules: `chlora-ui`)*:
   **1 Carbon Lead Art Director** (`[Carbon-UI-Lead]`, visual direction, design
   tokens/skeleton, visual review & final sign-off ONLY — never bulk-reads files
   or writes bulk code) + **`2–10` engineering/inspection workers**
   (`2 <= N_ui <= 10`: Hydrogen read-only file/inventory readers, Neon UI coders
   & GUI performance optimizers) + **Carbon visual sign-off + `>= 1` non-author
   code reviewer (`>= 2` independent reviewers total on core/large UI overhauls)**.
   Supports **2-tier** (Carbon spawns 1-hop `[Carbon-UI-Helper]` with explicit
   `model`) OR **flat peer** (Primary dispatches Swarm workers collaborating
   directly with `@ui-carbon`).
7. **Workspace Cleanup & Public GitHub Push**:
   1–2 bloat/tree/link scanners + 1–2 disjoint cleanup/trim writers + 1
   doc/index updater + **`>= 2` independent read-only security/privacy/secrets
   auditors** enforcing the Hard Redline in [verification.md](verification.md).
   Lanes: Hydrogen `medium` (inventory/size/junk/docs), Neon `high` + Carbon
   `medium` (dual independent pre-push security & redline audits).

## Phase-Scoped Resource Manifest & Lease Isolation

Record only what protects concurrent lanes in the active phase:

```text
Deliverable & acceptance signal:
Phase & immutable snapshot (branch/revision):
Writable paths & frozen shared interfaces:
Execution/build lane & external destinations:
Live controller (if any) & integration owner:
Peer handoff targets (@name / #seq):
```

- **Read vs. write concurrency:** multiple read-only workers may safely share
  the same immutable revision, frozen interface, or evidence snapshot. Writes
  conflict with any read or write sharing mutable state, transitive
  dependencies, build trees, generated artifacts, or live controllers.
- **No mid-flight mutation:** before editing an input shared as immutable, let
  dependent readers finish or isolate the writer (`workspace: "share"` or
  dedicated repo build lane) while readers stay on an identified revision. Never
  interrupt healthy workers merely to start a writer.
- **Narrowest lease:** keep one exclusive writer per path, behavior, build lane,
  or control plane; defer only the colliding phase when a shared hub file must
  be serialized on Primary.

## Separability Gates, Reassessment & Contract

A package is ready for dispatch when all hold:

- It answers one concrete question or delivers one bounded artifact.
- Its writable paths and transitive interfaces are exclusive or frozen.
- Its authorization boundary, falsifier, and stopping condition are explicit.
- Its execution environment and side effects do not collide with another lane.

Reassess separability after diagnosis, interface freeze, first green validation,
and repeated failed attempts. Keep implementation plus paired tests in one warm
writer where feasible. Before accepting any handoff, verify disk diffs, raw
command output, and required independent reviews per
[verification.md](verification.md) and [../SKILL.md](../SKILL.md); release a
lane (or land `workspace: "share"` changes before `kill`) only after integration
no longer needs its resources.
