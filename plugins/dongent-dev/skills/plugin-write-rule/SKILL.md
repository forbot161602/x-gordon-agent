---
name: plugin-write-rule
description: Use when authoring or editing a rule definition — a RULE.md, its frontmatter or body, or a sibling supplementary doc. A RULE.md is a shared rule an agent references when running a skill or command, mostly for dongent-style rule libraries (a plugins/*/rules layout). Applies the conventions for writing rules themselves. Fires on prompts such as "write a RULE.md", "add a rule to the library", or "edit a shared rule". Do NOT use for general Markdown or docs that aren't a rule definition.
---

# Writing a rule

Conventions for authoring a rule definition in a dongent-style rule library — what's specific to writing rules themselves, beyond the base rules every rule obeys.

## Builds on

MUST read and follow these first — this skill builds on them; they ship in the `dongent` plugin (a declared dependency of this one):

- [wording-rule][plugin:dongent/bedrocks/wording-rule/BEDROCK.md]
- [ssot-principle][plugin:dongent/rules/ssot-principle/RULE.md]
- [private-content][plugin:dongent/rules/private-content/RULE.md]
- [prose-convention][plugin:dongent/rules/prose-convention/RULE.md]
- [document-convention][plugin:dongent/rules/document-convention/RULE.md]
- [markdown-convention][plugin:dongent/rules/markdown-convention/RULE.md]

## Structure

### Frontmatter

`name` and `description` are REQUIRED:

- **`name`** — kebab-case, matching the rule's folder name; keep it simple and precise.
- **`description`** — a one-line summary of what the rule governs. Dependencies aren't listed here — they go in `## Builds on`.

### Sections

Use the sections the sibling `RULE.md` files use rather than inventing new ones — this list is both the whitelist and the order: `## Builds on`, `## Rule`, `## When to apply`, `## How to apply`, `## Out of scope`, `## References`. `## Prerequisites` (when the rule needs it) sits after `## How to apply`; add domain-specific sections only where genuinely needed. This is the style-consistency facet applied to rule files (per [ssot-principle][plugin:dongent/rules/ssot-principle/RULE.md]).

### Builds on

When a rule has upstream dependencies — base rules or bedrocks it builds on — declare them in a `## Builds on` section (also the source for hash-dependency tracking):

- Lead with `MUST read and follow these first — this rule builds on them:`, then reference-style links — **bedrocks first, then rules by importance**.
- [wording-rule][plugin:dongent/bedrocks/wording-rule/BEDROCK.md] always leads — every rule is read under its **unmarked-defaults-to-MUST** convention.
- **Pure links, no descriptions** — each dependency's summary lives in its own frontmatter; restating it here drifts.
- **No special field** — dependencies live in this section, not an invented frontmatter field (e.g. an `extends:`).

### Prerequisites

A `## Prerequisites` section lists what must be resolved before the rule can be applied — information the user provides or the agent detects on its own. It differs from `## Builds on`: Prerequisites is per-project preconditions to resolve, while Builds on is the static upstream rules and bedrocks read first. Omit it when the rule has no preconditions.

## File shape

Layered on [document-convention][plugin:dongent/rules/document-convention/RULE.md]'s File shape; a rule folder adds these role tiers:

- `RULE.md` (ALL-CAPS) is the canonical rule — the file an agent reads first. Keep it concise and on-topic — only what the rule itself needs.
- Long supplementary material (full algorithms, rationale, large examples) goes in a separate Initial-Cap doc beside it (e.g. `Specification.md` or `Design-Rationale.md`).
- Helpers such as scripts, templates, fixtures are lowercase. Pair any logic-carrying file with a test (e.g. `helper.py` and `helper_test.py`) so its behaviour stays verifiable.

## Out of scope

- Product or application code, and a plugin's non-rule parts (agents, skills, commands) — this skill is about `RULE.md` only.
- The base rules themselves — not restated here; e.g. keep the body self-contained — generic example paths (`docs/`, `tests/`), per [prose-convention][plugin:dongent/rules/prose-convention/RULE.md]; private detail described generically, per [private-content][plugin:dongent/rules/private-content/RULE.md].
- Compiling a rule into project memory — that's the [sync-rule-memory][plugin:dongent/commands/sync-rule-memory.md] command, run later; this skill covers write-time authoring only.

## References

- [wording-rule][plugin:dongent/bedrocks/wording-rule/BEDROCK.md]
- [ssot-principle][plugin:dongent/rules/ssot-principle/RULE.md]
- [private-content][plugin:dongent/rules/private-content/RULE.md]
- [prose-convention][plugin:dongent/rules/prose-convention/RULE.md]
- [document-convention][plugin:dongent/rules/document-convention/RULE.md]
- [markdown-convention][plugin:dongent/rules/markdown-convention/RULE.md]
- [sync-rule-memory][plugin:dongent/commands/sync-rule-memory.md]

[plugin:dongent/bedrocks/wording-rule/BEDROCK.md]: plugin:dongent/bedrocks/wording-rule/BEDROCK.md
[plugin:dongent/rules/ssot-principle/RULE.md]: plugin:dongent/rules/ssot-principle/RULE.md
[plugin:dongent/rules/private-content/RULE.md]: plugin:dongent/rules/private-content/RULE.md
[plugin:dongent/rules/prose-convention/RULE.md]: plugin:dongent/rules/prose-convention/RULE.md
[plugin:dongent/rules/document-convention/RULE.md]: plugin:dongent/rules/document-convention/RULE.md
[plugin:dongent/rules/markdown-convention/RULE.md]: plugin:dongent/rules/markdown-convention/RULE.md
[plugin:dongent/commands/sync-rule-memory.md]: plugin:dongent/commands/sync-rule-memory.md
