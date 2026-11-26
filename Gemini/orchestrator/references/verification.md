# Verification, Risk-Driven Review & Push Security

Single source of truth for layered validation, `R0`/`R1`/`R2` review gating,
zero full re-review, public GitHub push security redlines, and mechanical
receipt acceptance. Active repo and allowlisted domain rules
(`{web-research, immersive-audio, daw-control, chlora-ui}`) remain authoritative
for domain commands and thresholds.

## Layered Validation (L1–L5) & Artifact Provenance

Validate in strict order, stopping the affected slice at the first failing layer:

1. **L1:** Build, compile, or syntax/type-check the changed component.
2. **L2:** Re-run the original observable failure or acceptance signal.
3. **L3:** Verify one nearby unaffected behavior (adjacent regression).
4. **L4:** Run the focused test suite, schema/format validator, or link/allowlist check.
5. **L5:** Exercise the integrated, hosted, deployed, or live path when claimed.

Chaining L1–L4 in a single shell command (`&&`) is encouraged to cut round-trips.
Once L1–L2 pass and the diff freezes, L3–L4 may run in parallel with R1/R2 review.
A lower-level pass (unit test, mock, or screenshot) never proves an untested
hosted/live path—report exact untested layers instead of claiming closure. Record
tested revision, built artifact, deployed path, and runtime config; after an
in-place update, confirm the running process or host loaded the new binary.

## Risk-Driven Review Gate (`R0 / R1 / R2`)

Review depth is **decoupled from Light/Standard worker scale** and triggered
strictly by risk and determinism:

| Gate | Reviewers | Applicable Scope & Execution |
| :--- | :--- | :--- |
| **`R0`** | `0` LLM reviewers | Read-only repo/module audits (peer `#seq` conflict alignment only; no secondary review of auditors); `web-research` (already fetch-before-cite); mechanical/format/config/doc/test-only edits with automated checks; non-high-risk single-point bugfixes with deterministic failing→passing reproducer + adjacent regression + build/schema check. |
| **`R1`** | `1` non-author | Routine multi-module features/refactors, bugfixes lacking full automated coverage, routine Skill authoring/refactors (plus automated link/schema/allowlist checks; no extra verifier wave), routine UI updates. Code/Skill: 1 `Neon medium`. Visual UI: `Carbon medium` sign-off *is* the review. Complex UI (visual + logic/perf): `Carbon medium` (visual) + `Neon medium` (code) in parallel in the same wave (2 orthogonal lenses total; never stack double review). Launch in parallel with L3–L4 once L1–L2 pass and diff freezes. |
| **`R2`** | `>= 2` independent read-only | **Strict 4-category allowlist ONLY:** (1) **ALL public GitHub pushes** (Light & Standard, zero exemptions); (2) realtime audio DSP, lock-free concurrency, drivers/HAL, persistence migrations, or auth/security boundaries; (3) core frozen shared interfaces or `orchestrator` core routing/security-redline changes; (4) explicit user request. Use non-author `Neon high` + distinct second lens/model (`Neon xhigh` strictly allowlisted for lock-free/memory-ordering/crypto-security/deadlocked root causes). |

## Zero Full Re-Review, Max 1 Delta Re-Check & `[P0]`–`[P3]` Boundaries

Reviewers inspect actual files, diffs, and raw command output on disk, citing
`path:line`, failure scenario, and acceptance check (or `No findings.`).

- **`[P0]` (blocking):** security redline hit, crash, data corruption, realtime violation, or broken build.
- **`[P1]` (blocking):** reproducible defect or hard contract violation with `path:line` + repro.
- **`[P2]` (strictly non-blocking):** max 3 bullets; never triggers rework or re-review.
- **`[P3]` (nitpicks):** suppressed by default.
- **Delta-only re-check (cap = 1):** after fixing `[P0]`/`[P1]`, **never** re-run full review or wake other reviewers. Warm-reuse only the original finding's reviewer in place via `post_message` (never call `swarm(action: "model")` just to downgrade; R1/Carbon are already `medium`, and spawn `Neon medium` only if the original reviewer is unavailable) to inspect incremental `git diff` + new test/scan output, **capped at 1 round**; if still unresolved, escalate to `@coordinator`.
- **Deterministic closure shortcut:** if a `[P1]` is directly proved closed by a new deterministic test or automated scan, skip LLM re-review.
- **Public push redline cleanup:** run an automated full-tree/history rescan + 1 targeted delta sign-off on the cleaned paths/commits.

## Workspace Cleanup & Public GitHub Push Security Gate (Hard Redline)

**Mandatory across BOTH Light Tier and Standard Tier—zero exemptions.** Before
pushing any code or Skill to a public GitHub repo, run `R2` (including dedicated
read-only security/privacy audit) across **100% of candidate files, staged diffs,
and git history** if sensitive data was ever committed:

- **Permanently forbidden from public upload (zero exceptions):**
  1. **Server-ops Skills, configs, or scripts:** SSH keys/fingerprints, server/public IPs, hostnames/aliases, ports, ops runbooks, tunnel/proxy configs, or server-admin environments.
  2. **Secrets, credentials, or private identifiers:** API keys, cloud access/secret key IDs, access/refresh/bearer tokens, PEM/SSH private key blocks, `.env` files, cookies, webhook URLs, cloud/OAuth credentials, private session/conversation UUIDs, and unredacted local personal paths (hardcoded user home or private machine directories).
- **Size & tree hygiene:** warn `> 20 MB`, **block `> 50 MB`** binaries/media (MP4/GIF/PNG/archives); strip `.DS_Store`, `__pycache__/`, `*.pyc`, caches, temp logs, broken symlinks, and stray untracked files; verify directory layout, relative Markdown links (`0` dead links), and cross-skill allowlist hygiene.
- **Enforcement:** any hit is an automatic `[P0]` push blocker. Scrub on disk (and clean git history if ever committed), then pass automated full/history rescan + 1 targeted delta sign-off before `git push`.

## Mechanical Receipt Acceptance & Leased Execution

A worker's `[done]` post is a claim, not acceptance. Primary runs lightweight
mechanical receipt acceptance before integration:

- **Single mutable-resource owner:** serialize writes to shared build trees, running hosts/devices, live services, or external accounts; prefer scratch copies/fixtures for mutating checks.
- **Mechanical disk checks:** verify `git status --short`, `git diff --stat`, raw validation exit codes/summaries, and reviewer `[done]` verdicts directly on disk.
- **UI & lane boundaries:** verify zero Hydrogen edits to UI production code, design-token adherence on Neon GUI diffs, and Carbon's visual sign-off on visual UI changes (flat peer Swarm workers; see [complexity.md](complexity.md)).
- **Native route receipts:** confirm native `conversationId` or `swarm` `[done]` posts per [model-routing.md](model-routing.md#route-receipts).
- **Final gate:** accept only after layered validation, the applicable `R0`/`R1`/`R2` gate, and (for public pushes) the hard redline audit pass per [../SKILL.md](../SKILL.md).
