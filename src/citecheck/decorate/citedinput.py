"""A decorator to check citations of Cited objects in function annotations."""
import inspect
import warnings
from collections.abc import Callable
from functools import wraps
from typing import Annotated, Any, get_args, get_origin

from citecheck.core.cite import Cite
from citecheck.core.cited import _CitedProtocol
from citecheck.core.citedmixin import _CitedMixin
from citecheck.core.errors import CitationError, CitationWarning
from citecheck.core.types.citation import Citation, _CitationT
from citecheck.core.uncite import uncite


def _eq_compare(citation1: _CitationT, citation2: _CitationT) -> bool:
    return citation1 == citation2


def _get_compare_func(
    compare_func: Callable[[Citation, Citation], bool] | None,
) -> Callable[[Citation, Citation], bool]:
    if compare_func is None:
        return _eq_compare
    return compare_func


def citedinput(
    warn: bool = False,
    compare_func: Callable[[Citation, Citation], bool] | None = None,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """A decorator to check citations of Cited objects in function annotations."""
    _compare_func = _get_compare_func(compare_func)

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        # Get the function signature
        sig = inspect.signature(func)

        # Get the function annotations
        anns = func.__annotations__

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Iterate over the function arguments
            for arg_name, arg_value in sig.bind(*args, **kwargs).arguments.items():
                # Check if the argument is cited and annotated
                if isinstance(arg_value, _CitedMixin) and arg_name in anns:
                    # Check if the annotation is typing.Annotated
                    ann = anns[arg_name]
                    if get_origin(ann) is Annotated:
                        # Get the annotation arguments which are Cite type
                        ann_args = [
                            arg for arg in get_args(ann) if isinstance(arg, Cite)
                        ]

                        # Iterate over the annotation arguments
                        # pylint: disable=protected-access
                        any_match = any(
                            _compare_func(arg_value._citation, ann_arg.citation)
                            for ann_arg in ann_args
                        )

                        # Check if the citation matches
                        if not any_match:
                            annotated_citations = [arg.citation for arg in ann_args]
                            msg = (
                                f"Function {func.__name__} was called with "
                                f"an argument {arg_name} which has a "
                                f"citation {arg_value._citation} which "
                                f"does not match any of the annotated citations "
                                f"{annotated_citations}"
                            )
                            if warn:
                                warnings.warn(msg, CitationWarning)
                            else:
                                raise CitationError(msg)

                        # pylint: enable=protected-access

            argslist = list(args)

            for idx, arg in enumerate(argslist):
                if isinstance(arg, _CitedProtocol):
                    argslist[idx] = uncite(arg)

            for key, value in kwargs.items():
                if isinstance(value, _CitedProtocol):
                    kwargs[key] = uncite(value)

            # Call the function
            return func(*argslist, **kwargs)

        return wrapper

    return decorator
