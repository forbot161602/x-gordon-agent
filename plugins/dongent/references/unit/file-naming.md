# File naming

How a unit is named. Each unit is a folder — or a single file — named for it; that name identifies the unit.

## Naming patterns

Each name part is a single word by default; compound it only when one word would be ambiguous. Keep a family's category consistent so its members line up. A few patterns follow:

- **`<subject>`** — for rules, bedrocks, and the like:
  - **subject** — the subject the unit governs, as a noun or noun phrase, general before specific; no verb.
  - Examples: `wording-rule`, `ssot-principle`, `markdown-convention`.
- **`<category>(-<object>)-<verb>`** — for skills, commands, and the like:
  - **category** — the family the unit belongs to; a noun or gerund (`coding`, `doc`, `plugin`); SHOULD NOT be an identity or role (`developer`, `pm`, `qa`).
  - **verb** — a conventional action word (`write`, `update`, `verify`).
  - **object** — OPTIONAL, what the verb acts on (`doc`, `spec`, `rule`).
  - Examples: `memory-sync`, `coding-doc-init`, `coding-doc-update`.
