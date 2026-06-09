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

Foundational conventions that other docs are written and read against — each cross-cutting convention lives here once and is referenced rather than restated.

<!-- prettier-ignore -->
| Folder | Summary |
|---|---|
| [`wording-rule/`][wording-rule] | Requirement-level keywords (MUST / SHOULD / …) and behavior-trigger words, each with one fixed meaning |

## References

- [`wording-rule/`][wording-rule]

[wording-rule]: wording-rule/
