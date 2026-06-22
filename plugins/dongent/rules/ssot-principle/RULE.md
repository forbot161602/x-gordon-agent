---
name: ssot-principle
description: Base authoring principle inherited by domain rules. Applies to writing and reviewing any artifact — docs, code (and comments), yaml, config. Keep each fact in one canonical home and reference it instead of copying, keep references consistent, and cut redundancy.
---

# SSoT principle — one canonical home

A base principle that domain rules build on.

## Builds on

MUST read and follow these first — this rule builds on them:

- [wording-rule][../../bedrocks/wording-rule/BEDROCK.md]

## Rule

Three principles, in priority order. A _fact_ is any unit of content — a statement, a value, a behaviour; a _link_ is any reference to its home — a document link, an import, a call, inheritance.

### 1. Single source of truth

Each fact lives in exactly one canonical home; everywhere else MUST link to it instead of copying it.

**Why:** a copied fact drifts — one side gets updated, the other rots into a silent contradiction.

**Scope:** "one home" is bounded by what can reference it. When a boundary between scopes allows references in only one direction (e.g. public artifacts can't point at private notes), the same fact lives once in each scope — apply these principles within each scope, and across the boundary keep the copies non-contradictory.

### 2. Consistency

- _fact_ — two separate checks: (1) every occurrence of a fact agrees, no contradictions; (2) every reference stays live — a rename or move updates all links so none goes stale.
- _style_ — a new file follows its same-type siblings in naming, structure, order, and conventions (a doc's section order, tone, terminology; code's error-handling, module layout, tests).

**Why:** contradictory facts mislead the reader; a stale link wastes their time; mismatched style inflates reading cost.

### 3. No redundancy

Keep content concise and precise. Where a fact already has a canonical home and appears again, decide by context: link to the home, or cut a redundant copy or link. Cut outright:

- **speculative structure** — built for a scope you don't have yet (a "just in case").
- **zero-information filler** — a line that only restates the title or states the obvious.

**Why:** padding and vagueness make the reader work harder; every redundant copy is a future inconsistency, and unused complexity is dead weight to maintain.

## When to apply

Before writing or substantially editing any artifact. Also a pre-publish checkpoint: sweep for the issues above before declaring work done.

## How to apply

- **Before writing a fact**, ask whether it already lives somewhere. If so, link to it rather than restating it.
- **When a fact could live in several places**, make its home the most foundational one — lowest layer, most-depended-on, longest-lived (based on dependency role and expected stability, not seniority; being written first doesn't make a copy authoritative).
- **When a fact already sits in several places**, resolve the duplicates against the canonical home — link where a reference is needed, cut where it isn't.
- **Before changing a fact**, grep for it across files and update every occurrence so no copy drifts.
- **On rename or move**, update every link that pointed at the old name or path.
- **When asked for "a complete summary"**, assemble it by linking, not by copying.

## Across artifacts

<!-- prettier-ignore -->
| Artifact | "One canonical home" in practice |
|---|---|
| HTML / Markdown | a decision is stated once; others link to it |
| YAML / config | a value is defined once; shared values are referenced, not re-typed across files |
| Code | a value or behaviour has one definition that others call or import, not a copy; comments neither restate the code nor contradict it or another comment about the same thing |

## Out of scope

Topics with their own rules are out of scope here — e.g. keeping private content out of reviewable artifacts (leak prevention), or medium-specific conventions (e.g. markdown).

## References

- [wording-rule][../../bedrocks/wording-rule/BEDROCK.md]

[../../bedrocks/wording-rule/BEDROCK.md]: ../../bedrocks/wording-rule/BEDROCK.md
