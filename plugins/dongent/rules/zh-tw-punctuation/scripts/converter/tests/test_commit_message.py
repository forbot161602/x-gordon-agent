"""
Unit tests for the commit-message kind — the header prefix it protects.
"""

import unittest

from converter.kinds import convert_commit_message_line


class TestConvertCommitMessageLine(unittest.TestCase):
    """Matched by shape and position alone, never against a list of type names."""

    def test_header_separator_kept_while_the_description_converts(self) -> None:
        self.assertEqual(
            convert_commit_message_line('fix(hooks): 修正注入, 補上測試', 0),
            'fix(hooks): 修正注入，補上測試',
        )

    def test_type_needs_no_scope(self) -> None:
        self.assertEqual(
            convert_commit_message_line('feat: 加上旗標, 補測試', 0),
            'feat: 加上旗標，補測試',
        )

    def test_type_is_not_checked_against_a_vocabulary(self) -> None:
        """A project extends the type list at will, so shape is what decides."""
        self.assertEqual(
            convert_commit_message_line('wip: 還沒好, 先存著', 0),
            'wip: 還沒好，先存著',
        )

    def test_body_line_is_not_a_header(self) -> None:
        self.assertEqual(
            convert_commit_message_line('這段是 body, 照樣轉', 2),
            '這段是 body，照樣轉',
        )

    def test_colon_without_a_following_space_is_not_a_header(self) -> None:
        self.assertEqual(
            convert_commit_message_line('fix(hooks):修正注入', 0),
            'fix(hooks)：修正注入',
        )

    def test_chinese_led_line_holding_a_colon_is_not_a_header(self) -> None:
        """The match is anchored, so a line opening on Han never qualifies."""
        self.assertEqual(
            convert_commit_message_line('以下是 summary: 三點', 0),
            '以下是 summary：三點',
        )
