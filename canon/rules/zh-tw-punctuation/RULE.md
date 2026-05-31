---
name: zh-tw-punctuation
description: "zh-TW punctuation conventions — on Chinese-led lines in markdown content (documents, commit messages, PRs), convert ASCII , : ; ? to full-width; replace … with ... outside backticks. Script + tests at convert.py / convert_test.py; design rationale at Specification.md."
---

# zh-TW punctuation — full-width

## Rule

On zh-TW markdown lines that are Chinese-led (see [Algorithm summary][algorithm-summary]):

- ASCII `,` → 「，」
- ASCII `:` → 「：」 (including after markdown bold prefixes like `**標題**:`)
- ASCII `;` → 「；」
- ASCII `?` → 「？」

Plus a substitution that ignores the Chinese-led check (still respects backtick / fenced-code):

- Unicode `…` (U+2026) → ASCII `...`

## When to apply

When writing or editing any zh-TW markdown content (documents, commit messages, PRs, etc.). Also a pre-publish checkpoint before declaring work done.

## How to apply

At that checkpoint, run [convert.py][convert.py] with `--check` from the file's directory: it reports any punctuation that should be full-width and exits non-zero. Convert (run without `--check`) only when it flags something.

Trust `--check`, not a visual glance: a half-width comma buried in a long zh-TW file is exactly what the eye skips, and the script's job is to catch deterministically what a writer (or model) misses. The converter is idempotent — safe to re-run.

## Algorithm summary

Per line: strip matched quote/bracket pairs and inline backtick spans; if any Han ideograph remains in the prose, the line is **Chinese-led** and every eligible ASCII punctuation in it converts to full-width (except ASCII technical patterns). Full algorithm, bracket set, rationale in [Specification.md][Specification.md]; behavior matrix in [convert_test.py][convert_test.py].

## Out of scope

Never convert:

- Anything inside fenced code blocks or inline backticks
- ASCII technical patterns: `1,000`, `7:1`, `3:45`, `App.css:24`, `https://`, `A:B`, `cfg?.theme`, and similar (full categories in Specification.md)
- ASCII `(`, `.`, `!` and any punctuation outside the listed four — they collide with English/code/URL contexts
- Pure English lines (no Han ideograph in prose after stripping)

## References

- [Specification.md][Specification.md]
- [convert.py][convert.py]
- [convert_test.py][convert_test.py]

[algorithm-summary]: #algorithm-summary
[Specification.md]: Specification.md
[convert.py]: convert.py
[convert_test.py]: convert_test.py
