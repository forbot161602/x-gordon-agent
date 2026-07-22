---
name: publish-check
description: Pre-publish audit. Verify the target file set obeys ssot-principle, private-content, prose-convention, document-convention, markdown-convention, and zh-tw-punctuation before publishing. Designed to run mostly without author intervention.
---

Run before declaring work ready to leave the private workspace.

This command runs **mostly without author intervention**. By the time it fires, the facts have already been confirmed (typically post-design or post-implementation) and the session context holds the ground truth. The audit primarily reconciles the **written content** against that truth — docs, specs, plans, memory — since prose lags behind and accumulates drift (often from grep-based edit passes that miss occurrences). It still reads this change's code logic to see which side drifted — a green CI proves the code runs, not that it matches the docs. The agent therefore **fixes findings using its own judgement** rather than pausing to ask. Escalation to the author is the rare exception.

**Publish** here means any moment the content crosses the private→public boundary. Examples: `git commit` / `git stage` / `git push`, `gh pr create` / `gh pr edit`, posting to Confluence / external wiki / a technical blog, sending email, sharing presentation slides. Most invocations are pre-commit, but the audit applies to the broader publish moment.

## Arguments

None required. The forms:

- `/publish-check` — default. Audit all staged and unstaged files in the worktree (the typical "I'm about to commit" use).
- `/publish-check @<file>...` — audit only the file(s) `@`-mentioned in the prompt (from the agent client's `@` file picker).
- `/publish-check --all` — audit the full scope before opening a PR or publishing (e.g. catch cross-file conflicts across a PR's docs and code).
- `/publish-check --paths <glob...>` — audit only files matching the globs (paths are relative to the repo root). Examples: `--paths "docs/README.md"`, `--paths "**/README.md" "docs/**/*.md"`.
- `/publish-check --memory [--fold]` — audit the project's agent memory for internal consistency. Add `--fold` to reconcile tightly-bound rule content against the plugin-managed rules file as canonical.

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

The **target set** is every file this audit covers — a primary source plus the private layer, audited as one set. The set stays open: a relevant file that surfaces as the audit runs joins it and is audited too.

### 1. Resolve the primary source

- **Default**: every worktree path `git status --porcelain` reports, except deletions (status `D`).
- **`@<file>` mentions**: exactly the files `@`-mentioned in the arguments — each arrives as a literal `@<repo-relative-path>` token the agent client supplies. Unlike `--paths`, these are literal paths, not globs.
- **`--all`**: the PR scope — every file changed on HEAD since it diverged from its base (the local standing branch it forked from), **plus uncommitted changes (staged, unstaged, untracked)**. The agent identifies the base from session context or the local branch graph. With no base found, or no commits ahead of it, there is no PR scope — fall back to the default source and note it.
- **`--paths`**: the worktree files matching the globs (repo-relative), deduplicated. The agent corrects malformed globs (reporting the actual interpretation used) but doesn't broaden a syntactically valid glob just because it returned zero matches.
- **`--memory`**: the project's agent memory — its index and the files the index points at, including the plugin-managed rules files compiled by [memory-sync][memory-sync.md].

### 2. Identify the private layer

Step 1 surfaces **mostly public files** in the worktree modes (default, `--all`, `--paths`, `@`) — `git status` and `git diff` filter out gitignored content by default; file mention and glob expansion can match anywhere in principle but in practice target public folders (`docs/`, `specs/`, etc.). Private content (per [private-content][../rules/private-content/RULE.md]) usually doesn't make it into step 1's output, so — in every mode — the agent always pulls the *relevant* private content into the target set from its session context. This covers the **private planning and progress docs** — e.g. a gitignored personal plan recording why the work was split into these commits, or tracking their progress; the **resident private docs** — a personal doc holding house rules, project-architecture notes, and the like; and the **agent-memory entries in play** — those tracking this work, a status or a next-step. All need to stay consistent with what's being published. Here *relevant* means active to the current work — for each kind: pull in every such doc even if no diff touched it, and look through the folders in play for related siblings. In `--memory` mode this same step is how the private worktree docs join the memory folder to form the whole-private target set.

If the target set is empty — neither source contributes — report "nothing to audit" and stop.

### 3. Read the rules and gather the inputs

Read each rule in the table below — the `RULE.md` files — **in full** before applying its check. This command lists detection methods; the rule body carries the principles, nuances, examples, and edge cases that this command does not restate. **Skipping this step is the most common reason audits miss real violations.**

<!-- prettier-ignore -->
| Source rule | Detection method | Applies to | Run order |
|---|---|---|---|
| [ssot-principle][../rules/ssot-principle/RULE.md] | Agent inspection for restated facts, duplicated passages, and conflicting extensions within the file | All files | 6 |
| [private-content][../rules/private-content/RULE.md] | Grep against the project's forbidden list (private paths, names, internal vocab) | Public-layer files | 2 |
| [prose-convention][../rules/prose-convention/RULE.md] | Grep against the project's forbidden list; agent inspection per the rule's principles | All files | 3 |
| [document-convention][../rules/document-convention/RULE.md] | Agent inspection of file shape, document format, and authoring discipline, per the rule's How to apply cascade | All files | 4 |
| [markdown-convention][../rules/markdown-convention/RULE.md] | Per the rule's How to apply — its private/public style cascade | All files | 5 |
| [zh-tw-punctuation][../rules/zh-tw-punctuation/RULE.md] | Run the rule's `convert.py --check` from the rule folder | Chinese-led lines | 1 |

The **project's forbidden list** the grep checks use is assembled at audit time, not fixed here: gather it from these rules plus the project's agent memory — where, per [private-content][../rules/private-content/RULE.md] and [prose-convention][../rules/prose-convention/RULE.md], the project records the terms it must keep out — walking the memory index so no recorded term is missed.

### 4. Per-file checks

Across the target files, **read every written-content one in full — top to EOF, in this run** (docs, specs, plans, memory; prose can also live in code comments and docstrings). Any partial pass — grep, scripts, another targeted search, or earlier / same-session reading — only **seeds** findings; it NEVER substitutes for this read, and a drifted spot can sit anywhere in such a file. **No in-scope file is skipped — for any reason.** Treat every run as a fresh first run: prior coverage — an earlier run, or content already seen or edited earlier this session through a prompt, a command, or the like — NEVER drops a file from this run's full read. Then run step 3's checks per file, in the **Run order** its table gives — cheap checks (grep, scripts) run first, agent inspection on what they didn't resolve.

For each finding, apply the fix policy (step 6) before moving to the next file. Don't list every instance of the same violation in the final report — collapse to one example plus a count.

### 5. Cross-file checks

- **Conflicting extensions**: a canonical fact is extended or rephrased elsewhere (different contexts call for different framings), but the extensions contradict each other or the canonical. The agent compares related references across the file set and aligns the divergent text with the canonical.
- **Same fact in multiple files**: identify the canonical home; link to it where the reference is load-bearing, and cut a redundant copy or link where it isn't.
- **Stale references**: a name or concept has been renamed in this branch's diff but old occurrences remain elsewhere. Grep the file set for the old name and replace with the new.
- **Private leak across files**: any public file references a private file by path or content. Remove the reference.

#### Private layer and plugin-managed rules (`--memory`)

Among the memory files, the plugin-managed rules files are owned by the [memory-sync][memory-sync.md] command as an `ssot-principle` extension this audit doesn't re-decide: each section is the fixed canonical home for the facts it holds — point other memory files into the section; NEVER point it outward, empty it to name another home, or edit the region between its markers.

Beyond those sections, the private layer is **personal-first** by default — personal content is the canonical home, and per [private-content][../rules/private-content/RULE.md] a dedup pointer runs only from memory to it, NEVER back. `--fold` inverts this for **tightly-bound rule content** (the scope the `memory-sync` command dedups — bound to one rule): the plugin-managed rules file becomes canonical — a personal copy of a rule the plugin already provides is the redundancy `--fold` removes. Content spanning several rules or covered by none stays personal-first unless the invocation explicitly extends `--fold` to it.

### 6. Fix policy

**Default: fix.** When uncertain, prefer fixing with a brief justification in the report.

**Boundary: edit content, not files.** Editing content is in bounds — including removing a duplicated passage. What stays out of bounds is file-level destruction: NEVER delete, rename, or move a file, or hollow one down to an unreferenced stub. Surface those as delete candidates for the author to confirm (step 7).

**When facts conflict or are unclear, investigate.** Most ambiguities resolve under investigation. Gather evidence from sources the target file set might not contain:

- **Source code** — search and read the implementation the docs describe; its actual behavior is direct evidence for resolving the conflict.
- **Tests** — test names / assertions encode the contract in force; a relevant one usually settles the question.
- **Related docs** — README, architecture docs, sibling specs, parent-folder overview docs; canonical facts might live one folder up.
- **Git history** — `git log -p <file>` for context; `git blame` for when a line was introduced and why; `git log --diff-filter=R --summary` for prior renames.
- **External sources** — when the repo doesn't carry enough context: web docs (framework / API references), GitHub PR / issue threads, cloud-resource inspection (AWS / GCP / Azure), internal wikis (Confluence / Notion), ticket trackers (Linear / Jira), production telemetry (logs / metrics). The agent picks the right channel based on what the conflict points at.

**Escalate** only when investigation cannot resolve the ambiguity:

- **Genuinely ambiguous canonical home** — two files state contradicting or independent versions of the same fact; consolidating them would lose information.
- **Undocumented context** — the deciding context was never recorded in any file, history, or accessible external source.

### 7. Report

The report has two groups — **Coverage**, then the audit's **Findings** — each a top-level heading. The sections within a group are one heading level below, so both groups share one shape.

🗂️ **Coverage** — a complete ledger: every target file appears under one section, so under-coverage shows outright rather than by absence.

- 📖 **Read in full** — the files read top-to-EOF this run.
- 🧭 **Covered another way** — large code files or binaries, where a full read is disproportionate or doesn't apply; each with a one-line note on how it was covered instead of a full read.

🔍 **Findings** — the four buckets below; in Auto-fixed and Needs decision, group entries by the rule they came from (the audit runs per rule), then by file — one line per finding, with its line number where it has one. Auto-fixed entries are typically the bulk, already in the worktree as unstaged changes for `git diff` review; where "Needs decision" or "Delete candidates" is non-empty, the author MAY resolve them before publishing.

- 🔄 **Auto-fixed** — the changes applied (file path, line where applicable, one-line description per fix).
- ❌ **Needs decision** — escalated items (file path, line, the ambiguity, options the author can pick). **Usually empty**; non-empty signals a truly unresolvable case (see step 6).
- 🗑️ **Delete candidates** — by file, not rule: a file a fix left as only outward pointers (or empty) and referenced by nothing; NEVER auto-deleted (step 6's boundary), listed for the author to confirm removal.
- ✅ **Clean** — a one-line note on what it verified across the set (no per-file listing needed).

**No silent truncation**: if any bucket is capped to keep the report scannable (e.g. "first 10 SSoT findings"), state it with `... and N more` so the author knows coverage isn't complete.

## Example findings

A few patterns the audit commonly catches:

- **Code / spec drift** — code or in-line comments changed without syncing the spec / plan, or vice versa.
- **Stale status / progress doc** — a status banner, count, or checklist drifted from actual state in a spot no diff touches.
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
- [memory-sync][memory-sync.md]

[../bedrocks/wording-rule/BEDROCK.md]: ../bedrocks/wording-rule/BEDROCK.md
[../bedrocks/governance-scope/BEDROCK.md]: ../bedrocks/governance-scope/BEDROCK.md
[../bedrocks/reply-language/BEDROCK.md]: ../bedrocks/reply-language/BEDROCK.md
[../rules/ssot-principle/RULE.md]: ../rules/ssot-principle/RULE.md
[../rules/private-content/RULE.md]: ../rules/private-content/RULE.md
[../rules/prose-convention/RULE.md]: ../rules/prose-convention/RULE.md
[../rules/document-convention/RULE.md]: ../rules/document-convention/RULE.md
[../rules/markdown-convention/RULE.md]: ../rules/markdown-convention/RULE.md
[../rules/zh-tw-punctuation/RULE.md]: ../rules/zh-tw-punctuation/RULE.md
[memory-sync.md]: memory-sync.md
