# Commands

The slash commands this plugin provides. Each is namespaced `/dongent:<name>`; the definitions live in [`commands/`][commands/].

## Contents

<!-- prettier-ignore -->
| Command | What it does |
|---|---|
| [`/dongent:memory-sync`][commands/memory-sync.md] | Sync the rule library into the current project's agent memory. Idempotent — first run installs, later runs update only what changed upstream. |
| [`/dongent:publish-check`][commands/publish-check.md] | Pre-publish audit — verify changed files obey the rules before publishing; runs mostly without author intervention. |
| [`/dongent:compact-checkpoint`][commands/compact-checkpoint.md] | Before compaction or context loss, capture durable session state into the project's agent memory — or private content — so it survives future sessions. Write-side. |
| [`/dongent:compact-resume`][commands/compact-resume.md] | After compaction or on resuming, rebuild the working context — task, progress, decisions, rules — from the project's agent memory. Read-side. |

## References

- [`commands/`][commands/]
- [`commands/memory-sync.md`][commands/memory-sync.md]
- [`commands/publish-check.md`][commands/publish-check.md]
- [`commands/compact-checkpoint.md`][commands/compact-checkpoint.md]
- [`commands/compact-resume.md`][commands/compact-resume.md]

[commands/]: commands/
[commands/memory-sync.md]: commands/memory-sync.md
[commands/publish-check.md]: commands/publish-check.md
[commands/compact-checkpoint.md]: commands/compact-checkpoint.md
[commands/compact-resume.md]: commands/compact-resume.md
