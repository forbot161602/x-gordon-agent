"""
Unit tests for the engine — its predicates, and every conversion case, since the
engine is where the decisions live.
"""

import unittest

from converter.engine import (
    convert_span,
    is_ascii_technical,
    is_cjk_ideograph,
    prose_has_cjk,
)


def convert_line(text: str) -> str:
    """The engine over a whole line, the form every case below takes."""
    out_chars: list[str] = []
    convert_span(text, 0, len(text), out_chars)
    return ''.join(out_chars)


def convert_from(text: str, start: int) -> str:
    """The engine from `start` on, with everything before it copied unchanged."""
    out_chars = list(text[:start])
    convert_span(text, start, len(text), out_chars)
    return ''.join(out_chars)


# ---------------------------------------------------------------------------
# is_cjk_ideograph — the Han-range primitive the gate is built on
# ---------------------------------------------------------------------------


class TestIsCjkIdeograph(unittest.TestCase):
    def test_han_only(self) -> None:
        self.assertTrue(is_cjk_ideograph('中'))
        self.assertTrue(is_cjk_ideograph('文'))

    def test_excludes_full_width_punct(self) -> None:
        """Critical: full-width punctuation must not be classified as an
        ideograph, otherwise a stray 「。」 attached to an English token would
        fake-qualify the text as having CJK prose."""
        self.assertFalse(is_cjk_ideograph('。'))
        self.assertFalse(is_cjk_ideograph('，'))
        self.assertFalse(is_cjk_ideograph('「'))
        self.assertFalse(is_cjk_ideograph('」'))

    def test_excludes_ascii(self) -> None:
        self.assertFalse(is_cjk_ideograph('A'))
        self.assertFalse(is_cjk_ideograph('1'))
        self.assertFalse(is_cjk_ideograph(' '))
        self.assertFalse(is_cjk_ideograph(''))


class TestProseHasCjk(unittest.TestCase):
    """prose_has_cjk is the gate: set aside the nested spans — quote, bracket
    and emphasis pairs — along with inline backticks, then check whether any Han
    ideograph remains in what the span itself says."""

    def test_plain_chinese(self) -> None:
        self.assertTrue(prose_has_cjk('這是中文'))

    def test_plain_english(self) -> None:
        self.assertFalse(prose_has_cjk('pure English text'))

    def test_chinese_outside_quotes(self) -> None:
        self.assertTrue(prose_has_cjk('回答 "Yes", 然後繼續'))

    def test_chinese_only_inside_quotes(self) -> None:
        self.assertFalse(prose_has_cjk('pure English text, with quote "中文" inside.'))

    def test_chinese_only_inside_brackets(self) -> None:
        self.assertFalse(prose_has_cjk('see (中文) for details'))
        self.assertFalse(prose_has_cjk('cite 「中文」 here'))

    def test_chinese_only_inside_emphasis(self) -> None:
        """Emphasis markers open a span too, so a bold Chinese label leaves the
        surrounding prose English."""
        self.assertFalse(prose_has_cjk('**標題**: English body'))

    def test_chinese_only_inside_backticks(self) -> None:
        """Inline backtick content (typically code) is also stripped — CJK in
        a code snippet shouldn't flip the surrounding prose to Chinese-led."""
        self.assertFalse(prose_has_cjk('use `print("中文")` in code'))

    def test_full_width_punct_alone_doesnt_count(self) -> None:
        self.assertFalse(prose_has_cjk('text。'))

    def test_empty(self) -> None:
        self.assertFalse(prose_has_cjk(''))


# ---------------------------------------------------------------------------
# is_ascii_technical — every exemption, checked without going through a
# conversion
# ---------------------------------------------------------------------------


class TestAsciiTechnicalExemptions(unittest.TestCase):
    def test_is_ascii_technical_unit(self) -> None:
        """Every exemption checked directly, without going through convert_line()."""
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
# convert_line() — the line's own prose has a Han ideograph (after setting aside
# nested spans and inline backticks), so every eligible punctuation in that
# prose converts. Includes cases where the punctuation is between two English
# tokens — the gate treats them as Chinese prose context.
# ---------------------------------------------------------------------------


