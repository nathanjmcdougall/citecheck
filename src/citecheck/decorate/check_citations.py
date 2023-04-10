"""A decorator to check citations of Cited objects in function annotations."""
import inspect
from typing import Any, Callable

from citecheck.core.citedmixin import _CitedMixin
from citecheck.core.errors import CitationError, CitationWarning
from citecheck.core.types.citable import _Citable
from citecheck.core.types.citation import _CitationT


def _eq_compare(citation1: _CitationT, citation2: _CitationT) -> bool:
    return citation1 == citation2


def _get_compare_func(
    compare_func: Callable[[_CitationT, _CitationT], bool] | None
) -> Callable[[_CitationT, _CitationT], bool]:
    if compare_func is None:
        return _eq_compare
    return compare_func


def check_citations(
    warn: bool = False,
    compare_func: Callable[[_CitationT, _CitationT], bool] | None = None,
):
    """A decorator to check citations of Cited objects in function annotations."""

    compare_func = _get_compare_func(compare_func)

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

                        # Check if the annotation is a Cited object
                        if isinstance(ann, _CitedMixin) and isinstance(ann, _Citable):
                            # Check if the annotation matches the citation of the
                            # argument
                            # pylint: disable=protected-access
                            if not compare_func(ann._citation, arg_value._citation):
                                raise raiser(
                                    f"Function {func.__name__} was called with an "
                                    f"argument {arg_name} which has a "
                                    f"citation {arg_value._citation} which does not "
                                    f"match the annotation {ann._citation}"
                                )
                            # pylint: enable=protected-access

            # Call the function
            return func(*args, **kwargs)

        return wrapper

    return decorator
