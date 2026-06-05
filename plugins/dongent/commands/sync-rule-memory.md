---
name: sync-rule-memory
description: Sync this plugin's rule library into the current project's agent memory. Idempotent — first run installs, later runs only update what changed in the central rules.
---

Sync this plugin's rules into the current project's agent memory. Each rule gets a memory file at `<project-memory>/dongent_rule_<rule-name>.md`. The file follows the standard Claude memory format, with a plugin-managed region delimited by HTML markers (`<!-- dongent-section-start -->` / `<!-- dongent-section-end -->`).

The frontmatter is refreshed on each create or update. The body has two zones: inside the markers, plugin-managed content compiled from the current `RULE.md`; outside them, project-specific content that persists across syncs. The steps below cover how each zone is written and how conflicts are resolved. Outside of sync runs, this is a normal Claude memory; agents may update it as they would any memory.

## Steps

> **Per-rule atomicity**: each rule is processed independently across the steps below. If any step fails for a specific rule (e.g. `RULE.md` unreadable, project memory write fails), stop and report — don't write partial state for the failing rule. Rules completed earlier in the same run stay on disk; the failing rule retries on the next sync.

### 1. Locate paths

- **Plugin root**: the directory containing this command file's parent (`.../<plugin-root>/commands/sync-rule-memory.md` → `<plugin-root>`). Claude Code may expose this as an environment variable when the command runs; if not, derive from the command file's own location.
- **Project memory folder**: the conventional Claude Code memory folder for the user's current project (typically `~/.claude/projects/<encoded-cwd>/memory/`). If it can't be determined, ask the user. Create the folder if it doesn't exist.

### 2. Discover rules

Read the catalog at `<plugin-root>/rules/README.md` — it's the canonical list of rules (folder name + tier + summary). Each catalogued rule corresponds to a subfolder under `<plugin-root>/rules/` containing a `RULE.md`.

### 3. Decide which rules to sync, then skip / create / update each

Tier (from the catalog loaded in step 2) controls default install behavior:

- **`recommended`**: always sync this rule into the current project.
- **`optional`**: only sync if (a) the user has previously opted in (a compiled memory file already exists for this rule in this project), or (b) the user explicitly named this rule when invoking the command. **Don't prompt mid-run** — uninstalled optional rules surface in the report (step 8).

For each rule that should be synced:

1. Compute the SHA-256 hash of its `RULE.md` content (hex).
2. Check whether `<project-memory>/dongent_rule_<rule-name>.md` exists.
   - Doesn't exist → **create** (step 4)
   - Exists and `metadata.dongent.source_hash` matches the computed hash → **skip**, report as unchanged
   - Exists but hash differs → **update** (step 4)

**Reverse check (upstream orphans):** scan the project memory folder for files matching `dongent_rule_*.md`. For each, verify the corresponding rule still exists under `<plugin-root>/rules/`. If not → the rule was removed upstream. List it in the report (step 8); don't auto-delete, since the file may contain project-specific customizations the user still values.

### 4. Resolve Prerequisites (if any)

Read `RULE.md` for a `## Prerequisites` section. Prerequisites are anything that must be gathered before the compiled memory can be written — they can be questions for the user, agent-side detections (e.g. scan project files, check for a specific tool), or a mix.

- Absent: nothing to resolve from Prerequisites. Unless the project has overrides to record (step 5), the compiled memory ends at the `dongent-section-end` marker.
- Present, first-time install: work through each item — ask the user for inputs the user must provide; run detections the agent can do directly.
- Present, update: re-resolve items new since the last sync, and check existing body content — both inside and outside the markers — against the updated rule. Resolve conflicts (a reworded Prerequisite, an answer that no longer fits, project overrides or custom notes contradicting the updated logic, marker content diverging from the latest distillation) using judgment — merge compatible content, re-align stale text, take the updated rule where it clearly supersedes — and report each fix in step 8. Escalate only when the conflict is genuinely undecidable: resolving would discard project-specific content whose intent can't be confirmed, or two readings are equally defensible. Never silently discard user content — when unsure, keep it and flag the divergence.

**Batch all user-facing questions for the same rule into one round-trip — don't go question-by-question.**

Resolved results that are project-specific go below the `dongent-section-end` marker — the content itself, or (per step 5) a pointer to its canonical home elsewhere. The agent picks the section heading(s) freely — name them to fit the content (e.g. `## Project overrides`, `## Custom notes`, `## Detected tooling`, or any domain-specific label that suits).

### 5. Plan each fact's canonical home across memory

Apply [ssot-principle][../rules/ssot-principle/RULE.md] across the project's memory, not only within each file: the template in step 6 already points each file at its canonical `RULE.md` rather than copying it; on top of that, this compiled file is the canonical home for its rule's guidance, so any other memory file covering the same ground references it instead of restating, and cross-file duplication is removed.

