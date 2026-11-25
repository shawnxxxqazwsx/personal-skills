# Integrated Verification, Multi-Review & Push Security

Use this reference to gate acceptance across layered tests, independent
multi-reviewer audits, leased execution, and public GitHub pushes. Active
repository and allowlisted domain rules (`{web-research, immersive-audio,
daw-control, chlora-ui}`) remain authoritative for exact domain commands and
thresholds.

## Layered Validation & Artifact Provenance

Validate in strict order and stop the affected package at the first failing
applicable layer before broadening checks:

1. Build, compile, or syntax/type-check the changed component.
2. Re-run the original observable failure or acceptance signal.
3. Verify one nearby unaffected behavior (regression check).
4. Run the focused test suite, schema/format validator, or link/allowlist check.
5. Exercise the integrated, hosted, deployed, or live path when claimed.

A lower-level pass never proves an untested live path—report exact untested
layers instead of claiming closure. Record the tested revision, built artifact,
deployed path (if any), and runtime config; after an in-place update, confirm
the running process or host actually loaded the new binary/artifact.

## Multi-Way Independent Review Gate (Tiered)

- **Light Tier (`0 <= N <= 5` ultra-lightweight edits):** for ultra-simple
  `N = 0` or 1–3 tightly coupled file micro-tweaks (minor copy, config, or local
  patch), Primary direct verification or **1 lightweight read-only check**
  suffices. Any substantive Skill rule change (e.g., modifying core routing,
  gating, or safety policy) still warrants **`>= 2` independent read-only
  reviewers**.
- **Standard Tier (mandatory `>= 2`):** for core code changes, substantive Skill
  updates, large-scale refactors, or public releases, dispatch **at least 2
  independent read-only review subagents** in parallel before merge or delivery:
  - **Non-author & cross-perspective rule:** reviewers must never be the author
    of the diff under review. Combine distinct models and/or orthogonal lenses
    (e.g., read-only Neon `high|xhigh` on correctness, contracts, and security +
    read-only Carbon `medium|high` on Neon diffs, architecture, or visual craft).
  - **Evidence-backed findings:** reviewers inspect actual files, diffs, and raw
    command output on disk and report severity-ranked `[P0]`–`[P3]` findings
    with `path:line`, failure scenario, and acceptance check (or `No findings.`).
  - **Closure:** resolve and re-verify every `[P0]`/`[P1]` finding before
    integration; keep fix↔review loops bounded and peer-addressed (`@<author>` ↔
    `@<reviewer>`).

## Workspace Cleanup & Public GitHub Push Security Gate (Hard Redline)

**Non-negotiable across BOTH Light Tier and Standard Tier**—no Light Tier
exemption applies to public pushes. Before pushing any source code or Skill to a
public GitHub repository, dispatch dedicated read-only security & privacy audit
subagents (within the `>= 2` independent review gate) to scan **100% of
candidate files, staged diffs, and git history if sensitive data was ever
committed**:

- **Permanently forbidden from public upload (zero exceptions):**
  1. **Any server-operations Skills, configs, or scripts:** SSH keys or
     fingerprints, server/public IPs, host aliases, ports, ops runbooks,
     tunnel/proxy configs, or server-admin environments.
  2. **Any secrets, credentials, or private identifiers:** API keys, cloud
     access/secret key IDs, access/refresh/bearer tokens, PEM/SSH private key
     blocks, `.env` files, cookies, webhook URLs, cloud/OAuth credentials,
     private session/conversation UUIDs, and sensitive local personal paths
     (unredacted user home paths or hardcoded private machine directories).
- **Artifact size & directory-tree cleanliness:**
  - Flag any single file `> 20 MB` and **block `> 50 MB`** showcase binaries or
    media (MP4/GIF/PNG/archives) to avoid GitHub size warnings and rejections.
  - Strip `.DS_Store`, `__pycache__/`, `*.pyc`, broken symlinks, build caches,
    temp logs, and stray untracked files; verify target directory structure,
    relative Markdown links (0 dead links), and cross-skill allowlist hygiene.
- **Enforcement:** any redline hit is an automatic `[P0]` push blocker. Fix or
  scrub on disk (and inspect/clean git history if sensitive files or values were
  ever committed), then re-run a clean scan before executing `git push`.

## Leased Execution, Mutable Environments & Receipts

A worker's `[done]` post is a claim, not acceptance. Before integrating:

- **Single controller per mutable resource:** serialize writes to shared build
  trees, running hosts/devices, live services, or external accounts; prefer
  scratch copies/fixtures for mutating checks.
- **Inspect disk reality:** verify actual changed paths, `git diff`, command
  invocations, and raw stdout/stderr—never trust worker self-reports.
- **Enforce lane & UI boundaries:** confirm zero unauthorized frontend/GUI edits
  in Hydrogen or user-named external diffs; verify design-token adherence (no
  unrequested visual drift) in Neon GUI diffs; require Carbon's explicit visual
  sign-off plus disk diff inspection on all UI changes (both 1-hop
  `[Carbon-UI-Helper]` and flat peer Swarm workers; see
  [complexity.md](complexity.md)).
- **Verify route receipts:** confirm native `conversationId` or `swarm` `[done]`
  posts on disk, or `receipt.status == "verified"` for user-named external
  workers per [model-routing.md](model-routing.md#route-receipts).

## Claims vs. Evidence & Final Acceptance

Keep observation conditions attached to every performance, visual, hardware,
security, or external-service claim—a unit test, mock, or screenshot never
proves end-to-end integration. Primary performs final acceptance only after
layered validation, the applicable review tier (Light Tier self-check/1-reviewer
or Standard Tier `>= 2` independent reviews), and—for any public GitHub push in
either tier—the hard redline security audit all pass per [../SKILL.md](../SKILL.md).
