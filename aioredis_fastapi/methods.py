"""
aioredis_fastapi is an asynchronous redis based session backend for FastAPI powered applications.
"""

import asyncio
from fastapi import (
    Depends,
    Request,
    Response,
)
from typing import (
    Any,
    Generator,
)

from aioredis_fastapi.config import (
    settings,
)
from aioredis_fastapi.session import (
    SessionStorage,
)


async def get_session_storage() -> Generator:
    storage = SessionStorage()
    await storage.init_client()
    yield storage


async def get_session(
    request: Request, session_storage: SessionStorage = Depends(get_session_storage)
):
    session_id = request.cookies.get(settings().session_id_name, "")
    return await session_storage.get_key(session_id)


async def get_session_id(request: Request):
    session_id = request.cookies.get(settings().session_id_name, "")
    return session_id


async def set_session(
    response: Response, session: Any, session_storage: SessionStorage
) -> str:
    session_id = await session_storage.generate_session_id()
    await session_storage.set_key(session_id, session)
    response.set_cookie(settings().session_id_name, session_id, httponly=True)
    return session_id


async def del_session(session_id: str, session_storage: SessionStorage):
    await session_storage.del_key(session_id)


__all__ = [
    "get_session_storage",
    "get_session",
    "get_session_id",
    "set_session",
    "del_session",
]
