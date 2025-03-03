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
        """
        Check if User Logeed-in

        Args:
            token (Annotated[str, Depends): Dependencies with 'TokenManager.get_access_token'
            user_service (Annotated[UserService, Depends): Dependencies with 'src.dependencies.model_service.user_service'. User DAO service

        Raises:
            HTTPException: status - 401, Token is invalid
            HTTPException: status - 401, Token has expired
            HTTPException: status - 401, User ID not found
            HTTPException: status - 401, User not found

        Returns:
            User: User SQLAlchemy model
        """
        try:
            auth_data = settings.AUTH_DATA
            payload = jwt.decode(token, auth_data['secret_key'], algorithms=auth_data['algorithm'])
        except JWTError:
            logger.warning(msg='Token is invalid') # log
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={'message': 'Token is invalid', 'status_code' : status.HTTP_401_UNAUTHORIZED}
            )
            
        expire = payload.get('exp') # Take 'expire' from jwt
        expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc) # Converting to datetime
        if not expire or (expire_time < datetime.now(timezone.utc)):
            logger.warning(msg='Token has expired', extra={'expire': expire}) # log
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={'message': 'Token has expired', 'status_code' : status.HTTP_401_UNAUTHORIZED}
            )
            
        user_email = payload.get('sub') # Take 'sub' from jwt
        if user_email is None:
            logger.warning(msg='User ID not found', extra={'user_email': user_email}) # log
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={'message': 'User ID not found', 'status_code' : status.HTTP_401_UNAUTHORIZED}
            )
            
        user = await user_service.get_user_by_email(user_email) # Searching User in the Database
        if user is None:
            logger.warning(msg='User not found') # log
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={'message': 'User not found', 'status_code' : status.HTTP_401_UNAUTHORIZED}
            )
        return user