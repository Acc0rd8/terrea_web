from fastapi import HTTPException, status, Depends
from datetime import timezone, datetime
from jose import jwt, JWTError
from typing import Annotated

from src.dependencies.model_service import user_service
from src.dependencies.token_manager import TokenManager
from src.repositories.user_service import UserService
from src.models.model_user import User
from src.config import settings



class UserManager:
    @staticmethod
    async def get_current_user(token: Annotated[str, Depends(TokenManager.get_access_token)], user_service: Annotated[UserService, Depends(user_service)]) -> User:
        try:
            auth_data = settings.AUTH_DATA
            payload = jwt.decode(token, auth_data['secret_key'], algorithms=auth_data['algorithm'])
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Token is invalid'
            )
            
        expire = payload.get('exp')
        expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
        if not expire or (expire_time < datetime.now(timezone.utc)):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Токен истёк'
            )
            
        user_email = payload.get('sub')
        if user_email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Не найден ID пользователя'
            )
            
        user = await user_service.get_user_by_email(user_email)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Пользователь не найден'
            )
        return user