"""Test the enforce_cite decorator."""
from typing import Annotated as Ann

import numpy as np
import pytest
from numpy.typing import ArrayLike, NDArray

from citecheck.core.add_cite import add_cite
from citecheck.core.cite import Cite
from citecheck.decorate.citedreturn import (
    _get_cite_ann_args,
    _get_output_cite_ann_args,
    citedreturn,
)
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
        _x = add_cite(_v, citation)
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

    def test_numpy(self) -> None:
        """Check an example where numpy arrays are used"""

        citation = "Einstein 2023"

        @enforcecite()
        def my_func(
            value: Ann[ArrayLike, Cite(citation)]
        ) -> Ann[NDArray[np.float64], Cite(citation)]:
            _ = value
            return np.array([1.0, 2.0])

        _v = np.array([1.0, 2.0])
        _x = add_cite(_v, citation)
        assert np.all(my_func(_x) == _x)
        # pylint: disable=protected-access,no-member
        assert my_func(_x)._citation == citation
        # pylint: enable=protected-access,no-member


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
