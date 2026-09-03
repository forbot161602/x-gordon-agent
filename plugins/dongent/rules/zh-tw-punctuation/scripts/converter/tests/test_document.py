"""
Unit tests for the document kind — its own contract only; what it converts is
the engine's, and is covered there.
"""

import unittest

from converter.kinds import convert_document_line


class TestConvertDocumentLine(unittest.TestCase):
    """The whole line is one span, and the line's index never matters."""

    def test_whole_line_is_one_span(self) -> None:
        self.assertEqual(convert_document_line('這是中文, 結尾', 0), '這是中文，結尾')

    def test_index_is_ignored(self) -> None:
        self.assertEqual(
            convert_document_line('這是中文, 結尾', 5),
            convert_document_line('這是中文, 結尾', 0),
        )
