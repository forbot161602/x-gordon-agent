---
name: document-convention
description: Format-agnostic conventions for authoring any document — the file shape of the document system (casing, asset folders, folder grouping), its document format (title, sections, table of contents, headings, paragraphs, images, emphasis), and its authoring discipline (requirement levels, generic statements, impersonal prose, outward references); defaults for both layers, deferring to the established style nearby — the author's own for private content, the team's for public.
---

# Document conventions — format-agnostic authoring

Conventions for writing any document — and for laying out a body of documents as a system — independent of format. Format-specific mechanics layer on top in a downstream rule (e.g. `markdown-convention` for Markdown). Builds on the foundations in [Builds on][builds-on].

## Builds on

MUST read and follow these first — this rule builds on them:

- [wording-rule][../../bedrocks/wording-rule/BEDROCK.md]
- [governance-scope][../../bedrocks/governance-scope/BEDROCK.md]
- [ssot-principle][../ssot-principle/RULE.md]
- [private-content][../private-content/RULE.md]
- [prose-convention][../prose-convention/RULE.md]

## Rule

The conventions below are this domain's **defaults**; [governance-scope][../../bedrocks/governance-scope/BEDROCK.md] governs whether an established style in the document's own layer takes precedence — see [How to apply][how-to-apply]. They fall in three groups: the **file shape** of the document system (how its files and folders are laid out), the **document format** (how a document is structured and presented), and the **authoring discipline** every document observes.

### File shape

The document system SHOULD lay out its files and folders as follows:

- A multi-word file or folder name is kebab-case, except a conventional marker file, which keeps its established fixed name in ALL-CAPS (`README`, `LICENSE`).
- A file a document brings in (image, attachment, companion docs) sits in a kebab-case sibling folder (e.g. `assets/`, `images/`, `references/`).
- Documents are grouped into folders by what they cover or their kind, and a group that grows gets its own subfolder.

### Document format

#### Title

- Exactly one top-level title, with at least a one-line intro under it.
- The title — and every heading — is in Sentence case; the title echoes the file name, except a generic-marker name like `README.md` or `index.html`.
- The intro overviews the whole document; an overview overlaps the content by nature, so distil the essence and reword rather than copy verbatim (per [ssot-principle][../ssot-principle/RULE.md]).

#### Sections

- Sections run in a consistent order: the title and its intro, an optional table of contents, the body sections, then a references section last when present.

#### Table of contents

- A table of contents is OPTIONAL — add one only when asked; skip it by default, and NEVER for an agent-facing document (e.g. project memory).

#### Headings

- Don't skip levels — a third-level heading sits under a second-level one.
- Keep a heading visually separated from the content around it (a blank line where the format needs one).

#### Paragraphs

- Keep distinct paragraphs visually separated (a blank line where the format needs one).

#### Images

- Surround an image with text describing it.

#### Emphasis

- Bold for key terms; italic only for foreign terms or proper nouns.

### Authoring discipline

#### Requirement levels

Apply [wording-rule][../../bedrocks/wording-rule/BEDROCK.md]'s requirement-level keywords at write-time, so each statement reads at the strength intended.

- Unmarked already reads as MUST, so leave most prose unmarked; add an explicit level only where emphasis earns its place — e.g. an especially important requirement, or one agents repeatedly get wrong.
- Pick the level by the requirement's real strength — write MUST when it is inviolable, SHOULD when it is a strong default that genuinely bends, MAY when it is a free choice; the prohibitions (MUST NOT, SHOULD NOT) mirror these. Before writing SHOULD, confirm there is real give; with none, it is MUST.
- When stating a level, use only `wording-rule`'s keyword, in uppercase — not a lowercase form, a vaguer synonym, or an out-of-set keyword (e.g. SHALL, MANDATORY), each of which blunts the signal; within a sentence, hoist one keyword to govern a list rather than repeating it.
- Don't scatter levels where none is needed and blur the focus — reword the rest to plain phrasing (has to, needs to, is meant to); but don't go the other way either, flattening a genuine requirement into a bare statement (is, are) or a near-synonym (needed) to dodge its keyword. A real requirement takes the keyword.

#### Generic statement

- State a fact as generally as it actually holds — no narrower (which shrinks the rule into needless enumeration), no broader (which overstates it). A genuinely domain-specific fact stays specific.
- For the execution plane, prefer a generic term to a product name (agent / harness / runtime, not Codex or Claude Code); demote a genuinely product-specific detail to a parenthetical or "e.g." aside (e.g. a `~/.claude/…` path).

#### Impersonal prose

- Directive guidance SHOULD NOT use personal pronouns (you, we, I) or "please"; write it as a plain statement or a subjectless imperative.
- Explanatory or illustrative second person is fine (an aside such as "the reader is not in your session", or a quoted "I'm about to commit"), and generic they / their (for rules, files, a team) is always fine.

#### Outward references

- Declare a document's dependencies by what it itself needs, not by what those dependencies in turn need — list every base it directly draws on, and don't drop one just because another base also reaches it.
- Reference the upstream bases a document builds on, and a peer only for a genuine connection (e.g. a see-also or a hand-off).
- Avoid gratuitous cross-references — they couple documents. For a downstream document (one that builds on this) or a peer, prefer a plain-prose mention, and add a link only where the pointer is load-bearing.

## When to apply

When writing or editing any document, in any format. Also a pre-publish checkpoint: re-check each convention before declaring work done.

## How to apply

- **Before writing**, place the document by layer ([private-content][../private-content/RULE.md]), then run [governance-scope][../../bedrocks/governance-scope/BEDROCK.md]'s cascade — this rule supplies its two domain inputs:
  - **The established style to observe** — the conventions the nearby artifacts in the document's own layer follow (sibling documents, a same-folder README, an index doc): the **author-only** artifacts for a private document, the **shared** ones for a public one.
  - **The defaults** to fall back to — the conventions above.
- **Before publishing**, re-check each convention against whichever source won its cascade; fix anything flagged.
- **Either way**, summarise the observed style from the nearby artifacts once, not convention by convention or line by line — then resolve each convention against that summary. When a signal is genuinely ambiguous, weigh impact — apply a default that renders identically or sits orthogonal to the observed house voice, and reserve deference for a clearly contrary convention.

## Out of scope

- Format-specific mechanics — owned by the format's own rule (e.g. `markdown-convention` for Markdown).
- Non-document artifacts and their file names (source code, configuration, build output) — covered by the base principle directly, or by their own domain rule.

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
[builds-on]: #builds-on
[how-to-apply]: #how-to-apply
