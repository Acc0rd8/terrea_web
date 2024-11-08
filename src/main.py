from fastapi import FastAPI

from src.auth.router import router as auth_router


app = FastAPI(
    title='Terrea'
)


app.include_router(auth_router)


@app.get('/')
async def hello():
    return {'message': 'hello, main'}
