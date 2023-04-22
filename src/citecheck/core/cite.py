"""An annotation for a citation."""
from dataclasses import dataclass

from citecheck.core.types.citation import Citation


@dataclass(frozen=True)
class Cite:
    """An annotation for a citation.

    Used in a typing.Annotated annotation for a function to indicate that the
    argument or return value should be associated with the given citation, potentially
    this could be enforced.

    Attributes:
        citation: The citation to associate with the annotated value.
    """

    citation: Citation
