"""Test the CiteAs class."""
from citecheck.core.citeas import CiteAs, _BaseCiteAs


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

        assert CiteAs[1, 2] == _BaseCiteAs(1, 2)

    def test_class_get_item(self) -> None:
        """Test the __getitem__ method of the CiteAs class."""
        citation = "Einstein 2023"
        _x = CiteAs[5, citation]
        # pylint: disable=protected-access, no-member
        assert _x._citation == citation
        # pylint: enable=protected-access, no-member
