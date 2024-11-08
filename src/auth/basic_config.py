from passlib.context import CryptContext
from fastapi import Request, HTTPException, status
from jose import jwt

from datetime import timedelta, timezone, datetime

from ..config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRES_DAYS


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


#PASSWORD 
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


#PASSWORD
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


#TOKEN
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=ACCESS_TOKEN_EXPIRES_DAYS)
        
    to_encode.update({'exp': expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


#TOKEN
def get_token(request: Request) -> str:
    token = request.cookies.get('users_access_token')
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token not found'
        )
    return token