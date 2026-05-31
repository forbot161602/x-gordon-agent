---
name: commit-convention
description: Conventional commits format with header / body / footer parts — concise structured header, free body, standard trailers. Messages scoped to the project's reviewers; cross-domain references only when load-bearing. A domain rule building on ssot-principle, private-content, and prose-convention.
---

# Commit convention — concise structured project-scoped messages

A commit message is shared prose that future readers see. This rule covers the message's structural form — three parts (header / body / footer) — and its project scope; the content of those parts inherits from [ssot-principle][../ssot-principle/RULE.md], [private-content][../private-content/RULE.md], and [prose-convention][../prose-convention/RULE.md].

## Rule

Two principles. A commit message has three semantic parts (header / body / footer) with different format expectations; the whole message stays scoped to the current project's reviewers. These principles are **defaults** — the team's documented commit style takes precedence where it exists; see How to apply for the cascade.

### 1. Three-part commit structure (header / body / footer)

- **Header** — the single line at the top (shown in `git log --oneline`). Concise, structured, imperative.
  - Format: `type(scope): description` (conventional commits); `type` is usually required (common values: `feat` / `fix` / `docs` / `refactor` / `test` / `chore` / `perf` / `build` / `ci` / `style` / `revert`); `scope` is optional.
  - Length: typically 6-12 English words (or equivalent in the writing system used; CJK roughly 12-24 characters).
  - Phrasing: imperative complete sentence; one main action — additional actions go in the body.
  - Symbols: reads as plain prose; avoid `+`, `/`, and similar symbols unless necessary.
- **Body** — paragraphs of context, motivation, trade-offs. Free prose; no length cap; symbols allowed when they communicate better than words, not forced out.
- **Footer** — include something like `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>` when an agent assisted; other standard trailers per project policy.

**Why:** the header is the at-a-glance summary of what the body explains (visible in `git log --oneline`); the body has room for context; the footer carries fixed-form metadata.

### 2. Project-domain scope

The commit message is written from the perspective of the project's reviewers — the people who read it in `git log`, `git blame`, or PR review. Cross-domain references — implementation details from another layer or service (e.g. a frontend commit naming a backend column type like `JSONB`) — appear **only when load-bearing**: when the change can't be understood without them.

**Why:** the reviewer is in the project's domain, not yours. Cross-domain shorthand forces them to bridge a context they don't share.

## When to apply

When writing or editing any commit message. Also a pre-publish (pre-commit) checkpoint: run the audit before declaring the commit ready.

## How to apply

- **Before writing**, follow this priority cascade:
  1. The team's documented commit style (if it exists) — defer to it.
  2. Recent commits as a style reference (when the team has no documented commit style, and recent commits meet basic standards).
  3. Fall back to the principles above.
- **Before commit**, the agent reads the staged diff and the drafted message, then verifies header / body / footer against the applied principles plus inherited content rules; fix anything flagged.
- The forbidden-list mechanism lives in [private-content][../private-content/RULE.md] and [prose-convention][../prose-convention/RULE.md]; this rule does not maintain its own list. Violations caught while reviewing a commit go into those rules' lists.

## Out of scope

- PR title and PR description / GitHub issue body — see pr-convention rule.
- Commit-workflow concerns: when and how often to commit (e.g. stage-by-stage with reviews, or commit immediately), restaging after edits.
- Language-specific punctuation (e.g. zh-TW commit messages — see [zh-tw-punctuation][../zh-tw-punctuation/RULE.md]).

## References

- [ssot-principle][../ssot-principle/RULE.md]
- [private-content][../private-content/RULE.md]
- [prose-convention][../prose-convention/RULE.md]
- [zh-tw-punctuation][../zh-tw-punctuation/RULE.md]

[../ssot-principle/RULE.md]: ../ssot-principle/RULE.md
[../private-content/RULE.md]: ../private-content/RULE.md
[../prose-convention/RULE.md]: ../prose-convention/RULE.md
[../zh-tw-punctuation/RULE.md]: ../zh-tw-punctuation/RULE.md
