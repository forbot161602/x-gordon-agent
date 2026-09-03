---
name: zh-tw-punctuation
description: "zh-TW punctuation conventions — in Chinese-led markdown content (documents, commit messages, PRs), convert ASCII , : ; ? to full-width and the ellipsis character to ASCII dots. Converter and tests under scripts/converter/; design rationale at Specification.md."
---

# zh-TW punctuation — full-width

Chinese-led zh-TW prose wants full-width punctuation, not the ASCII forms. This rule sets which punctuation converts and when — applied deterministically by a script, not judged by eye.

## Builds on

MUST read and follow these first — this rule builds on them:

- [wording-rule][../../bedrocks/wording-rule/BEDROCK.md]

## Rule

The principles below cover what converts, where, and who decides. Full algorithm, delimiter set, rationale in [Specification.md][Specification.md]; behavior matrix in [the converter's tests][scripts/converter/tests/].

### 1. What converts

In zh-TW markdown text that is Chinese-led:

- ASCII `,` → 「，」
- ASCII `:` → 「：」 (including after markdown bold prefixes like `**標題**:`)
- ASCII `;` → 「；」
- ASCII `?` → 「？」
- Unicode `…` (U+2026) → ASCII `...`

### 2. What counts as prose

Per span: set aside the nested spans — matched quote, bracket and emphasis pairs — along with inline backtick spans; if any Han ideograph remains in what the span itself says, it is **Chinese-led** and every eligible punctuation in that text converts (except ASCII technical patterns). A line is the outermost span, and each nested one is judged the same way on its own text, so a Chinese aside inside an English sentence — or the reverse — keeps its own punctuation.

### 3. What the script settles, and what stays a judgement

Trust `--check`, not a visual glance: a half-width comma buried in a long zh-TW file is exactly what the eye skips, and the script's job is to catch deterministically what a writer (or model) misses.

The script settles what qualifies; applying it stays a judgement. Converting rewrites the whole file, so read what changed before keeping it: restore by hand anything the conversion was never meant to touch — a false positive, a region the caller has declared off-limits — then give it the markup its own content calls for (brackets, quotes, and the like), so the next run stops flagging it. Such a flag is usually a known edge case rather than something to reason out afresh: [Specification.md][Specification.md] tables them with the way out for each.

## When to apply

When writing or editing any zh-TW markdown content (documents, commit messages, PRs, etc.). Also a pre-publish checkpoint before declaring work done.

## How to apply

At that checkpoint, run [the converter][scripts/converter/] with `--check`: it prints a unified diff of every line whose punctuation needs converting and exits non-zero. Convert (run without `--check`) only when the flags are right. The converter is idempotent — safe to re-run.

It runs as a module — `python3 -m scripts.converter [--as <kind>] [--check] <file.md>` — from this folder, which is what `scripts.converter` resolves against; the file to check usually sits elsewhere, so give it an absolute path. `--as` takes the kind: `document` by default, `commit-message` for a commit message.

## Out of scope

NEVER convert:

- Anything inside fenced code blocks or inline backticks
- ASCII technical patterns: `1,000`, `7:1`, `3:45`, `App.css:24`, `https://`, `A:B`, `cfg?.theme`, and similar (full categories in [Specification.md][Specification.md])
- ASCII `(`, `.`, `!` and any punctuation the Rule section doesn't list — they collide with English/code/URL contexts
- Pure English prose (no Han ideograph left in the span's own text)

## References

- [wording-rule][../../bedrocks/wording-rule/BEDROCK.md]
- [Specification.md][Specification.md]
- [scripts/converter/][scripts/converter/]
- [scripts/converter/tests/][scripts/converter/tests/]

[../../bedrocks/wording-rule/BEDROCK.md]: ../../bedrocks/wording-rule/BEDROCK.md
[Specification.md]: Specification.md
[scripts/converter/]: scripts/converter/
[scripts/converter/tests/]: scripts/converter/tests/
