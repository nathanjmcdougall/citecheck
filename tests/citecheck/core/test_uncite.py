"""Test the uncite function."""
from citecheck.core.cited import _get_cited_class
from citecheck.core.uncite import uncite


class TestUncite:
    """Test the uncite function."""

    def test_basic(self) -> None:
        """Test the uncite function."""
        citation = "Einstein 2023"
        _v = "v"
        _x = _get_cited_class(type(_v), citation)(_v)
        val = uncite(_x)
        assert val == _v
