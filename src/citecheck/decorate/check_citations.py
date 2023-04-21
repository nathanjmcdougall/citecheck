"""A decorator to check citations of Cited objects in function annotations."""
import inspect
from typing import Annotated, Any, Callable, get_args, get_origin

from citecheck.core.cite import Cite
from citecheck.core.citedmixin import _CitedMixin
from citecheck.core.errors import CitationError, CitationWarning
from citecheck.core.types.citation import Citation, _CitationT


def _eq_compare(citation1: _CitationT, citation2: _CitationT) -> bool:
    return citation1 == citation2


def _get_compare_func(
    compare_func: Callable[[Citation, Citation], bool] | None
) -> Callable[[Citation, Citation], bool]:
    if compare_func is None:
        return _eq_compare
    return compare_func


def check_citations(
    warn: bool = False,
    compare_func: Callable[[Citation, Citation], bool] | None = None,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """A decorator to check citations of Cited objects in function annotations."""

    _compare_func = _get_compare_func(compare_func)

    raiser = CitationWarning if warn else CitationError

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        # Get the function signature
        sig = inspect.signature(func)

        # Get the function annotations
        anns = func.__annotations__

        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Get the function arguments
            bound_args = sig.bind(*args, **kwargs)

            # Iterate over the function arguments
            for arg_name, arg_value in bound_args.arguments.items():
                # Check if the argument is cited
                if isinstance(arg_value, _CitedMixin):
                    # Check if the argument is annotated
                    if arg_name in anns:
                        ann = anns[arg_name]

                        # Check if the annotation is typing.Annotated
                        if get_origin(ann) is Annotated:
                            # Get the annotation arguments which are Cite type
                            ann_args = [
                                arg for arg in get_args(ann) if isinstance(arg, Cite)
                            ]

                            # Iterate over the annotation arguments
                            any_match = False
                            for ann_arg in ann_args:
                                # pylint: disable=protected-access
                                citation = arg_value._citation
                                # pylint: enable=protected-access

                                match = _compare_func(citation, ann_arg.citation)
                                any_match = any_match or match

                            # Check if the citation matches
                            if not any_match:
                                annotated_citations = [arg.citation for arg in ann_args]
                                raise raiser(
                                    f"Function {func.__name__} was called with "
                                    f"an argument {arg_name} which has a "
                                    f"citation {citation} which "
                                    f"does not match any of the annotated citations "
                                    f"{annotated_citations}"
                                )

            # Call the function
            return func(*args, **kwargs)

        return wrapper

    return decorator