class TestConvertsWhenProseHasCjk(unittest.TestCase):
    def test_basic_chinese_sentence(self) -> None:
        self.assertEqual(
            convert_line('這是第一句, 這是第二句: 結束。'),
            '這是第一句，這是第二句：結束。',
        )

    def test_semicolon_and_question_mark(self) -> None:
        self.assertEqual(
            convert_line('這是分號測試; 這是問號測試? 結束。'),
            '這是分號測試；這是問號測試？結束。',
        )

    def test_markdown_bold_prefix(self) -> None:
        self.assertEqual(
            convert_line('**標題**: 接續說明, 段落結尾。'),
            '**標題**：接續說明，段落結尾。',
        )

    def test_no_space_after_bold(self) -> None:
        self.assertEqual(
            convert_line('**標題**:接續說明'),
            '**標題**：接續說明',
        )

    def test_quoted_cjk_phrase(self) -> None:
        """A quoted CJK phrase gets stripped from the prose check, but the
        surrounding 按下/然後繼續 still makes the line Chinese-led."""
        self.assertEqual(
            convert_line('按下 "確定", 然後繼續'),
            '按下 "確定"，然後繼續',
        )

    def test_english_quote_within_chinese_prose(self) -> None:
        """Strip the two quoted English words and the line's own prose
        (回答/和/兩種) remains, so it is Chinese-led."""
        self.assertEqual(
            convert_line('回答 "Yes", 和 "No" 兩種'),
            '回答 "Yes"，和 "No" 兩種',
        )

    def test_english_token_pair_in_chinese_line(self) -> None:
        """The comma sits between two English tokens, but the line's own prose
        (升級到/模式) is Chinese, so it converts."""
        self.assertEqual(
            convert_line('升級到 v2, Edit 模式。'),
            '升級到 v2，Edit 模式。',
        )

    def test_chinese_label_with_english_list(self) -> None:
        """The label makes the line Chinese-led, so the colon and every comma in
        the English list convert — an explicit choice: visual consistency within
        the line wins."""
        self.assertEqual(
            convert_line('清單: item1, item2, item3。'),
            '清單：item1，item2，item3。',
        )

    def test_letter_colon_chinese(self) -> None:
        """The exemption fires for letter:letter, letter:digit and letter:slash —
        not letter:CJK — so this colon falls through to the gate."""
        self.assertEqual(
            convert_line('代號 A:中 還沒定義'),
            '代號 A：中 還沒定義',
        )

    def test_english_structure_with_cjk_terms(self) -> None:
        """English sentence structure with Chinese UI terms inline: the CJK sits
        outside any span, so the line is Chinese-led and the comma between two
        English words converts. Accepted false positive — telling the two
        structures apart would need grammar-grade analysis."""
        self.assertEqual(
            convert_line('Click 儲存 button, and returns to 首頁.'),
            'Click 儲存 button，and returns to 首頁.',
        )


# ---------------------------------------------------------------------------
# Cases the gate deliberately does not convert: the prose is entirely English
# (no CJK ideograph outside spans and backticks).
# ---------------------------------------------------------------------------


class TestEnglishProseKeepsAscii(unittest.TestCase):
    def test_no_cjk_at_all(self) -> None:
        """All four ASCII marks on one English line, none of them touched."""
        line = 'This line has no CJK, so commas, colons: and semicolons; stay ASCII. Question? Yes.'
        self.assertEqual(convert_line(line), line)

    def test_cjk_only_inside_ascii_quotes(self) -> None:
        line = 'pure English text, with quote "中文" inside.'
        self.assertEqual(convert_line(line), line)

    def test_cjk_only_inside_brackets(self) -> None:
        line = 'see footnote (中文 note) for details'
        self.assertEqual(convert_line(line), line)

    def test_cjk_only_inside_backticks(self) -> None:
        line = 'the helper `打印("中文")`, returns void'
        self.assertEqual(convert_line(line), line)

    def test_cjk_only_inside_cjk_quotes(self) -> None:
        """Regression: this line once converted, on the strength of the 「中文」
        alone. A bold prefix and a CJK quote pair both open spans, so the prose
        left over is entirely English."""
        line = '**English Only**: This line has CJK in 「中文」 elsewhere, so nothing converts.'
        self.assertEqual(convert_line(line), line)


# ---------------------------------------------------------------------------
# convert_line() — ASCII technical patterns are kept half-width regardless of the
# gate, and wherever a delimiter falls
# ---------------------------------------------------------------------------


