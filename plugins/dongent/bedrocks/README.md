# Bedrock conventions

Each subfolder under `bedrocks/` is one bedrock.

## Layout

```
bedrocks/
├── README.md                  # this file — bedrock overview
└── <bedrock-name>/
    └── BEDROCK.md             # canonical bedrock (ALL-CAPS, agent reads first)
```

Each bedrock folder has at minimum a `BEDROCK.md`; any supplementary docs (Initial-Cap) and helpers (lowercase) sit beside it.

## Bedrocks

Foundational conventions that other docs are written and read against — each cross-cutting convention lives here once and is referenced rather than restated. Bedrocks are grouped by what they govern; within a group they run from the most foundational outward (general before specific).

### Core

Cross-cutting foundations every rule and document builds on; tied to no particular artifact type.

<!-- prettier-ignore -->
| Folder | Summary |
|---|---|
| [`wording-rule/`][wording-rule] | Requirement-level keywords (MUST / SHOULD / …) and behavior-trigger words, each with one fixed meaning |
| [`governance-scope/`][governance-scope] | Whose conventions content follows — the author's own established convention for private content, the team's for public, and the plugin's defaults where neither has established one |
| [`reply-language/`][reply-language] | Reply to the user in their customary language — separate from the language of the artifacts produced |

## References

- [`wording-rule/`][wording-rule]
- [`governance-scope/`][governance-scope]
- [`reply-language/`][reply-language]

[wording-rule]: wording-rule/
[governance-scope]: governance-scope/
[reply-language]: reply-language/
