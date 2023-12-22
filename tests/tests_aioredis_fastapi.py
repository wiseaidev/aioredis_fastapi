"""
aioredis_fastapi is an asynchronous redis based session backend for FastAPI powered applications.
"""


import pytest

from aioredis_fastapi import (
    __version__,
)


def test_version():
    assert __version__ == "1.0.0"
