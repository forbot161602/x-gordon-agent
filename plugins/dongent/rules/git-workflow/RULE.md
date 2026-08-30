---
name: git-workflow
description: Operational git conventions — work branches from where it starts and returns by PR, one commit is one self-explanatory change, and a PR goes out rebased onto the latest base; the author reviews both before either leaves. These are defaults; an established team workflow takes precedence.
---

# Git workflow — where work happens, and when it leaves

Which branch work sits on, where one commit ends, and what has to hold before anything leaves the workspace. What a commit message or a PR body then says is `commit-convention`'s and `pr-convention`'s.

## Builds on

MUST read and follow these first — this rule builds on them:

- [wording-rule][../../bedrocks/wording-rule/BEDROCK.md]
- [governance-scope][../../bedrocks/governance-scope/BEDROCK.md]
- [agent-autonomy][../../bedrocks/agent-autonomy/BEDROCK.md]
- [private-content][../private-content/RULE.md]
- [prose-convention][../prose-convention/RULE.md]

## Rule

The principles below cover where work happens, how it is cut into commits, and when it goes out. They are **defaults**; [governance-scope][../../bedrocks/governance-scope/BEDROCK.md] governs whether the team's established workflow takes precedence — see [How to apply][how-to-apply].

### 1. Work branches from where it starts and returns there

- Work gets its own branch off the branch it started on and merges back through a PR, never a direct push — whatever flow the team follows, the branch it left is the branch it returns to.
- A branch is named after the sibling branches already on the remote; with no pattern to follow, `<type>/<short-description>` in kebab-case — the type usually one of those `commit-convention` lists for a header.
- Work following a still-open PR never continues on that branch itself — its commits would fold into the review. Work that genuinely needs the unmerged code branches off it; anything independent branches from that branch's own base, taken **from the remote** rather than the stale local copy.

**Why:** a team's flow must be inferred from evidence that is often missing. Branching from where the work sits needs no guess, and errs the cheap way: an unnecessary PR costs a step, while the wrong direct push costs a revert on a branch others have pulled.

### 2. One commit is one self-explanatory change

- A commit explains itself read alone, and delivers something whole. Too small is one file per commit, or a fragment too partial to state a purpose; too large is a PR's worth of unrelated work. The number of files changed is not the test.
- A phase of a plan is the first candidate boundary, not an exemption: a phase that stands alone is one commit, one that reaches PR size is cut further, and output the plan never called for — exploration, analysis, scaffolding — enters no commit at all.
- Small lint, formatting, and typo repairs — and whatever a hook rewrote or blocked — go into the commit at hand rather than one of their own.
- What was missed in the previous commit is folded back into it with `--amend`, force-pushing with `--force-with-lease` if it was already pushed — a commit that says only that the previous one was flawed is noise beside the commits carrying the work. The lease refuses when the remote holds anything the agent has not seen — overwriting another's work is the push that cannot be undone. Whenever a push is rejected, report and wait for instructions; NEVER stack a new commit instead.
- Read the whole index before committing or amending, not only what was just added — it can already hold work staged for a later commit.
- Under stepwise review, staging is the author's reading ledger, not a workspace to tidy: what is unstaged is still in their queue, what is staged they have approved. The agent stages only as the immediate step of an authorized commit.

**Why:** only a commit with a single purpose can carry a header that names it, so [commit-convention][../commit-convention/RULE.md]'s header rests on this test. A typo committed on its own costs the reader the thread of the work.

### 3. Publishing needs consent and the latest base

- A PR opens once the change is implemented and verified, documentation included where needed. Before it opens, the base is brought up to date, the work rebased, and conflicts resolved — the PR is not published until that round is done.
- Every push that changes the branch repeats that round, and the PR description is updated where it no longer matches what the branch holds.
- Under stepwise review, each publishing step (a commit, a push, opening or re-publishing a PR) is consented to separately; an instruction about how work is cut — which commit something belongs in, whether to split it — settles scope, not consent.

**Why:** the reviewer reads the diff as a claim about the latest base; against a stale one, the conflicts and the superseded lines stay hidden until the merge. An earlier rebase adds nothing this one does not.

## When to apply

Before any git operation that creates, rewrites, or publishes work — branching, committing, amending, pushing, opening or updating a PR. Also a pre-publish checkpoint: verify the branch, the cut, and the base before the operation runs.

## How to apply

- **Before writing**, run [governance-scope][../../bedrocks/governance-scope/BEDROCK.md]'s cascade — this rule supplies its domain inputs:
  - **The team workflow to observe** — a contributing guide where the team has one, and otherwise what the remote itself shows.
  - **The defaults** to fall back to are the principles above.
- **Before a commit**, read the full index, confirm the change is self-explanatory, and decide between a new commit and an `--amend` of the previous one.
- **Before a publish**, confirm consent for this step; where it opens or re-publishes a PR, bring the base up to date and rebase onto it first.

## Prerequisites

- Identify the remote's default branch, and which of the others are long-lived, as against the short-lived branch a single change opens and ends.
- Observe the naming pattern the branches follow, and whether the long-lived ones take PRs or direct pushes.

## Out of scope

- A commit message's content and format — see [commit-convention][../commit-convention/RULE.md]; a PR's title and body — see [pr-convention][../pr-convention/RULE.md].
- When an agent stops for consent, and what it reports — [agent-autonomy][../../bedrocks/agent-autonomy/BEDROCK.md] owns that; this rule only names the git operations those stops land on.
- Hosting-platform mechanics (protected-branch settings, required checks, merge-queue configuration) — the project's own concern, observed through the cascade above.

## References

- [wording-rule][../../bedrocks/wording-rule/BEDROCK.md]
- [governance-scope][../../bedrocks/governance-scope/BEDROCK.md]
- [agent-autonomy][../../bedrocks/agent-autonomy/BEDROCK.md]
- [private-content][../private-content/RULE.md]
- [prose-convention][../prose-convention/RULE.md]
- [commit-convention][../commit-convention/RULE.md]
- [pr-convention][../pr-convention/RULE.md]

[../../bedrocks/wording-rule/BEDROCK.md]: ../../bedrocks/wording-rule/BEDROCK.md
[../../bedrocks/governance-scope/BEDROCK.md]: ../../bedrocks/governance-scope/BEDROCK.md
[../../bedrocks/agent-autonomy/BEDROCK.md]: ../../bedrocks/agent-autonomy/BEDROCK.md
[../private-content/RULE.md]: ../private-content/RULE.md
[../prose-convention/RULE.md]: ../prose-convention/RULE.md
[../commit-convention/RULE.md]: ../commit-convention/RULE.md
[../pr-convention/RULE.md]: ../pr-convention/RULE.md
[how-to-apply]: #how-to-apply
