from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware import Middleware
from prometheus_fastapi_instrumentator import Instrumentator

from src.exceptions import CustomError
from src.routers.router_profile import router_profile
from src.routers.router_project import router_project


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


app = FastAPI(
    title='Terrea',
    description=description,
    version='0.1.0',
)


# CORS
origins = [
    "http://localhost:3000",
]

cors_middleware = Middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE'],
    allow_headers=['*'],
    expose_headers=['*']
)


# Exception Handlers
@app.exception_handler(CustomError)
async def unicorn_exception_handler(request: Request, exc: CustomError):
    return JSONResponse(
        status_code=exc.code,
        content={'status': False, 'message': exc.message}
    )


# Prometheus
instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*", "/metrics"],
)
Instrumentator().instrument(app).expose(app)


# Routers
app.include_router(router_profile)
app.include_router(router_project)
