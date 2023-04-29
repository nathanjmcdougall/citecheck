"""A class for adding citation attributes to citable objects."""

from citecheck.core.cited import _CitedT, _get_cited_class
from citecheck.core.citedmixin import _CitedMixinT
from citecheck.core.types.citable import _CitableT
from citecheck.core.types.citation import Citation


class _CiteAsMeta(type):
    def __call__(
        cls, value: _CitableT, citation: Citation
    ) -> _CitedT[_CitedMixinT, _CitableT]:
        citable_type = type(value)
        _cited_class = _get_cited_class(citable_type, citation)
        return _cited_class(value)


class CiteAs(metaclass=_CiteAsMeta):
    """A class for adding citation attributes to citable objects.

    Usage is `CiteAs(value, citation)`.
    """
