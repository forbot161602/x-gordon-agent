---
name: wording-rule
description: Requirement-level keywords (MUST, SHOULD, MAY, MUST NOT, SHOULD NOT) and behavior-trigger words, each with one fixed meaning.
---

# Wording — fixed-meaning keywords

Keywords that each carry one fixed meaning — do not swap one for a vaguer synonym.

## Rule

### Requirement levels

Write the keyword in uppercase to mark how binding a statement is:

<!-- prettier-ignore -->
| Keyword | Meaning |
|---|---|
| MUST / REQUIRED | Inviolable — breaking it is an error. |
| SHOULD / RECOMMENDED | Strong default — comply unless there is a sound, stated reason to deviate. |
| MAY / OPTIONAL | Free choice — either way is acceptable. |
| MUST NOT / NEVER | Inviolable prohibition. |
| SHOULD NOT / NOT RECOMMENDED | Strong default against — avoid unless there is a sound, stated reason to deviate. |

Based on [RFC 2119][rfc2119], narrowed to these (the rarer SHALL is dropped).

**Unmarked defaults to MUST** — in a rule or instruction, a statement with no requirement-level keyword is read as mandatory.

### Behavior triggers

These mark _when_ a rule's behavior fires — the moment, event, or condition that triggers it:

<!-- prettier-ignore -->
| Keyword | Meaning |
|---|---|
| Proactively | Act without waiting for an explicit request. |
| Before / After | The behavior runs before / after a named event. |
| When | The behavior runs while a condition holds. |

## References

- [RFC 2119][rfc2119]

[rfc2119]: https://www.rfc-editor.org/rfc/rfc2119
