from fastapi import APIRouter, Response, Depends
from typing import Annotated

from src.schemas.user_schemas import UserCreate, UserAuth, UserRead
from src.utils.profile_config import get_current_user
from src.services.user_service import UserService
from src.utils.endpoint_config import Profile
from src.schemas.token_schemas import Token
from src.dependencies import user_service
from src.models.model_user import User


router = APIRouter(
    prefix='/profile',
    tags=['Profile'],
)


@router.post('/register/')
async def register_user(user_data: UserCreate, user_service: Annotated[UserService, Depends(user_service)]) -> dict:
    result = await Profile.register_new_user(user_data, user_service)
    return result


@router.post('/login/')
async def authenticate_user(response: Response, user_data: UserAuth, user_service: Annotated[UserService, Depends(user_service)]) -> Token:
    result = await Profile.user_authentication(response, user_data, user_service)
    return result


@router.get('/me/')
async def get_me(user_data: Annotated[User, Depends(get_current_user)]) -> UserRead:
    result = await Profile.get_user_me(user_data)
    return result


@router.post('/logout/')
async def logout_user(response: Response, user_data: Annotated[User, Depends(get_current_user)], user_service: Annotated[UserService, Depends(user_service)]) -> dict:
    result = await Profile.logout_current_user(response, user_data, user_service)
    return result


@router.delete('/delete_account')
async def delete_user_account(response: Response, user_data: Annotated[User, Depends(get_current_user)], user_service: Annotated[UserService, Depends(user_service)]) -> dict:
    result = await Profile.delete_current_user(response, user_data, user_service)
    return result
