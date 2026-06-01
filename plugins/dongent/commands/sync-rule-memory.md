---
name: sync-rule-memory
description: Sync this plugin's rule library into the current project's Claude memory. Idempotent — first run installs, later runs only update what changed in the central rules.
---

Sync this plugin's rules into the current project's Claude memory. Each rule gets a memory file at `<project-memory>/dongent_rule_<rule-name>.md`. The file follows the standard Claude memory format, with a plugin-managed region delimited by HTML markers (`<!-- dongent-section-start -->` / `<!-- dongent-section-end -->`). The frontmatter is regenerated each sync. The body has two zones: inside the markers, content is refreshed from the current `RULE.md` and merged with any compatible existing modifications (no blind overwrites); outside the markers (H1, intro, project-specific notes) is preserved as-is by default. Either zone, any conflict with the updated rule surfaces to the user for trade-off resolution — sync doesn't overwrite without consent. Outside of sync runs, this is a normal Claude memory; agents may update it as they would any memory.

## Steps

> **Per-rule atomicity**: each rule is processed independently across the steps below. If any step fails for a specific rule (e.g. `RULE.md` unreadable, project memory write fails), stop and report — don't write partial state for the failing rule. Rules completed earlier in the same run stay on disk; the failing rule retries on the next sync.

### 1. Locate paths

- **Plugin root**: the directory containing this command file's parent (`.../<plugin-root>/commands/sync-rule-memory.md` → `<plugin-root>`). Claude Code may expose this as an environment variable when the command runs; if not, derive from the command file's own location.
- **Project memory folder**: the conventional Claude Code memory folder for the user's current project (typically `~/.claude/projects/<encoded-cwd>/memory/`). If you can't determine it, ask the user. Create the folder if it doesn't exist.

### 2. Discover rules

Read the catalog at `<plugin-root>/rules/README.md` — it's the canonical list of rules (folder name + tier + summary). Each catalogued rule corresponds to a subfolder under `<plugin-root>/rules/` containing a `RULE.md`.

### 3. Decide which rules to sync, then skip / create / update each

Tier (from the catalog loaded in step 2) controls default install behavior:

- **`recommended`**: always sync this rule into the current project.
- **`optional`**: only sync if (a) the user has previously opted in (a compiled memory file already exists for this rule in this project), or (b) the user explicitly named this rule when invoking the command. **Don't prompt mid-run** — uninstalled optional rules surface in the report (step 7).

For each rule that should be synced:

1. Compute the SHA-256 hash of its `RULE.md` content (hex).
2. Check whether `<project-memory>/dongent_rule_<rule-name>.md` exists.
   - Doesn't exist → **create** (step 4)
   - Exists and `metadata.dongent.source_hash` matches the computed hash → **skip**, report as unchanged
   - Exists but hash differs → **update** (step 4)

**Reverse check (upstream orphans):** scan the project memory folder for files matching `dongent_rule_*.md`. For each, verify the corresponding rule still exists under `<plugin-root>/rules/`. If not → the rule was removed upstream. List it in the report (step 7); don't auto-delete, since the file may contain project-specific customizations the user still values.

### 4. Resolve Prerequisites (if any)

Read `RULE.md` for a `## Prerequisites` section. Prerequisites are anything that must be gathered before the compiled memory can be written — they can be questions for the user, agent-side detections (e.g. scan project files, check for a specific tool), or a mix.

- Absent: nothing to resolve. The compiled memory will end at the `dongent-section-end` marker (no below-marker content).
- Present, first-time install: work through each item — ask the user for inputs the user must provide; run detections the agent can do directly.
- Present, update: re-resolve items new since the last sync. Also check existing body content — both inside and outside the markers — against the updated rule. If anything is stale or conflicting (e.g. a Prerequisite was reworded, an answer no longer fits the new rule's shape, custom notes contradict the updated logic, or existing marker content diverges from the latest distillation), flag it in the same batch round-trip and let the user decide the trade-off: accept the new rule (revise / discard the conflicting content) or keep what's there (and note the divergence). Merge compatible existing content into the refreshed version where possible; don't auto-overwrite without consent.

**Batch all user-facing questions for the same rule into one round-trip — don't go question-by-question.**

When organizing results in the compiled memory, write them **below the `dongent-section-end` marker**. The agent picks the section heading(s) freely — name them to fit the content (e.g. `## Project settings`, `## Detected tooling`, or any domain-specific label that suits).

### 5. Write the compiled memory file

Write the compiled memory in English by default, regardless of the conversation language — it mirrors the English rule library, and one consistent language keeps it portable.

Apply [ssot-principle][../rules/ssot-principle/RULE.md] across the project's memory, not only within each file: the template below already points each file at its canonical `RULE.md` rather than copying it; on top of that, this compiled file is the canonical home for its rule's guidance, so any other memory file covering the same ground references it instead of restating, and cross-file duplication is removed.

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

> Below this marker: project-specific space (Prerequisites answers, custom notes, etc.) — preserved across syncs. Use whatever section headings fit the content; omit entirely if there's nothing project-specific.
```

- **Create**: write the whole file. Agent chooses the H1 title and intro. Fill the canonical pointer and the summary inside the `dongent-section-*` markers. Below the end marker, add Prerequisites answers (with section names you choose), or leave empty if nothing project-specific.
- **Update**: bump `metadata.dongent.source_hash` and refresh `description` if the central `RULE.md`'s description changed. Preserve `metadata.originSessionId` (immutable after creation). Apply step 4's resolutions to the body — inside the markers gets the refreshed distillation merged with any preserved existing content; outside the markers stays as-is plus any user-approved appends, modifications, or removals.

### 6. Update MEMORY.md index

In the project memory folder, ensure `MEMORY.md` exists. For each created or updated compiled file, ensure there's an index entry of the form:

```
- [dongent_rule_<rule-name>](dongent_rule_<rule-name>.md) — <description from frontmatter>
```

Don't duplicate; if an entry already exists for the same name, update its description if it changed but otherwise leave it.

### 7. Report

Summarize per rule:

- ✨ Created: list rule names with their compiled file paths; include any Prerequisites resolved during creation (e.g. "3 Prerequisites resolved")
- 🔄 Updated: list rule names with a one-line note on what changed (e.g. "central RULE.md updated; 2 new Prerequisites resolved")
- ✅ Unchanged: list rule names skipped (sync'd previously, hash matches central)
- 📦 Available (not installed): list optional rules the user hasn't opted into yet
- 👻 Orphan (rule removed upstream): list project memory files whose corresponding rule no longer exists in the plugin; user can decide whether to clean them

If something was unclear (couldn't locate the plugin root, couldn't determine the project memory folder, ambiguous file conflicts, etc.) — stop and ask the user instead of guessing.

## References

- [ssot-principle][../rules/ssot-principle/RULE.md]

[../rules/ssot-principle/RULE.md]: ../rules/ssot-principle/RULE.md
