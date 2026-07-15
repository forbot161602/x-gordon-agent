---
name: commit-convention
description: Conventional commits format with header / body / footer parts — concise structured header, free body, standard trailers. Messages scoped to the project's reviewers; cross-domain references only when load-bearing. These are defaults; an established team style takes precedence.
---

# Commit convention — concise structured project-scoped messages

A commit message is shared prose that future readers see. This rule covers the message's structural form and its project scope; the content of its parts inherits from the base rules in [Builds on][builds-on].

## Builds on

MUST read and follow these first — this rule builds on them:

- [wording-rule][../../bedrocks/wording-rule/BEDROCK.md]
- [governance-scope][../../bedrocks/governance-scope/BEDROCK.md]
- [ssot-principle][../ssot-principle/RULE.md]
- [private-content][../private-content/RULE.md]
- [prose-convention][../prose-convention/RULE.md]

## Rule

Two principles. A commit message has three semantic parts with different format expectations; the whole message stays scoped to the current project's reviewers. These principles are **defaults**; [governance-scope][../../bedrocks/governance-scope/BEDROCK.md] governs whether the team's commit style takes precedence — see [How to apply][how-to-apply] for what to observe.

### 1. Three-part commit structure (header / body / footer)

- **Header** — the single line at the top (shown in `git log --oneline`). Concise, structured, imperative.
  - Format: `type(scope): description` (conventional commits); a `type` is usually included (common values: `feat` / `fix` / `docs` / `refactor` / `test` / `chore` / `perf` / `build` / `ci` / `style` / `revert`); `scope` is OPTIONAL.
  - Length: typically 6-12 English words (or equivalent in the writing system used; CJK roughly 12-24 characters).
  - Phrasing: imperative mood; name the primary change's **purpose or scope** — what it is for, not a list of what changed — leaving secondary changes to the body.
  - Symbols: reads as plain prose; avoid `+`, `/`, and similar symbols unless necessary.
- **Body** — paragraphs of context, motivation, trade-offs. Free prose; no length cap; symbols allowed when they communicate better than words, not forced out. Soft-wrap: one line per paragraph, no hard breaks mid-paragraph, a blank line between paragraphs.
- **Footer** — when an agent assisted, MUST include a `Co-Authored-By:` trailer (e.g. `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`); other standard trailers per project policy.

**Why:** the header is the at-a-glance summary of what the body explains; the body has room for context; the footer carries fixed-form metadata.

### 2. Project-domain scope

The commit message is written from the perspective of the project's reviewers — the people who read it in `git log`, `git blame`, or PR review. Cross-domain references — implementation details from another layer or service (e.g. a frontend commit naming a backend column type like `JSONB`) — appear **only when load-bearing**: when the change can't be understood without them.

**Why:** the reviewer is in the project's domain, not yours. Cross-domain shorthand forces them to bridge a context they don't share.

## When to apply

When writing or editing any commit message. Also a pre-publish (pre-commit) checkpoint: run the audit before declaring the commit ready.

## How to apply

- **Before writing**, run [governance-scope][../../bedrocks/governance-scope/BEDROCK.md]'s cascade — this rule supplies its two domain inputs:
  - **The team style to observe** — the team's documented commit style, or recent commits as a style reference where none is documented.
  - **The defaults** to fall back to are the principles above.
- **Before commit**, the agent reads the staged diff and the drafted message, then verifies header / body / footer against the applied principles plus inherited content rules; fix anything flagged.
- The forbidden-list mechanism lives in [private-content][../private-content/RULE.md] and [prose-convention][../prose-convention/RULE.md]; this rule does not maintain its own list. Violations caught while reviewing a commit go into those rules' lists.

## Out of scope

- PR title and PR description / GitHub issue body — see pr-convention rule.
- Git-workflow concerns: when and how often to commit (e.g. stage-by-stage with reviews, or commit immediately), restaging after edits.
- Language-specific punctuation (e.g. zh-TW commit messages — see [zh-tw-punctuation][../zh-tw-punctuation/RULE.md]).

## References

- [wording-rule][../../bedrocks/wording-rule/BEDROCK.md]
- [governance-scope][../../bedrocks/governance-scope/BEDROCK.md]
- [ssot-principle][../ssot-principle/RULE.md]
- [private-content][../private-content/RULE.md]
- [prose-convention][../prose-convention/RULE.md]
- [zh-tw-punctuation][../zh-tw-punctuation/RULE.md]

[../../bedrocks/wording-rule/BEDROCK.md]: ../../bedrocks/wording-rule/BEDROCK.md
[../../bedrocks/governance-scope/BEDROCK.md]: ../../bedrocks/governance-scope/BEDROCK.md
[../ssot-principle/RULE.md]: ../ssot-principle/RULE.md
[../private-content/RULE.md]: ../private-content/RULE.md
[../prose-convention/RULE.md]: ../prose-convention/RULE.md
[../zh-tw-punctuation/RULE.md]: ../zh-tw-punctuation/RULE.md
[builds-on]: #builds-on
[how-to-apply]: #how-to-apply
