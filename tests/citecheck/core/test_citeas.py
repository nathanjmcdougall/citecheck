"""Test the CiteAs class."""
from citecheck.core.citeas import CiteAs
from citecheck.core.cited import _get_cited


class TestCiteAs:
    """Test the CiteAs class."""

    def test_call(self) -> None:
        """Test the citeas function."""
        citation = "Einstein 2023"
        _v = 5
        _x = CiteAs(_v, citation)

        # pylint: disable=protected-access, no-member
        assert _x._citation == citation
        # pylint: enable=protected-access, no-member
        assert _x == _v

        assert CiteAs[1, 2] == _get_cited(1, 2)

    def test_class_get_item(self) -> None:
        """Test the __getitem__ method of the CiteAs class."""
        citation = "Einstein 2023"
        _x = CiteAs[5, citation]
        # pylint: disable=protected-access, no-member
        assert _x._citation == citation
        # pylint: enable=protected-access, no-member

    def test_is_type(self) -> None:
        """Test that CiteAs[..., ...] is a type."""
        assert isinstance(CiteAs[int, "example"], type)

    def test_compatibility_between_new_and_getitem(self) -> None:
        value = 5
        citation = "example"
        assert isinstance(CiteAs(value, citation), type(CiteAs(value, citation)))
        assert isinstance(CiteAs(value, citation), CiteAs[type(value), citation])

    def test_subtype(self) -> None:
        """Test that CiteAs is a subtype of the base type."""
        value = 5
        base_type = type(value)

        assert issubclass(CiteAs[base_type, "example"], base_type)

    def test_isinstance_of_base(self) -> None:
        """Test that CiteAs is an instance of the base type."""
        value = 5
        base_type = type(value)

        assert isinstance(CiteAs(value, "example"), base_type)
