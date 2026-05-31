---
name: zh-tw-punctuation-specification
description: Design rationale and detailed specification for the zh-tw-punctuation rule. Not a standalone rule — read RULE.md first.
---

# zh-TW punctuation — spec

Companion to [RULE.md][RULE.md]. Detailed algorithm, design choices, accepted trade-offs.

## Conversion decision

Per candidate ASCII punctuation, three checks in order:

1. **ASCII technical pattern → keep half-width.** See [Skip when][skip-when] below. Fires regardless of other checks.
2. **Compute once per line: does the prose have a Han ideograph?** Strip matched quote/bracket pairs (`"..."`, `()`, `[]`, `{}`, `「」`, `『』`, `（）`, `《》`, `【】`) and inline backtick spans from the line. The remaining text is the "prose". A Han ideograph is `0x4E00–0x9FFF` or `0x3400–0x4DBF` — full-width punctuation does NOT count.
3. **If yes → convert; otherwise keep.** All-or-nothing per line: apply the four ASCII mappings from [RULE.md][RULE.md].

The `…` → `...` substitution is a flat substitution outside this decision — see [RULE.md][RULE.md].

## Why this shape

- **Strip first, then check.** Quoted / bracketed content and inline code are "non-prose"; what's left is the narrative voice. CJK in the narrative voice signals Chinese-led writing.
- **Han ideograph only.** Full-width punctuation must not count, otherwise a stray 「。」 attached to an English token would fake-qualify the line.
- **Line-level, all-or-nothing.** Simpler than per-punctuation context detection and matches the writer's mental model: "this line is Chinese prose, so its punctuation should look Chinese."
- **Accepted false positive.** Lines that are English in structure but include Chinese terms inline (e.g. `Click 儲存 button, and returns to 首頁.`) still flip — the rule can't tell English-led from Chinese-led structure without grammar-grade analysis.
- **English sentence with quoted CJK stays English.** A line like `**English Only**: This line has CJK in 「中文」 elsewhere, ...` strips the quoted CJK and finds no remaining ideograph → not Chinese-led → punctuation stays half-width.

## Skip when

ASCII technical patterns kept half-width:

- `,` between digits → number formatting (`1,000`)
- `:` between digits → ratio or time (`7:1`, `3:45`)
- `:` letter before, digit or `/` after → file-line (`App.css:24`) or URL scheme (`https://`)
- `:` letter before, letter after → ASCII identifier (`A:B`, `Tab:Detail`, `key:value`)
- `?` followed by `.` → optional chaining (`cfg?.theme`)

## Considered alternatives

- **Ratio threshold** (line has X% Chinese chars → convert): tried; produced false positives in long mostly-English lines that quoted CJK + false negatives in short lines where the threshold rejected legitimate Chinese-led prose.
- **Per-punctuation flanked-by-CJK detection**: tried; rejected legitimate cases like `升級到 v2, Edit 模式。` where the comma sat between English tokens in otherwise Chinese-led prose.

The line-level strip-then-check rule is simpler and avoids both failure modes.

## References

- [RULE.md][RULE.md]

[RULE.md]: RULE.md
[skip-when]: #skip-when
