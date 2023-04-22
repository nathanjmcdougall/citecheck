"""A function to remove the citations from an object"""

from typing import TypeVar

from citecheck.core.cited import _CitedT
from citecheck.core.citedmixin import _CitedMixin
from citecheck.core.types.citable import _CitableT

_T = TypeVar("_T", bound=object)


def uncite(value: _CitedT[_CitedMixin, _CitableT]) -> _CitableT:
    """Remove the citation from a cited object.

    This function is the inverse of :class:`citecheck.core.citeas.CiteAs`.

    Args:
        value: The cited object.

    Returns:
        The uncited object.
    """
    # pylint: disable=protected-access
    uncited_type = value._uncited_type()
    # pylint: enable=protected-access

    uncited = uncited_type.__new__(uncited_type, value)

    return uncited