The same discipline covers the rule's project-specific variants (a team-style override, a local specialization). Memory is the agent-facing index: a variant's home is wherever it's actually maintained — often a human-readable place, not memory — so this file points to that home, and becomes the home itself only when there's none outside memory — staying the single index of where each variant lives and which authority finally applies. Slice by slice — locate where each is actually maintained (search the repo and committed docs; don't assume the memory file it sits in is its home), and match it by what it governs (not its label):

- **Maintained outside memory** → that file is its canonical home (per ssot-principle); point straight to it from here, don't copy it in. This covers a config a program reads (the file itself, not a doc that describes one), or — per [private-content][../rules/private-content/RULE.md] — a team-owned doc (team-committed, review-gated) or the author's own gitignored notes or drafts.
- **Only in memory, or with no home yet** (scattered across memory files, or surfaced in-session) → consolidate it below the markers here, this rule's single memory home, leaving a pointer in any memory file it was pulled from. Don't over-consolidate: a slice under no rule stays where it is.

### 6. Write the compiled memory file

Write the compiled memory in English by default, regardless of the conversation language — it mirrors the English rule library, and one consistent language keeps it portable.

Template — inline `<placeholders>` are slot-fills (replace with the actual value); lines starting with `>` are hints describing what to write in that block (replace the whole block with actual content):

```markdown
---
name: dongent_rule_<rule-name>
description: <one-line description of when the agent should load this memory; distill from the central RULE.md's frontmatter description>
metadata:
  node_type: memory
  type: feedback
  originSessionId: <Claude session id when this memory was first created — set on create, preserved on update>
  dongent:
    source: dongent/rules/<rule-folder-name>
    source_hash: <sha256 of central RULE.md content>
---

# <human-readable title, e.g. "zh-TW doc punctuation">

> Short intro: describe this memory's purpose; mention that part of its content is inherited from a plugin rule.

<!-- dongent-section-start -->

Canonical: `dongent/rules/<rule-folder-name>/RULE.md` in the installed dongent plugin — resolve under the plugin's current install root, not a hard-coded path (the cache keeps per-version dirs; use the active install, which Claude Code's installed-plugin record designates).

> 2-5 lines distilling the rule from RULE.md: what to do, when. Don't reproduce algorithms or examples — point at the canonical RULE.md for full text.

<!-- dongent-section-end -->

> Below this marker: the project-specific content — Prerequisites answers, project overrides, custom notes. Use whatever section headings fit it; omit entirely if there's none.
```

- **Create**: write the whole file. Agent chooses the H1 title and intro. Fill the canonical pointer and the summary inside the `dongent-section-*` markers, and any project-specific content below them.
- **Update**: bump `metadata.dongent.source_hash` and refresh `description` if the central `RULE.md`'s description changed. Preserve `metadata.originSessionId` (immutable after creation). Re-distill the inside-marker content from the updated `RULE.md`, then apply step 4's resolutions to the body.

### 7. Update MEMORY.md index

In the project memory folder, ensure `MEMORY.md` exists, and for each created or updated compiled file, ensure there's an index entry of the form:

```
- [dongent_rule_<rule-name>](dongent_rule_<rule-name>.md) — <concise one-line summary: what it is, when to load>
```

These index lines are what an agent scans to decide what to load, so distil each summary tightly rather than pasting the frontmatter. Don't duplicate; refresh an entry's summary when the rule changes, otherwise leave it.

### 8. Report

Summarize per rule:

- ✨ Created: rule name + compiled file path, plus any project-specific content captured
- 🔄 Updated: rule name + a one-line note on what changed (e.g. `RULE.md` refreshed, conflicts auto-resolved, project-specific content revised)
- ✅ Unchanged: rule name skipped (hash matches central)
- 📦 Available (not installed): optional rules not yet opted into
- 👻 Orphan (rule removed upstream): memory files whose rule is gone upstream; user decides whether to clean
- 🗑️ Emptied (delete candidate): a memory file left holding only outward pointers after this sync and referenced by nothing else — list it for the user to confirm deletion; never auto-delete

## Out of scope

Reconciling the rest of project memory — beyond the rules this command syncs (step 5) — is out of scope; run [check-consistency][check-consistency.md] in `--memory` mode for that.

## References

- [ssot-principle][../rules/ssot-principle/RULE.md]
- [private-content][../rules/private-content/RULE.md]
- [check-consistency][check-consistency.md]

[../rules/ssot-principle/RULE.md]: ../rules/ssot-principle/RULE.md
[../rules/private-content/RULE.md]: ../rules/private-content/RULE.md
[check-consistency.md]: check-consistency.md
