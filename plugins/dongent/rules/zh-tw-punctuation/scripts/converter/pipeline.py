"""
The pipeline: pick the line converter the declared kind names, then drive every
line of the input through it.
"""

from collections.abc import Callable
from enum import Enum

from .kinds import convert_commit_message_line, convert_document_line


class InputKind(Enum):
    """What kind of content the input holds. The caller declares it — the text
    never implies it."""

    DOCUMENT = 'document'
    COMMIT_MESSAGE = 'commit-message'

# What converts one line, given the line and its index in the input.
_LineConverter = Callable[[str, int], str]

# One line converter per kind. A kind's whole departure from plain-document
# behaviour lives inside its own converter, so nothing else branches on the
# kind — adding a kind means adding an entry here and the function it names.
_LINE_CONVERTERS: dict[InputKind, _LineConverter] = {
    InputKind.DOCUMENT: convert_document_line,
    InputKind.COMMIT_MESSAGE: convert_commit_message_line,
}


def convert_lines(lines: list[str], kind: InputKind) -> list[str]:
    """One output line per input line, so the two lists pair up by position.
    `kind` selects the line converter; a fenced block is copied verbatim
    whatever the kind."""
    out_lines = []
    in_fence = False
    convert_line = _LINE_CONVERTERS[kind]
    for index, line in enumerate(lines):
        if line.lstrip().startswith('```'):
            in_fence = not in_fence
            out_lines.append(line)
            continue
        if in_fence:
            out_lines.append(line)
            continue

        out_lines.append(convert_line(line, index))

    return out_lines


def convert(text: str, kind: InputKind) -> str:
    """A whole file's text at once — see convert_lines for the per-line rule."""
    return '\n'.join(convert_lines(text.split('\n'), kind))
