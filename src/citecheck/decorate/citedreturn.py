"""A decorator to add a citation to its output via function annotations."""

from collections.abc import Callable
from functools import wraps
from typing import Annotated, Any, get_args, get_origin

from citecheck.core.cite import Cite
from citecheck.core.cited import _CitedT, _get_cited_class
from citecheck.core.citedmixin import _CitedMixinT
from citecheck.core.types.citable import _CitableT
from citecheck.core.types.citation import Citation


def citedreturn(
    func: Callable[..., _CitableT]
) -> Callable[..., _CitedT[_CitedMixinT, _CitableT]]:
    """A decorator to check ciations and cite output via function annotations."""

    citation = _get_output_citation(func)

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> _CitedT[_CitedMixinT, _CitableT]:
        # Call the function
        output = func(*args, **kwargs)

        # Add the citation to the output
        citable_type = type(output)
        _cited_class: type[_CitedT[_CitedMixinT, _CitableT]] = _get_cited_class(
            citable_type, citation
        )
        return _cited_class(output)

    return wrapper


def _get_output_citation(func: Callable[..., Any]) -> Citation:
    ann = _get_return_ann(func)

    if ann is None:
        raise ValueError(
            "The function must have a return annotation to be able to cite its "
            "output."
        )

    ann_args = _get_output_cite_ann_args(func)

    # Check if the annotation is typing.Annotated
    if not ann_args:
        raise ValueError("The return annotation must be of type Annotated[Cite, ...]")

    if len(ann_args) > 1:
        raise ValueError("The return Annotated annoation must have only one Cite type.")

    (ann_arg,) = ann_args

    citation = ann_arg.citation

    return citation


def _get_output_cite_ann_args(func: Callable[..., Any]) -> list[Cite]:
    ann = _get_return_ann(func)
    ann_args = _get_cite_ann_args(ann)
    return ann_args


def _get_return_ann(func: Callable[..., Any]) -> Any | None:
    return func.__annotations__.get("return")


def _get_cite_ann_args(ann: Any) -> list[Cite]:
    if get_origin(ann) is not Annotated:
        return []

    ann_args = [arg for arg in get_args(ann) if isinstance(arg, Cite)]

    return ann_args
