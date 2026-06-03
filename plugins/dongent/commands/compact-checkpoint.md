---
name: compact-checkpoint
description: Before compaction or any context loss, capture durable session state into the project's agent memory — or private content that is its more canonical home — so it survives into future sessions. Write-side.
---

Run before `/compact`, or any time the working context is about to be lost, to persist what must outlive it. Compaction leaves only a lossy auto-summary that survives the current session; this command writes the durable, important facts into the project's agent memory — or into private content where that is a fact's more canonical home — so they survive into future sessions.

## Steps

### 1. Select what's worth keeping

Keep only **durable and important** facts that a lossy summary might drop and that aren't already in the durable record (e.g. code, docs, commits, memory):

- the current task and goal,
- progress — milestones reached and the next step,
- pending items,
- open questions,
- key decisions, corrections, or conventions established this session.

**Skip** the running log of what was done — the in-session compaction summary already covers that — and anything already in the durable record.

### 2. Find each fact's canonical home

Find each fact's canonical home — the most foundational existing place it belongs, per [ssot-principle][../rules/ssot-principle/RULE.md]. The default home is the project's agent memory; defer to private content — the user's drafts or plan / progress notes (per [private-content][../rules/private-content/RULE.md]) — only when it is a fact's more canonical home than memory. A checkpoint stashes only into these private homes, never into public content (which is published and reviewed separately); if no existing home fits, create a memory file under the standard conventions. Memory may also hold plugin-managed `dongent_*` files — synced rules owned by [sync-rule-memory][sync-rule-memory.md] — so keep session state in the ordinary memory files, not there.

### 3. Record the fact

Write the distilled fact into that home, keeping it consistent within and across files: update existing content in place rather than duplicating it, and link to a fact that already lives elsewhere instead of repeating it. Keep it a concise distillation, not a transcript dump.

### 4. Report

Group by the file written, each marked ✨ created or 🔄 updated, with the facts captured into it listed underneath, one terse line each. Skipped facts (already in the durable record) need no entry.

## Out of scope

Syncing the rule library into memory — that's [sync-rule-memory][sync-rule-memory.md]. This captures session-derived facts — mainly work state, sometimes new corrections or conventions — not the published rule library.

## References

- [ssot-principle][../rules/ssot-principle/RULE.md]
- [private-content][../rules/private-content/RULE.md]
- [sync-rule-memory][sync-rule-memory.md]

[../rules/ssot-principle/RULE.md]: ../rules/ssot-principle/RULE.md
[../rules/private-content/RULE.md]: ../rules/private-content/RULE.md
[sync-rule-memory.md]: sync-rule-memory.md
