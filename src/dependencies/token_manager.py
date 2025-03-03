from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, Request, status
from jose import jwt

from src.config import settings
from src.logger import logger


class TokenManager:
    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(days=int(settings.ACCESS_TOKEN_EXPIRE_DAYS))
            
        to_encode.update({'exp': expire}) # Add expire to jwt
        auth_data = settings.AUTH_DATA
        encode_jwt = jwt.encode(to_encode, auth_data['secret_key'], algorithm=auth_data['algorithm'])
        return encode_jwt

    @staticmethod
    def get_access_token(request: Request) -> str:
        token = request.cookies.get('user_access_token')
        if not token: # If User doesn't have a cookie 'user_access_token'
            logger.warning(msg='Token not found') # log
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={'message': 'Token not found', 'status_code': status.HTTP_401_UNAUTHORIZED}
            )
        return token
