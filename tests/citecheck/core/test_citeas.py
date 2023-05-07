"""Test the add_cite function."""
from citecheck.core.add_cite import add_cite
from citecheck.core.cited import _get_cited_class


class TestCiteAs:
    """Test the add_cite function."""

    def test_call(self) -> None:
        """Test the add_cite function."""
        citation = "Einstein 2023"
        _v = 5
        _x = add_cite(_v, citation)

        # pylint: disable=protected-access
        assert _x._citation == citation
        # pylint: enable=protected-access
        assert _x == _v

    def test_is_type(self) -> None:
        """Test that _get_cited_class(...) gives a type."""
        assert isinstance(_get_cited_class(int, "example"), type)

    def test_subtype(self) -> None:
        """Test that _get_cited_class gives a subtype of the base type."""
        value = 5
        base_type = type(value)

        assert issubclass(_get_cited_class(base_type, "example"), base_type)

    def test_isinstance_of_base(self) -> None:
        """Test that add_cite gives an instance of the base type."""
        value = 5
        base_type = type(value)

        assert isinstance(add_cite(value, "example"), base_type)

    def test_basic(self):
        value = 5
        citable = add_cite(value, "math")
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
        assert add_cite(value, citation) == add_cite(value, citation)
