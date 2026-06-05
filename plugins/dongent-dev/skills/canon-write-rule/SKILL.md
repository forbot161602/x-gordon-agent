---
name: canon-write-rule
description: Use when authoring or editing a rule definition — a RULE.md, its frontmatter or body, or a sibling supplementary doc. A RULE.md is a shared rule an agent references when running a skill or command, mostly for dongent-style rule libraries (a canon/rules or plugins/*/rules layout). Applies the conventions for writing rules themselves. Fires on prompts such as "write a RULE.md", "add a rule to the library", or "edit a shared rule". Do NOT use for general Markdown or docs that aren't a rule definition.
---

# Writing a canon rule

Conventions for authoring a rule definition in a dongent-style rule library. A `RULE.md` is a shared rule that must stay consistent and portable, so beyond the conventions here it still obeys the library's base rules, which ship in the `dongent` plugin (a declared dependency of this one):

- [ssot-principle][dongent/rules/ssot-principle/RULE.md]
- [private-content][dongent/rules/private-content/RULE.md]
- [prose-convention][dongent/rules/prose-convention/RULE.md]
- [markdown-convention][dongent/rules/markdown-convention/RULE.md]

This skill adds only what is specific to writing rules themselves.

## Structure

### Frontmatter

`name` and `description` are required:

- **`name`** — kebab-case, matching the rule's folder name; keep it simple and precise.
- **`description`** — a one-line summary of what the rule governs; a domain rule also names the base rules it builds on.

### Sections

Follow the section shape of the sibling `RULE.md` files in the same library rather than inventing one — typically `## Rule`, `## When to apply`, `## How to apply`, `## Out of scope`, `## References`, plus `## Prerequisites` or domain-specific sections where the rule needs them. This is the style-consistency facet applied to rule files (per [ssot-principle][dongent/rules/ssot-principle/RULE.md]).

## File shape

- `RULE.md` (ALL-CAPS) is the canonical rule — the file an agent reads first. Keep it concise and on-topic — only what the rule itself needs.
- Long supplementary material (full algorithms, rationale, large examples) goes in a separate Initial-Cap doc beside it (e.g. `Specification.md` or `Design-Rationale.md`).
- Helpers such as scripts, templates, fixtures are lowercase. Pair any logic-carrying file with a test (e.g. `helper.py` and `helper_test.py`) so its behaviour stays verifiable.
- Group files of the same kind or purpose into a subfolder (e.g. `references/`, `scripts/`) once they grow numerous and interdependent.

## Cross-rule references

Two conventions govern how one rule points at another:

- **Express reuse in prose, not a special syntax.** When a rule builds on another, say so in words plus a reference — don't invent an inheritance field (e.g. an `extends:` in frontmatter). The verb marks the degree: `inherits from` / `building on` (wholesale) vs `shares` / `follows` (selective).
- **Link only to a base** (a rule this one obeys or builds on) — a reference-style link, per [markdown-convention][dongent/rules/markdown-convention/RULE.md]. Cross-reference a non-base only when truly needed: plain text or inline code, not a link. E.g. `pr-convention` links its base `commit-convention`, not the reverse.

## Out of scope

- Product or application code, and a plugin's non-rule parts (agents, skills, commands) — this skill is about `RULE.md` only.
- The base rules themselves — not restated here; e.g. keep the body self-contained — generic example paths (`docs/`, `tests/`), per [prose-convention][dongent/rules/prose-convention/RULE.md]; private detail described generically, per [private-content][dongent/rules/private-content/RULE.md].
- Compiling a rule into project memory — that's the [sync-rule-memory][dongent/commands/sync-rule-memory.md] command, run later; this skill covers write-time authoring only.

## References

- [ssot-principle][dongent/rules/ssot-principle/RULE.md]
- [private-content][dongent/rules/private-content/RULE.md]
- [prose-convention][dongent/rules/prose-convention/RULE.md]
- [markdown-convention][dongent/rules/markdown-convention/RULE.md]
- [sync-rule-memory][dongent/commands/sync-rule-memory.md]

[dongent/rules/ssot-principle/RULE.md]: dongent/rules/ssot-principle/RULE.md
[dongent/rules/private-content/RULE.md]: dongent/rules/private-content/RULE.md
[dongent/rules/prose-convention/RULE.md]: dongent/rules/prose-convention/RULE.md
[dongent/rules/markdown-convention/RULE.md]: dongent/rules/markdown-convention/RULE.md
[dongent/commands/sync-rule-memory.md]: dongent/commands/sync-rule-memory.md
