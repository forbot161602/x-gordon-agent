# Rule library

Each subfolder under `rules/` is one rule.

## Layout

```
rules/
├── README.md                  # this file — rule overview
└── <rule-name>/
    ├── RULE.md                # canonical rule (ALL-CAPS, agent reads first)
    ├── Specification.md       # optional supplementary doc (Initial-Cap)
    ├── <script>.py            # if the rule has implementation logic, pair it with…
    ├── <script>_test.py       # …a test file pinning the behavior
    └── ...                    # other optional files (fixtures, templates, sub-modules)
```

Each rule folder has at minimum a `RULE.md`. Other Initial-Cap markdown files (`Specification.md`, etc.) are supplementary, read on demand. Lowercase files are helpers — whatever the rule needs to operate (scripts, templates, tests, fixtures). When a rule has implementation logic, always pair the script with a test file so behavior is verifiable.

## Rules

Rules are grouped by what they govern; within a group they run from the most foundational outward (general before specific). `Tier` controls default install behavior when a rule is being synced into a project: `required` installs automatically; `optional` installs only on explicit request.

### Core

Cross-cutting principles every other rule builds on; tied to no particular artifact type.

<!-- prettier-ignore -->
| Folder | Tier | Summary |
|---|---|---|
| [`ssot-principle/`][ssot-principle/] | required | One canonical home per fact (reference, don't copy), consistent references, no redundancy |
| [`private-content/`][private-content/] | required | Private/public layer separation with one-way references (private → public) |
| [`prose-convention/`][prose-convention/] | required | Shared prose remains self-contained — independent of session, clock, or team |

### Document

Rules for written documents — prose and markup.

<!-- prettier-ignore -->
| Folder | Tier | Summary |
|---|---|---|
| [`document-convention/`][document-convention/] | required | Format-agnostic document authoring — file shape, document format, and authoring discipline; the base that format rules build on |
| [`markdown-convention/`][markdown-convention/] | required | Markdown-specific mechanics layered on document-convention — frontmatter, lists, tables, reference-style links, fenced code |
| [`zh-tw-punctuation/`][zh-tw-punctuation/] | required | Convert ASCII `,` `:` `;` `?` to full-width and `…` to ASCII dots on Chinese-led lines (markdown documents, commits, PRs) |

### Git

Rules for git artifacts — commits and PRs.

<!-- prettier-ignore -->
| Folder | Tier | Summary |
|---|---|---|
| [`commit-convention/`][commit-convention/] | required | Conventional commits with three-part structure (header / body / footer); messages scoped to the project's reviewers |
| [`pr-convention/`][pr-convention/] | required | PR title defaults to the commit-header shape; body is terse, template-driven; cross-domain references and code snippets only when load-bearing |

## References

- [`ssot-principle/`][ssot-principle/]
- [`private-content/`][private-content/]
- [`prose-convention/`][prose-convention/]
- [`document-convention/`][document-convention/]
- [`markdown-convention/`][markdown-convention/]
- [`zh-tw-punctuation/`][zh-tw-punctuation/]
- [`commit-convention/`][commit-convention/]
- [`pr-convention/`][pr-convention/]

[ssot-principle/]: ssot-principle/
[private-content/]: private-content/
[prose-convention/]: prose-convention/
[document-convention/]: document-convention/
[markdown-convention/]: markdown-convention/
[zh-tw-punctuation/]: zh-tw-punctuation/
[commit-convention/]: commit-convention/
[pr-convention/]: pr-convention/
