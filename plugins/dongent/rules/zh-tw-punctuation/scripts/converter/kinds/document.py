"""
The document kind: plain prose, with no structure to carve out.
"""

from ..engine import convert_span


def convert_document_line(line: str, _: int) -> str:
    """One line of a plain document: the whole line is one span, judged on its
    own prose."""
    out_chars: list[str] = []
    convert_span(line, 0, len(line), out_chars)
    return ''.join(out_chars)
