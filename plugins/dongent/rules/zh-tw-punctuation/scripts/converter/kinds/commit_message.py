"""
The commit-message kind: the header line is structure, the rest is prose.
"""

import re

from ..engine import convert_span


# The prefix a conventional-commit header opens with: a type token, an optional
# scope, then the separator — the description after it is prose and converts, so
# it stays outside the match. Matched by shape, never against a list of type
# names, which a project extends at will. `re` serves the per-kind converters;
# the engine stays regex-free.
_COMMIT_HEADER_PREFIX = re.compile(r'[A-Za-z][\w-]*(\([^()]*\))?: ')


def convert_commit_message_line(line: str, index: int) -> str:
    """One line of a commit message: only the first line is a header, and every
    later line is body prose that converts whole."""
    match = _COMMIT_HEADER_PREFIX.match(line) if index == 0 else None
    start = match.end() if match else 0
    out_chars = list(line[:start])
    convert_span(line, start, len(line), out_chars)
    return ''.join(out_chars)
