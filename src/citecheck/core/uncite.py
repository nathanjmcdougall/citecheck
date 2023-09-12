"""A function to remove the citations from an object"""

from typing import TypeVar

from citecheck.core.cited import _CitedProtocol
from citecheck.core.types.citable import _Citable

_T = TypeVar("_T", bound=object)


def uncite(value: _CitedProtocol) -> _Citable:
    """Remove the citation from a cited object.

    This function is the inverse of :class:`citecheck.core.add_cite.add_cite`.

    Args:
        value: The cited object.

    Returns:
        The uncited object.
    """
    # pylint: disable=protected-access
    uncited_type = value._uncited_type()
    return uncited_type.__new__(uncited_type, value)
