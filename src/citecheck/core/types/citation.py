"""Citation class."""
from typing import NewType, TypeAlias, TypeVar

_Citation: TypeAlias = object
Citation = NewType("Citation", _Citation)
_CitationT = TypeVar("_CitationT", bound=Citation)
