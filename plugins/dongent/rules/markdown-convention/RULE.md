---
name: markdown-convention
description: Markdown authoring conventions — document structure and element formatting (headings, lists, tables, links, code, images, emphasis); defaults for private and public content, deferring to nearby team style for public.
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

## Rule

The conventions below are this domain's **defaults**; [governance-scope][../../bedrocks/governance-scope/BEDROCK.md] governs whether public content yields to team style — see [How to apply][how-to-apply] for what markdown observes.

### Frontmatter

- Frontmatter is OPTIONAL; when present, it MUST be valid YAML. A plain scalar can't contain `": "` (a colon followed by a space) — it breaks parsing and rendering (e.g. GitHub). Reword to remove the colon, or double-quote the whole value when the colon needs to stay.

### Sections

- Sections run in this order: the H1 and its intro, an optional TOC, the body sections, then `## References` last when present.

### H1

- Exactly one H1, with at least a one-line intro under it.
- The H1 echoes the file name in Sentence case, except a generic-marker name like README.md.
- The intro overviews the whole document; an overview overlaps the content by nature, so distil the essence and reword rather than copy verbatim (per [ssot-principle][../ssot-principle/RULE.md]).

### TOC

- OPTIONAL — add a TOC only when the user asks; skip it by default, and NEVER for an agent-facing doc (e.g. project memory).
- When present, it sits directly under the H1 intro, in the VSCode **Markdown All in One** auto-generated format.

### Headings

- A blank line follows each heading.
- Don't skip levels — an H3 sits under an H2.

### Paragraphs

- A blank line between paragraphs.

### Lists

- Unordered lists use `-`, not `*` or `+`; reserve numbered lists for when order matters; no blank line between items.

### Tables

- Write tables in compact form — `|---|` separators, single-space cells, no alignment padding. Convert existing padded tables to compact.
- Precede every table with `<!-- prettier-ignore -->` on its own line so a formatter (prettier, editor format-on-save) won't reflow it; re-check tables after a format pass.

### Links

- Reference a file, document, or section with Markdown link syntax, not a bare path or plain prose. MUST use **reference-style** `[text][id]`, not **inline** `[text](path)`.
- For a reference-style link to a file or doc, the `id` MUST be the **relative path** to the target — the same string as the link's destination (e.g. `../ssot-principle/RULE.md`, or a sibling's `config.yaml`). It's derived from the path — there's no name to invent, and none to keep consistent across files — so a rename is a clean grep of the path, and it needs no repo-root assumption. For an in-document section, the `id` is the heading's anchor slug.
- On a rename or move, update every link to the target so none goes stale — [ssot-principle][../ssot-principle/RULE.md]'s consistency facet, applied to links.

### Images

- Surround an image with text describing it.
- An image file takes a kebab-case name in a sibling folder (e.g. `images/`).
- Render a structural diagram (flow, architecture, ER) as an inline Mermaid fenced block.

### Code

- Mention a filename or path in inline code (`README.md`, `docs/`), not bare prose — to reference it, use a [link][links] instead; a frontmatter `description` is the exception, where a filename stays plain (house style).
- Fence multi-line code or output; tag the fence with its language when it has one (Python, YAML, …), and leave it bare for language-less content (plain text, command output, a file tree).

### Emphasis

- Bold for keywords; italic only for foreign terms or proper nouns.

### References

- Collect every reference-style link's `[id]: target` definition at the bottom of the document — each target written once.
- If the document cites external sources (files, docs, URLs), put a `## References` heading above those definitions with a visible bullet list of them, so the section isn't empty when rendered. Internal `#` section anchors are navigation, not citations: defined, but not in the visible list.
- Keep both in sync with the links actually used — no unused definitions, none missing.

## When to apply

When writing or editing any markdown document. Also a pre-publish checkpoint: re-check each convention before declaring work done.

## How to apply

- **Before writing**, place the document by layer ([private-content][../private-content/RULE.md]), then run [governance-scope][../../bedrocks/governance-scope/BEDROCK.md]'s cascade — this rule supplies its two domain inputs:
  - **The team style to observe** lives in **nearby files**: read 2-3 (sibling files, the same-folder README, a docs/ index) and defer to what they do, judged per convention independently — inline links, spread-out tables, no prettier-ignore are all respected.
  - **The defaults** to fall back to are the conventions above.
- **Before publishing**, the agent re-checks each convention against whichever source won its cascade; fix anything flagged.

## Out of scope

Non-markdown artifacts (yaml, config, code) — covered by the base principle directly, or their own domain rule.

## References

- [wording-rule][../../bedrocks/wording-rule/BEDROCK.md]
- [governance-scope][../../bedrocks/governance-scope/BEDROCK.md]
- [ssot-principle][../ssot-principle/RULE.md]
- [private-content][../private-content/RULE.md]
- [prose-convention][../prose-convention/RULE.md]

[../../bedrocks/wording-rule/BEDROCK.md]: ../../bedrocks/wording-rule/BEDROCK.md
[../../bedrocks/governance-scope/BEDROCK.md]: ../../bedrocks/governance-scope/BEDROCK.md
[../ssot-principle/RULE.md]: ../ssot-principle/RULE.md
[../private-content/RULE.md]: ../private-content/RULE.md
[../prose-convention/RULE.md]: ../prose-convention/RULE.md
[links]: #links
[how-to-apply]: #how-to-apply
[builds-on]: #builds-on
