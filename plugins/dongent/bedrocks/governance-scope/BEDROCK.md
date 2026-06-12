---
name: governance-scope
description: Whose conventions a piece of content follows — the plugin's own defaults for private (author-only) content, the team's established rules for public (shared) content.
---

# Governance scope — defaults for private, team rules for public

Within a project, every artifact sits in one of two **layers**, each a group of artifacts sharing an audience: **private** (what the author keeps to themselves) or **public** (shared with others). Together they cover all of it. Which layer a piece of content is in decides whose conventions it follows: the plugin's own defaults, or the team's.

## Rule

### Private and public

<!-- prettier-ignore -->
| Layer | The content |
|---|---|
| **Private** | author-only — personal drafts, internal documents, memory references; anything the author does not want to publish |
| **Public** | shared with anyone else (teammates, reviewers, the world) — team-visible, committed, published |

Gitignore is the strongest practical signal of author-only intent, though not the whole story — agent memory and internal vocabulary are private but aren't gitignore-expressible. The test underneath is audience — whether content is shared with others or kept to the author — so the split holds for projects without git too.

### Whose conventions apply

- **Private** → the plugin's own defaults, applied directly.
- **Public** → the team's established convention takes precedence over the plugin defaults, but only when it exists and meets at least a basic industry standard (judged from the relevant shared artifacts — nearby files, recent commits, templates, and the like). With no qualifying convention, fall back to the plugin defaults.

**Why:** public content belongs to the team that reads and maintains it, so it follows their established way; the author's private content answers only to the defaults.

A rule that builds on this supplies the rest for its own domain — what counts as "the relevant artifacts" to observe, and what its own defaults are.
