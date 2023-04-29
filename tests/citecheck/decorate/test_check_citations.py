"""Test the citedinput function."""
from typing import Annotated as Ann

import pytest

from citecheck.core.cite import Cite
from citecheck.core.citeas import CiteAs
from citecheck.core.cited import _get_cited_class
from citecheck.core.errors import CitationError
from citecheck.decorate.citedinput import citedinput
from citecheck.decorate.enforcecite import enforcecite


class TestCheckCitations:
    """Test the citedinput decorator."""

    @pytest.mark.parametrize(
        "decorator",
        [
            citedinput,
            # when there are no output annotations then enforcecite is equivalent to
            # citedinput
            enforcecite,
        ],
    )
    def test_basic(self, decorator):
        """Test the citedinput decorator."""

        citation = "Einstein 2023"

        @decorator()
        def my_func(value: Ann[float, Cite(citation)]) -> float:
            return value

        _v = 5.0
        _x = CiteAs(_v, citation)
        assert my_func(_x) == _v

        with pytest.raises(CitationError):
            assert my_func(CiteAs(_v, "Frank 2022"))

    def test_multiple_same(self):
        """Test multiple identical citations"""

        citation = "Einstein 2023"

        @citedinput()
        def my_func(value: Ann[float, Cite(citation), Cite(citation)]) -> float:
            return value

        _v = 5.0
        _x = CiteAs(_v, citation)
        assert my_func(_x) == _v

        with pytest.raises(CitationError):
            assert my_func(CiteAs(_v, "Frank 2022"))

    def test_multiple_different(self):
        """Test multiple identical citations"""

        citation1 = "Einstein 2023"
        citation2 = "Worsfold 2000"

        @citedinput(compare_func=lambda x, y: y in x)
        def my_func(value: Ann[float, Cite(citation1), Cite(citation2)]) -> float:
            return value

        _v = 5.0
        _x = CiteAs(_v, citation1)
        assert my_func(_x) == _v
        _y = CiteAs(_v, citation2)
        assert my_func(_y) == _v

        with pytest.raises(CitationError):
            assert my_func(CiteAs(_v, "Frank 2022"))

    def test_uncited_within_decorated(self):
        """Check that citations are automatically removed be the decorator

        Once inputs are passed into the decorated functino body, they should be the
        original, uncited value.
        """

        citation = "Einstein 2023"

        @citedinput()
        def my_func(
            value: Ann[float, Cite(citation)],
            other_value: Ann[int, Cite(citation)] = 1,
        ) -> float:
            assert isinstance(value, float)
            assert not hasattr(value, "_citation")
            assert not isinstance(value, _get_cited_class(float, citation))
            assert isinstance(other_value, int)
            assert not hasattr(other_value, "_citation")
            assert not isinstance(other_value, _get_cited_class(int, citation))
            return value

        _v = 5.0
        _x = CiteAs(_v, citation)
        assert my_func(_x) == _v
