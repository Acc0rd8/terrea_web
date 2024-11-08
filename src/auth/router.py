from fastapi import APIRouter, HTTPException, status, Response, Request, Depends
from typing import Annotated

import re

from .schemas import UserCreate, UserAuth, UserRead, Token
from .basic_config import get_password_hash, verify_password, create_access_token, get_current_user
from ..models.user_and_role import User
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


@router.post('/login/')
async def authenticate_user(response: Response, user_data: UserAuth) -> Token:
    user = await get_user(user_data.email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверная почта или пароль'
        )
        
    user_check = UserAuth.from_orm(user)
    if user_data.email != user_check.email and (not verify_password(user_data.password, user_check.password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверная почта или пароль'
        )
        
    access_token = create_access_token({'sub': str(user_data.email)})
    response.set_cookie(key='users_access_token', value=access_token,httponly=True)
    return Token(access_token=access_token, token_type='cookie')


@router.post('/me/', response_model=UserRead)
async def get_me(user_data: Annotated[User, Depends(get_current_user)]):
    user_dict = UserRead.from_orm(user_data)
    date = re.search(r'\d{4}-\d{2}-\d{2}', f'{user_dict.registred_at}')
    user_dict.registred_at = date[0]
    return user_dict