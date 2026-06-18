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
- **Public** → the team's established convention takes precedence over the plugin defaults; with none that qualifies, the defaults apply.

**Why:** public content belongs to the team that reads and maintains it, so a convention they have actually established wins; private content answers only to the defaults.

### When a team convention applies

A team convention overrides a default only on **positive evidence** the team does it differently — an explicit team style guide, or a consistent contrary pattern across the relevant shared artifacts (nearby files, recent commits, templates) that also clears at least a basic industry standard; not finding the default's convention nearby is NEVER such evidence. It overrides only the specific defaults that evidence actually speaks to; every other default holds — whether the team is silent there or the signal is genuinely ambiguous.

**Why:** the defaults exist to govern wherever the team has not spoken; reading deference into silence invents a team rule that isn't there and discards a sound default for nothing.

A rule that builds on this supplies the rest for its own domain — what counts as "the relevant artifacts" to observe, and what its own defaults are.
