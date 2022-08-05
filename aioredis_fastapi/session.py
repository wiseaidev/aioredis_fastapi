import aioredis
import pickle
from config import settings
from typing import Any
import attr
import asyncio


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
        try:
            self.loop = asyncio.get_event_loop()
        except RuntimeError as e:
            if str(e).startswith("There is no current event loop in thread"):
                self.loop = asyncio.new_event_loop()
                asyncio.set_event_loop(self.loop)
            else:
                raise

    def set_client(self):
        self.client = self.loop.run_until_complete(self._init_client())

    async def _init_client(self):
        client = await self.create_connection()
        return client

    def __getitem__(self, key: str):
        return self.loop.run_until_complete(self._get_item(key))

    async def _get_item(self, key: str):
        raw = await self.client.get(key)
        return raw and pickle.loads(raw)

    def __setitem__(self, key: str, value: Any):
        self.loop.run_until_complete(self._set_item(key, value))

    async def _set_item(self, key: str, value: Any):
        await self.client.set(
            key,
            pickle.dumps(value, protocol=pickle.HIGHEST_PROTOCOL),
            ex=self.settings.expire_time,
        )

    def __delitem__(self, key: str):
        self.client.delete(key)
        self.loop.run_until_complete(self._del_item(key))

    async def _del_item(self, key: str):
        await self.client.delete(key)

    def generate_session_id(self) -> str:
        return self.loop.run_until_complete(self._generate())

    async def _generate(self) -> str:
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
