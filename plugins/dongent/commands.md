# commands

The slash commands this plugin provides. Each is namespaced `/dongent:<name>`; the definitions live in [`commands/`][commands/].

<!-- prettier-ignore -->
| Command | What it does |
|---|---|
| [`/dongent:check-consistency`][commands/check-consistency.md] | Pre-publish audit — verify changed files obey the rules before publishing; runs mostly without author intervention. |
| [`/dongent:sync-rule-memory`][commands/sync-rule-memory.md] | Sync the rule library into the current project's agent memory. Idempotent — the first run installs, later runs only update what changed upstream. |

## References

- [`commands/`][commands/]
- [`commands/check-consistency.md`][commands/check-consistency.md]
- [`commands/sync-rule-memory.md`][commands/sync-rule-memory.md]

[commands/]: commands/
[commands/check-consistency.md]: commands/check-consistency.md
[commands/sync-rule-memory.md]: commands/sync-rule-memory.md
