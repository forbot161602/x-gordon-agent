"""
Convert punctuation to its zh-TW form on Chinese-led text. The rule contract —
what converts, when to run this, and what to do with what it flags — is in the
rule folder's RULE.md.
"""

import argparse
import sys

from .pipeline import InputKind, convert_lines


def changed_lines(
    original: list[str], converted: list[str]
) -> list[tuple[int, str, str]]:
    """Each line conversion would change, as (1-based number, before, after)."""
    return [
        (n, before, after)
        for n, (before, after) in enumerate(zip(original, converted), 1)
        if before != after
    ]


def format_diff(path: str, pending: list[tuple[int, str, str]]) -> list[str]:
    """Unified-diff output lines for what changed_lines found — and nothing at
    all, not even the file header, when nothing pends."""
    if not pending:
        return []
    out = [f"--- {path}", f"+++ {path}"]
    for n, before, after in pending:
        out.extend((f"@@ -{n} +{n} @@", f"-{before}", f"+{after}"))
    return out


def main() -> None:
    parser = argparse.ArgumentParser(
        prog='python3 -m scripts.converter',
        description=__doc__,
    )
    parser.add_argument(
        '--as',
        dest='kind',
        default=InputKind.DOCUMENT.value,
        choices=[k.value for k in InputKind],
        help='what the input holds (default: %(default)s)',
    )
    parser.add_argument(
        '--check',
        action='store_true',
        help='print a unified diff of the lines that would change and exit '
             'non-zero if any, without writing the file',
    )
    parser.add_argument('path', metavar='<file.md>', help='the file to convert')
    args = parser.parse_args()
    kind = InputKind(args.kind)

    # A path the caller mistyped is a bad invocation, so argparse reports it.
    try:
        with open(args.path, 'r', encoding='utf-8') as f:
            lines = f.read().split('\n')
    except OSError as exc:
        parser.error(f'cannot read {args.path}: {exc.strerror}')
    converted_lines = convert_lines(lines, kind)

    if args.check:
        pending = changed_lines(lines, converted_lines)
        for line in format_diff(args.path, pending):
            print(line)
        sys.exit(1 if pending else 0)
    with open(args.path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(converted_lines))
