---
name: markdown-convention
description: Markdown authoring conventions (tables, links, references); defaults for private content, deferring to nearby team style for public content.
---

# Markdown conventions — authoring mechanics

Markdown-specific mechanics, layered on the foundations in [Builds on][builds-on].

## Builds on

MUST read and follow these first — this rule builds on them:

- [wording-rule][../../bedrocks/wording-rule/BEDROCK.md]
- [ssot-principle][../ssot-principle/RULE.md]
- [private-content][../private-content/RULE.md]
- [prose-convention][../prose-convention/RULE.md]

## Rule

The conventions below are **defaults** — for public content, the team style observed in nearby files takes precedence where it exists; see [How to apply][how-to-apply] for the cascade.

### Frontmatter

- Frontmatter is OPTIONAL; when present, it MUST be valid YAML. A plain scalar can't contain `": "` (a colon followed by a space) — it breaks parsing and rendering (e.g. GitHub). Reword to remove the colon, or double-quote the whole value when the colon needs to stay.

### Tables

- Precede every table with `<!-- prettier-ignore -->` on its own line so a formatter (prettier, editor format-on-save) won't reflow it; re-check tables after a format pass.
- Write tables in compact form — `|---|` separators, single-space cells, no alignment padding. Convert existing padded tables to compact.

### Links

- Reference a file, document, or section with Markdown link syntax (`[link text](path)` or `[link text][id]`), not a bare path or plain prose.
- For a reference-style link to a file or doc, the `id` MUST be the **relative path** to the target — the same string as the link's destination (e.g. `../ssot-principle/RULE.md`, or a sibling's `config.yaml`). It's derived from the path — there's no name to invent, and none to keep consistent across files — so a rename is a clean grep of the path, and it needs no repo-root assumption. For an in-document section, the `id` is the heading's anchor slug.
- On a rename or move, update every link to the target so none goes stale — [ssot-principle][../ssot-principle/RULE.md]'s consistency facet, applied to links.

### Inline code

- Mention a filename or path in inline code (`README.md`, `docs/`), not bare prose — to reference it, use a [link][links] instead.
- Exception: a frontmatter `description` (e.g. on a skill, command, or agent doc) stays plain — a filename in it takes no backticks (house style).

### References

- Collect every reference-style link's `[id]: target` definition at the bottom of the document — each target written once.
- If the document cites external sources (files, docs, URLs), put a `## References` heading above those definitions with a visible bullet list of them, so the section isn't empty when rendered. Internal `#` section anchors are navigation, not citations: defined, but not in the visible list.
- Keep both in sync with the links actually used — no unused definitions, none missing.

## When to apply

When writing or editing any markdown document. Also a pre-publish checkpoint: re-check each convention before declaring work done.

## How to apply

- **Before writing**, place the document by layer ([private-content][../private-content/RULE.md]). Private content applies the conventions directly; public content follows this priority cascade, judged per convention independently:
  1. The team style observed in nearby files — read 2-3 of them (sibling files, the same-folder README, a docs/ index) and defer to what they do (inline links, spread-out tables, no prettier-ignore are all respected).
  2. Fall back to the conventions above — only where no team style emerges, or for a brand-new file with no nearby files to read.
- **Before publishing**, the agent re-checks each convention against whichever source won its cascade; fix anything flagged.

## Out of scope

Non-markdown artifacts (yaml, config, code) — covered by the base principle directly, or their own domain rule.

## References

- [wording-rule][../../bedrocks/wording-rule/BEDROCK.md]
- [ssot-principle][../ssot-principle/RULE.md]
- [private-content][../private-content/RULE.md]
- [prose-convention][../prose-convention/RULE.md]

[../../bedrocks/wording-rule/BEDROCK.md]: ../../bedrocks/wording-rule/BEDROCK.md
[../ssot-principle/RULE.md]: ../ssot-principle/RULE.md
[../private-content/RULE.md]: ../private-content/RULE.md
[../prose-convention/RULE.md]: ../prose-convention/RULE.md
[links]: #links
[how-to-apply]: #how-to-apply
[builds-on]: #builds-on
