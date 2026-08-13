#!/usr/bin/env python3
"""
Convert punctuation to its zh-TW form on Chinese-led lines.

Usage: python3 convert.py [--check] <file.md>

--check reports the lines that would change and exits non-zero if any, without
writing the file (exit 0 when nothing needs converting).

Idempotent — safe to re-run. See sibling RULE.md for the rule contract.
"""

import re
import sys


def is_cjk_ideograph(ch):
    """Han ideograph range only — excludes full-width punctuation and symbols.
    Used by prose_has_cjk so a trailing 「。」 doesn't make a line look dominant
    on its own."""
    if not ch:
        return False
    o = ord(ch)
    return (0x4E00 <= o <= 0x9FFF) or (0x3400 <= o <= 0x4DBF)


# Matched quote / bracket / backtick pairs whose interior is stripped from the
# line before the prose-level CJK check. Each pattern uses `[^X]*` so it cannot
# cross its closing delimiter — mismatched pairs are left alone.
_NON_PROSE_PATTERNS = [
    re.compile(r'`[^`]*`'),       # inline backtick
    re.compile(r'"[^"]*"'),       # ASCII double quote
    re.compile(r'\([^)]*\)'),     # round bracket
    re.compile(r'\[[^\]]*\]'),    # square bracket
    re.compile(r'\{[^}]*\}'),     # curly bracket
    re.compile(r'「[^」]*」'),     # CJK quote
    re.compile(r'『[^』]*』'),     # CJK book title quote
    re.compile(r'（[^）]*）'),     # full-width round bracket
    re.compile(r'《[^》]*》'),     # CJK book title
    re.compile(r'【[^】]*】'),     # lenticular bracket
]


def prose_has_cjk(line):
    """True if the line, after stripping matched quote/bracket pairs and inline
    backtick spans, still contains a Han ideograph. This is the line-level gate
    that decides whether eligible punctuation in the line converts to full-width."""
    stripped = line
    for pattern in _NON_PROSE_PATTERNS:
        stripped = pattern.sub('', stripped)
    return any(is_cjk_ideograph(c) for c in stripped)


def is_ascii_technical(ch, prev_ch, next_ch):
    """Detect ASCII technical patterns that must keep half-width punctuation
    regardless of surrounding language context."""
    if ch == ',' and prev_ch.isdigit() and next_ch.isdigit():
        return True  # 1,000
    if ch == ':':
        if prev_ch.isdigit() and next_ch.isdigit():
            return True  # 7:1, 3:45
        if prev_ch.isascii() and prev_ch.isalpha():
            if next_ch.isdigit() or next_ch == '/':
                return True  # App.css:24, https://
            if next_ch.isascii() and next_ch.isalpha():
                return True  # A:B letter:letter identifier
    if ch == '?' and next_ch == '.':
        return True  # cfg?.theme optional chaining
    return False


ZH_TW_FORM = {',': '，', ':': '：', ';': '；', '?': '？', '…': '...'}


def convert(text):
    """Per line: when the prose has a Han ideograph (see prose_has_cjk),
    rewrite ASCII , : ; ? to full-width and … to ... — except ASCII technical
    patterns, and content inside backticks / fenced code which is preserved
    verbatim."""
    out_lines = []
    in_fence = False
    for line in text.split('\n'):
        if line.lstrip().startswith('```'):
            in_fence = not in_fence
            out_lines.append(line)
            continue
        if in_fence:
            out_lines.append(line)
            continue

        has_cjk_prose = prose_has_cjk(line)

        out_chars, in_bt = [], False
        chars = list(line)
        for i, ch in enumerate(chars):
            prev_ch = chars[i - 1] if i > 0 else ''
            next_ch = chars[i + 1] if i + 1 < len(chars) else ''

            if ch == '`':
                in_bt = not in_bt
                out_chars.append(ch)
                continue
            if in_bt:
                out_chars.append(ch)
                continue

            if ch in ',:;?…':
                if is_ascii_technical(ch, prev_ch, next_ch):
                    out_chars.append(ch)
                    continue
                if has_cjk_prose:
                    out_chars.append(ZH_TW_FORM[ch])
                else:
                    out_chars.append(ch)
                continue

            if ch == ' ' and out_chars and out_chars[-1] in '，：；？':
                continue

            out_chars.append(ch)
        out_lines.append(''.join(out_chars))

    return '\n'.join(out_lines)


def changed_lines(original, converted):
    """1-based line numbers where conversion would change the text."""
    return [
        n
        for n, (before, after) in enumerate(
            zip(original.split('\n'), converted.split('\n')), 1
        )
        if before != after
    ]


def main():
    args = sys.argv[1:]
    check = '--check' in args
    paths = [a for a in args if a != '--check']
    if len(paths) != 1:
        print(f"Usage: {sys.argv[0]} [--check] <file.md>", file=sys.stderr)
        sys.exit(1)
    path = paths[0]
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    converted = convert(text)
    if check:
        pending = changed_lines(text, converted)
        for n in pending:
            print(f"{path}:{n}: would convert punctuation")
        sys.exit(1 if pending else 0)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(converted)


if __name__ == '__main__':
    main()
