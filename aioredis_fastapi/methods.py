from config import (
    settings,
)
from fastapi import (
    Depends,
    Request,
    Response,
)
from session import (
    SessionStorage,
)
from typing import (
    Any,
    Generator,
)


def get_session_storage() -> Generator:
    storage = SessionStorage()
    storage.set_client()
    yield storage


def get_session(
    request: Request, session_storage: SessionStorage = Depends(get_session_storage)
):
    session_id = request.cookies.get(settings().session_id_name, "")
    return session_storage[session_id]


def get_session_id(request: Request):
    session_id = request.cookies.get(settings().session_id_name, "")
    return session_id


def set_session(
    response: Response, session: Any, session_storage: SessionStorage
) -> str:
    session_id = session_storage.generate_session_id()
    session_storage[session_id] = session
    response.set_cookie(settings().session_id_name, session_id, httponly=True)
    return session_id


def del_session(session_id: str, session_storage: SessionStorage):
    del session_storage[session_id]
