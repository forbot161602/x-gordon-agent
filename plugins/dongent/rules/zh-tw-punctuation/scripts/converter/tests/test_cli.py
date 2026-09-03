"""
Unit tests for the CLI — the diff helpers and main()'s two modes.
"""

import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

from converter import pipeline
from converter.cli import changed_lines, format_diff, main
from converter.pipeline import InputKind


def convert(text: str) -> str:
    """A whole text through the pipeline, as a plain document."""
    return pipeline.convert(text, InputKind.DOCUMENT)


def convert_lines(lines: list[str]) -> list[str]:
    """The line list through the pipeline, as a plain document."""
    return pipeline.convert_lines(lines, InputKind.DOCUMENT)


class TestChangedLines(unittest.TestCase):
    def test_numbers_each_changed_line_by_the_file(self) -> None:
        """The English line between the two keeps its comma, so the second pair
        is numbered 3 by the file — not 2 by its place among the changes."""
        original = [
            '字級只留 sm, md, lg。',
            'Use the toolbar, then reload.',
            '深色模式共用 token, 不另開檔。',
        ]
        self.assertEqual(
            changed_lines(original, convert_lines(original)),
            [
                (1, '字級只留 sm, md, lg。', '字級只留 sm，md，lg。'),
                (3, '深色模式共用 token, 不另開檔。', '深色模式共用 token，不另開檔。'),
            ],
        )

    def test_empty_when_already_full_width(self) -> None:
        original = ['這句已經是全形，結尾。']
        self.assertEqual(changed_lines(original, convert_lines(original)), [])


class TestFormatDiff(unittest.TestCase):
    def test_heads_the_file_once_then_one_hunk_per_change(self) -> None:
        """The given numbers are echoed as they are — neither renumbered from
        one nor merged into a single hunk because they sit apart."""
        pending = [
            (2, '按鈕改用主色, 邊框留白。', '按鈕改用主色，邊框留白。'),
            (5, '間距單位統一, 不混用 px。', '間距單位統一，不混用 px。'),
        ]
        self.assertEqual(
            format_diff('RULE.md', pending),
            [
                '--- RULE.md',
                '+++ RULE.md',
                '@@ -2 +2 @@',
                '-按鈕改用主色, 邊框留白。',
                '+按鈕改用主色，邊框留白。',
                '@@ -5 +5 @@',
                '-間距單位統一, 不混用 px。',
                '+間距單位統一，不混用 px。',
            ],
        )

    def test_nothing_pending_yields_nothing(self) -> None:
        """Not even the file header — a clean run says nothing at all."""
        self.assertEqual(format_diff('RULE.md', []), [])


class TestMain(unittest.TestCase):
    """Two modes: with --check it is a dry-run — print the diff, set a non-zero
    exit code, leave the file alone; without it, write the conversion in place.
    The dry-run is the deterministic gate RULE.md asks for — run it before
    commit, convert only if it flags. An invocation the parser rejects reaches
    neither mode."""

    def _invoke(self, argv: list[str]) -> tuple[int, str, str]:
        """One invocation with `argv`: its exit code, stdout, and stderr."""
        saved = sys.argv
        sys.argv = ['python3 -m scripts.converter', *argv]
        out, err = io.StringIO(), io.StringIO()
        try:
            with redirect_stdout(out), redirect_stderr(err):
                main()
            code = 0
        except SystemExit as exc:
            code = exc.code if isinstance(exc.code, int) else int(bool(exc.code))
        finally:
            sys.argv = saved
        return code, out.getvalue(), err.getvalue()

    def _run(self, argv: list[str], content: str) -> tuple[int, str, str, str]:
        """One invocation over a temp file holding `content`: its exit code,
        stdout, stderr, and what the file holds afterwards."""
        with tempfile.NamedTemporaryFile(
            'w', suffix='.md', encoding='utf-8', delete=False
        ) as f:
            f.write(content)
            path = f.name
        self.addCleanup(os.unlink, path)
        code, stdout, stderr = self._invoke([*argv, path])
        with open(path, encoding='utf-8') as f:
            after = f.read()
        return code, stdout, stderr, after

    def test_check_flags_and_keeps_file(self) -> None:
        content = '中文, 需要轉'
        code, stdout, _, after = self._run(['--check'], content)
        self.assertEqual(code, 1)         # non-zero: conversion pending
        self.assertEqual(after, content)  # file untouched
        self.assertIn('+中文，需要轉', stdout)  # the diff reached stdout

    def test_check_clean_is_silent_and_exits_zero(self) -> None:
        content = '這句已經是全形，結尾。'
        code, stdout, _, after = self._run(['--check'], content)
        self.assertEqual(code, 0)
        self.assertEqual(stdout, '')
        self.assertEqual(after, content)

    def test_no_check_writes_conversion(self) -> None:
        content = '中文, 需要轉'
        code, _, _, after = self._run([], content)
        self.assertEqual(code, 0)
        self.assertEqual(after, convert(content))
        self.assertNotEqual(after, content)

    def test_unreadable_path_is_a_usage_error(self) -> None:
        """A path the caller mistyped is rejected like any other bad argument,
        so its exit code is not the one that means a conversion is pending."""
        path = '/nonexistent/no.md'
        code, _, stderr = self._invoke(['--check', path])
        self.assertEqual(code, 2)
        self.assertIn(f'cannot read {path}', stderr)
