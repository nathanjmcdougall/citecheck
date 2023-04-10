"""Test the citable module."""
from citecheck.core.citeas import CiteAs


class TestCited:
    """Test the Citeable class."""

    def test_basic(self):
        value = 5
        citable = CiteAs(value, "math")
        assert citable == value
        # pylint: disable=protected-access
        assert citable._citation == "math"
        # pylint: enable=protected-access
        assert repr(citable) == f"{value} (cited as math)"
        assert hash(citable) == hash((value, "math"))
        assert citable + 2 == 7

    def test_equality(self):
        value = 5
        citation = "math"
        assert CiteAs(value, citation) == CiteAs(value, citation)
