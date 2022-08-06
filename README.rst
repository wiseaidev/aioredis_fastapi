================
aioredis_fastapi
================

.. image:: https://img.shields.io/badge/License-GPLv3-blue.svg
   :target: https://github.com/wiseaidev/aioredis_fastapi/blob/main/LICENSE
   :alt: License

.. image:: https://raw.githubusercontent.com/wiseaidev/aioredis_fastapi/main/assets/banner.jpeg
   :target: https://github.com/wiseaidev/aioredis_fastapi/
   :alt: Banner



**aioredis_fastapi** is an asynchronous `redis based session`_ backend for FastAPI powered applications.

🚸This repository is currently under testing, kind of production-ready.🚸


🛠️ Requirements
---------------

**aioredis_fastapi** requires Python 3.9 or above.

To install Python 3.9, I recommend using `pyenv`_. You can refer to `this section`_ of the readme file on how to install poetry and pyenv into your linux machine.

🚨 Installation
---------------

With :code:`pip`:

.. code-block:: console

   python3.9 -m pip install aioredis-fastapi

or by checking out the repo and installing it with `poetry`_:

.. code-block:: console

   git clone https://github.com/wiseaidev/aioredis_fastapi.git && cd aioredis_fastapi && poetry install


🚸 Usage
--------

.. code-block:: python3

   from typing import Any
   from fastapi import Depends, FastAPI, Request, Response
   from aioredis_fastapi import (
       get_session_storage,
       get_session,
       get_session_id,
       set_session,
       del_session,
       SessionStorage,
   )

   app = FastAPI(title=__name__)


   @app.post("/set-session")
   async def _set_session(
       request: Request,
       response: Response,
       session_storage: SessionStorage = Depends(get_session_storage),
   ):
       session_data = await request.json()
       await set_session(response, session_data, session_storage)


   @app.get("/get-session")
   async def _get_session(session: Any = Depends(get_session)):
       return session


   @app.post("/del-session")
   async def _delete_session(
       session_id: str = Depends(get_session_id),
       session_storage: SessionStorage = Depends(get_session_storage),
   ):
       await del_session(session_id, session_storage)
       return None


🛠️ Custom Config
----------------

.. code-block:: python3

   from aioredis_fastapi import settings
   from datetime import timedelta
   import random

   settings(
      redis_url="redis://localhost:6379",
      session_id_name="session-id",
      session_id_generator=lambda: str(random.randint(1000, 9999)),
      expire_time= timedelta(days=1)
   )


🌐 Interacting with the endpoints
---------------------------------

.. code-block:: python3

   from httpx import AsyncClient
   import asyncio
   from config import settings

   async def main():
       client = AsyncClient()
       r = await client.post("http://127.0.0.1:8000/set-session", json=dict(a=1, b="data", c=True))
       r = await client.get("http://127.0.0.1:8000/get-session", cookies={settings().session_id_name: "ssid"})
       print(r.text)
       return r.text

   loop = asyncio.new_event_loop()
   asyncio.set_event_loop(loop)
   try:
       loop.run_until_complete(main())
   finally:
       loop.close()
       asyncio.set_event_loop(None)


🎉 Credits
----------

The following projects were used to build and test :code:`aioredis_fastapi`.

- `python`_
- `poetry`_
- `pytest`_
- `flake8`_
- `coverage`_
- `rstcheck`_
- `mypy`_
- `pytestcov`_
- `tox`_
- `isort`_
- `black`_
- `precommit`_


👋 Contribute
-------------

If you are looking for a way to contribute to the project, please refer to the `Guideline`_.


📝 License
----------

This program and the accompanying materials are made available under the terms and conditions of the `GNU GENERAL PUBLIC LICENSE`_.

.. _GNU GENERAL PUBLIC LICENSE: http://www.gnu.org/licenses/
.. _redis based session: https://github.com/duyixian1234/fastapi-redis-session
.. _Guideline: https://github.com/wiseaidev/aioredis_fastapi/blob/main/CONTRIBUTING.rst
.. _this section: https://github.com/wiseaidev/frozndict#%EF%B8%8F-requirements
.. _pyenv: https://github.com/pyenv/pyenv
.. _poetry: https://github.com/python-poetry/poetry
.. _python: https://www.python.org/
.. _pytest: https://docs.pytest.org/en/7.1.x/
.. _flake8: https://flake8.pycqa.org/en/latest/
.. _coverage: https://coverage.readthedocs.io/en/6.3.2/
.. _rstcheck: https://pypi.org/project/rstcheck/
.. _mypy: https://mypy.readthedocs.io/en/stable/
.. _pytestcov: https://pytest-cov.readthedocs.io/en/latest/
.. _tox: https://tox.wiki/en/latest/
.. _isort: https://github.com/PyCQA/isort
.. _black: https://black.readthedocs.io/en/stable/
.. _precommit: https://pre-commit.com/
