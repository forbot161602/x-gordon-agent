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
| `UserPromptSubmit` | [`reply-language.json`][contexts/reply-language.json] | Injects the reply-language reminder as fresh context each turn. Enforces the [reply-language][../bedrocks/reply-language/BEDROCK.md] bedrock. |

## References

- [`hooks.json`][hooks.json]
- [`contexts/`][contexts/]
- [`reply-language.json`][contexts/reply-language.json]
- [reply-language][../bedrocks/reply-language/BEDROCK.md]

[hooks.json]: hooks.json
[contexts/]: contexts/
[contexts/reply-language.json]: contexts/reply-language.json
[../bedrocks/reply-language/BEDROCK.md]: ../bedrocks/reply-language/BEDROCK.md
