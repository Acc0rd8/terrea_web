from fastapi import APIRouter, HTTPException, status, Response, Request

from .schemas import UserCreate, UserAuth, Token
from .basic_config import get_password_hash, verify_password, create_access_token
from ..crud import get_user, create_user

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


@router.post('/register/')
async def register_user(user_data: UserCreate) -> dict:
    user = await get_user(user_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь уже существует'
        )
    user_dict = user_data.model_dump()
    user_dict['password'] = get_password_hash(user_data.password)
    await create_user(UserCreate(**user_dict))
    return {'message': 'Вы успешно зарегистрированы'}


@router.post('/login/')
async def authenticate_user(response: Response, user_data: UserAuth) -> Token:
    user = get_user(user_data.email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверная почта или пароль'
        )
        
    user_check = UserAuth.from_orm(user)
    if user_data.email != user_check.email and (not verify_password(user_data.password, user_check.password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверная почта или пароль'
        )
        
    access_token = create_access_token({'sub': str(user_data.email)})
    response.set_cookie(key='users_access_token', value=access_token,httponly=True)
    return Token(access_token=access_token, token_type='cookie')