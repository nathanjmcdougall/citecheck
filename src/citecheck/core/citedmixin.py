"""A type for objects cited with a citation."""
from functools import cache
from typing import ClassVar, Protocol, TypeVar, runtime_checkable

from citecheck.core.types.citable import _Citable
from citecheck.core.types.citation import Citation

_T = TypeVar("_T", bound="_CitedMixin")


@runtime_checkable
class _CitedMixin(Protocol):
    _citation: ClassVar[Citation]

    def __new__(cls: type[_T], value: _Citable) -> _T:
        ...


_CitedMixinT = TypeVar("_CitedMixinT", bound=_CitedMixin)


@cache
def _get_cited_mixin(citation: Citation) -> type[_CitedMixin]:
    _S = TypeVar("_S", bound="CitedMixin")

    class CitedMixin:
        """A Mixin class to add a fixed citation to another class"""

        _citation: ClassVar[Citation] = citation

        def __new__(cls: type[_S], value: _Citable) -> _S:
            _super: _Citable = super()

            # Clumsy syntax because of a bug in pylint:
            # https://github.com/pylint-dev/pylint/issues/8554
            if isinstance(_super, _Citable):
                pass
            else:
                raise TypeError(f"""{_super} must follow the Citable protocol""")

            xprsn = f"{_super}.__new__({cls}, {value})"
            try:
                self = _super.__new__(cls, value)
            except TypeError as err:
                raise TypeError(
                    f"""{xprsn} must return a value. Likely, {cls}.__new__ does not
                    accept exactly one argument.
                    """
                ) from err

            if self != value:
                raise ValueError(f"""{xprsn} must equal {value}""")

            return self

    return CitedMixin
