# x-gordon-agent

Reusable agent components, shared across projects. Published as the **`dongent`** marketplace: `x-gordon-agent` is the repository name, but the marketplace, its plugin, and every reference to them — here and downstream — use the name `dongent`.

## Lifecycle

### Install

Add the marketplace, then install the plugin:

```bash
claude plugin marketplace add <source>
claude plugin install dongent@dongent
```

`<source>` is this repository — a git URL or a local path to the folder holding [`.claude-plugin/marketplace.json`][.claude-plugin/marketplace.json].

### Update

```bash
claude plugin update dongent
```

This refreshes the plugin itself from its source — no manual `git pull` needed. **But distributed state stays at the version produced by the last sync**: per-project state written by plugin components like `sync-rule-memory` (e.g. memory files) doesn't update automatically. Re-run the relevant components in each affected project after a plugin update.

### Uninstall

```bash
claude plugin uninstall dongent
```

Same caveat as update — only removes the plugin itself. State written by plugin components elsewhere remains on disk: per-project memory at `<project-memory>/dongent-*.md`, plus any other yaml / md / config files components might have generated into project folders. There's no dedicated cleanup command — if you want it gone, ask the agent to scan affected locations and remove the relevant files.

## Layout

<!-- prettier-ignore -->
| Path | What's in there |
|---|---|
| [`plugins/`][plugins/] | Plugins published by this marketplace — each holds the bedrocks, rules, commands, skills, and hooks it ships |

## References

- [`.claude-plugin/marketplace.json`][.claude-plugin/marketplace.json]
- [`plugins/`][plugins/]

[.claude-plugin/marketplace.json]: .claude-plugin/marketplace.json
[plugins/]: plugins/