class TestAsciiTechnicalKept(unittest.TestCase):
    def assertSkipped(self, line: str) -> None:
        """The line contains an ASCII technical pattern that must keep half-width."""
        self.assertEqual(convert_line(line), line)

    def test_number_formatting_commas(self) -> None:
        self.assertSkipped('數字 1,000 與 1,234,567 都保留半形')

    def test_ratio_between_digits(self) -> None:
        self.assertSkipped('比例 7:1 不轉')

    def test_time_between_digits(self) -> None:
        self.assertSkipped('時間 3:45 不轉')

    def test_file_line_letter_digit(self) -> None:
        self.assertSkipped('檔案位置 App.css:24 不轉')

    def test_url_scheme_letter_slash(self) -> None:
        self.assertSkipped('URL https://example.com 不轉')

    def test_letter_colon_letter_identifier(self) -> None:
        """`A:B` letter:letter is kept half-width by the ASCII technical skip,
        even when the surrounding line has CJK prose. The comma between `)` and
        `但` falls under the gate and still converts."""
        self.assertEqual(
            convert_line('A:B 不轉 (字母之間), 但其他都可。'),
            'A:B 不轉 (字母之間)，但其他都可。',
        )

    def test_optional_chaining_question_dot(self) -> None:
        self.assertSkipped('在中文段落使用 cfg?.theme 沒問題')

    def test_technical_pattern_inside_a_span(self) -> None:
        """A span is judged on its own prose, but the exemptions apply within it
        exactly as they do outside."""
        self.assertSkipped('對比度（見 7:1）維持不變')

    def test_punctuation_next_to_a_delimiter_still_converts(self) -> None:
        """The colon opens a prose segment, yet its neighbours are still read
        from the whole line: `）` is neither digit nor letter, so no exemption
        fires and the gate converts it."""
        self.assertEqual(convert_line('中文（註）: 說明'), '中文（註）：說明')


# ---------------------------------------------------------------------------
# Nested spans — a delimited span is judged on its own prose, so an aside in
# the other language keeps its own punctuation
# ---------------------------------------------------------------------------


class TestNestedSpans(unittest.TestCase):
    def test_english_span_in_a_chinese_line(self) -> None:
        """The bracketed parameter list is English, so its comma stays ASCII
        while the Chinese prose around it converts."""
        self.assertEqual(
            convert_line('參數（epoch seconds, ge=0）不變, 見說明'),
            '參數（epoch seconds, ge=0）不變，見說明',
        )

    def test_chinese_span_in_an_english_line(self) -> None:
        """The aside is Chinese, so the comma inside it converts while the one
        in the English prose stays."""
        self.assertEqual(
            convert_line('see (深色模式, 對比度) below, page 3'),
            'see (深色模式，對比度) below, page 3',
        )

    def test_nested_spans_each_judged_on_their_own(self) -> None:
        self.assertEqual(
            convert_line('樣式表（色彩 [primary, accent] 兩組）已更新, 請重新整理'),
            '樣式表（色彩 [primary, accent] 兩組）已更新，請重新整理',
        )

    def test_quoted_english_keeps_ascii(self) -> None:
        self.assertEqual(
            convert_line('錯誤訊息是 "invalid token, retry" 這句, 要照抄'),
            '錯誤訊息是 "invalid token, retry" 這句，要照抄',
        )

    def test_same_kind_pairs_count_depth(self) -> None:
        """`（` closes on the last `）`, not the first: the outer span keeps the
        inner one, whose English list stays ASCII while the outer Chinese prose
        converts."""
        self.assertEqual(
            convert_line('設定（顏色, 含次要（accent, muted）兩種）已套用'),
            '設定（顏色，含次要（accent, muted）兩種）已套用',
        )

    def test_same_character_pairs_do_not_nest(self) -> None:
        """A quote closes on the next quote, so these read as two spans side by
        side — `draft, temp` sits in the line's own prose and converts with it."""
        self.assertEqual(
            convert_line('他說 "先存 "draft, temp" 再送" 就好'),
            '他說 "先存 "draft，temp" 再送" 就好',
        )

    def test_pairing_never_crosses_a_span(self) -> None:
        """Each closing search is bounded by the span it runs in, so the `*`
        inside the bracket cannot pair with the one after it. Were it able to,
        `fallback, none）` would become an English span and keep its comma."""
        self.assertEqual(
            convert_line('設定（預設 auto *fallback, none）*見下方備註'),
            '設定（預設 auto *fallback，none）*見下方備註',
        )

    def test_unmatched_delimiter_is_literal(self) -> None:
        """Everything after the opener is English, so the writer expects it to
        be left alone — but with no `）` there is no span, and the list joins the
        Chinese prose ahead of it and converts. Adding the closer is the whole
        difference."""
        self.assertEqual(convert_line('字級改用 rem（sm, md, lg'), '字級改用 rem（sm，md，lg')

    def test_mismatched_delimiter_widths_never_pair(self) -> None:
        """`（` closes only against `）`, so a half-width partner leaves both
        literal: nothing is set aside, the aside's Han counts toward the line's
        gate, and even the English comma outside converts. The two forms look
        alike on screen, so only the diff catches it."""
        self.assertEqual(
            convert_line('Toast shows （成功, 失敗) states, then fades out.'),
            'Toast shows （成功，失敗) states，then fades out.',
        )
        self.assertEqual(
            convert_line('Toast shows （成功, 失敗） states, then fades out.'),
            'Toast shows （成功，失敗） states, then fades out.',
        )

    def test_emphasis_markers_of_every_width(self) -> None:
        """`*`, `**` and `***` each close against a run of their own length, and
        each span is then judged on its own — the Chinese one converts, the two
        English ones do not, and the prose holding them converts too."""
        self.assertEqual(
            convert_line('主題 **深色, 淺色** 與狀態 *hover, focus* 在 ***sm, md*** 都要測, 其餘略過'),
            '主題 **深色，淺色** 與狀態 *hover, focus* 在 ***sm, md*** 都要測，其餘略過',
        )

    def test_unpaired_star_is_literal(self) -> None:
        """A glob's `*` never closes, so it opens no span and the line reads as
        one piece of Chinese prose."""
        self.assertEqual(convert_line('文件只收 *.md, 其餘略過'), '文件只收 *.md，其餘略過')

    def test_bare_star_pairs_with_a_later_italic_marker(self) -> None:
        """Known edge: a bare `*` closes against the next run of the same
        length, so a glob and a later italic marker pair up and swallow what
        sits between them — here an English fragment, which then keeps its ASCII
        comma. Inline code is immune, and markdown-convention asks for a path to
        be written that way regardless; a renderer reads the bare form just as
        ambiguously."""
        self.assertEqual(
            convert_line('建置時忽略 *.min.css, JS *tree shaking* 仍會正常執行。'),
            '建置時忽略 *.min.css, JS *tree shaking* 仍會正常執行。',
        )
        self.assertEqual(
            convert_line('建置時忽略 `*.min.css`, JS *tree shaking* 仍會正常執行。'),
            '建置時忽略 `*.min.css`，JS *tree shaking* 仍會正常執行。',
        )

    def test_bold_chinese_label_with_english_body_keeps_ascii(self) -> None:
        """The label sits in its own span, so what follows the colon decides
        the line — here English, which keeps its ASCII punctuation."""
        line = '**標題**: English content, here'
        self.assertEqual(convert_line(line), line)


