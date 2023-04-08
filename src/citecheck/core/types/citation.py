"""Citation class."""
from typing import NewType, TypeAlias

CitationBase: TypeAlias = object
Citation = NewType("Citation", CitationBase)
