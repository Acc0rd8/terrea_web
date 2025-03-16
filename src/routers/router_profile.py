from typing import Annotated

from fastapi import APIRouter, Depends, Response, Request

from src.dependencies.user_manager import UserManager
from src.dependencies.router_service import get_profile_config
from src.models.model_user import User
from src.schemas.user_schemas import UserAuth, UserCreate, UserRead, UserUpdate
from src.services.profile_config import ProfileConfig
from src.redis_config import app_redis

router = APIRouter(
    prefix='/profile',
    tags=['Profile'],
)


@router.post('/register') # HTTP POST
async def register_user(
    response: Response,
    user_data: UserCreate,
    profile_config: Annotated[ProfileConfig, Depends(get_profile_config)]
) -> dict:
    """
    Register new User

    Args:
        response (Response): Response to User
        user_data (UserCreate): User data Validation

    Returns:
        dict[str, str | int]: Successfull registration 
    """
    return await profile_config.register_new_user(response, user_data)


@router.post('/login') # HTTP POST
async def authenticate_user(
    response: Response,
    request: Request,
    user_data: UserAuth,
    profile_config: Annotated[ProfileConfig, Depends(get_profile_config)]
) -> dict:
    """
    User Login

    Args:
        response (Response): Response to User
        request (Request): Request from User
        user_data (UserAuth): User data Validation

    Returns:
        dict[str, bool]: True
    """
    return await profile_config.user_authentication(response, request, user_data)


@router.patch('/update_profile') # HTTP PATCH
async def update_user(
    response: Response,
    user_data_update: UserUpdate,
    user_data: Annotated[User, Depends(UserManager.get_current_user)],
    profile_config: Annotated[ProfileConfig, Depends(get_profile_config)]
) -> UserRead:
    """
    Update User Account

    Args:
        response (Response): Response to User
        user_data_update (UserUpdate): User update data Validation
        user_data (User): User data (SQLAlchemy Model)

    Returns:
        UserRead: Updated User data
    """
    return await profile_config.update_current_user(response, user_data, user_data_update)


@router.get('/me') # HTTP GET
@app_redis.cache
async def get_me(
    user_data: Annotated[User, Depends(UserManager.get_current_user)],
    profile_config: Annotated[ProfileConfig, Depends(get_profile_config)]
) -> UserRead:
    """
    Show current User profile

    Args:
        user_data (User): User data (SQLAlchemy Model)

    Returns:
        UserRead: User data
    """
    return await profile_config.get_user_me(user_data)


@router.get('/@{username}') # HTTP GET
async def get_user(
    username: str,
    profile_config: Annotated[ProfileConfig, Depends(get_profile_config)]
) -> UserRead:
    """
    Show another User profile

    Args:
        username (str): Another User username

    Returns:
        UserRead: User data
    """
    return await profile_config.get_another_user(username)


@router.post('/logout') # HTTP POST
async def logout_user(
    response: Response,
    user_data: Annotated[User, Depends(UserManager.get_current_user)],
    profile_config: Annotated[ProfileConfig, Depends(get_profile_config)]
) -> dict:
    """
    Current User Logout

    Args:
        response (Response): Response to User
        user_data (User): User data (SQLAlchemy model)

    Returns:
        dict[str, str | int]: User successfull logout 
    """
    return await profile_config.logout_current_user(response, user_data)


@router.delete('/delete_account') # HTTP DELETE
async def delete_user_account(
    response: Response,
    user_data: Annotated[User, Depends(UserManager.get_current_user)],
    profile_config: Annotated[ProfileConfig, Depends(get_profile_config)]
) -> dict:
    """
    Delete User account

    Args:
        response (Response): Response to User
        user_data (User): User data (SQLAlchemy model)

    Returns:
        dict[str, str | int]: User account has been deleted
    """
    return await profile_config.delete_current_user(response, user_data)
