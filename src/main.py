from fastapi import FastAPI

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


app = FastAPI(
    title='Terrea',
    description=description,
    version='0.1.0',
)


app.include_router(auth_router)
app.include_router(projects_router)


@app.get('/')
async def hello():
    return {'message': 'hello, main'}
