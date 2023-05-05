"""Test the enforce_cite decorator."""
from typing import Annotated as Ann
from typing import TypeVar

import pytest

from citecheck.core.cite import Cite
from citecheck.core.citeas import CiteAs
from citecheck.decorate.citedreturn import (
    _get_cite_ann_args,
    _get_output_cite_ann_args,
    citedreturn,
)
from citecheck.decorate.enforcecite import enforcecite

_T = TypeVar("_T")


class TestEnforceCite:
    """Test the enforce_cite decorator."""

    @pytest.mark.parametrize(
        "typefunc, _v",
        [
            (int, 5),
            (float, 5.0),
        ],
    )
    def test_basic(self, typefunc: type[_T], _v: _T) -> None:
        """Check a case where we check inputs and cite output too"""

        citation = "Einstein 2023"

        @enforcecite()
        def my_func(
            value: Ann[typefunc, Cite(citation)]
        ) -> Ann[typefunc, Cite(citation)]:
            return value

        _x = CiteAs(_v, citation)
        assert my_func(_x) == _x
        assert _get_output_cite_ann_args(my_func)
        # pylint: disable=protected-access
        assert my_func(_x)._citation == citation
        # pylint: enable=protected-access

    def test_citedreturn_no_ann(self) -> None:
        """Check we get a ValueError when we don't have an Ann"""

        with pytest.raises(ValueError):

            @citedreturn
            def my_func() -> float:
                return 1.0


def test_get_output_cite_ann_args() -> None:
    """Test the _get_output_cite_ann_args function."""

    citation = "Einstein 2023"
    other = "Frank 2022"

    def my_func(
        value: Ann[float, Cite(citation)]
    ) -> Ann[float, Cite(citation), Cite(other)]:
        return value

    assert _get_output_cite_ann_args(my_func) == [Cite(citation), Cite(other)]
    assert my_func(1.0) == 1.0


def test_get_cite_ann_args() -> None:
    """Test the _get_cite_ann_args function."""

    ann = Ann[float, Cite("Einstein 2023"), Cite("Frank 2022")]

    assert _get_cite_ann_args(ann) == [Cite("Einstein 2023"), Cite("Frank 2022")]
    assert _get_cite_ann_args(float) == []
