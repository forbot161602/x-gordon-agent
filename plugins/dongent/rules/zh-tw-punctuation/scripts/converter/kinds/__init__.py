"""
One module per input kind, each exposing its own converter.

Adding a kind means adding a module here and re-exporting it below, then naming
it in the registry in `pipeline`.
"""

from .commit_message import convert_commit_message_line
from .document import convert_document_line

__all__ = ['convert_commit_message_line', 'convert_document_line']
