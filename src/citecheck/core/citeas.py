"""Checking a citation of a Citand object, or turning it into one"""
from dataclasses import dataclass
from typing import Generic, TypeVar

from citecheck.core.cited import Cited
from citecheck.core.types.citand import Citand
from citecheck.core.types.citation import Citation

T = TypeVar("T", bound=Citand)


@dataclass
class _BaseCiteAs:
    _value_cls: type[Citand]
    _citation: Citation


class CiteAs(Generic[T]):
    """Checking a citation of a Citand object, or turning it into one"""

    def __class_getitem__(cls, item: tuple[type[Citand], Citation]):
        value_cls, citation = item
        return _BaseCiteAs(_value_cls=value_cls, _citation=citation)

    def __new__(cls, value: T, citation: Citation):
        return Cited[type(value)](value, _citation=citation)
