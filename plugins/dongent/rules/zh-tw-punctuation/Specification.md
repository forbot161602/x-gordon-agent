---
name: zh-tw-punctuation-specification
description: Design rationale and detailed specification for the zh-tw-punctuation rule. Not a standalone rule — read RULE.md first.
---

# zh-TW punctuation — spec

Companion to [RULE.md][RULE.md]. Detailed algorithm, design choices, accepted trade-offs.

## Conversion decision

Per candidate punctuation mark, the checks run in order:

1. **ASCII technical pattern → keep half-width.** See [Skip when][skip-when] below. Fires regardless of other checks.
2. **Compute once per span: does the span's own prose have a Han ideograph?** Set aside the nested spans (see [Spans][spans]) and inline backtick spans. The remaining text is that span's "prose". A Han ideograph is `0x4E00–0x9FFF` or `0x3400–0x4DBF` — full-width punctuation does not count.
3. **If yes → convert; otherwise keep.** All-or-nothing per span: apply the mappings from [RULE.md][RULE.md].

The `…` → `...` substitution runs through this same decision, so English prose keeps its ellipsis: there it is English typography, not a zh-TW punctuation slip.

## Spans

The recursion starts at the line: a line is the outermost span, and each nested span runs the decision above on its own prose instead of inheriting the answer.

For example, in `Pick a locale (English, 中文, 日本語), then reload the page.` the bracketed list of on-screen options reads as Chinese-led and converts its commas, while the English prose around it keeps its own. When every Han sits inside a span like that, the line has no Chinese prose of its own and nothing outside converts.

Delimiter pairs that open a nested span:

<!-- prettier-ignore -->
| Delimiter | Notes |
|---|---|
| `` ` `` | Inline code. Read before anything else and copied verbatim, so a delimiter inside it opens and closes nothing |
| `"` `()` `[]` `{}` | ASCII quote and brackets |
| `「」` `『』` `（）` `《》` `【】` | CJK quotes and brackets |
| `*` `**` `***` | Emphasis. A run of stars closes only against a run of the same length |

Distinct pairs nest: `（甲（乙）丙）` closes on the last `）` and holds a nested span inside it, while a same-character pair closes on its next occurrence and so never nests. When a pair does not close:

- The delimiter is literal text and opens no span, so what it would have enclosed stays in the surrounding prose — [Edge cases][edge-cases] tables what that costs.
- A backtick is the exception: unpaired, it protects to the end of the line rather than turning literal, since a dropped closing backtick is the likely cause and leaving code alone is the safer reading.
- `'` never opens a span to begin with: in prose it is overwhelmingly an apostrophe (`it's`, `the author's`), so pairing it would invent spans that swallow whole sentences.

## Edge cases

Where the answer differs from what a reader might expect, it is accepted rather than patched — and most such cases disappear once the text follows the markup conventions it should follow anyway:

<!-- prettier-ignore -->
| Case | Example | What happens | Way out |
|---|---|---|---|
| A pair that never closes | `Toast shows （成功, 失敗) states, then fades out.` | `（` never finds `）`, so nothing is set aside — the aside's Han joins the line's prose and flips even the English comma | Close the pair and match the widths; the halves look alike, so trust the diff over the eye |
| A bare `*` before a later italic marker | `建置時忽略 *.min.css, JS *tree shaking* 仍會正常執行。` | The glob's star pairs with the italic's opening star and swallows the fragment between them, which then keeps its ASCII punctuation | Write the path in inline code — a renderer reads the bare form just as ambiguously |
| Chinese terms with nothing delimiting them | `Click 儲存 button, and returns to 使用者列表.` | Reads as Chinese-led, so its ASCII punctuation flips — only grammar-grade analysis could tell the structure is English | Italicise the foreign terms (`*儲存*`) to give each a span of its own |
| A delimiter pair broken by a hard wrap | `按鈕支援三種尺寸（sm,` then `md, lg）可切換。` | Neither half pairs, so each line is gated alone and the English list takes the Chinese gate | Soft wrap, one line per paragraph — nothing records where a wrap fell, so nothing can rejoin it |

## Why this shape

- **Set the spans aside first, then check.** Quoted / bracketed content and inline code are "non-prose" to the text around them; what's left is that text's narrative voice. CJK in the narrative voice signals Chinese-led writing.
- **Han ideograph only.** Full-width punctuation does not count, otherwise a stray 「。」 attached to an English token would fake-qualify the text.
- **Span-level, all-or-nothing.** Within one span, simpler than per-punctuation context detection, and it matches the writer's mental model: "this text is Chinese prose, so its punctuation should look Chinese." Recursing gives each aside its own answer without importing per-punctuation heuristics.
- **Neighbours come from the line, not the span.** A mark at a span's edge still sees its real neighbours — the colon in `字級（rem）: 相對單位` sees `）` — so an exemption behaves the same wherever delimiters land, and the recursion carries indexes into the line rather than slicing it.

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
- **Line-level, all-or-nothing** (the original shape): one gate per line, with delimited text dropped from the gate yet still converted by it. Simpler, but a mixed line forced one language's punctuation onto the other — an English list inside a Chinese sentence flipped, a Chinese aside inside an English one was missed. Delimiters already mark where one language stops, so recursing on them fixes both directions.

The span-level set-aside-then-check rule is simpler than the per-punctuation alternatives and avoids their failure modes.

## References

- [RULE.md][RULE.md]

[RULE.md]: RULE.md
[skip-when]: #skip-when
[spans]: #spans
[edge-cases]: #edge-cases
