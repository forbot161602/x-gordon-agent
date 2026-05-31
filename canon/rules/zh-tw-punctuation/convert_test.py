#!/usr/bin/env python3
"""
Unit tests for the converter — behavior matrix in executable form.

Run: python3 convert_test.py -v

When a new edge case turns up, add a failing test here first, then update
the converter until it passes.
"""

import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

# Allow running directly: `python3 convert_test.py`
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from convert import (
    is_cjk_ideograph,
    prose_has_cjk,
    is_ascii_technical,
    convert,
    changed_lines,
    main,
)


# ---------------------------------------------------------------------------
# Primitives
# ---------------------------------------------------------------------------


class TestPrimitives(unittest.TestCase):
    def test_is_cjk_ideograph_han_only(self):
        self.assertTrue(is_cjk_ideograph('中'))
        self.assertTrue(is_cjk_ideograph('文'))

    def test_is_cjk_ideograph_excludes_full_width_punct(self):
        # Critical: full-width punctuation must NOT be classified as ideographs,
        # otherwise a stray 「。」 attached to an English token would fake-qualify
        # the line as having CJK prose.
        self.assertFalse(is_cjk_ideograph('。'))
        self.assertFalse(is_cjk_ideograph('，'))
        self.assertFalse(is_cjk_ideograph('「'))
        self.assertFalse(is_cjk_ideograph('」'))

    def test_is_cjk_ideograph_excludes_ascii(self):
        self.assertFalse(is_cjk_ideograph('A'))
        self.assertFalse(is_cjk_ideograph('1'))
        self.assertFalse(is_cjk_ideograph(' '))
        self.assertFalse(is_cjk_ideograph(''))


class TestProseHasCjk(unittest.TestCase):
    """prose_has_cjk is the line-level gate: strip matched quote/bracket pairs
    and inline backticks, then check whether any Han ideograph remains."""

    def test_plain_chinese(self):
        self.assertTrue(prose_has_cjk('這是中文'))

    def test_plain_english(self):
        self.assertFalse(prose_has_cjk('pure English text'))

    def test_chinese_outside_quotes(self):
        self.assertTrue(prose_has_cjk('回答 "Yes", 然後繼續'))

    def test_chinese_only_inside_quotes(self):
        """If every CJK ideograph sits inside a quote/bracket, the prose is
        effectively English — line shouldn't trigger conversion."""
        self.assertFalse(prose_has_cjk('pure English text, with quote "中文" inside.'))

    def test_chinese_only_inside_brackets(self):
        self.assertFalse(prose_has_cjk('see (中文) for details'))
        self.assertFalse(prose_has_cjk('cite 「中文」 here'))

    def test_chinese_inside_inline_backticks(self):
        """Inline backtick content (typically code) is also stripped — CJK in
        a code snippet shouldn't flip the surrounding prose to dominant."""
        self.assertFalse(prose_has_cjk('use `print("中文")` in code'))

    def test_full_width_punct_alone_doesnt_count(self):
        """Trailing 「。」 etc. are NOT ideographs; a line with only full-width
        punctuation does not count as having CJK prose."""
        self.assertFalse(prose_has_cjk('text。'))

    def test_empty(self):
        self.assertFalse(prose_has_cjk(''))


# ---------------------------------------------------------------------------
# convert() — ASCII technical patterns are kept half-width regardless of the
# line-level gate
# ---------------------------------------------------------------------------


