from fastapi import APIRouter, HTTPException, status, Response, Request, Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession


import re

from src.profile.schemas import UserCreate, UserAuth, UserRead, UserUpdate, UserDelete, Token
from src.profile.basic_config import get_password_hash, verify_password, create_access_token, get_current_user
from src.profile.models import User
from src.profile.crud.crud_user import get_user, create_user, update_user, delete_user
from src.database import get_async_session


router = APIRouter(
    prefix='/profile',
    tags=['Profile'],
)


@router.post('/register/')
async def register_user(user_data: UserCreate, session: AsyncSession = Depends(get_async_session)) -> dict:
    user = await get_user(user_data.email, session)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь уже существует'
        )
    user_dict = user_data.model_dump()
    user_dict['password'] = get_password_hash(user_data.password)
    await create_user(UserCreate(**user_dict), session)
    return {'message': 'Вы успешно зарегистрированы'}


@router.post('/login/', response_model=Token)
async def authenticate_user(response: Response, user_data: UserAuth,  session: AsyncSession = Depends(get_async_session)):
    user = await get_user(user_data.email, session)
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
        
    user_update_dict = UserUpdate.from_orm(user)
    if not user_update_dict.is_active:
        user_update_dict.is_active = True
        await update_user(user_update_dict, user_update_dict.email, session)
    
    access_token = create_access_token({'sub': str(user_data.email)})
    response.set_cookie(key='user_access_token', value=access_token,httponly=True)
    return Token(access_token=access_token, token_type='cookie')


@router.get('/me/', response_model=UserRead)
async def get_me(user_data: Annotated[User, Depends(get_current_user)]):
    user_dict = UserRead.from_orm(user_data)
    date = re.search(r'\d{4}-\d{2}-\d{2}', f'{user_dict.registred_at}')
    user_dict.registred_at = date[0]
    return user_dict


@router.post('/logout/')
async def logout_user(response: Response, user_data: Annotated[User, Depends(get_current_user)],  session: AsyncSession = Depends(get_async_session)) -> dict:
    response.delete_cookie(key='user_access_token')
    user_update_dict = UserUpdate.from_orm(user_data)
    user_update_dict.is_active = False
    await update_user(user_update_dict, user_update_dict.email, session)
    return {'message': 'Пользователь успешно вышел из системы'}


@router.delete('/delete_account')
async def delete_user_account(response: Response, user_data: Annotated[User, Depends(get_current_user)], session: AsyncSession = Depends(get_async_session)) -> dict:
    response.delete_cookie(key='user_access_token')
    user_data_dict = UserDelete.from_orm(user_data)
    await delete_user(user_data_dict.email, session)
    return {'message': 'Аккаунт пользователя был удалён'}
