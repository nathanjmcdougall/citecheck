"""A class for any arbitary object being cited"""
from __future__ import annotations

from typing import Any, Protocol, TypeVar, runtime_checkable

_T = TypeVar("_T")


@runtime_checkable
class _Citable(Protocol):
    """A class for any arbitary object being cited"""

    def __new__(cls: type[_T], *args: Any, **kwargs: Any) -> _T:
        ...


_CitableT = TypeVar("_CitableT", bound=_Citable)
