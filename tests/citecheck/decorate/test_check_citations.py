"""Test the check_citations function."""
import pytest

from citecheck.core.citeas import CiteAs
from citecheck.core.errors import CitationError
from citecheck.decorate.check_citations import check_citations


class TestCheckCitations:
    """Test the check_citations function."""

    def test_basic(self):
        """Test the check_citations function."""

        citation = "Einstein 2023"

        @check_citations()
        def my_func(value: CiteAs[float, citation]) -> float:
            return value

        _v = 5
        _x = CiteAs(_v, citation)
        assert my_func(_x) == _v

        with pytest.raises(CitationError):
            assert my_func(CiteAs(_v, "Frank 2022"))
