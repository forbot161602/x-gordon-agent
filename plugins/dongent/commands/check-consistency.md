---
name: check-consistency
description: Pre-publish audit. Verify the target file set obeys ssot-principle, private-content, prose-convention, document-convention, markdown-convention, and zh-tw-punctuation before publishing. Designed to run mostly without author intervention.
---

Run before declaring work ready to leave the private workspace.

This command runs **mostly without author intervention**. By the time it fires, the facts have already been confirmed (typically post-design or post-implementation) and the session context holds the ground truth. The audit primarily reconciles **documentation** against that truth — markdown, plan files, specs, README — since code is validated by tests and CI while docs lag behind and accumulate drift (often from grep-based edit passes that miss occurrences). The agent therefore **fixes findings using its own judgement** rather than pausing to ask. Escalation to the author is the rare exception.

**Publish** here means any moment the content crosses the private→public boundary. Examples: `git commit` / `git stage` / `git push`, `gh pr create` / `gh pr edit`, posting to Confluence / external wiki / a technical blog, sending email, sharing presentation slides. Most invocations are pre-commit, but the audit applies to the broader publish moment.

## Arguments

None required. The forms:

- `/check-consistency` — default. Audit all staged and unstaged files in the worktree (the typical "I'm about to commit" use).
- `/check-consistency @<file>...` — audit only the file(s) `@`-mentioned in the prompt (from the agent client's `@` file picker).
- `/check-consistency --all` — audit the full PR-scope (use before opening a PR to catch cross-file conflicts between docs and code).
- `/check-consistency --paths <glob...>` — audit only files matching the globs (paths are relative to the repo root). Examples: `--paths "docs/README.md"`, `--paths "**/README.md" "docs/**/*.md"`.
- `/check-consistency --memory [--fold]` — audit the project's agent memory for internal consistency. Add `--fold` to reconcile tightly-bound rule content against the plugin-managed rules file as canonical.

`@<file>`, `--all`, `--paths`, and `--memory` are mutually exclusive; pass at most one form.

## Read first

MUST read these first — this command relies on them:

- [wording-rule][../bedrocks/wording-rule/BEDROCK.md]
- [governance-scope][../bedrocks/governance-scope/BEDROCK.md]
- [reply-language][../bedrocks/reply-language/BEDROCK.md]
- [ssot-principle][../rules/ssot-principle/RULE.md]
- [private-content][../rules/private-content/RULE.md]
- [prose-convention][../rules/prose-convention/RULE.md]
- [document-convention][../rules/document-convention/RULE.md]
- [markdown-convention][../rules/markdown-convention/RULE.md]
- [zh-tw-punctuation][../rules/zh-tw-punctuation/RULE.md]

## Steps

> **Prerequisite for every step below**: read each rule cited in steps 3 and 4 (`RULE.md` files) **in full** before applying its check. This command lists detection methods; the rule body carries the principles, nuances, examples, and edge cases that this command does not restate. **Skipping this step is the most common reason audits miss real violations.**

### 1. Resolve the target file set

- **Default**: `git status --porcelain` → keep paths whose status is not `D` (deleted).
- **`@<file>` mentions**: the target set is exactly the files `@`-mentioned in the arguments — each arrives as a literal `@<repo-relative-path>` token the agent client supplies. Unlike `--paths`, these are literal paths, not globs.
- **`--all`**: audit the PR scope — every file changed on HEAD since it diverged from its base (the local standing branch it forked from), **plus uncommitted changes (staged, unstaged, untracked)**. The agent identifies the base from session context or the local branch graph. With no base found, or no commits ahead of it, there is no PR scope — fall back to the default target set and note it.
- **`--paths`**: expand each glob against the worktree (repo-relative); deduplicate. The agent corrects malformed globs (reporting the actual interpretation used) but doesn't broaden a syntactically valid glob just because it returned zero matches.
- **`--memory`**: the target set is the project's agent memory — its index and the files the index points at, including the plugin-managed rules files compiled by [sync-rule-memory][sync-rule-memory.md].

If the resolved set is empty, report "nothing to audit" and stop.

### 2. Identify the private layer

Step 1 surfaces **mostly public files** in the worktree modes (default, `--all`, `--paths`, `@`) — `git status` and `git diff` filter out gitignored content by default; file mention and glob expansion can match anywhere in principle but in practice target public folders (`docs/`, `specs/`, etc.). Private content (per [private-content][../rules/private-content/RULE.md]) usually doesn't make it into step 1's output, so — in every mode — the agent always pulls the relevant private content into scope from its session context. This covers both **relevant private planning and progress docs** — e.g. a gitignored personal plan recording why the work was split into these commits, or tracking their progress — and **resident private docs** — a personal doc holding house rules, project-architecture notes, and the like. Both need to stay consistent with what's being published, and these resident docs are where rule duplication tends to accumulate (see step 4). In `--memory` mode this same step is how the private worktree docs join the memory folder to form the whole-private target set.

### 3. Per-file checks

For each target file, run these checks. The **Run order** column gives the execution sequence — cheap checks (grep, scripts) run first; agent inspection runs on what those didn't resolve.

<!-- prettier-ignore -->
| Source rule | Detection method | Applies to | Run order |
|---|---|---|---|
| [ssot-principle][../rules/ssot-principle/RULE.md] | agent inspection for restated facts, duplicated passages, and conflicting extensions within the file | All files | 6 |
| [private-content][../rules/private-content/RULE.md] | grep against the project's forbidden list (private paths, names, internal vocab) | Public-layer files | 2 |
| [prose-convention][../rules/prose-convention/RULE.md] | grep against the project's forbidden list; agent inspection per the rule's principles | All files | 3 |
| [document-convention][../rules/document-convention/RULE.md] | Agent inspection of file shape, document format, and authoring discipline, per the rule's How to apply cascade | All files | 4 |
| [markdown-convention][../rules/markdown-convention/RULE.md] | Per the rule's How to apply — its private/public style cascade. | All files | 5 |
| [zh-tw-punctuation][../rules/zh-tw-punctuation/RULE.md] | Run the rule's `convert.py --check` from the rule folder | Chinese-led lines | 1 |

For each finding, apply the fix policy (step 5) before moving to the next file. Don't list every instance of the same violation in the final report — collapse to one example plus a count.

### 4. Cross-file checks

- **Conflicting extensions**: a canonical fact is extended or rephrased elsewhere (different contexts call for different framings), but the extensions contradict each other or the canonical. The agent compares related references across the file set and aligns the divergent text with the canonical.
- **Same fact in multiple files**: identify the canonical home; link to it where the reference is load-bearing, and cut a redundant copy or link where it isn't.
- **Stale references**: a name or concept has been renamed in this branch's diff but old occurrences remain elsewhere. Grep the file set for the old name and replace with the new.
- **Private leak across files**: any public file references a private file by path or content. Remove the reference.

#### Private layer and plugin-managed rules (`--memory`)

Among the memory files, the plugin-managed rules files are owned by the [sync-rule-memory][sync-rule-memory.md] command as an `ssot-principle` extension this audit doesn't re-decide: each source's section is the fixed canonical home for that rule's facts — point other memory files into the section; NEVER point it outward, empty it to name another home, or edit the region between its markers.

Beyond those sections, the private layer is **personal-first** by default — personal content is the canonical home, and per [private-content][../rules/private-content/RULE.md] a dedup pointer runs only from memory to it, NEVER back. `--fold` inverts this for **tightly-bound rule content** (the scope the `sync-rule-memory` command dedups — bound to one rule): the plugin-managed rules file becomes canonical — a personal copy of a rule the plugin already provides is the redundancy `--fold` removes. Content spanning several rules or covered by none stays personal-first unless the invocation explicitly extends `--fold` to it.

### 5. Fix policy

**Default: fix.** When uncertain, prefer fixing with a brief justification in the report.

**Boundary: edit content, not files.** Editing content is in bounds — including removing a duplicated passage. What stays out of bounds is file-level destruction: NEVER delete, rename, or move a file, or hollow one down to an unreferenced stub. Surface those as delete candidates for the author to confirm (step 6).

**When facts conflict or are unclear, investigate.** Most ambiguities resolve under investigation. Gather evidence from sources the target file set might not contain:

- **Source code** — search and read the implementation the docs describe; code is usually closer to ground truth than its surrounding prose.
- **Tests** — test names / assertions encode contracts; a docs claim contradicting a green test is usually the docs being stale.
- **Related docs** — README, architecture docs, sibling specs, parent-folder overview docs; canonical facts might live one folder up.
- **Git history** — `git log -p <file>` for context; `git blame` for when a line was introduced and why; `git log --diff-filter=R --summary` for prior renames.
- **External sources** — when the repo doesn't carry enough context: web docs (framework / API references), GitHub PR / issue threads, cloud-resource inspection (AWS / GCP / Azure), internal wikis (Confluence / Notion), ticket trackers (Linear / Jira), production telemetry (logs / metrics). The agent picks the right channel based on what the conflict points at.

**Escalate** only when investigation cannot resolve the ambiguity:

- **Genuinely ambiguous canonical home** — two files state contradicting or independent versions of the same fact; consolidating them would lose information.
- **Undocumented context** — the deciding context was never recorded in any file, history, or accessible external source.

### 6. Report

Group by the rule checked — the audit runs per rule, so the report mirrors it. These buckets; entries listed under each rule cited:

- 🔄 **Auto-fixed** — under each rule: the changes applied (file path, line where applicable, one-line description per fix).
- ❌ **Needs decision** — under each rule: escalated items (file path, line, the ambiguity, options the author can pick). **Usually empty**; non-empty signals a truly unresolvable case (see step 5).
- 🗑️ **Delete candidates** — a file a fix left as only outward pointers (or empty) and referenced by nothing; NEVER auto-deleted (step 5's boundary), listed for the author to confirm removal.
- ✅ **Clean** — per rule: a one-line note on what it verified across the set (no per-file listing needed).

Auto-fixed entries — typically the bulk of the report — are already in the worktree as unstaged changes for `git diff` review. If "Needs decision" or "Delete candidates" is non-empty, the author resolves them before publishing.

**No silent truncation**: if any bucket is capped to keep the report scannable (e.g. "first 10 SSoT findings"), state it with `... and N more` so the author knows coverage isn't complete.

## Example findings

A few patterns the audit commonly catches:

- **Code / spec drift** — code or in-line comments changed without syncing the spec / plan, or vice versa.
- **Decision-change leftovers** — a decision was changed in one place but its dependents still reflect the old version.
- **Duplicated pending item** — the same `TBD` / `(to be decided)` is repeated across plan-style docs (proposal, design, plan, task, etc.) instead of living once where its scope belongs; different-scope TBDs are fine.

## Out of scope

- File-level destruction — out of scope; the audit edits content only.
- Build / type-check / test runs — separate tooling.
- Style enforcement against team norms — [document-convention][../rules/document-convention/RULE.md] already defers to observed team style; this command honors that and won't auto-fix into a team-conflicting style.

## References

- [wording-rule][../bedrocks/wording-rule/BEDROCK.md]
- [governance-scope][../bedrocks/governance-scope/BEDROCK.md]
- [reply-language][../bedrocks/reply-language/BEDROCK.md]
- [ssot-principle][../rules/ssot-principle/RULE.md]
- [private-content][../rules/private-content/RULE.md]
- [prose-convention][../rules/prose-convention/RULE.md]
- [document-convention][../rules/document-convention/RULE.md]
- [markdown-convention][../rules/markdown-convention/RULE.md]
- [zh-tw-punctuation][../rules/zh-tw-punctuation/RULE.md]
- [sync-rule-memory][sync-rule-memory.md]

[../bedrocks/wording-rule/BEDROCK.md]: ../bedrocks/wording-rule/BEDROCK.md
[../bedrocks/governance-scope/BEDROCK.md]: ../bedrocks/governance-scope/BEDROCK.md
[../bedrocks/reply-language/BEDROCK.md]: ../bedrocks/reply-language/BEDROCK.md
[../rules/ssot-principle/RULE.md]: ../rules/ssot-principle/RULE.md
[../rules/private-content/RULE.md]: ../rules/private-content/RULE.md
[../rules/prose-convention/RULE.md]: ../rules/prose-convention/RULE.md
[../rules/document-convention/RULE.md]: ../rules/document-convention/RULE.md
[../rules/markdown-convention/RULE.md]: ../rules/markdown-convention/RULE.md
[../rules/zh-tw-punctuation/RULE.md]: ../rules/zh-tw-punctuation/RULE.md
[sync-rule-memory.md]: sync-rule-memory.md