# ---------------------------------------------------------------------------
# Inline backticks — content inside is never converted, and they are read
# before any delimiter
# ---------------------------------------------------------------------------


class TestInlineBackticks(unittest.TestCase):
    def test_inline_backtick_preserves_ascii(self) -> None:
        self.assertEqual(
            convert_line('改完直接 `git add .; git commit -m "fix: 版面"` 送出, 不用等。'),
            '改完直接 `git add .; git commit -m "fix: 版面"` 送出，不用等。',
        )

    def test_backticks_beat_delimiters(self) -> None:
        """Inline code is read first, so a bracket inside it opens no span and
        its punctuation survives whatever the surrounding prose says."""
        self.assertEqual(
            convert_line('參數寫成 `(a, b)` 就好, 不用改'),
            '參數寫成 `(a, b)` 就好，不用改',
        )

    def test_closer_inside_code_does_not_close_a_span(self) -> None:
        """The delimiter search steps over backtick spans, so the `)` in
        `init()` leaves the outer bracket open until the real one."""
        self.assertEqual(
            convert_line('注意 (先呼叫 `init()` 再送出, 順序不能反) 完成'),
            '注意 (先呼叫 `init()` 再送出，順序不能反) 完成',
        )

    def test_unpaired_backtick_protects_to_end_of_line(self) -> None:
        """An unpaired backtick reads as a dropped closing one, so the rest of
        the line is left alone — the comma before it still converts."""
        self.assertEqual(
            convert_line('安裝步驟, 先跑 `npm ci, 然後 npm test'),
            '安裝步驟，先跑 `npm ci, 然後 npm test',
        )


# ---------------------------------------------------------------------------
# Ellipsis — same gate as , : ; ?
# ---------------------------------------------------------------------------


