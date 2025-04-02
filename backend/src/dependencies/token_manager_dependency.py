from datetime import datetime, timedelta, timezone

from fastapi import Request
from jose import jwt

from src.exceptions import AuthError
from src.config import settings
from src.logger import logger


class TokenManagerDependency:
    """
    JWT + Cookie token manager
    """
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        
        # Check on expire
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(days=int(settings.ACCESS_TOKEN_EXPIRE_DAYS))
        
        # Encode token
        to_encode.update({'exp': expire}) # Add expire to jwt
        auth_data = settings.AUTH_DATA
        encode_jwt = jwt.encode(to_encode, auth_data['secret_key'], algorithm=auth_data['algorithm'])
        
        return encode_jwt

    @staticmethod
    def get_access_token(request: Request) -> str:
        token = request.cookies.get('user_access_token')
        if not token: # If User doesn't have a cookie 'user_access_token'
            logger.warning(msg='Token not found') # log
            raise AuthError(msg='Token not found')
        return token