class TestAsciiTechnicalKept(unittest.TestCase):
    def assertSkipped(self, line):
        """The line contains an ASCII technical pattern that must keep half-width."""
        self.assertEqual(convert(line), line)

    def test_number_formatting_commas(self):
        self.assertSkipped('數字 1,000 與 1,234,567 都保留半形')

    def test_ratio_between_digits(self):
        self.assertSkipped('比例 7:1 不轉')

    def test_time_between_digits(self):
        self.assertSkipped('時間 3:45 不轉')

    def test_file_line_letter_digit(self):
        self.assertSkipped('檔案位置 App.css:24 不轉')

    def test_url_scheme_letter_slash(self):
        self.assertSkipped('URL https://example.com 不轉')

    def test_letter_colon_letter_identifier(self):
        """`A:B` letter:letter is kept half-width by the ASCII technical skip,
        even when the surrounding line has CJK prose. The comma between `)`
        and `但` falls under the line-level rule and still converts."""
        self.assertEqual(
            convert('A:B 不轉 (字母之間), 但其他都可。'),
            'A:B 不轉 (字母之間)，但其他都可。',
        )

    def test_letter_colon_letter_multichar(self):
        self.assertEqual(
            convert('Tab:Detail 在中文段落內: 應保留半形。'),
            'Tab:Detail 在中文段落內：應保留半形。',
        )

    def test_optional_chaining_question_dot(self):
        self.assertSkipped('在中文段落使用 cfg?.theme 沒問題')

    def test_is_ascii_technical_unit(self):
        # Direct primitive checks.
        self.assertTrue(is_ascii_technical(',', '1', '0'))
        self.assertFalse(is_ascii_technical(',', '。', '中'))
        self.assertTrue(is_ascii_technical(':', '7', '1'))
        self.assertTrue(is_ascii_technical(':', 'A', 'B'))
        self.assertTrue(is_ascii_technical(':', 's', '/'))
        self.assertTrue(is_ascii_technical(':', 'e', '2'))
        self.assertFalse(is_ascii_technical(':', '中', '文'))
        self.assertTrue(is_ascii_technical('?', 'g', '.'))
        self.assertFalse(is_ascii_technical('?', '嗎', ' '))


# ---------------------------------------------------------------------------
# convert() — line's prose has a Han ideograph (after stripping matched
# quote/bracket pairs and inline backticks), so every eligible punctuation
# in the line converts to full-width. Includes cases where the punctuation
# is between two English tokens — the line-level rule treats them as
# Chinese prose context.
# ---------------------------------------------------------------------------


class TestConvertsWhenProseHasCjk(unittest.TestCase):
    def test_basic_chinese_sentence(self):
        self.assertEqual(
            convert('這是第一句, 這是第二句: 結束。'),
            '這是第一句，這是第二句：結束。',
        )

    def test_markdown_bold_prefix(self):
        self.assertEqual(
            convert('**標題**: 接續說明, 段落結尾。'),
            '**標題**：接續說明，段落結尾。',
        )

    def test_all_four_punctuation(self):
        self.assertEqual(
            convert('這是分號測試; 這是問號測試? 結束。'),
            '這是分號測試；這是問號測試？結束。',
        )

    def test_chinese_label_with_chinese_value(self):
        self.assertEqual(
            convert('本次決定: 採方案 A。'),
            '本次決定：採方案 A。',
        )

    def test_no_space_after_bold(self):
        """No whitespace between `**標題**` and the colon — still converts."""
        self.assertEqual(
            convert('**標題**:接續說明'),
            '**標題**：接續說明',
        )

    def test_quoted_cjk_phrase(self):
        """A quoted CJK phrase gets stripped from the prose check, but the
        surrounding 按下/然後繼續 still makes the line dominant."""
        self.assertEqual(
            convert('按下 "確定", 然後繼續'),
            '按下 "確定"，然後繼續',
        )

    def test_english_token_pair_in_chinese_line(self):
        """`升級到 v2, Edit 模式。` — comma sits between English tokens v2/Edit,
        but the line's prose (升級到/模式) is Chinese → convert."""
        self.assertEqual(
            convert('升級到 v2, Edit 模式。'),
            '升級到 v2，Edit 模式。',
        )

    def test_chinese_label_with_english_list(self):
        """`清單: item1, item2, item3。` — prose 清單 makes the line dominant,
        so the colon AND every comma in the English list convert. Explicit
        rule choice: visual consistency within the line wins."""
        self.assertEqual(
            convert('清單: item1, item2, item3。'),
            '清單：item1，item2，item3。',
        )

    def test_long_bold_label_with_chinese_value(self):
        """`**設定 標籤 detail row**: 描述。` — prose has 設定/標籤/描述 → convert."""
        self.assertEqual(
            convert('**設定 標籤 detail row**: 描述。'),
            '**設定 標籤 detail row**：描述。',
        )

    def test_english_quote_within_chinese_prose(self):
        """`回答 "Yes", 和 "No" 兩種` — strip "Yes"/"No" → 回答/和/兩種 remain →
        line is dominant → convert."""
        self.assertEqual(
            convert('回答 "Yes", 和 "No" 兩種'),
            '回答 "Yes"，和 "No" 兩種',
        )

    def test_letter_colon_chinese_converts(self):
        """`代號 A:中` — line is dominant. ASCII technical skip only fires for
        letter:letter / letter:digit / letter:slash — not letter:CJK — so the
        colon falls through to the line-level rule and converts."""
        self.assertEqual(
            convert('代號 A:中 還沒定義'),
            '代號 A：中 還沒定義',
        )

    def test_english_structure_with_cjk_terms_converts(self):
        """`Click 儲存 button, and returns to 首頁.` — English sentence structure
        with Chinese UI terms inline. Line has CJK outside quotes/brackets →
        line is dominant → convert, even though the comma actually sits between
        two English words. Documented and accepted false positive: telling
        English-led vs Chinese-led sentence structure apart would need
        grammar-grade analysis."""
        self.assertEqual(
            convert('Click 儲存 button, and returns to 首頁.'),
            'Click 儲存 button，and returns to 首頁.',
        )


