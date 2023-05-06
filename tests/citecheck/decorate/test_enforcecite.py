"""Test the enforce_cite decorator."""
from typing import Annotated as Ann
from typing import Any, TypeVar

import pytest
from pytest import param

from citecheck.core.cite import Cite
from citecheck.core.citeas import CiteAs
from citecheck.decorate.citedreturn import (
    _get_cite_ann_args,
    _get_output_cite_ann_args,
    citedreturn,
)
from citecheck.decorate.enforcecite import enforcecite

_T = TypeVar("_T")


class _UnhashableMeta(type):
    """A metaclass that makes a class unhashable."""

    __hash__: Any = None


class Unhashable(int, metaclass=_UnhashableMeta):
    """A class that is unhashable."""


class TestEnforceCite:
    """Test the enforce_cite decorator."""

    @pytest.mark.parametrize(
        "_v",
        [
            5,
            5.0,
            param(
                Unhashable(0),
                id="Unhashable class (not instance)",
                marks=pytest.mark.raises(exception=TypeError),
            ),
        ],
    )
    def test_basic(self, _v: _T) -> None:
        """Check a case where we check inputs and cite output too"""

        citation = "Einstein 2023"

        @enforcecite()
        def my_func(value: Ann[Any, Cite(citation)]) -> Ann[Any, Cite(citation)]:
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
