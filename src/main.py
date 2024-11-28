from fastapi import FastAPI

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from src.routers.router_profile import router as auth_router
from src.routers.router_project import router as projects_router


description = """
Terrea API.

## User

You will be able to:

* **Create User**.
* **Read User**.
* **Update User**.
* **Delete User**.
* **Delete all Users**.


## Role

You will be able to:

* **Create Role**.
* **Read Role**.
* **Update Role**.
* **Delete Role**.
* **Delete all Roles**.
"""

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield

app = FastAPI(
    title='Terrea',
    description=description,
    version='0.1.0',
    lifespan=lifespan,
)


app.include_router(auth_router)
app.include_router(projects_router)


@app.get('/')
async def hello():
    return {'message': 'hello, main'}
