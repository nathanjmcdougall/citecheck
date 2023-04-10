"""Test the citable module."""
from typing import TypeVar

import pytest

from citecheck.core.cited import Cited
from citecheck.core.types.citable import Citable


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
        with pytest.raises(ValueError):
            assert Cited[int](5.362, _citation="math") == 5
        with pytest.raises(ValueError):
            assert Cited[str](5.362, _citation="math") == "5.362"
        with pytest.raises(ValueError):
            Cited[int]("5.362", _citation="math")

    def test_typehint(self):
        def my_func(value: int) -> Cited[int]:
            return Cited[int](value, _citation="math")

        assert my_func(5) == 5

    def test_typevar_hint(self):
        T = TypeVar("T", bound=Citable)

        def my_func(value: T) -> T:
            return Cited[int](value, _citation="math")

        assert my_func(5) == 5

    def test_equality(self):
        base_type = int
        assert Cited[base_type] == Cited[base_type]
