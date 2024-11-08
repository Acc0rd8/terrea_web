from fastapi import APIRouter, HTTPException, status

from .schemas import UserCreate
from .basic_config import get_password_hash
from ..crud import get_user, create_user

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


@router.post('/register/')
async def register_user(user_data: UserCreate) -> dict:
    user = await get_user(user_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь уже существует'
        )
    user_dict = user_data.model_dump()
    user_dict['password'] = get_password_hash(user_data.password)
    await create_user(UserCreate(**user_dict))
    return {'message': 'Вы успешно зарегистрированы'}