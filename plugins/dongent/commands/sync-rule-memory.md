---
name: sync-rule-memory
description: Sync this plugin's rule library into the current project's agent memory — one foundational memory file holding all rules. Idempotent — first run installs, later runs only update what changed in the central rules.
---

Sync this plugin's rules into the current project's agent memory. All rules — and the bedrocks they build on — compile into **one** file, `<project-memory>/<plugin-name>-plugin-managed-rules.md` (one per plugin). Each **source** — a rule or bedrock — is a single H2 section, ordered bedrocks first then rules per the plugin catalog, headed by its name (e.g. `ssot-principle`); its canonical path lives in the frontmatter. This file is foundational and read-first.

The **frontmatter** is plugin-managed — a `description` and the `sources` list. In the **body**, each H2 wraps a one-line distillation in `<!-- dongent-section-start -->` / `<!-- dongent-section-end -->` markers, with project-specific lines below them. Sync maintains the frontmatter and the inside-marker distillations and preserves what sits below the markers — both the managed and the project-specific content matter, and neither is discarded recklessly. The steps below cover how each is written and how conflicts resolve; outside of sync runs this is a normal agent memory, and agents edit below the markers as they would any memory.

## Read first

MUST read these first — this command relies on them:

- [wording-rule][../bedrocks/wording-rule/BEDROCK.md]
- [governance-scope][../bedrocks/governance-scope/BEDROCK.md]
- [ssot-principle][../rules/ssot-principle/RULE.md]
- [private-content][../rules/private-content/RULE.md]

## Steps

> **Per-source atomicity**: each source is processed independently across the steps below. If any step fails for a source (e.g. `RULE.md` unreadable, file write fails), stop and report — don't write partial state for that source's section; leave its existing section intact. Sources handled earlier in the same run keep their updated sections; the failing source retries on the next sync.

### 1. Locate paths

