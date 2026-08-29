---
name: markdown-convention
description: Markdown-specific authoring mechanics layered on document-convention — frontmatter, lists, tables, reference-style links, fenced code, and the references section; defaults for both layers, deferring to the established style nearby — the author's own for private content, the team's for public.
---

# Markdown conventions — authoring mechanics

Markdown-specific mechanics, layered on the foundations in [Builds on][builds-on].

## Builds on

MUST read and follow these first — this rule builds on them:

- [wording-rule][../../bedrocks/wording-rule/BEDROCK.md]
- [governance-scope][../../bedrocks/governance-scope/BEDROCK.md]
- [ssot-principle][../ssot-principle/RULE.md]
- [private-content][../private-content/RULE.md]
- [prose-convention][../prose-convention/RULE.md]
- [document-convention][../document-convention/RULE.md]

## Rule

The conventions below are the **Markdown-specific** layer over the format-agnostic conventions in [document-convention][../document-convention/RULE.md] — file shape, document format, and authoring discipline live there; only Markdown's own mechanics are restated here. They are this domain's **defaults**; [governance-scope][../../bedrocks/governance-scope/BEDROCK.md] governs whether an established style in the document's own layer takes precedence — see [How to apply][how-to-apply].

### Frontmatter

- Frontmatter is OPTIONAL; when present, it MUST be valid YAML. A plain scalar can't contain `": "` (a colon followed by a space) — it breaks parsing and rendering (e.g. GitHub). Reword to remove the colon, or double-quote the whole value when the colon needs to stay.

### Headings

- The top-level title is the H1 (`#`); each deeper heading level adds one `#` (`##`, `###`, …).

### Table of contents

- When a table of contents is included, keep it in sync with the document's headings, in the VSCode **Markdown All in One** format.

### Lists

- Unordered lists use `-`, not `*` or `+`; reserve numbered lists for when order matters; no blank line between items.

### Tables

- Write tables in compact form — `|---|` separators, single-space cells, no alignment padding. Convert existing padded tables to compact.
- Precede every table with `<!-- prettier-ignore -->` on its own line so a formatter (prettier, editor format-on-save) won't reflow it; re-check tables after a format pass.

### Links

- Reference a file, document, or section with Markdown link syntax, not a bare path or plain prose. MUST use **reference-style** `[text][id]`, not **inline** `[text](path)`.
- For a reference-style link to a file or doc, the `id` MUST be the **relative path** to the target — the same string as the link's destination (e.g. `../ssot-principle/RULE.md`, or a sibling's `config.yaml`). It's derived from the path — there's no name to invent, and none to keep consistent across files — so a rename is a clean grep of the path, and it needs no repo-root assumption. For an in-document section, the `id` is the heading's anchor slug.
- On a rename or move, update every link to the target so none goes stale — [ssot-principle][../ssot-principle/RULE.md]'s consistency facet, applied to links.

### Code

- Mention a filename or path in inline code (`README.md`, `docs/`), not bare prose — to reference it, use a [link][links] instead; a frontmatter `description` is the exception, where a filename stays plain (house style).
- Fence multi-line code or output; tag the fence with its language when it has one (Python, YAML, …), and leave it bare for language-less content (plain text, command output, a file tree).
- Render a structural diagram (flow, architecture, ER) as an inline Mermaid fenced block.

### References

- Collect every reference-style link's `[id]: target` definition at the bottom of the document — each target written once.
- If the document cites external sources (files, docs, URLs), put a `## References` heading above those definitions with a visible bullet list of them, so the section isn't empty when rendered. Internal `#` section anchors are navigation, not citations: defined, but not in the visible list.
- Keep both in sync with the links actually used — no unused definitions, none missing.

## When to apply

When writing or editing any markdown document. Also a pre-publish checkpoint: re-check each convention before declaring work done.

## How to apply

Follow [document-convention][../document-convention/RULE.md]'s How to apply; for Markdown its domain inputs are:

- **The established style to observe** — the conventions the nearby Markdown files in the document's own layer follow (sibling `.md` files, a same-folder `README.md`, a `docs/` index): the **author-only** files for a private document, the **shared** ones for a public one.
- **The defaults** to fall back to — the conventions above.

## Out of scope

Non-markdown artifacts (yaml, config, code) — covered by the base principle directly, or their own domain rule.

## References

- [wording-rule][../../bedrocks/wording-rule/BEDROCK.md]
- [governance-scope][../../bedrocks/governance-scope/BEDROCK.md]
- [ssot-principle][../ssot-principle/RULE.md]
- [private-content][../private-content/RULE.md]
- [prose-convention][../prose-convention/RULE.md]
- [document-convention][../document-convention/RULE.md]

[../../bedrocks/wording-rule/BEDROCK.md]: ../../bedrocks/wording-rule/BEDROCK.md
[../../bedrocks/governance-scope/BEDROCK.md]: ../../bedrocks/governance-scope/BEDROCK.md
[../ssot-principle/RULE.md]: ../ssot-principle/RULE.md
[../private-content/RULE.md]: ../private-content/RULE.md
[../prose-convention/RULE.md]: ../prose-convention/RULE.md
[../document-convention/RULE.md]: ../document-convention/RULE.md
[links]: #links
[how-to-apply]: #how-to-apply
[builds-on]: #builds-on
