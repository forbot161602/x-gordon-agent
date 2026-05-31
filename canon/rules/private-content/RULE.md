---
name: private-content
description: Keep private content (personal drafts, documents, memory references, internal terms) out of public artifacts. Each project declares its layers; references flow one way — private may cite public, public must not cite private. Operationalises the Scope note of ssot-principle.
---

# Private content — one-way information flow

Content separates by audience: what the author keeps to themselves lives in a **private** layer, what is shared with others lives in a **public** layer. This rule keeps the two apart and stops the private side from leaking into the public side. It operationalises the **Scope** note of [ssot-principle][../ssot-principle/RULE.md] (SSoT applies within a reference scope; references between scopes are allowed in only one direction).

## Rule

Three principles, applied within the layers each project declares (see Prerequisites). A _layer_ is a group of artifacts sharing an audience: **private** (author-only) or **public** (anyone else — teammates, reviewers, the world). Gitignore is the strongest practical signal of author-only intent, though not the whole story — agent memory and internal vocabulary are private but aren't gitignore-expressible.

### 1. Place content in the right layer

Personal drafts, internal documents, memory references, and anything the author does not want to publish go to **private**. Shared, committed, team-visible content goes to **public**. When in doubt, ask who should see this — if "only me", it is private.

**Why:** the boundary is only as good as the discipline of putting content on the right side; mixing the two is how leaks start.

### 2. References flow one way: public never points at private

A public artifact must **never** reference the private layer — not as a path (`.me/dev-notes.md`), not as a file name (`my_draft.md`), not in prose ("see the agent's memory for auth"), not as a private-only term.

Agent memory itself counts as private — treat its paths and file names (e.g. Claude's `~/.claude/...`, `MEMORY.md`, `feedback_*.md`) as forbidden in any public artifact. Content from the agent's working session — conversation transcripts, personal thoughts, intermediate decisions, session shorthand (e.g. P1, Q1) — is similarly universally forbidden in public artifacts. A private artifact may reference anything — public, other private, source code, memory.

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
- **Whenever a new term surfaces that shouldn't leak** — a codename, alias, or characteristic phrasing from a private decision, description, or idea — add it to the forbidden list so future audits catch it. The list is **memory of past mistakes**, not a pre-seeded enumeration.
- **When the same fact lives in both layers**, update both on change — otherwise one side goes stale and misleads future reads.

## Prerequisites

- Scan this project's `.gitignore` and the user's `~/.gitignore_global` for private paths.
- Locate the project's agent memory directory (e.g. Claude's `~/.claude/projects/<encoded-cwd>/memory/`).

## Out of scope

- Behaviors within a layer — see [ssot-principle][../ssot-principle/RULE.md]. This rule is about _which_ layer; ssot-principle covers what happens within one.
- Prose quality of shared text — see [prose-convention][../prose-convention/RULE.md]. Some terms (e.g. session shorthand) are addressed by both rules from different angles.

## References

- [ssot-principle][../ssot-principle/RULE.md]
- [prose-convention][../prose-convention/RULE.md]

[../ssot-principle/RULE.md]: ../ssot-principle/RULE.md
[../prose-convention/RULE.md]: ../prose-convention/RULE.md