# ---------------------------------------------------------------------------
# Cases the line-level rule deliberately does NOT convert: prose is entirely
# English (no CJK ideograph outside quotes/brackets/backticks).
# ---------------------------------------------------------------------------


class TestNotConverted(unittest.TestCase):
    def test_chinese_only_inside_quotes(self):
        """English sentence quoting a CJK phrase — strip the quoted region and
        nothing remains, so the line is not dominant."""
        self.assertEqual(
            convert('pure English text, with quote "中文" inside.'),
            'pure English text, with quote "中文" inside.',
        )

    def test_chinese_only_inside_brackets(self):
        self.assertEqual(
            convert('see footnote (中文 note) for details'),
            'see footnote (中文 note) for details',
        )

    def test_chinese_only_inside_backticks(self):
        """CJK in inline code shouldn't make the surrounding prose convert."""
        self.assertEqual(
            convert('the helper `打印("中文")`, returns void'),
            'the helper `打印("中文")`, returns void',
        )


# ---------------------------------------------------------------------------
# Bug 1: English-dominant line with quoted CJK — must NOT convert
# ---------------------------------------------------------------------------


class TestBug1EnglishDominant(unittest.TestCase):
    def test_english_with_quoted_cjk_fragment(self):
        """The line has CJK only inside `「中文」`. prose_has_cjk strips that
        and finds no Han ideograph in the remaining prose → line is not
        dominant → no punctuation converts despite 「中文」 living on the line."""
        line = '**English Only**: This line has CJK in 「中文」 elsewhere, so the colon converts.'
        self.assertEqual(convert(line), line)

    def test_pure_english_line(self):
        line = 'This line has no CJK, so commas, colons: and semicolons; stay ASCII. Question? Yes.'
        self.assertEqual(convert(line), line)


# ---------------------------------------------------------------------------
# Code blocks and backticks — content inside must never be converted
# ---------------------------------------------------------------------------


class TestCodeBlocks(unittest.TestCase):
    def test_fenced_code_preserves_ascii(self):
        text = (
            '中文段落, 後續說明:\n'
            '```python\n'
            'def foo(a, b):\n'
            '    return a, b  # 不該被轉\n'
            '```\n'
            '結束。'
        )
        result = convert(text)
        # Outside the fence — line has CJK prose, so comma and colon convert.
        self.assertIn('中文段落，後續說明：', result)
        # Inside the fence — every ASCII punctuation stays.
        self.assertIn('def foo(a, b):', result)
        self.assertIn('return a, b  # 不該被轉', result)

    def test_inline_backtick_preserves_ascii(self):
        self.assertEqual(
            convert('使用 `npm install, npm run` 安裝, 跑 `make: test:unit` 測試。'),
            '使用 `npm install, npm run` 安裝，跑 `make: test:unit` 測試。',
        )

    def test_fenced_code_toggle_state(self):
        # Two separate fences in one document — the second fence must reopen, not stay open.
        text = (
            '前段, 中文。\n'
            '```\n'
            'a, b\n'
            '```\n'
            '中段, 中文。\n'
            '```\n'
            'c, d\n'
            '```\n'
            '後段, 中文。'
        )
        result = convert(text)
        self.assertIn('前段，中文。', result)
        self.assertIn('a, b', result)
        self.assertIn('中段，中文。', result)
        self.assertIn('c, d', result)
        self.assertIn('後段，中文。', result)


# ---------------------------------------------------------------------------
# Ellipsis — unconditional substitution
# ---------------------------------------------------------------------------


