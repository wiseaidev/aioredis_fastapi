"""
aioredis_fastapi is an asynchronous redis based session backend for FastAPI powered applications.
"""

import attr
from attrs import (
    field,
    frozen,
    validators,
)
from datetime import (
    timedelta,
)
from functools import (
    lru_cache,
)
from typing import (
    Callable,
    Optional,
)
from uuid import (
    uuid4,
)


@frozen
@attr.s(auto_attribs=True, slots=True, init=False, repr=False)
class Settings:
    _redis_url: str = field(
        default="redis://localhost:6379",
        validator=validators.instance_of(str),
        converter=str,
    )
    _session_id_name: str = field(
        default="ssid", validator=validators.instance_of(str), converter=str
    )
    _session_id_generator: Callable[[], str] = field(
        default=None, validator=validators.instance_of(Callable), converter=Callable
    )
    _expire_time: timedelta = field(
        default=timedelta(hours=6), validator=validators.instance_of(timedelta)
    )
    _session_id: str = field(
        default=None, validator=validators.instance_of(str), converter=str
    )

    def __attrs_post_init__(self):
        def inner_session_id_generator() -> str:
            return uuid4().hex

        if not self._session_id_generator:
            object.__setattr__(
                self, "_session_id_generator", inner_session_id_generator
            )
        object.__setattr__(self, "_session_id", self._session_id_generator())

    @property
    def redis_url(self) -> str:
        """
        A getter method that returns the value of the `redis_url` attribute.
        :param self: Instance of the class.
        :return: A string that represents the value of the `redis_url` attribute.
        """
        if not hasattr(self, "_redis_url"):
            raise AttributeError(
                f"Your {self.__class__.__name__!r} instance has no attribute named redis_url."
            )
        return self._redis_url

    @property
    def session_id_name(self) -> str:
        """
        A getter method that returns the value of the `session_id_name` attribute.
        :param self: Instance of the class.
        :return: A string that represents the value of the `session_id_name` attribute.
        """
        if not hasattr(self, "_session_id_name"):
            raise AttributeError(
                f"Your {self.__class__.__name__!r} instance has no attribute named session_id_name."
            )
        return self._session_id_name

    @property
    def session_id_generator(self) -> Callable[[], str]:
        """
        A getter method that returns the value of the `session_id_generator` attribute.
        :param self: Instance of the class.
        :return: A callable that represents the value of the `session_id_generator` attribute.
        """
        if not hasattr(self, "_session_id_generator"):
            raise AttributeError(
                f"Your {self.__class__.__name__!r} instance has no attribute named session_id_generator."
            )
        return self._session_id_generator.__name__

    @property
    def expire_time(self) -> timedelta:
        """
        A getter method that returns the value of the `expire_time` attribute.
        :param self: Instance of the class.
        :return: A timedelta value that represents the value of the `expire_time` attribute.
        """
        if not hasattr(self, "_expire_time"):
            raise AttributeError(
                f"Your {self.__class__.__name__!r} instance has no attribute named expire_time."
            )
        return self._expire_time

    @property
    def session_id(self) -> str:
        """
        A getter method that returns the value of the `session_id` attribute.
        :param self: Instance of the class.
        :return: A timedelta value that represents the value of the session_id` attribute.
        """
        if not hasattr(self, "_session_id"):
            raise AttributeError(
                f"Your {self.__class__.__name__!r} instance has no attribute named session_id."
            )
        return self._session_id

    def generate_session_id(self) -> str:
        object.__setattr__(self, "_session_id", self._session_id_generator())
        return self._session_id

    def __repr__(self) -> str:
        """
        A method that Return a formatted string for a given Settings instance.
        :param self: a reference for a given instance.
        :return: a formatted string of attributes for a given instance.
        """
        ret = f"{self.__class__.__name__}(redis_url='{self.redis_url}', session_id_name='{self.session_id_name}'"
        ret += f", session_id_generator='{self.session_id_generator}', expire_time='{self.expire_time}'"
        ret += f", session_id='{self.session_id}')"
        return ret


@lru_cache
def settings(
    redis_url: Optional[str] = "redis://localhost:6379",
    session_id_name: Optional[str] = "ssid",
    session_id_generator: Optional[Callable[[], str]] = None,
    expire_time: Optional[timedelta] = timedelta(hours=6),
):

    return Settings(redis_url, session_id_name, session_id_generator, expire_time)


__all__ = ["settings"]
