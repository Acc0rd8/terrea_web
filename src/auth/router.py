from fastapi import APIRouter

from .schemas import UserCreate


router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


@router.get('/', response_model=UserCreate)
async def hello(user_data: UserCreate):
    return {'user_data': user_data}