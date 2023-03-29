"""Error and warning classes for when citations aren't correct."""


class CitationError(Exception):
    """An error to be raised when a citation is incorrect."""


class CitationWarning(Warning):
    """A warning to be raised when a citation is incorrect."""
