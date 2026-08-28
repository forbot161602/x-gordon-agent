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
| `UserPromptSubmit` | [`reply-convention.json`][contexts/reply-convention.json] | Injects the reply-convention reminder as fresh context each turn. Enforces the [reply-convention][../bedrocks/reply-convention/BEDROCK.md] bedrock. |

## References

- [`hooks.json`][hooks.json]
- [`contexts/`][contexts/]
- [`reply-convention.json`][contexts/reply-convention.json]
- [reply-convention][../bedrocks/reply-convention/BEDROCK.md]

[hooks.json]: hooks.json
[contexts/]: contexts/
[contexts/reply-convention.json]: contexts/reply-convention.json
[../bedrocks/reply-convention/BEDROCK.md]: ../bedrocks/reply-convention/BEDROCK.md
