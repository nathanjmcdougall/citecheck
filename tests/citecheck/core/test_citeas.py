"""Test the CiteAs class."""
import pytest

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

    @pytest.mark.skip(reason="Not implemented yet")
    def test_is_type(self) -> None:
        """Test that CiteAs[..., ...] is a type."""
        assert isinstance(CiteAs[5, "example"], type)

    @pytest.mark.skip(reason="Not implemented yet")
    def test_compatibility_between_new_and_getitem(self) -> None:
        value = 5
        citation = "citation"

        # pylint: disable=isinstance-second-argument-not-valid-type
        # We should re-enable this check once test_is_type passes
        assert isinstance(CiteAs(value, citation), CiteAs[type(value), citation])
        # pylint: enable=isinstance-second-argument-not-valid-type

    @pytest.mark.skip(reason="Not implemented yet")
    def test_subtype(self) -> None:
        """Test that CiteAs is a subtype of the base type."""
        base_type = int

        assert isinstance(CiteAs[base_type, "example"], base_type)
