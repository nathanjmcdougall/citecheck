"""A type for objects cited with a citation."""
from __future__ import annotations

from functools import cache
from typing import Any, Generic, TypeVar

from citecheck.core.types.citable import Citable
from citecheck.core.types.citation import Citation, CitationBase


class CitedMixin:
    """A Mixin class to add citations to another class"""

    _citation: Citation | None

    def __new__(cls, value: Citable, _citation: Citation | None = None) -> CitedMixin:
        _super: Citable = super()
        # Clumsy syntax because of a bug in pylint:
        # https://github.com/pylint-dev/pylint/issues/8554
        if isinstance(_super, Citable):
            pass
        else:
            raise TypeError(f"""{_super} must follow the Citable protocol""")

        self = _super.__new__(cls, value)
        if self != value:
            raise ValueError(
                f"""{_super}.__new__({cls}, {value}) must return {value}"""
            )

        self._citation = _citation
        return self

    def __repr__(self) -> str:
        return f"{super().__repr__()} (cited as {self._citation})"

    def __hash__(self) -> int:
        return hash((super().__hash__(), self._citation))


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
        return cls._get_cited_class(citable_type=item)

    @staticmethod
    @cache
    def _get_cited_class(
        citable_type: type[_CitableT],
    ) -> type[_CitedT[CitedMixin, _CitableT]]:
        # There seems to be a bug in mypy:
        # https://github.com/python/mypy/issues/14458
        # For now, we need to use Any with --allow-subclassing-any.
        _citable_type: Any = citable_type

        class _Cited(CitedMixin, _citable_type):
            pass

        return _Cited
