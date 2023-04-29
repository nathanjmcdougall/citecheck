"""Test the Cited class and its helper classes"""
from citecheck.core.cited import _CitedProtocol, _CitedT


def test_citedt_follows_protocol() -> None:
    assert isinstance(_CitedT, _CitedProtocol)
    assert not isinstance(float, _CitedProtocol)
