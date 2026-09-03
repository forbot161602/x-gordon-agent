"""
The span engine: split a line into spans, decide which of them are Chinese-led,
and rewrite the eligible punctuation in those.

A span is the unit of judgement — a line is the outermost one, and each nested
quote, bracket or emphasis pair is judged on its own text — so a caller converts
a range and that range carries its own gate. Full algorithm and rationale in the
rule folder's Specification.md.
"""

from enum import Enum


class _SegmentKind(Enum):
    """What a segment of a span holds. PROSE is the span's own text, the only
    kind the gate reads and the converter rewrites."""

    PROSE = 'prose'
    VERBATIM = 'verbatim'   # copied unchanged: backtick spans, delimiters
    SPAN = 'span'           # a nested range, judged on its own prose


# One segment of a span: its kind and the half-open range it covers.
_Segment = tuple[_SegmentKind, int, int]


def is_cjk_ideograph(ch: str) -> bool:
    """Han ideograph range only — excludes full-width punctuation and symbols.
    Used by prose_has_cjk so a trailing 「。」 doesn't make text look Chinese-led
    on its own."""
    if not ch:
        return False
    o = ord(ch)
    return (0x4E00 <= o <= 0x9FFF) or (0x3400 <= o <= 0x4DBF)


# Delimiter pairs that open a nested span. `'` is deliberately absent: in prose
# it is an apostrophe (`it's`, `the author's`), not a paired delimiter.
_DELIMITERS = {
    '(': ')',      # round bracket
    '[': ']',      # square bracket
    '{': '}',      # curly bracket
    '"': '"',      # ASCII double quote
    '「': '」',     # CJK quote
    '『': '』',     # CJK book title quote
    '（': '）',     # CJK full-width round bracket
    '《': '》',     # CJK book title
    '【': '】',     # CJK lenticular bracket
}


def _skip_backtick_span(text: str, start: int, end: int) -> int:
    """Index just past the inline-code span opening at `start`. An unpaired
    backtick protects the rest of the range, so the span runs to `end`: a
    dropped closing backtick is the likely cause, and leaving code alone is the
    safer reading."""
    close = text.find('`', start + 1, end)
    return end if close < 0 else close + 1


def _find_closing_delimiter(
    text: str, start: int, end: int, open_ch: str, close_ch: str
) -> int | None:
    """Index of the delimiter that closes the one at `start`, or None when the
    pair never closes. Nested pairs of the same kind are counted; backtick spans
    are skipped, so a delimiter inside inline code closes nothing outside it."""
    depth, i = 1, start + 1
    while i < end:
        ch = text[i]
        if ch == '`':
            i = _skip_backtick_span(text, i, end)
            continue
        if ch == close_ch:
            depth -= 1
            if not depth:
                return i
        elif ch == open_ch:
            depth += 1
        i += 1
    return None


def _measure_star_run(text: str, start: int, end: int) -> int:
    """Length of the run of `*` beginning at `start`. Emphasis markup doubles
    and triples its marker, so `**` and `***` are single delimiters rather than
    nested pairs — a run only ever closes against a run of the same length."""
    i = start
    while i < end and text[i] == '*':
        i += 1
    return i - start


def _find_closing_star_run(text: str, start: int, end: int, width: int) -> int | None:
    """Index where a run of exactly `width` stars closes the marker opened
    before `start`, or None. Runs of a different length are markup of their own
    and are stepped over."""
    i = start
    while i < end:
        ch = text[i]
        if ch == '`':
            i = _skip_backtick_span(text, i, end)
            continue
        if ch == '*':
            run = _measure_star_run(text, i, end)
            if run == width:
                return i
            i += run
            continue
        i += 1
    return None


def _find_span_bounds(text: str, start: int, end: int) -> tuple[int, int]:
    """The span opening at `start`: its delimiter width and the index where the
    closing delimiter begins. (0, 0) when no delimiter opens there, or when the
    pair never closes — an unmatched delimiter is literal text."""
    ch = text[start]
    if ch == '*':
        width = _measure_star_run(text, start, end)
        close = _find_closing_star_run(text, start + width, end, width)
    elif ch in _DELIMITERS:
        width = 1
        close = _find_closing_delimiter(text, start, end, ch, _DELIMITERS[ch])
    else:
        return 0, 0
    return (width, close) if close is not None else (0, 0)


def _split_segments(text: str, start: int, end: int) -> list[_Segment]:
    """Split one span's range into `(kind, start, end)` segments — see
    _SegmentKind. Every position in the range lands in exactly one segment."""
    segments, prose_start, i = [], start, start
    while i < end:
        if text[i] == '`':
            if i > prose_start:
                segments.append((_SegmentKind.PROSE, prose_start, i))
            stop = _skip_backtick_span(text, i, end)
            segments.append((_SegmentKind.VERBATIM, i, stop))
            i = prose_start = stop
            continue
        width, close = _find_span_bounds(text, i, end)
        if width:
            if i > prose_start:
                segments.append((_SegmentKind.PROSE, prose_start, i))
            segments.append((_SegmentKind.VERBATIM, i, i + width))
            segments.append((_SegmentKind.SPAN, i + width, close))
            segments.append((_SegmentKind.VERBATIM, close, close + width))
            i = prose_start = close + width
            continue
        i += 1
    if end > prose_start:
        segments.append((_SegmentKind.PROSE, prose_start, end))
    return segments


def prose_has_cjk(text: str, segments: list[_Segment] | None = None) -> bool:
    """True if the prose has a Han ideograph — the prose being everything the
    span itself says, outside its nested spans, backtick spans and delimiters.
    This is the gate that decides whether eligible punctuation in that prose
    converts. Defaults to the whole string, one line as the outermost span; a
    caller that has already split it passes its segments in."""
    if segments is None:
        segments = _split_segments(text, 0, len(text))
    return any(
        is_cjk_ideograph(text[i])
        for kind, segment_start, segment_end in segments
        if kind is _SegmentKind.PROSE
        for i in range(segment_start, segment_end)
    )


def is_ascii_technical(ch: str, prev_ch: str, next_ch: str) -> bool:
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


def _convert_prose(
    text: str, start: int, end: int, has_cjk_prose: bool, out_chars: list[str]
) -> None:
    """Rewrite one prose segment under its span's gate, appending to out_chars.
    Neighbours come from the whole string, never from the segment, so an ASCII
    technical pattern is recognised the same wherever a delimiter falls."""
    for i in range(start, end):
        ch = text[i]
        prev_ch = text[i - 1] if i > 0 else ''
        next_ch = text[i + 1] if i + 1 < len(text) else ''

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


def convert_span(text: str, start: int, end: int, out_chars: list[str]) -> None:
    """Convert one span: its own prose under its own gate, each nested span
    recursively under its own. out_chars is shared across the recursion so the
    whitespace cleanup still sees the character emitted before it."""
    segments = _split_segments(text, start, end)
    has_cjk_prose = prose_has_cjk(text, segments)
    for kind, segment_start, segment_end in segments:
        if kind is _SegmentKind.SPAN:
            convert_span(text, segment_start, segment_end, out_chars)
        elif kind is _SegmentKind.VERBATIM:
            out_chars.extend(text[segment_start:segment_end])
        else:
            _convert_prose(text, segment_start, segment_end, has_cjk_prose, out_chars)