class TestEllipsis(unittest.TestCase):
    def test_unicode_to_ascii_dots(self) -> None:
        self.assertEqual(convert_line('這裡略… 還有更多…'), '這裡略... 還有更多...')

    def test_pure_english_line_keeps_ellipsis(self) -> None:
        """No Han ideograph in the prose → the line is English, where `…` is
        legitimate typography rather than a zh-TW punctuation slip."""
        line = 'Requirement levels (MUST / SHOULD / …) are uppercase.'
        self.assertEqual(convert_line(line), line)

    def test_ellipsis_follows_its_own_span(self) -> None:
        """English line with a Chinese aside: the ellipsis inside the aside
        converts, the one in the English prose stays."""
        self.assertEqual(convert_line('English (中文…) tail…'), 'English (中文...) tail…')

    def test_ellipsis_inside_inline_backtick_preserved(self) -> None:
        """Inline backticks protect it too; the `…` outside one still converts."""
        self.assertEqual(
            convert_line('使用 `略…` 後接 ellipsis…'),
            '使用 `略…` 後接 ellipsis...',
        )


# ---------------------------------------------------------------------------
# Whitespace cleanup — a space left after a full-width mark is the residue
# of a half-done conversion, so the conversion takes it too
# ---------------------------------------------------------------------------


class TestWhitespaceCleanup(unittest.TestCase):
    def test_trailing_space_after_full_width_stripped(self) -> None:
        """A full-width mark followed by a space is the residue of a half-done
        conversion; the cleanup takes the space with it."""
        self.assertEqual(convert_line('這句， 結尾'), '這句，結尾')
        self.assertEqual(convert_line('標題： 內容'), '標題：內容')

    def test_multiple_trailing_spaces_after_full_width_stripped(self) -> None:
        """Multiple consecutive spaces after a full-width punctuation are all
        stripped — inline check beats the old single-pass `str.replace` which
        only stripped one space at a time."""
        self.assertEqual(convert_line('這句，  結尾'), '這句，結尾')

    def test_space_before_a_span_is_stripped(self) -> None:
        """The cleanup sees the character emitted before it even across a span
        boundary, so the space between a converted comma and a span opener goes
        the same way as anywhere else."""
        self.assertEqual(
            convert_line('已更新樣式, （含深色模式）請重新整理'),
            '已更新樣式，（含深色模式）請重新整理',
        )


# ---------------------------------------------------------------------------
# Idempotency — converting an already-converted line changes nothing
# ---------------------------------------------------------------------------


class TestIdempotency(unittest.TestCase):
    def test_already_full_width_unchanged(self) -> None:
        line = '這句已經是全形，結尾。'
        self.assertEqual(convert_line(line), line)

    def test_double_apply_stable(self) -> None:
        original = '這是第一句, 第二句: 結束。'
        once = convert_line(original)
        self.assertEqual(once, convert_line(once))

    def test_double_apply_stable_across_spans(self) -> None:
        """Two languages, two gates, one converted result — re-running must not
        drift either way."""
        original = 'set (行高, 字距) first, 其他沿用預設'
        once = convert_line(original)
        self.assertEqual(once, convert_line(once))


# ---------------------------------------------------------------------------
# Boundary inputs — empty text, punctuation at a line edge
# ---------------------------------------------------------------------------


class TestBoundaryInputs(unittest.TestCase):
    def test_empty_string(self) -> None:
        self.assertEqual(convert_line(''), '')

    def test_punctuation_at_line_start_and_end(self) -> None:
        # `:` at the very start of a CJK-prose line still converts.
        self.assertEqual(convert_line(': 開始'), '：開始')
        # `,` at the very end of a CJK-prose line still converts.
        self.assertEqual(convert_line('結尾,'), '結尾，')


# ---------------------------------------------------------------------------
# convert_span() over part of a line — the range carries its own gate, and what
# lies outside it is never read
# ---------------------------------------------------------------------------


class TestPartialRange(unittest.TestCase):
    """A caller converting a range gets that range judged on its own prose."""

    def test_range_converts_while_the_text_before_it_is_left_alone(self) -> None:
        text = '標題: 這是中文, 結尾'
        self.assertEqual(convert_from(text, text.index('這是')), '標題: 這是中文，結尾')

    def test_english_range_keeps_ascii_though_the_line_is_chinese_led(self) -> None:
        """The gate reads the range, not the line, so the comma stays half-width."""
        text = '標題: set the width, then ship'
        self.assertEqual(
            convert_from(text, text.index('set')),
            '標題: set the width, then ship',
        )
