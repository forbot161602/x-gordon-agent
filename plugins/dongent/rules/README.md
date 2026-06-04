# Rule library

Each subfolder under `rules/` is one rule category.

## Layout

```
rules/
├── README.md                  # this file — rule catalog overview
└── <rule-name>/
    ├── RULE.md                # canonical rule (ALL-CAPS, agent reads first)
    ├── Specification.md       # optional supplementary doc (Initial-Cap)
    ├── <script>.py            # if the rule has implementation logic, pair it with…
    ├── <script>_test.py       # …a test file pinning the behavior
    └── ...                    # other optional files (fixtures, templates, sub-modules)
```

Each rule folder has at minimum a `RULE.md`. Other Initial-Cap markdown files (`Specification.md`, etc.) are supplementary, read on demand. Lowercase files are helpers — whatever the rule needs to operate (scripts, templates, tests, fixtures). When a rule has implementation logic, always pair the script with a test file so behavior is verifiable.

## Rules

`Tier` controls default install behavior when a rule is being synced into a project: `recommended` installs automatically; `optional` installs only on explicit request.

### Base

Cross-cutting principles inherited by domain rules.

<!-- prettier-ignore -->
| Folder | Tier | Summary |
|---|---|---|
| [`ssot-principle/`][ssot-principle/] | recommended | One canonical home per fact (reference, don't copy), consistent references, no redundancy |
| [`private-content/`][private-content/] | recommended | Private/public layer separation with one-way references (private → public) |
| [`prose-convention/`][prose-convention/] | recommended | Shared prose remains self-contained — independent of session, clock, or team |

### Domain

Rules tied to specific artifact types; build on base rules.

<!-- prettier-ignore -->
| Folder | Tier | Summary |
|---|---|---|
| [`markdown-convention/`][markdown-convention/] | recommended | Markdown mechanics: valid-YAML frontmatter, compact tables, Markdown-syntax links, reference-style References |
| [`commit-convention/`][commit-convention/] | recommended | Conventional commits with three-part structure (header / body / footer); messages scoped to the project's reviewers |
| [`pr-convention/`][pr-convention/] | recommended | PR title defaults to the commit-header shape; body is terse, template-driven; cross-domain references and code snippets only when load-bearing |
| [`zh-tw-punctuation/`][zh-tw-punctuation/] | recommended | Convert ASCII `,` `:` `;` `?` to full-width on Chinese-led lines (markdown documents, commits, PRs) |

## References

- [`ssot-principle/`][ssot-principle/]
- [`private-content/`][private-content/]
- [`prose-convention/`][prose-convention/]
- [`markdown-convention/`][markdown-convention/]
- [`commit-convention/`][commit-convention/]
- [`pr-convention/`][pr-convention/]
- [`zh-tw-punctuation/`][zh-tw-punctuation/]

[ssot-principle/]: ssot-principle/
[private-content/]: private-content/
[prose-convention/]: prose-convention/
[markdown-convention/]: markdown-convention/
[commit-convention/]: commit-convention/
[pr-convention/]: pr-convention/
[zh-tw-punctuation/]: zh-tw-punctuation/
