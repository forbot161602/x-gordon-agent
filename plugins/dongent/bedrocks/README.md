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
| [`wording-rule/`][wording-rule/] | Requirement-level keywords (MUST / SHOULD / …) and behavior-trigger words, each with one fixed meaning |
| [`governance-scope/`][governance-scope/] | Whose conventions content follows — the author's own established convention for private content, the team's for public, and the plugin's defaults where neither has established one |

### Interaction

How the agent deals with whoever gave it the instruction — the language and order of what it says back, and the authority it acts under.

<!-- prettier-ignore -->
| Folder | Summary |
|---|---|
| [`reply-convention/`][reply-convention/] | Answer in the user's own language — not the artifacts' — and open with the judgement when the reply carries one |
| [`agent-autonomy/`][agent-autonomy/] | Stepwise under the user until a grant says otherwise, automatic within the grant where no answer can arrive during the run, and a report of what was done owed back either way |

## References

- [`wording-rule/`][wording-rule/]
- [`governance-scope/`][governance-scope/]
- [`reply-convention/`][reply-convention/]
- [`agent-autonomy/`][agent-autonomy/]

[wording-rule/]: wording-rule/
[governance-scope/]: governance-scope/
[reply-convention/]: reply-convention/
[agent-autonomy/]: agent-autonomy/
