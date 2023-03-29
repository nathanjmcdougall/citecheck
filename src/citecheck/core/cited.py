"""A type for objects cited with a citation."""
from typing import Generic, TypeVar

from citecheck.core.types.citand import Citand
from citecheck.core.types.citation import Citation

T = TypeVar("T", bound=Citand)


class _BaseCited:
    def __new__(cls, value: Citand, _citation: Citation | None = None):
        self = super().__new__(cls, value)
        self._citation = _citation
        return self

    def __repr__(self):
        return f"{super().__repr__()} (cited as {self._citation})"

    def __hash__(self):
        return hash((super().__hash__(), self._citation))


class Cited(Generic[T]):
    """A type for objects cited with a citation."""

    def __class_getitem__(cls, item: type[T]) -> type[T]:
        class _Cited(_BaseCited, item):
            pass

        return _Cited
