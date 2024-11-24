from fastapi import APIRouter, Response, Depends, HTTPException
from typing import Annotated

from src.schemas.user_schemas import UserCreate, UserAuth, UserRead, UserUpdate
from src.business.auth_manager import UserManager
from src.services.user_service import UserService
from src.business.profile_config import Profile
from src.schemas.token_schemas import Token
from src.dependencies import user_service
from src.models.model_user import User


router = APIRouter(
    prefix='/profile',
    tags=['Profile'],
)


@router.post('/register')
async def register_user(response: Response, user_data: UserCreate, user_service: Annotated[UserService, Depends(user_service)]) -> dict:
    result = await Profile.register_new_user(response, user_data, user_service)
    return result


@router.post('/login')
async def authenticate_user(response: Response, user_data: UserAuth, user_service: Annotated[UserService, Depends(user_service)]) -> Token:
    result = await Profile.user_authentication(response, user_data, user_service)
    return result


@router.patch('/update_profile')
async def update_user(response: Response, user_data: Annotated[User, Depends(UserManager.get_current_user)], user_data_update: UserUpdate, user_service: Annotated[UserService, Depends(user_service)]):
    result = await Profile.update_current_user(response, user_data, user_data_update, user_service)
    return result


@router.get('/me')
async def get_me(user_data: Annotated[User, Depends(UserManager.get_current_user)]) -> UserRead:
    result = await Profile.get_user_me(user_data)
    return result


@router.get('/@{username}')
async def get_user(username: str, user_service: Annotated[UserService, Depends(user_service)]) -> UserRead:
    result = await Profile.get_another_user(username, user_service)
    return result


@router.post('/logout')
async def logout_user(response: Response, user_data: Annotated[User, Depends(UserManager.get_current_user)], user_service: Annotated[UserService, Depends(user_service)]) -> dict:
    result = await Profile.logout_current_user(response, user_data, user_service)
    return result


@router.delete('/delete_account')
async def delete_user_account(response: Response, user_data: Annotated[User, Depends(UserManager.get_current_user)], user_service: Annotated[UserService, Depends(user_service)]) -> dict:
    result = await Profile.delete_current_user(response, user_data, user_service)
    return result
