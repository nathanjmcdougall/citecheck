"""Checking a citation of a Citable object, or turning it into one"""
from dataclasses import dataclass
from typing import Generic, TypeVar

from citecheck.core.cited import Cited
from citecheck.core.types.citable import Citable
from citecheck.core.types.citation import Citation

T = TypeVar("T", bound=Citable)


@dataclass
class _BaseCiteAs:
    _value_cls: type[Citable]
    _citation: Citation


class CiteAs(Generic[T]):
    """Checking a citation of a Citable object, or turning it into one"""

    def __class_getitem__(cls, item: tuple[type[Citable], Citation]):
        value_cls, citation = item
        return _BaseCiteAs(_value_cls=value_cls, _citation=citation)

    def __new__(cls, value: T, citation: Citation):
        return Cited[type(value)](value, _citation=citation)
