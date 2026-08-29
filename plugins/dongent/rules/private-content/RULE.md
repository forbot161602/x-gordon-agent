---
name: private-content
description: Keep private content (personal drafts, internal documents, memory references, private-only terms) out of public artifacts. Each project declares its layers; references flow one way — private can cite public, but not the reverse.
---

# Private content — one-way information flow

A project's content splits into private and public layers (see [governance-scope][../../bedrocks/governance-scope/BEDROCK.md]). This rule keeps the two apart and stops the private side from leaking into the public side. It operationalises the **Scope** note of [ssot-principle][../ssot-principle/RULE.md] (SSoT applies within a reference scope; references between scopes are allowed in only one direction).

## Builds on

MUST read and follow these first — this rule builds on them:

- [wording-rule][../../bedrocks/wording-rule/BEDROCK.md]
- [governance-scope][../../bedrocks/governance-scope/BEDROCK.md]
- [ssot-principle][../ssot-principle/RULE.md]

## Rule

The principles below apply within the private and public layers each project declares (see [Prerequisites][prerequisites]).

### 1. Place content in the right layer

Decide each artifact's layer before writing it. When in doubt, ask who should see this — if "only me", it is private.

The private layer has two kinds, distinguished by who they face: **agent memory** — the agent-facing index (e.g. Claude Code's `~/.claude/...`, `MEMORY.md`, `feedback_*.md`, plus working-session content: conversation transcripts, personal thoughts, intermediate decisions, session shorthand like P1, Q1) — and **personal content** — the author-facing private docs (drafts, plans, notes, resident docs).

**Why:** the boundary is only as good as the discipline of putting content on the right side; mixing the two is how leaks start.

### 2. References flow one way: public NEVER points at private

A public artifact MUST NOT reference the private layer — not as a path (`.me/dev-notes.md`), not as a file name (`my_draft.md`), not in prose ("see the agent's memory for auth"), not as a private-only term. This covers **agent memory** in full — its paths, file names, and working-session content are forbidden in any public artifact.

Within the private layer the same one-way discipline holds for agent memory: it can reference anything, but **personal content MUST NOT reach into it** — a personal doc pointing into the agent-facing index inverts that role. That one exception aside, private content references freely — public artifacts, source code, and other private content.

**Why:** the public layer is what reviewers see. A private reference exposes internal state and can leak content the author meant to keep.

### 3. Any public file requires consensus to change

Public files are collectively owned — changes go through the team's process (PR review, approval). Do not edit them on personal authority; draft proposed changes in private and route them through the team's process.

**Why:** without enforced consensus, public files accumulate one-sided edits and silent forks where each contributor thinks their version is canonical.

## When to apply

When writing or editing any artifact, private or public. Also a pre-publish checkpoint: run the leak audit before declaring work done.

## How to apply

- **Before placing content**, decide its layer.
- **Before a reference in a public artifact**, confirm the target is also public.
- **Before publishing**, grep the public layer against the project's forbidden list; stop and fix whatever it flags.
- **Whenever a new term surfaces that needs to stay private** — a codename, alias, or characteristic phrasing from a private decision, description, or idea — add it to the project's forbidden list — anchored in agent memory (inline or by pointer) — so future audits catch it. The list is **memory of past mistakes**, not a pre-seeded enumeration; the pre-publish grep assembles it from there.
- **When the same fact lives in both layers**, update both on change — otherwise one side goes stale and misleads future reads.

## Prerequisites

- Scan this project's `.gitignore` and the user's `~/.gitignore_global` for private paths.
- Locate the project's agent memory directory (e.g. Claude Code's `~/.claude/projects/<encoded-cwd>/memory/`).

## Out of scope

- Behaviors within a layer — see [ssot-principle][../ssot-principle/RULE.md]; this rule is about _which_ layer, ssot-principle covers what happens within one.
- Prose quality of shared text — see [prose-convention][../prose-convention/RULE.md]. Some terms (e.g. session shorthand) are addressed by more than one rule from different angles.

## References

- [wording-rule][../../bedrocks/wording-rule/BEDROCK.md]
- [governance-scope][../../bedrocks/governance-scope/BEDROCK.md]
- [ssot-principle][../ssot-principle/RULE.md]
- [prose-convention][../prose-convention/RULE.md]

[../../bedrocks/wording-rule/BEDROCK.md]: ../../bedrocks/wording-rule/BEDROCK.md
[../../bedrocks/governance-scope/BEDROCK.md]: ../../bedrocks/governance-scope/BEDROCK.md
[../ssot-principle/RULE.md]: ../ssot-principle/RULE.md
[../prose-convention/RULE.md]: ../prose-convention/RULE.md
[prerequisites]: #prerequisites