- **Plugin root**: the directory containing this command file's parent (`.../<plugin-root>/commands/sync-rule-memory.md` → `<plugin-root>`). It may be exposed as an environment variable when the command runs; otherwise derive it from this command file's own location.
- **Project memory folder**: the conventional agent-memory folder for the current project (e.g. Claude Code's `~/.claude/projects/<encoded-cwd>/memory/` → `<project-memory>`). If it can't be determined, ask the user. Create the folder if it doesn't exist.
- **Memory file**: this plugin's single compiled file, `<project-memory>/<plugin-name>-plugin-managed-rules.md` — `<plugin-name>` is the plugin's name — usually the `<plugin-root>` folder name above. Create it if absent; everything below is written into this one file.

### 2. Discover sources and decide what to sync

Read the catalog at `<plugin-root>/rules/README.md` — the canonical list of rules (folder name + tier + summary); each catalogued rule is a subfolder under `<plugin-root>/rules/` containing a `RULE.md`. The tier decides default install behavior:

- **`required`**: always sync this rule into the current project.
- **`optional`**: only sync if (a) the user has previously opted in (this rule already has a `sources` entry), or (b) the user explicitly named this rule when invoking the command. **Don't prompt mid-run** — uninstalled optional rules surface in the report (step 8).

Then parse each rule's `## Builds on` to resolve its transitive closure (follow the chain, dedupe by path, sort by path) — the path-ordered list step 3 hashes. A **bedrock** enters the file only when some synced rule builds on it (transitively) — pulled in as a **`required`** source, no tier or opt-in. The file's sources are the deduped union of those closures, laid out in **catalog order** — bedrocks then rules as `bedrocks/README.md` and `rules/README.md` list them (not the hash's path sort). This is the order of the `sources` list and the H2 sections.

### 3. Create, skip, or update each (by source hash)

A source's **source hash** (hex SHA-256) covers its step-2 closure: concatenate each file's content `sha256` in the closure's path order, then `sha256` that. With no `## Builds on`, the closure is just the source's own file. The outer `sha256` keeps it a fixed 64 hex chars however large the closure.

Hash each file's **content**, not its own source hash — so nothing needs syncing first; the closure is gathered by reading files directly. Transitive coverage matters because distilling a rule reads what it builds on, so a deep dependency can still shape the summary. Example — `R` builds on `R1`, and `R1` builds on `R2`: `source_hash(R) = sha256( sha256(R) + sha256(R1) + sha256(R2) )` (here the files' path order happens to be `R`, `R1`, `R2`). `R2` sits in `R`'s closure, so editing `R2` can change `R`'s own distilled summary — that summary can lean on what `R` builds on, transitively down to `R2` — so folding `R2`'s content into `R`'s hash re-distills `R`, even though `R`'s `RULE.md` is untouched. (Base rules and bedrocks rarely change, so such cascades stay uncommon.)

For each source from step 2:

1. Compute its source hash.
2. Look up the source by name — its entry in the frontmatter `sources` list and its H2 section in the body.
   - No section → **create** the section (step 4)
   - Section exists and the recorded `hash` matches → **skip**, report as unchanged
   - Section exists but the hash differs → **update** the section (step 4)

**Reverse check (upstream orphans):** scan the `sources` list (and the body's H2 sections) for an entry whose source no longer exists upstream. If any → it was removed upstream. List it in the report (step 8); don't auto-delete, since the section might hold project-specific content below its markers that the user still values.

### 4. Resolve Prerequisites (if any)

Read `RULE.md` for a `## Prerequisites` section. Prerequisites are anything that needs to be gathered before the compiled memory can be written — they can be questions for the user, agent-side detections (e.g. scan project files, check for a specific tool), or a mix.

- Absent: nothing to resolve from Prerequisites. Unless the project has overrides to record (step 5), the source's section is just its distillation inside the markers.
- Present, first-time install: work through each item — ask the user for inputs the user needs to provide; run detections the agent can do directly.
- Present, update: re-resolve items new since the last sync, and check existing body content — both inside and outside the markers — against the updated rule. Resolve conflicts (a reworded Prerequisite, an answer that no longer fits, project overrides or custom notes contradicting the updated logic, marker content diverging from the latest distillation) using judgment — merge compatible content, re-align stale text, take the updated rule where it clearly supersedes — and report each fix in step 8. Escalate only when the conflict is genuinely undecidable: resolving would discard project-specific content whose intent can't be confirmed, or two readings are equally defensible. NEVER silently discard user content — when unsure, keep it and flag the divergence.

**Batch all user-facing questions for the same rule into one round-trip — don't go question-by-question.**

Resolved results that are project-specific go below the source's `<!-- dongent-section-end -->` marker (before the next H2) as one-line `- **key**: …` entries — the content itself, or (per step 5) pointers to its canonical home(s) elsewhere; several can share one line. Pick a fitting bold key per line (e.g. `prerequisite`, `project override`, `custom notes`, `detected tooling`); don't add new H2 (reserved for source names), and use H3 only where a section genuinely needs sub-structure.

### 5. Plan each fact's canonical home across memory

Apply [ssot-principle][../rules/ssot-principle/RULE.md] across the project's memory, not only within this file: each source's `path` already points at its `RULE.md` / `BEDROCK.md` rather than copying it; on top of that, a source's H2 section is the canonical home for its rule's guidance, so any other memory file covering the same ground references it instead of restating, and cross-file duplication is removed.

The same discipline covers the rule's project-specific variants (a team-style override, a local specialization). Memory is the agent-facing index: a variant's home is wherever it's actually maintained — often a human-readable place, not memory — so the section points to that home rather than holding it, and becomes the home itself only when there's none outside memory. Either way, the section stays this rule's single index — recording, for each variant, where it lives and which authority finally applies. Slice by slice — locate where each is actually maintained (search the repo and committed docs; don't assume this file is its home), and match it by what it governs (not its label):

- **Maintained outside memory** → that file is its canonical home (per [ssot-principle][../rules/ssot-principle/RULE.md]); point straight to it from the source's section, don't copy it in. This covers a config a program reads (the file itself, not a doc that describes one), or — per [private-content][../rules/private-content/RULE.md] — a team-owned doc (team-committed, review-gated) or the author's own gitignored notes or drafts.
- **Only in memory, or with no home yet** (scattered across memory files, or surfaced in-session) → if it's **tightly bound to this one rule**, add it below that rule's markers as a one-line entry (or merge into a matching one), leaving a pointer in any memory file it was pulled from. Content **not specific to one rule** (e.g. a project convention, a user reminder, or feedback — whether spanning several rules or covered by none) is out of this command's scope: leave it alone. Only where it already lives in a memory file and bears on this rule, point to it from the source's section.

**Keep this file lean.** It loads whole when recalled, so its budget is total size (content, not line count): distil to a line. When a source's below-marker content genuinely grows, move the bulky parts to their own memory file and leave a one-line pointer; what each sync re-derives — the distillation and the Prerequisites answers — stays in the section. That split-out file is ordinary project memory, not plugin-managed: name it `<plugin-name>_<source-name>_<topic>` so its origin stays traceable, give it standard memory frontmatter (`type: feedback`, matching the rest of the rule memory), point it back at the source's section, and index it in `MEMORY.md`. Judge by relevance and size, and prune as the rules evolve.

### 6. Write the compiled memory file

Write the compiled memory in English by default, regardless of the conversation language — it mirrors the English rule library, and one consistent language keeps it portable.

Template — follow it as written: reproduce everything verbatim except inline `<placeholders>` (slot-fills) and lines starting with `>` (hints describing what to write in that block). It shows one source's section; append one H2 per remaining source in the same shape.

```markdown
---
name: <plugin-name>-plugin-managed-rules
description: Foundational <plugin-name> rules; canonical home of <the source names in `sources` order, comma-separated, kept in sync with `sources`>. MUST be read when writing or reviewing ANY artifact.
metadata:
  node_type: memory
  type: feedback
  dongent:
    sources:
      - name: ssot-principle
        path: dongent/rules/ssot-principle/RULE.md
        hash: <hex source hash; see step 3>
      # … one entry per source
---

# <human-readable title, e.g. "dongent — foundational rules">

This is `<plugin-name>`'s foundational rule memory. Each H2 is a source's name; its canonical path — resolved within the installed plugin — is in the matching `sources` entry. Inside a source's markers sits its distilled rule; the lines below are project-specific.

## ssot-principle

<!-- dongent-section-start -->

> One line distilling the rule: what to do, when. Don't reproduce algorithms or examples — the canonical source (its `path`) holds the full text.

<!-- dongent-section-end -->

- **prerequisite**: <one line — resolved Prerequisites answer, if the rule has any>
- **project-specific**: <one line — a tightly-bound override or note>
- **external links**: <one line — pointers to canonical home(s) elsewhere, per step 5>
```

A bedrock's section takes the same shape but has no Prerequisites; a source with no project-specific content has nothing below its markers.

- **Create the file**: write the frontmatter and one H2 per source, each with its distillation inside the markers and any project-specific lines below.
- **Add a source**: insert its H2 and `sources` entry at its place in the step-2 order; leave the other sources untouched.
- **Update a source** (already synced): bump its `hash` in `sources`, re-distill inside its markers, and apply step 4's resolutions to the lines below; leave other sources untouched.

### 7. Update MEMORY.md index

In the project memory folder, ensure `MEMORY.md` exists with a single index entry for this file, placed **first** (it's foundational, read before any authoring or review). This line is what an agent scans to decide whether to load the file; use the file's frontmatter `description` verbatim as its summary — one canonical wording, refreshed here whenever that `description` changes:

```
- [<plugin-name>-rules](<plugin-name>-plugin-managed-rules.md) — <the file's `description`, verbatim>
```

### 8. Report

Group by status — under each bucket, list the sources that fall in it (one line each); omit empty buckets:

- ✨ **Created** — source name, plus any project-specific content captured.
- 🔄 **Updated** — source name + what changed (distillation re-distilled, conflicts auto-resolved, project-specific content revised).
- ✅ **Unchanged** — source name skipped (hash matches central).
- 📦 **Available (not installed)** — optional rules not yet opted into.
- 👻 **Orphan (removed upstream)** — sections whose source is gone upstream; the user decides whether to clean — NEVER auto-delete, the section may hold project content below its markers.
- 🗑️ **Emptied (delete candidate)** — a section left holding only outward pointers after this sync and referenced by nothing else; list it for the user to confirm removal — NEVER auto-delete.

## Out of scope

Reconciling the rest of project memory — beyond the rules this command syncs (step 5) — is out of scope; run [check-consistency][check-consistency.md] in `--memory` mode for that, and [compact-checkpoint][compact-checkpoint.md] to land session-surfaced facts in memory.

## References

- [wording-rule][../bedrocks/wording-rule/BEDROCK.md]
- [governance-scope][../bedrocks/governance-scope/BEDROCK.md]
- [ssot-principle][../rules/ssot-principle/RULE.md]
- [private-content][../rules/private-content/RULE.md]
- [check-consistency][check-consistency.md]
- [compact-checkpoint][compact-checkpoint.md]

[../bedrocks/wording-rule/BEDROCK.md]: ../bedrocks/wording-rule/BEDROCK.md
[../bedrocks/governance-scope/BEDROCK.md]: ../bedrocks/governance-scope/BEDROCK.md
[../rules/ssot-principle/RULE.md]: ../rules/ssot-principle/RULE.md
[../rules/private-content/RULE.md]: ../rules/private-content/RULE.md
[check-consistency.md]: check-consistency.md
[compact-checkpoint.md]: compact-checkpoint.md
