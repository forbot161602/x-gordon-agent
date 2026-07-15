# Markdown frontmatter

The YAML block heading a unit's entry doc.

## Shared fields

These fields are common across kinds; a kind adds its own on top.

- **`name`** — the unit's identifier, matching its folder or file name, per [`file-naming`][file-naming].
- **`description`** — a concise summary of what the unit does, why, and how; third-person, written as a statement or an imperative.

## Summary layers

The `description`, the H1 intro, and the body each state what the unit is at a different scope — none repeats another:

- **`description`** — what it does, why, and how, in brief.
- **H1 intro** — the whole doc distilled to its essence, leading into the body.
- **body** — the full content, living only here; NEVER copied into the `description` or the H1 intro.

## References

- [`file-naming`][file-naming]

[file-naming]: file-naming.md
