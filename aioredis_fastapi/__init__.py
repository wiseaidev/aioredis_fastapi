"""
aioredis_fastapi is an asynchronous redis based session backend for FastAPI powered applications.
"""


__author__ = """Mahmoud Harmouch"""
__email__ = "business@wiseai.dev"
__version__ = "0.0.1"

from aioredis_fastapi.config import (
    settings,
)
from aioredis_fastapi.methods import (
    del_session,
    get_session,
    get_session_id,
    get_session_storage,
    set_session,
)
from aioredis_fastapi.session import (
    SessionStorage,
)
