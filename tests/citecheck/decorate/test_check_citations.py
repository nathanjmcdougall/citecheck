"""Test the check_citations function."""
from typing import Annotated as Ann

import pytest

from citecheck.core.cite import Cite
from citecheck.core.citeas import CiteAs
from citecheck.core.errors import CitationError
from citecheck.decorate.check_citations import check_citations


class TestCheckCitations:
    """Test the check_citations decorator."""

    def test_basic(self):
        """Test the check_citations decorator."""

        citation = "Einstein 2023"

        @check_citations()
        def my_func(value: Ann[float, Cite(citation)]) -> float:
            return value

        _v = 5
        _x = CiteAs(_v, citation)
        assert my_func(_x) == _v

        with pytest.raises(CitationError):
            assert my_func(CiteAs(_v, "Frank 2022"))

    def test_multiple_same(self):
        """Test multiple identical citations"""

        citation = "Einstein 2023"

        @check_citations()
        def my_func(value: Ann[float, Cite(citation), Cite(citation)]) -> float:
            return value

        _v = 5
        _x = CiteAs(_v, citation)
        assert my_func(_x) == _v

        with pytest.raises(CitationError):
            assert my_func(CiteAs(_v, "Frank 2022"))

    def test_multiple_different(self):
        """Test multiple identical citations"""

        citation1 = "Einstein 2023"
        citation2 = "Worsfold 2000"

        @check_citations(compare_func=lambda x, y: y in x)
        def my_func(value: Ann[float, Cite(citation1), Cite(citation2)]) -> float:
            return value

        _v = 5
        _x = CiteAs(_v, citation1)
        assert my_func(_x) == _v
        _y = CiteAs(_v, citation2)
        assert my_func(_y) == _v

        with pytest.raises(CitationError):
            assert my_func(CiteAs(_v, "Frank 2022"))
