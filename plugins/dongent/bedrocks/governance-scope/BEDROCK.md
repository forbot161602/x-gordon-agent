---
name: governance-scope
description: Whose conventions a piece of content follows — within each layer, its own established convention (the author's own for private, the team's for public) when the layer's artifacts show one, else the plugin's defaults.
---

# Governance scope — each layer's own convention, then the defaults

Within a project, every artifact sits in one of two **layers**, each a group of artifacts sharing an audience: **private** (what the author keeps to themselves) or **public** (shared with others). Together they cover all of it. Which layer a piece of content is in decides whose convention it follows — the author's own for private, the team's for public — and the plugin's defaults where neither has established one.

## Rule

### Private and public

<!-- prettier-ignore -->
| Layer | The content |
|---|---|
| **Private** | author-only — personal drafts, internal documents, memory references; anything the author does not want to publish |
| **Public** | shared with anyone else (teammates, reviewers, the world) — team-visible, committed, published |

Gitignore is the strongest practical signal of author-only intent, though not the whole story — agent memory and internal vocabulary are private but aren't gitignore-expressible. The test underneath is audience — whether content is shared with others or kept to the author — so the split holds for projects without git too.

### Whose conventions apply

Within either layer, an **established convention** — one the layer's own artifacts actually show — takes precedence over the plugin defaults; with none that qualifies, the defaults apply. Whose convention that is differs by layer:

- **Private** → the **author's own** established convention, drawn from the author-only artifacts.
- **Public** → the **team's** established convention, drawn from the shared artifacts.

**Why:** public content belongs to the team that reads and maintains it, so a convention they have actually established wins; private content likewise answers to the author's own.

### When an established convention applies

An established convention — the team's in the public layer, the author's own in the private one — overrides a default only on **positive evidence** they do it differently — an explicit style guide, or a consistent contrary pattern across the relevant artifacts (nearby files, recent commits, templates) that also clears at least a basic industry standard; not finding the default's convention nearby is NEVER such evidence. It overrides only the specific defaults that evidence actually speaks to; every other default holds — whether the layer is silent there or the signal is genuinely ambiguous.

**Why:** the defaults exist to govern wherever the layer has not spoken; reading deference into silence invents a rule that isn't there and discards a sound default for nothing.

A rule that builds on this supplies the rest for its own domain — what counts as "the relevant artifacts" to observe, and what its own defaults are.
