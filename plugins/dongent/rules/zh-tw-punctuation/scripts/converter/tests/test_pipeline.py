"""
Unit tests for the pipeline — fenced blocks, multi-line text, line pairing,
and the kind the caller declares.
"""

import unittest

from converter import pipeline
from converter.pipeline import InputKind


def convert(text: str) -> str:
    """A whole text through the pipeline, as a plain document."""
    return pipeline.convert(text, InputKind.DOCUMENT)


def convert_lines(lines: list[str]) -> list[str]:
    """The line list through the pipeline, as a plain document."""
    return pipeline.convert_lines(lines, InputKind.DOCUMENT)


# ---------------------------------------------------------------------------
# Fenced code — the fence toggles, and nothing inside it is examined
# ---------------------------------------------------------------------------


class TestFencedCode(unittest.TestCase):
    def test_fenced_code_preserves_ascii(self) -> None:
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

    def test_fenced_code_toggle_state(self) -> None:
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

    def test_ellipsis_inside_code_block_preserved(self) -> None:
        """Inside fenced code, `…` is preserved — code is sacred, consistent
        with how every other punctuation rule treats fenced code."""
        text = '```\nprint("略…")\n```'
        result = convert(text)
        self.assertIn('略…', result)
        self.assertNotIn('略...', result)


# ---------------------------------------------------------------------------
# convert_lines() — the line-list core that convert() and the CLI share
# ---------------------------------------------------------------------------


class TestConvertLines(unittest.TestCase):
    def test_one_output_line_per_input_line(self) -> None:
        """Lines that pass through untouched — a fence, its content, a blank one
        — are still emitted, which is what lets changed_lines pair the input and
        output lists by position."""
        lines = ['中文, 要轉', '```', 'a, b', '```', '']
        self.assertEqual(len(convert_lines(lines)), len(lines))

    def test_only_whitespace(self) -> None:
        lines = ['   ', '  ', '']
        self.assertEqual(convert_lines(lines), lines)


# ---------------------------------------------------------------------------
# Kind dispatch — the registry picks the converter the declared kind names
# ---------------------------------------------------------------------------


class TestKindDispatch(unittest.TestCase):
    """The same line, converted differently because the kind differs."""

    def test_document_converts_a_commit_header(self) -> None:
        self.assertEqual(
            pipeline.convert('fix(hooks): 修正注入, 補上測試', InputKind.DOCUMENT),
            'fix(hooks)：修正注入，補上測試',
        )

    def test_commit_message_keeps_the_header_separator(self) -> None:
        self.assertEqual(
            pipeline.convert('fix(hooks): 修正注入, 補上測試', InputKind.COMMIT_MESSAGE),
            'fix(hooks): 修正注入，補上測試',
        )
