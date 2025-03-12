from typing import Annotated

from fastapi import APIRouter, Depends, Response, Request
from fastapi_cache.decorator import cache

from src.dependencies.model_service import user_service
from src.dependencies.redis_service import redis_string_type_service, redis_hash_type_service
from src.dependencies.user_manager import UserManager
from src.models.model_user import User
from src.repositories.user_service import UserService
from src.redis_repositories.redis_string_type_service import RedisStringTypeService
from src.redis_repositories.redis_hash_type_service import RedisHashTypeService
from src.schemas.token_schemas import Token
from src.schemas.user_schemas import UserAuth, UserCreate, UserRead, UserUpdate
from src.services.profile_config import ProfileConfig

router = APIRouter(
    prefix='/profile',
    tags=['Profile'],
)


@router.post('/register') # HTTP POST
async def register_user(
    response: Response,
    user_data: UserCreate,
    user_service: Annotated[UserService, Depends(user_service)]
) -> dict:
    """
    Register new User

    Args:
        response (Response): Response to User
        user_data (UserCreate): User data Validation
        user_service (UserService): User DAO service

    Returns:
        dict[str, str | int]: Successfull registration 
    """
    return await ProfileConfig.register_new_user(response, user_data, user_service)


@router.post('/login') # HTTP POST
async def authenticate_user(
    response: Response,
    request: Request,
    user_data: UserAuth,
    user_service: Annotated[UserService, Depends(user_service)]
) -> dict:
    """
    User Login

    Args:
        response (Response): Response to User
        request (Request): Request from User
        user_data (UserAuth): User data Validation
        user_service (UserService): User DAO service

    Returns:
        dict[str, bool]: True
    """
    return await ProfileConfig.user_authentication(response, request, user_data, user_service)


@router.patch('/update_profile') # HTTP PATCH
async def update_user(
    response: Response,
    user_data_update: UserUpdate,
    user_data: Annotated[User, Depends(UserManager.get_current_user)],
    user_service: Annotated[UserService, Depends(user_service)]
) -> UserRead:
    """
    Update User Account

    Args:
        response (Response): Response to User
        user_data_update (UserUpdate): User update data Validation
        user_data (User): User data (SQLAlchemy Model)
        user_service (UserService): User DAO service

    Returns:
        UserRead: Updated User data
    """
    return await ProfileConfig.update_current_user(response, user_data, user_data_update, user_service)


@router.get('/me') # HTTP GET
async def get_me(
    user_data: Annotated[User, Depends(UserManager.get_current_user)],
    redis_hash_type_service: Annotated[RedisHashTypeService, Depends(redis_hash_type_service)]
) -> UserRead:
    """
    Show current User profile

    Args:
        user_data (User): User data (SQLAlchemy Model)
        redis_hash_type_service (RedisHashTypeService): Redis hash type service

    Returns:
        UserRead: User data
    """
    return await ProfileConfig.get_user_me(user_data, redis_hash_type_service)


@router.get('/@{username}') # HTTP GET
async def get_user(
    username: str,
    user_service: Annotated[UserService, Depends(user_service)],
    redis_hash_type_service: Annotated[RedisHashTypeService, Depends(redis_hash_type_service)]
) -> UserRead:
    """
    Show another User profile

    Args:
        username (str): Another User username
        user_service (UserService): User DAO service
        redis_hash_type_service (RedisHashTypeService): Redis hash type service

    Returns:
        UserRead: User data
    """
    return await ProfileConfig.get_another_user(username, user_service, redis_hash_type_service)


@router.post('/logout') # HTTP POST
async def logout_user(
    response: Response,
    user_data: Annotated[User, Depends(UserManager.get_current_user)],
    user_service: Annotated[UserService, Depends(user_service)]
) -> dict:
    """
    Current User Logout

    Args:
        response (Response): Response to User
        user_data (User): User data (SQLAlchemy model)
        user_service (UserService): User DAO service

    Returns:
        dict[str, str | int]: User successfull logout 
    """
    return await ProfileConfig.logout_current_user(response, user_data, user_service)


@router.delete('/delete_account') # HTTP DELETE
async def delete_user_account(
    response: Response,
    user_data: Annotated[User, Depends(UserManager.get_current_user)],
    user_service: Annotated[UserService, Depends(user_service)],
    redis_hash_type_service: Annotated[RedisHashTypeService, Depends(redis_hash_type_service)]
) -> dict:
    """
    Delete User account

    Args:
        response (Response): Response to User
        user_data (User): User data (SQLAlchemy model)
        user_service (UserService): User DAO service
        redis_hash_type_service (RedisHashTypeService): Redis hash type service

    Returns:
        dict[str, str | int]: User account has been deleted
    """
    return await ProfileConfig.delete_current_user(response, user_data, user_service, redis_hash_type_service)
