# Reference links

How one unit references another — the form a reference link takes.

## Form

Within a plugin, links follow `markdown-convention` — reference-style, with the target's relative path as the id. Across plugins this relaxes: the id takes a `plugin:<name>/…` form rooted at the depended plugin (`plugin:dongent/rules/ssot-principle/RULE.md`), resolved at the install root and only where that dependency is declared. The prefix marks a plugin reference rather than a literal path; it isn't file-clickable — a deliberate relaxation of `markdown-convention` for the cross-plugin case.
