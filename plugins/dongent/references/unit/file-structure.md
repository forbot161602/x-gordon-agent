# File structure

How a folder's files are laid out — a file's role fixes its casing.

## Roles

A folder holds whichever of these it needs:

- **Entry doc** — a unit's canonical file, read first; ALL-CAPS, named for its kind (`RULE.md`, `SKILL.md`, `ARCHITECTURE.md`). A single-file unit — such as a command (`publish-check.md`) — is itself the entry, named for the unit rather than the kind.
- **Index doc** — catalogs a folder of units. A `README.md` inside the folder (ALL-CAPS, per `document-convention`); a lowercase fixed name (`index.md`, `_index.md`) where the tooling expects one; or, when the folder can't hold an index inside it, a sibling catalog beside it named for the folder (`skills/` → `Skills.md`).
- **Supplementary doc** — longer material (full algorithms, rationale, large examples) goes in a separate Initial-Cap doc beside the entry (e.g. `Specification.md` or `Design-Rationale.md`).
- **Helper** — scripts, templates, fixtures are lowercase; pair any logic-carrying file with a test named for it (`helper.py` → `test_helper.py`) so its behaviour stays verifiable.
