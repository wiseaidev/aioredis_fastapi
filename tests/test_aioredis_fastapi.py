"""
aioredis_fastapi is an asynchronous redis based session backend for FastAPI powered applications.
"""


import pytest

from frozndict import (
    __version__,
)


def test_version():
    assert __version__ == "0.0.1"
