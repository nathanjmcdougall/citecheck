"""A type for objects cited with a citation."""
from __future__ import annotations

from typing import Any, Generic, TypeVar

from citecheck.core.citedmixin import CitedMixin
from citecheck.core.types.citable import Citable
from citecheck.core.types.citation import CitationBase

_CitableT = TypeVar("_CitableT", bound=Citable)
_CitedMixinT = TypeVar("_CitedMixinT", bound=CitedMixin)


class _CitedT(Generic[_CitedMixinT, _CitableT], CitedMixin, CitationBase):
    pass


class Cited:
    """A type for objects cited with a citation."""

    def __class_getitem__(
        cls,
        item: type[_CitableT],
    ) -> type[_CitedT[CitedMixin, _CitableT]]:
        # There seems to be a bug in mypy:
        # https://github.com/python/mypy/issues/14458
        # For now, we need to use Any with --allow-subclassing-any.
        citable_type: Any = item

        class _Cited(CitedMixin, citable_type):
            pass

        return _Cited
