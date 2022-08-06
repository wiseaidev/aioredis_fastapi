"""
aioredis_fastapi is an asynchronous redis based session backend for FastAPI powered applications.
"""

import aioredis
import asyncio
import attr
import pickle
from typing import (
    Any,
)

from aioredis_fastapi.config import (
    settings,
)


class Redis:
    def __init__(self, redis_url):
        self.connection_url = redis_url

    async def create_connection(self):
        connection = aioredis.from_url(self.connection_url, db=0)

        return connection


class SessionStorage(Redis):
    def __init__(self):
        self.settings = settings()
        super().__init__(self.settings.redis_url)

    async def init_client(self):
        self.client = await self.create_connection()

    async def get_key(self, key: str):
        raw = await self.client.get(key)
        return raw and pickle.loads(raw)

    async def set_key(self, key: str, value: Any):
        await self.client.set(
            key,
            pickle.dumps(value, protocol=pickle.HIGHEST_PROTOCOL),
            ex=self.settings.expire_time,
        )

    async def del_key(self, key: str):
        await self.client.delete(key)

    async def generate_session_id(self) -> str:
        session_id = self.settings.session_id
        while await self.client.get(session_id):
            session_id = self.settings.generate_session_id()
        return session_id

    def __repr__(self) -> str:
        """
        A method that returns a formatted string for a given SessionStorage instance.
        :param self: a reference for a given instance.
        :return: a formatted string of attributes for a given instance.
        """
        ret = f"{self.__class__.__name__}(redis_url='{self.connection_url}')"
        return ret


__all__ = ["SessionStorage"]
