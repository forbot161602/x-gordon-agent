---
name: prose-convention
description: Shared prose reads without access to the original session, clock, or team. Forbids time-bound references (session shorthand, relative time) and space-bound references (in-group abbreviations, names, addressee imperatives).
---

# Prose convention — self-contained shared prose

Shared prose outlasts the moment of writing. The future reader is not in your session, your clock, or your team. Prose is **self-contained** — the text alone gives the reader everything they need.

## Builds on

MUST read and follow these first — this rule builds on them:

- [wording-rule][../../bedrocks/wording-rule/BEDROCK.md]

## Rule

Two principles, both serving one goal: **self-contained meaning** — every claim MUST be decodable without access to the original context. A future reader — next session, next week, or outside your team — cannot be expected to guess or reverse-engineer what you meant.

### 1. Time-bound references are out

- **Session shorthand** (P1, Q1, T1, ...) — bound to a specific conversation; meaningless to anyone outside that session.
- **Relative time references** ("yesterday", "recently", "will fix next week") — use absolute dates (e.g. 2026-05-29) or directly restate the event the writer had in mind.

**Why:** the future reader has no clock and no session log; anything relative to a moment of writing goes stale once the writing ages.

### 2. Space-bound references are out

- **In-group abbreviations** (BE, FE, PM, QA, CEO, ...) — bare use is opaque; "the PM said" or "the BE API needs change" forces readers to reverse-engineer the in-group. These need explicit grounding by the surrounding text — a doc whose subject is the company's strategy can use "CEO" naturally.
- **People's names in prose body** — attribution metadata (commit author, code owners) is the right place; in prose body, people move on and named references become orphaned.
- **Imperatives at specific people or roles** ("ask QA", "tell PM", "Alice should review") — these inherit both problems: the addressee is space-bound, and the directive itself becomes time-bound (when does it expire? who confirms it was done?).

**Why:** the future reader is not in your team; in-group vocabulary, names, and addressee-specific phrasing all require in-group context to interpret.

## When to apply

When writing or editing any shared prose (README, design doc, code comment, commit body, PR description). Also a pre-publish checkpoint: run the audit before declaring work done.

## How to apply

- **Before writing**, ask: would a reader who lacks my session, my clock, and my team understand this? If not, restate it.
- **Before publishing**, run the audit:
  - Agent reads each shared artifact and checks against both principles; flag anything that depends on outside context.
  - Cheap pass: grep against the project's forbidden list.
- **Whenever a violation slips through and surfaces later**, add the specific term or pattern to the project's forbidden list — anchored in agent memory (inline or by pointer) — so future audits catch it. The list is **memory of past mistakes**, not a pre-seeded enumeration; the pre-publish grep assembles it from there.

## Out of scope

Layer separation (private vs public artifacts) — see [private-content][../private-content/RULE.md]. Some terms (e.g. session shorthand) are addressed by more than one rule from different angles.

## References

- [wording-rule][../../bedrocks/wording-rule/BEDROCK.md]
- [private-content][../private-content/RULE.md]

[../../bedrocks/wording-rule/BEDROCK.md]: ../../bedrocks/wording-rule/BEDROCK.md
[../private-content/RULE.md]: ../private-content/RULE.md
