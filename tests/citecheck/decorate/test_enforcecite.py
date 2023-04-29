"""Test the enforce_cite decorator."""
from typing import Annotated as Ann

from citecheck.core.cite import Cite
from citecheck.core.citeas import CiteAs
from citecheck.decorate.cite_output import _get_cite_ann_args, _get_output_cite_ann_args
from citecheck.decorate.enforcecite import enforcecite


class TestEnforceCite:
    """Test the enforce_cite decorator."""

    def test_basic(self) -> None:
        """Check a case where we check inputs and cite output too"""

        citation = "Einstein 2023"

        @enforcecite()
        def my_func(value: Ann[float, Cite(citation)]) -> Ann[float, Cite(citation)]:
            return value

        _v = 5.0
        _x = CiteAs(_v, citation)
        assert my_func(_x) == _x
        assert _get_output_cite_ann_args(my_func)
        # pylint: disable=protected-access
        assert my_func(_x)._citation == citation
        # pylint: enable=protected-access


def test_get_output_cite_ann_args() -> None:
    """Test the _get_output_cite_ann_args function."""

    citation = "Einstein 2023"
    other = "Frank 2022"

    def my_func(
        value: Ann[float, Cite(citation)]
    ) -> Ann[float, Cite(citation), Cite(other)]:
        return value

    assert _get_output_cite_ann_args(my_func) == [Cite(citation), Cite(other)]


def test_get_cite_ann_args() -> None:
    """Test the _get_cite_ann_args function."""

    ann = Ann[float, Cite("Einstein 2023"), Cite("Frank 2022")]

    assert _get_cite_ann_args(ann) == [Cite("Einstein 2023"), Cite("Frank 2022")]
    assert _get_cite_ann_args(float) == []
