---
name: zh-tw-punctuation
description: "zh-TW punctuation conventions — in Chinese-led markdown content (documents, commit messages, PRs), convert ASCII , : ; ? to full-width and the ellipsis character to ASCII dots. Script + tests at convert.py / convert_test.py; design rationale at Specification.md."
---

# zh-TW punctuation — full-width

Chinese-led zh-TW prose wants full-width punctuation, not the ASCII forms. This rule sets which punctuation converts and when — applied deterministically by a script, not judged by eye.

## Builds on

MUST read and follow these first — this rule builds on them:

- [wording-rule][../../bedrocks/wording-rule/BEDROCK.md]

## Rule

In zh-TW markdown text that is Chinese-led (see [Algorithm summary][algorithm-summary]):

- ASCII `,` → 「，」
- ASCII `:` → 「：」 (including after markdown bold prefixes like `**標題**:`)
- ASCII `;` → 「；」
- ASCII `?` → 「？」
- Unicode `…` (U+2026) → ASCII `...`

## When to apply

When writing or editing any zh-TW markdown content (documents, commit messages, PRs, etc.). Also a pre-publish checkpoint before declaring work done.

## How to apply

At that checkpoint, run [convert.py][convert.py] with `--check` from the file's directory: it prints a unified diff of every line whose punctuation needs converting and exits non-zero. Convert (run without `--check`) only when it flags something. The converter is idempotent — safe to re-run.

Trust `--check`, not a visual glance: a half-width comma buried in a long zh-TW file is exactly what the eye skips, and the script's job is to catch deterministically what a writer (or model) misses.

Converting rewrites the whole file, so read what changed before keeping it. `--check` settles what qualifies, but applying it stays a judgement: restore by hand anything the conversion was never meant to touch — a false positive, a region the caller has declared off-limits — then give it the markup its own content calls for (brackets, quotes, and the like), so the next run stops flagging it.

## Algorithm summary

Per span: set aside the nested spans — matched quote, bracket and emphasis pairs — along with inline backtick spans; if any Han ideograph remains in what the span itself says, it is **Chinese-led** and every eligible punctuation in that text converts (except ASCII technical patterns). A line is the outermost span, and each nested one is judged the same way on its own text, so a Chinese aside inside an English sentence — or the reverse — keeps its own punctuation. Full algorithm, delimiter set, rationale in [Specification.md][Specification.md]; behavior matrix in [convert_test.py][convert_test.py].

## Out of scope

NEVER convert:

- Anything inside fenced code blocks or inline backticks
- ASCII technical patterns: `1,000`, `7:1`, `3:45`, `App.css:24`, `https://`, `A:B`, `cfg?.theme`, and similar (full categories in [Specification.md][Specification.md])
- ASCII `(`, `.`, `!` and any punctuation the Rule section doesn't list — they collide with English/code/URL contexts
- Pure English prose (no Han ideograph left in the span's own text)

## References

- [wording-rule][../../bedrocks/wording-rule/BEDROCK.md]
- [Specification.md][Specification.md]
- [convert.py][convert.py]
- [convert_test.py][convert_test.py]

[../../bedrocks/wording-rule/BEDROCK.md]: ../../bedrocks/wording-rule/BEDROCK.md
[algorithm-summary]: #algorithm-summary
[Specification.md]: Specification.md
[convert.py]: convert.py
[convert_test.py]: convert_test.py
