from fastapi import Request, HTTPException, status, Depends
from datetime import timedelta, timezone, datetime
from passlib.context import CryptContext
from jose import jwt, JWTError
from typing import Annotated

from src.services.user_service import UserService
from src.dependencies import user_service
from src.models.model_user import User
from src.config import settings


class PasswordManager:
    def __init__(self, schemes: list[str] = ['bcrypt'], deprecated: str = 'auto'):
        self.pwd_context = CryptContext(schemes=schemes, deprecated=deprecated)
    
    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)


class TokenManager:
    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(days=int(settings.ACCESS_TOKEN_EXPIRE_DAYS))
            
        to_encode.update({'exp': expire})
        auth_data = settings.AUTH_DATA
        encode_jwt = jwt.encode(to_encode, auth_data['secret_key'], algorithm=auth_data['algorithm'])
        return encode_jwt

    @staticmethod
    def get_token(request: Request) -> str:
        token = request.cookies.get('user_access_token')
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Token not found'
            )
        return token


class UserManager:
    @staticmethod
    async def get_current_user(token: Annotated[str, Depends(TokenManager.get_token)], user_service: Annotated[UserService, Depends(user_service)]) -> User:
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
            
        user = await user_service.get_user(user_email)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Пользователь не найден'
            )
        return user
