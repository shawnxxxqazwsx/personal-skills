---
name: session-handoff
description: >-
  Create or resume a continuation brief for moving work to a new session or task
  or continuing later. Use when the user asks for a handoff, 交接, continuation
  summary, saved state, fresh-session context, or resuming from a saved brief.
---

# Session Handoff

Dedicated to **single-task / window-switch temporary working-state handoff briefs** (exact stopping point, branch/dirty state, run vs. unrun verification, rejected approaches, and first continuation instruction); do **not** use this to record cross-session long-term preferences or stable architecture facts (those belong in long-term knowledge stores).

Preserve decisions, evidence, local state, and the exact next action (or completed terminal state) without replaying the full conversation. Use [references/templates.md](references/templates.md), and append its optional game-engine/Unity serialization note only when the task actually touches engine scenes, prefabs, packages, or project settings.

## Choose the operation

| User intent | Action |
|---|---|
| Wants a handoff or continuation summary | Produce one copyable brief |
| Explicitly wants a fresh session/task | Create a new session/task with the brief as its initial context (if supported by host) |
| Explicitly wants copied completed history | Fork the current session/task, then send any missing current-turn brief |
| Wants the brief saved | Write it to `.handoffs/YYYY-MM-DD-HHMM-[slug].md` (or a user-specified path) |
| Wants to resume a brief | Read it fully, verify current state, then continue from its first valid next step |

Do not create, fork, or save a session/task unless the user explicitly asks.

## CREATE

Collect the strongest available facts from the current session and workspace:

- objective, scope, milestone, and exact stopping point;
- completed outcomes (not tool-call narration) and remaining work;
- decisions, rationale, and rejected approaches worth avoiding;
- relevant files or external objects and what changed in each;
- verification performed (pass/fail), exact failures, and tests not run;
- blockers, assumptions, and ordered next actions;
- repository path, branch/worktree, and scoped dirty-state summary when relevant;
- if the host has an active Goal/task object, include its objective, status, evidence, and remaining concern (note that goal state does not auto-transfer).

Distinguish verified facts from assumptions. Do not attribute pre-existing user changes to this task. Never include secrets, full logs, or large code blocks. Prefer project-relative paths so the brief stays portable across worktrees.

### Save or start a new session only when requested

- **Save:** Create the target directory if needed (default `.handoffs/YYYY-MM-DD-HHMM-[slug].md`). For a chained handoff, add `Continues from: [previous filename]` near the top and tell the user where it was written.
- **New session / fork:** If a new session was created with the brief, do not also instruct the user to copy and paste the same text. On a fork, send any unfinished current-turn facts missing from completed history.

## RESUME

1. Read the supplied or saved brief completely (and any chained predecessor only for still-needed decisions/context).
2. Verify project, branch/worktree, referenced paths, Git state, and external state; treat the brief as potentially stale.
3. Report material deltas before editing; do not re-ask facts that still verify.
4. Confirm the objective and first valid next action briefly, then execute if authorized.
5. Re-run verification for any changed state; never inherit old passing evidence as fresh proof.

## Delivery

Return one brief, not separate short and long versions. Label unknown facts `未确认` rather than inventing them. If work remains, end with the ordered first action for the next session. If complete, state `已完成，无需继续执行` and omit the new-session instruction without inventing follow-up work.