class TestEllipsis(unittest.TestCase):
    def test_unicode_to_ascii_dots(self):
        self.assertEqual(convert('這裡略… 還有更多…'), '這裡略... 還有更多...')

    def test_ellipsis_inside_code_block_preserved(self):
        """Inside fenced code, `…` is preserved — code is sacred, consistent
        with how every other punctuation rule treats fenced code."""
        text = '```\nprint("略…")\n```'
        result = convert(text)
        self.assertIn('略…', result)
        self.assertNotIn('略...', result)

    def test_ellipsis_inside_inline_backtick_preserved(self):
        """Same rule for inline backticks; `…` outside the backtick still converts."""
        self.assertEqual(
            convert('使用 `略…` 後接 ellipsis…'),
            '使用 `略…` 後接 ellipsis...',
        )


# ---------------------------------------------------------------------------
# Idempotency and whitespace cleanup
# ---------------------------------------------------------------------------


class TestIdempotency(unittest.TestCase):
    def test_already_full_width_unchanged(self):
        line = '這句已經是全形，結尾。'
        self.assertEqual(convert(line), line)

    def test_double_apply_stable(self):
        original = '這是第一句, 第二句: 結束。'
        once = convert(original)
        twice = convert(once)
        self.assertEqual(once, twice)

    def test_trailing_space_after_full_width_stripped(self):
        """The inline cleanup strips the leftover space when ASCII-style 「全形 + space」
        was halfway converted."""
        self.assertEqual(convert('這句， 結尾'), '這句，結尾')
        self.assertEqual(convert('標題： 內容'), '標題：內容')

    def test_multiple_trailing_spaces_after_full_width_stripped(self):
        """Multiple consecutive spaces after a full-width punctuation are all
        stripped — inline check beats the old single-pass `str.replace` which
        only stripped one space at a time."""
        self.assertEqual(convert('這句，  結尾'), '這句，結尾')


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases(unittest.TestCase):
    def test_empty_string(self):
        self.assertEqual(convert(''), '')

    def test_only_whitespace(self):
        self.assertEqual(convert('   \n  \n'), '   \n  \n')

    def test_zero_cjk_line_unchanged(self):
        line = 'pure ASCII, no CJK at all.'
        self.assertEqual(convert(line), line)

    def test_punctuation_at_line_start_and_end(self):
        # `:` at the very start of a CJK-prose line still converts.
        self.assertEqual(convert(': 開始'), '：開始')
        # `,` at the very end of a CJK-prose line still converts.
        self.assertEqual(convert('結尾,'), '結尾，')


# ---------------------------------------------------------------------------
# CLI — changed_lines() and the --check (dry-run) mode
# ---------------------------------------------------------------------------


class TestChangedLines(unittest.TestCase):
    def test_reports_only_changed_line_numbers(self):
        original = '純中文\n中文, 逗號\n結尾'
        self.assertEqual(changed_lines(original, convert(original)), [2])

    def test_empty_when_already_full_width(self):
        original = '這句已經是全形，結尾。'
        self.assertEqual(changed_lines(original, convert(original)), [])


class TestCheckMode(unittest.TestCase):
    """--check is a dry-run: report the lines that would change, set a non-zero
    exit code, never write the file. This is the deterministic gate RULE.md
    asks for — run before commit, convert only if it flags."""

    def _run(self, argv, content):
        with tempfile.NamedTemporaryFile(
            'w', suffix='.md', encoding='utf-8', delete=False
        ) as f:
            f.write(content)
            path = f.name
        self.addCleanup(os.unlink, path)
        saved = sys.argv
        sys.argv = ['convert.py', *argv, path]
        out = io.StringIO()
        try:
            with redirect_stdout(out):
                main()
            code = 0
        except SystemExit as exc:
            code = exc.code if isinstance(exc.code, int) else int(bool(exc.code))
        finally:
            sys.argv = saved
        with open(path, encoding='utf-8') as f:
            after = f.read()
        return code, out.getvalue(), after

    def test_check_flags_and_keeps_file(self):
        content = '中文, 需要轉'
        code, stdout, after = self._run(['--check'], content)
        self.assertEqual(code, 1)         # non-zero: conversion pending
        self.assertEqual(after, content)  # file untouched
        self.assertIn('would convert', stdout)

    def test_check_clean_exits_zero(self):
        content = '這句已經是全形，結尾。'
        code, _, after = self._run(['--check'], content)
        self.assertEqual(code, 0)
        self.assertEqual(after, content)

    def test_no_check_writes_conversion(self):
        content = '中文, 需要轉'
        code, _, after = self._run([], content)
        self.assertEqual(code, 0)
        self.assertEqual(after, convert(content))
        self.assertNotEqual(after, content)


if __name__ == '__main__':
    unittest.main(verbosity=2)
