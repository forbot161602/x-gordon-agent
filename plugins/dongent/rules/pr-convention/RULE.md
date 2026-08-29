---
name: pr-convention
description: Pull request convention — title defaults to the commit-header shape; body is terse and framed around the repo's PR template; cross-domain references and code snippets only when load-bearing. These are defaults; an established team style takes precedence.
---

# PR convention — terse template-driven body

A PR is shared prose the reviewer reads alongside the diff. Most of a PR's structure comes from the repo's PR template; this rule covers what's universal (title shape, body brevity, code-snippet policy) and inherits the rest from the base rules in [Builds on][builds-on].

## Builds on

MUST read and follow these first — this rule builds on them:

- [wording-rule][../../bedrocks/wording-rule/BEDROCK.md]
- [governance-scope][../../bedrocks/governance-scope/BEDROCK.md]
- [ssot-principle][../ssot-principle/RULE.md]
- [private-content][../private-content/RULE.md]
- [prose-convention][../prose-convention/RULE.md]
- [commit-convention][../commit-convention/RULE.md]

## Rule

The principles below are **defaults**; [governance-scope][../../bedrocks/governance-scope/BEDROCK.md] governs whether the repo's PR template takes precedence — see [How to apply][how-to-apply] for what to observe.

### 1. Title defaults to the commit-header shape

By default the PR title shares the same format constraints as the commit header in [commit-convention][../commit-convention/RULE.md] — `type(scope): description` shape, length window, imperative voice, plain-prose phrasing. Single-commit PR: title is typically the commit's header verbatim; multi-commit PR: title summarises the chain in the same shape. Teams can set a different PR-title style — see [How to apply][how-to-apply].

**Why:** the title is `gh pr list`'s at-a-glance; reviewers scan it the same way they scan `git log --oneline`. The same shape keeps the two surfaces consistent.

### 2. Body is terse and template-driven

The PR body carries a **precise, concise summary** of the change — what, why, and how (approach + verification) — and **pointers** to ticket / related PRs / specs. Code-level explanations stay in in-code comments, not the body.

- **Length**: short. Each section is a sentence or a few bullets; rarely more than a screen. A long body usually means the diff itself needs splitting, or better in-code comments.
- **Sections**: defined by the repo's PR template — follow its section names verbatim; don't rename, reorder, or add. When no template, keep the minimum that frames the change (typically Why / What).
- **Cross-domain references**: include only when load-bearing — follows [commit-convention][../commit-convention/RULE.md]'s project-domain scope.
- **Code snippets**: include only when load-bearing — a snippet earns its place when it anchors a discussion the diff alone can't show (the new public-API shape, the one critical line whose semantics changed). Keep it short and to the essence; don't paste full functions or duplicate the diff.

**Why:** the body summarises and frames the change; reviewers go to the diff and in-code comments for code-level detail. Long PR bodies trade off against being read.

## When to apply

When opening or editing any PR. Also a pre-publish checkpoint: run the audit before `gh pr create` or `gh pr edit`.

## How to apply

- **Before writing**, run [governance-scope][../../bedrocks/governance-scope/BEDROCK.md]'s cascade — this rule supplies its domain inputs:
  - **The team style to observe** — the repo's PR template (`.github/pull_request_template.md` or `.github/PULL_REQUEST_TEMPLATE/*`), followed verbatim when present; failing that, recent merged PRs as a style reference: `gh pr list --state merged --limit 10` then `gh pr view <pr-number>` (if `gh` is unavailable, `git log --grep="^Merge pull request" --merges -n 10` to find merge commits and look up bodies through whatever interface is reachable).
  - **The defaults** to fall back to are the principles above.
- **Before opening**, the agent reads the diff and the drafted body, then verifies title and body against the applied principles plus inherited content rules; fix anything flagged.
- The forbidden-list mechanism lives in [private-content][../private-content/RULE.md] and [prose-convention][../prose-convention/RULE.md]; this rule does not maintain its own list. Violations caught while reviewing a PR go into those rules' lists.

## Out of scope

- Git-workflow concerns: when to open the PR, rebase cadence, reviewer assignment, `gh pr edit --body-file` mechanics.
- Language-specific punctuation (e.g. zh-TW PRs — see [zh-tw-punctuation][../zh-tw-punctuation/RULE.md]).

## References

- [wording-rule][../../bedrocks/wording-rule/BEDROCK.md]
- [governance-scope][../../bedrocks/governance-scope/BEDROCK.md]
- [ssot-principle][../ssot-principle/RULE.md]
- [private-content][../private-content/RULE.md]
- [prose-convention][../prose-convention/RULE.md]
- [zh-tw-punctuation][../zh-tw-punctuation/RULE.md]
- [commit-convention][../commit-convention/RULE.md]

[../../bedrocks/wording-rule/BEDROCK.md]: ../../bedrocks/wording-rule/BEDROCK.md
[../../bedrocks/governance-scope/BEDROCK.md]: ../../bedrocks/governance-scope/BEDROCK.md
[../ssot-principle/RULE.md]: ../ssot-principle/RULE.md
[../private-content/RULE.md]: ../private-content/RULE.md
[../prose-convention/RULE.md]: ../prose-convention/RULE.md
[../zh-tw-punctuation/RULE.md]: ../zh-tw-punctuation/RULE.md
[../commit-convention/RULE.md]: ../commit-convention/RULE.md
[builds-on]: #builds-on
[how-to-apply]: #how-to-apply
