from typing import Annotated

from fastapi import APIRouter, Depends, Response, Request
from fastapi_cache.decorator import cache

from src.dependencies.model_service import user_service
from src.dependencies.user_manager import UserManager
from src.models.model_user import User
from src.repositories.user_service import UserService
from src.schemas.token_schemas import Token
from src.schemas.user_schemas import UserAuth, UserCreate, UserRead, UserUpdate
from src.services.profile_config import ProfileConfig

router = APIRouter(
    prefix='/profile',
    tags=['Profile'],
)


@router.post('/register')
async def register_user(response: Response, user_data: UserCreate, user_service: Annotated[UserService, Depends(user_service)]) -> dict:
    return await ProfileConfig.register_new_user(response, user_data, user_service)


@router.post('/login')
async def authenticate_user(response: Response, request: Request, user_data: UserAuth, user_service: Annotated[UserService, Depends(user_service)]) -> Token:
    return await ProfileConfig.user_authentication(response, request, user_data, user_service)


@router.patch('/update_profile')
async def update_user(response: Response, user_data: Annotated[User, Depends(UserManager.get_current_user)], user_data_update: UserUpdate, user_service: Annotated[UserService, Depends(user_service)]) -> UserRead:
    return await ProfileConfig.update_current_user(response, user_data, user_data_update, user_service)


@router.get('/me')
# @cache(expire=600)
async def get_me(user_data: Annotated[User, Depends(UserManager.get_current_user)]) -> UserRead:
    return await ProfileConfig.get_user_me(user_data)


@router.get('/@{username}')
async def get_user(username: str, user_service: Annotated[UserService, Depends(user_service)]) -> UserRead:
    return await ProfileConfig.get_another_user(username, user_service)


@router.post('/logout')
async def logout_user(response: Response, user_data: Annotated[User, Depends(UserManager.get_current_user)], user_service: Annotated[UserService, Depends(user_service)]) -> dict:
    return await ProfileConfig.logout_current_user(response, user_data, user_service)


@router.delete('/delete_account')
async def delete_user_account(response: Response, user_data: Annotated[User, Depends(UserManager.get_current_user)], user_service: Annotated[UserService, Depends(user_service)]) -> dict:
    return await ProfileConfig.delete_current_user(response, user_data, user_service)
