"""A dynamically-created type for objects cited with a citation."""
from abc import abstractmethod
from typing import Any, Generic, Protocol, runtime_checkable

from citecheck.core.citedmixin import _CitedMixin, _CitedMixinT, _get_cited_mixin
from citecheck.core.types.citable import _Citable, _CitableT
from citecheck.core.types.citation import Citation


@runtime_checkable
class _CitedProtocol(Protocol):
    def _uncited_type(self) -> type[_Citable]:
        ...


class _CitedT(_CitedMixin, _Citable, Generic[_CitedMixinT, _CitableT]):
    @abstractmethod
    def _uncited_type(self) -> type[_CitableT]:
        ...


def _get_cited_class(
    citable_type: type[_CitableT],
    citation: Citation,
) -> type[_CitedT[_CitedMixinT, _CitableT]]:
    _cited_class_cache = _CitedClassCache[_CitedMixinT, _CitableT]()
    cited_class = _cited_class_cache.get(citable_type, citation)
    return cited_class


class _CitedClassCache(Generic[_CitedMixinT, _CitableT]):
    _cache: dict[int, type[_CitedT[_CitedMixinT, _CitableT]]] = {}

    def get(
        self, citable_type: type[_CitableT], citation: Citation
    ) -> type[_CitedT[_CitedMixinT, _CitableT]]:
        key = hash((hash(citation), id(citable_type)))

        if key in self._cache:
            cited_class: type[_CitedT[_CitedMixinT, _CitableT]] = self._cache[key]
        else:
            cited_class = _get_new_cited_class(citable_type, citation)
            self._cache[key] = cited_class

        return cited_class


def _get_new_cited_class(
    citable_type: type[_CitableT],
    citation: Citation,
) -> type[_CitedT[_CitedMixinT, _CitableT]]:
    # There seems to be a bug in mypy:
    # https://github.com/python/mypy/issues/14458
    # For now, we need to use Any with --allow-subclassing-any.
    cited_mixin: Any = _get_cited_mixin(citation)
    _citable_type: Any = citable_type

    if not isinstance(citable_type, type):
        raise TypeError(f"{citable_type} must be a type")

    class _Cited(cited_mixin, _citable_type, metaclass=type):
        def _uncited_type(self) -> type[_CitableT]:
            return citable_type

        def __repr__(self) -> str:
            return f"{super().__repr__()} (cited as {self._citation})"

        def __hash__(self) -> int:
            return hash((super().__hash__(), self._citation))

    return _Cited
