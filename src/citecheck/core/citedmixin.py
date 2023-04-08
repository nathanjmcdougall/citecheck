"""A Mixin class to add citations to another class
"""
from __future__ import annotations

from citecheck.core.types.citable import Citable
from citecheck.core.types.citation import Citation


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
