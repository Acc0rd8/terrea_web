from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi.middleware.cors import CORSMiddleware
from redis import asyncio as aioredis
import time

from src.config import settings
from src.routers.router_profile import router as auth_router
from src.routers.router_project import router as projects_router
from src.logger import logger

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
    redis = aioredis.from_url(f"redis://{settings.REDIS_INFO['REDIS_HOST']:{settings.REDIS_INFO['REDIS_PORT']}}")
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield

app = FastAPI(
    title='Terrea',
    description=description,
    version='0.1.0',
    lifespan=lifespan,
)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE'],
    allow_headers=['*'],
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    logger.info('Request execution time', extra={
        'process_time': round(process_time, 4)
    })
    return response

app.include_router(auth_router)
app.include_router(projects_router)
