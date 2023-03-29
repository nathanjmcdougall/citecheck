"""Test the citable module."""
from typing import TypeVar

import pytest

from citecheck.core.cited import Cited
from citecheck.core.types.citand import Citand


class TestCited:
    """Test the Citeable class."""

    def test_basic(self):
        citable = Cited[int](5, _citation="math")
        assert citable == 5
        # pylint: disable=protected-access
        assert citable._citation == "math"
        # pylint: enable=protected-access
        assert repr(citable) == "5 (cited as math)"
        assert hash(citable) == hash((5, "math"))
        assert citable + 2 == 7

    def test_bad_class(self):
        assert Cited[int](5.362, _citation="math") == 5
        assert Cited[str](5.362, _citation="math") == "5.362"
        with pytest.raises(ValueError):
            Cited[int]("5.362", _citation="math")

    def test_typehint(self):
        def my_func(value: int) -> Cited[int]:
            return Cited[int](value, _citation="math")

        assert my_func(5) == 5

    def test_typevar_hint(self):
        T = TypeVar("T", bound=Citand)

        def my_func(value: T) -> T:
            return Cited[int](value, _citation="math")

        assert my_func(5) == 5
