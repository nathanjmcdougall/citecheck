"""A class for adding citation attributes to citable objects."""

from citecheck.core.cited import _CitedT, _get_cited_class
from citecheck.core.citedmixin import _CitedMixinT
from citecheck.core.types.citable import _CitableT
from citecheck.core.types.citation import Citation


def add_cite(value: _CitableT, citation: Citation) -> _CitedT[_CitedMixinT, _CitableT]:
    """Add citation attributes to a citable object.

    Usage is `add_cite(value, citation)`.
    """
    citable_type = type(value)
    _cited_class = _get_cited_class(citable_type, citation)  # type: ignore
    return _cited_class(value)  # type: ignore
