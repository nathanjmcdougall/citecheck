"""Test the citable module."""
from inspect import signature

from citecheck.core.citeas import CiteAs
from citecheck.core.cited import _get_cited_class


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

    def test_get_cited_class_init_sig(self):
        citable_type = int
        citation = "math"
        cls = _get_cited_class(citable_type, citation)
        sig = signature(cls.__init__)
        try:
            self_param, value_param = list(sig.parameters)
        except ValueError as err:
            raise AssertionError(
                f"Expected two parameters, got {sig.parameters}"
            ) from err
        assert self_param == "self"
        assert value_param == "value"
