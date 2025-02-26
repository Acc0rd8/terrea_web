from datetime import datetime, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

from src.config import settings
from src.dependencies.model_service import user_service
from src.dependencies.token_manager import TokenManager
from src.models.model_user import User
from src.repositories.user_service import UserService
from src.logger import logger


class UserManager:
    @staticmethod
    async def get_current_user(token: Annotated[str, Depends(TokenManager.get_access_token)], user_service: Annotated[UserService, Depends(user_service)]) -> User:
        try:
            auth_data = settings.AUTH_DATA
            payload = jwt.decode(token, auth_data['secret_key'], algorithms=auth_data['algorithm'])
        except JWTError:
            logger.warning(msg='Token is invalid')
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={'message': 'Token is invalid', 'status_code' : status.HTTP_401_UNAUTHORIZED}
            )
            
        expire = payload.get('exp')
        expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
        if not expire or (expire_time < datetime.now(timezone.utc)):
            logger.warning(msg='Token expired', extra={'expire': expire})
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={'message': 'Токен истёк', 'status_code' : status.HTTP_401_UNAUTHORIZED}
            )
            
        user_email = payload.get('sub')
        if user_email is None:
            logger.warning(msg='ID have not found', extra={'user_email': user_email})
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={'message': 'Не найден ID пользователя', 'status_code' : status.HTTP_401_UNAUTHORIZED}
            )
            
        user = await user_service.get_user_by_email(user_email)
        if user is None:
            logger.warning(msg='User have not found')
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={'message': 'Пользователь не найден', 'status_code' : status.HTTP_401_UNAUTHORIZED}
            )
        return user