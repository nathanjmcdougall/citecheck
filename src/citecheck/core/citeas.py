"""Checking a citation of a citable object, or turning it into one"""

from citecheck.core.cited import _CitedT, _get_cited_class
from citecheck.core.citedmixin import _CitedMixin
from citecheck.core.types.citable import _CitableT
from citecheck.core.types.citation import Citation, _CitationT


class _CiteAsMeta(type):
    def __call__(
        cls, value: _CitableT, citation: Citation
    ) -> _CitedT[_CitedMixin, _CitableT]:
        citable_type = type(value)
        _cited_class = _get_cited_class(citable_type, citation)
        return _cited_class(value)

    def __getitem__(
        cls, item: tuple[type[_CitableT], _CitationT]
    ) -> type[_CitedT[_CitedMixin, _CitableT]]:
        citable_type, citation = item
        return _get_cited_class(citable_type, citation)


class CiteAs(metaclass=_CiteAsMeta):
    """Checking a citation of a citable object, or turning it into one"""
