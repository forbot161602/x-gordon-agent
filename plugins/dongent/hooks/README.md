# Hooks

Event hooks this plugin ships. The harness auto-loads [`hooks.json`][hooks.json] when the plugin is installed — no setup — and drops it when the plugin is removed.

## Contents

<!-- prettier-ignore -->
| Path | What's in there |
|---|---|
| [`hooks.json`][hooks.json] | Hook manifest — maps each event to a command |
| [`contexts/`][contexts/] | Static context payloads the hooks emit |

## Events

<!-- prettier-ignore -->
| Event | Payload | What it does |
|---|---|---|
| `UserPromptSubmit` | [`reply-convention.md`][contexts/reply-convention.md] | Enforces the [reply-convention][../bedrocks/reply-convention/BEDROCK.md] bedrock by injecting its reminder as fresh context each turn. |

## References

- [`hooks.json`][hooks.json]
- [`contexts/`][contexts/]
- [`reply-convention.md`][contexts/reply-convention.md]
- [reply-convention][../bedrocks/reply-convention/BEDROCK.md]

[hooks.json]: hooks.json
[contexts/]: contexts/
[contexts/reply-convention.md]: contexts/reply-convention.md
[../bedrocks/reply-convention/BEDROCK.md]: ../bedrocks/reply-convention/BEDROCK.md
