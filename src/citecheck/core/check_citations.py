"""A decorator to check citations of Cited objects in function annotations."""
import inspect
from typing import Any, Callable, TypeVar

from citecheck.core.citeas import _BaseCiteAs
from citecheck.core.cited import CitedMixin
from citecheck.core.errors import CitationError, CitationWarning

C = TypeVar("C", bound=Any)


def _eq_compare(citation1: C, citation2: C) -> bool:
    return citation1 == citation2


def check_citations(
    warn: bool = False, compare_func: Callable[[C, C], bool] | None = None
):
    """A decorator to check citations of Cited objects in function annotations."""

    if compare_func is None:
        compare_func = _eq_compare

    raiser = CitationWarning if warn else CitationError

    def decorator(func):
        # Get the function signature
        sig = inspect.signature(func)

        # Get the function annotations
        anns = func.__annotations__

        def wrapper(*args, **kwargs):
            # Get the function arguments
            bound_args = sig.bind(*args, **kwargs)

            # Iterate over the function arguments
            for arg_name, arg_value in bound_args.arguments.items():
                # Check if the argument is cited
                if isinstance(arg_value, CitedMixin):
                    # Check if the argument is annotated
                    if arg_name in anns:
                        ann = anns[arg_name]

                        # Check if the annotation is a Cited object
                        if isinstance(ann, _BaseCiteAs):
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
