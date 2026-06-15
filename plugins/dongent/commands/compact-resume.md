---
name: compact-resume
description: After compaction or on resuming a session, rebuild the working context from the project's agent memory — current task, progress, decisions, and the rules in play. Read-side.
---

Run after `/compact`, or when picking a session back up, to reorient from durable memory. Memory is the reliable source; an in-session compaction summary, if present, is a lossy supplement.

## Read first

MUST read these first — this command relies on them:

- [wording-rule][../bedrocks/wording-rule/BEDROCK.md]

## Steps

### 1. Read the memory

Read the project's agent memory: the index, the checkpoint state, and the rule-related memories — whatever their prefix, not only the plugin-managed rules files (synced rules owned by [sync-rule-memory][sync-rule-memory.md]).

### 2. Reconstruct the context

From what you read, re-establish: the current task and goal, progress and the next step, pending items, open questions and key decisions, and the rules in play.

### 3. Report

Produce a readable brief — under each heading below, in this order, a few bullets, each a concise one-line sentence (not terse fragments). Show every heading, marking an empty one _none_:

- 🎯 **Goal**
- 📋 **Current task**
- ✅ **Done**
- ➡️ **Next step**
- ⏳ **Pending items**
- ❓ **Open questions**
- ⚖️ **Key decisions**
- 📜 **Rules** — each with its key sub-rules

## Out of scope

This command is read-only: it doesn't modify memory or re-sync the rule library (that's [sync-rule-memory][sync-rule-memory.md]).

## References

- [wording-rule][../bedrocks/wording-rule/BEDROCK.md]
- [sync-rule-memory][sync-rule-memory.md]

[../bedrocks/wording-rule/BEDROCK.md]: ../bedrocks/wording-rule/BEDROCK.md
[sync-rule-memory.md]: sync-rule-memory.md
