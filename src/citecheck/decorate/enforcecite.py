"""A decorator to check ciations and cite output via function annotations."""

from collections.abc import Callable
from typing import Any

from citecheck.core.types.citable import _CitableT
from citecheck.core.types.citation import Citation
from citecheck.decorate.citedinput import citedinput
from citecheck.decorate.citedreturn import _get_output_cite_ann_args, citedreturn


def enforcecite(
    warn: bool = False,
    compare_func: Callable[[Citation, Citation], bool] | None = None,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """A decorator to check ciations and cite output via function annotations."""

    def decorator(func: Callable[..., _CitableT]) -> Callable[..., Any]:
        checked_func = citedinput(warn=warn, compare_func=compare_func)(func)
        if _get_output_cite_ann_args(checked_func):
            citer_func = citedreturn(checked_func)
        else:
            citer_func = checked_func
        return citer_func

    return decorator
