"""Tests of the errors module."""

import warnings

import pytest

from citecheck.core.errors import CitationError, CitationWarning


class TestCheckCitations:
    """Test errors and warnings."""

    def test_error(self):
        """Test we can raise an error."""
        with pytest.raises(CitationError):
            raise CitationError("This is an error")

    def test_warning(self):
        """Test we can raise a warning."""
        with pytest.warns(CitationWarning):
            warnings.warn("This is a warning", CitationWarning)
