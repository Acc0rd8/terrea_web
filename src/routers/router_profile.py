from fastapi import APIRouter, HTTPException, status, Response, Depends
from typing import Annotated
import re

from src.utils.basic_config import get_password_hash, verify_password, create_access_token, get_current_user
from src.schemas.user_schemas import UserCreate, UserAuth, UserRead, UserUpdate, UserDelete
from src.services.user_service import UserService
from src.schemas.token_schemas import Token
from src.dependencies import user_service
from src.models.model_user import User


router = APIRouter(
    prefix='/profile',
    tags=['Profile'],
)


@router.post('/register/')
async def register_user(user_data: UserCreate, user_service: Annotated[UserService, Depends(user_service)]) -> dict:
    user = await user_service.get_user(user_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь уже существует'
        )
    user_dict = user_data.model_dump()
    user_dict['password'] = get_password_hash(user_data.password)
    await user_service.create_user(UserCreate(**user_dict))
    return {'message': 'Вы успешно зарегистрированы'}


@router.post('/login/')
async def authenticate_user(response: Response, user_data: UserAuth, user_service: Annotated[UserService, Depends(user_service)]) -> Token:
    user = await user_service.get_user(user_data.email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверная почта или пароль'
        )
        
    user_check = UserAuth.from_orm(user)
    if user_data.email != user_check.email or (not verify_password(user_data.password, user_check.password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверная почта или пароль'
        )
        
    user_update = UserUpdate.from_orm(user)
    if not user_update.is_active:
        user_update.is_active = True
        await user_service.update_user(user_update, user_update.email)
    
    access_token = create_access_token({'sub': str(user_data.email)})
    response.set_cookie(key='user_access_token', value=access_token, httponly=True)
    return Token(access_token=access_token, token_type='cookie')


@router.get('/me/')
async def get_me(user_data: Annotated[User, Depends(get_current_user)]) -> UserRead:
    user_dict = UserRead.from_orm(user_data)
    date = re.search(r'\d{4}-\d{2}-\d{2}', f'{user_dict.registred_at}')
    user_dict.registred_at = date[0]
    return user_dict


@router.post('/logout/')
async def logout_user(response: Response, user_data: Annotated[User, Depends(get_current_user)], user_service: Annotated[UserService, Depends(user_service)]) -> dict:
    response.delete_cookie(key='user_access_token')
    user_update = UserUpdate.from_orm(user_data)
    user_update.is_active = False
    await user_service.update_user(user_update, user_update.email)
    return {'message': 'Пользователь успешно вышел из системы'}


@router.delete('/delete_account')
async def delete_user_account(response: Response, user_data: Annotated[User, Depends(get_current_user)], user_service: Annotated[UserService, Depends(user_service)]) -> dict:
    response.delete_cookie(key='user_access_token')
    user_data = UserDelete.from_orm(user_data)
    await user_service.delete_one_user(user_data.email)
    return {'message': 'Аккаунт пользователя был удалён'}
