"""An annotation for a citation."""
from dataclasses import dataclass
from citecheck.core.types.citation import Citation


@dataclass(frozen=True)
class Cite:
    """An annotation for a citation."""

    citation: Citation
