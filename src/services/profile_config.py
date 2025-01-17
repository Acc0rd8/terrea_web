import re

from fastapi import HTTPException, Response, status, Request

from src.dependencies.model_service import UserService
from src.dependencies.password_manager import PasswordManager
from src.dependencies.token_manager import TokenManager
from src.models.model_user import User
from src.schemas.token_schemas import Token
from src.schemas.user_schemas import UserAuth, UserCreate, UserDelete, UserRead, UserUpdate
from src.logger import logger


class ProfileConfig:
    @staticmethod
    async def register_new_user(response: Response, user_data: UserCreate, user_service: UserService) -> dict:
        user_exist = await user_service.get_user_by_email(user_data.email)
        if user_exist:
            msg = 'User already exists'
            extra = user_data.model_dump()
            logger.warning(msg=msg, extra=extra)
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='User already exists'
            )
        
        username_exist = await user_service.get_user_by_name(user_data.username)
        if username_exist:
            msg = 'Username is already taken'
            extra = {'username': username_exist}
            logger.warning(msg=msg, extra=extra)
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Username is already taken'
            )
        
        user_dict = user_data.model_dump()
        user_dict['password'] = PasswordManager().get_password_hash(user_data.password)
        await user_service.create_user(UserCreate(**user_dict))
        
        access_token = TokenManager.create_access_token({'sub': str(user_data.email)})
        response.set_cookie(key='user_access_token', value=access_token, httponly=True)
        return {'message': 'Successful registration'}

    @staticmethod
    async def user_authentication(response: Response, request: Request, user_data: UserAuth, user_service: UserService) -> Token:
        token = request.cookies.get('user_access_token')
        if token:
            msg = 'User is already login'
            logger.warning(msg=msg)
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='User is already login'
            )
        
        user = await user_service.get_user_by_email(user_data.email)
        if user is None:
            msg = 'User doesnt exist'
            logger.warning(msg=msg)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Incorrect email or password'
            )
        user_model_check = UserAuth.model_validate(user)
        if user_data.email != user_model_check.email or (not PasswordManager().verify_password(user_data.password, user_model_check.password)):
            msg = 'Incorrect email or password'
            extra = {'email': user_data.email, 'password': user_data.password}
            logger.warning(msg=msg, extra=extra)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Incorrect email or password'
            )
            
        user_model_update = UserUpdate.model_validate(user)
        if not user_model_update.is_active:
            user_model_update.is_active = True
            await user_service.update_user(user_model_update, user_model_update.email)
        
        access_token = TokenManager.create_access_token({'sub': str(user_data.email)})
        response.set_cookie(key='user_access_token', value=access_token, httponly=True)
        return Token(access_token=access_token, token_type='cookie')

    @staticmethod
    async def update_current_user(response: Response, user_data: User, user_data_update: UserUpdate, user_service: UserService) -> UserRead:
        new_user_dict = user_data_update.model_dump()
        new_user_dict['password'] = PasswordManager().get_password_hash(user_data_update.password)
        
        new_user_data = await user_service.update_user(UserUpdate(**new_user_dict), user_data.email)
        
        #TODO May be create refresh_token?....
        response.delete_cookie(key='user_access_token')
        access_token = TokenManager.create_access_token({'sub': str(user_data_update.email)})
        response.set_cookie(key='user_access_token', value=access_token, httponly=True)
        
        new_user_model = UserRead.model_validate(new_user_data)
        date = re.search(r'\d{4}-\d{2}-\d{2}', f'{new_user_model.registred_at}')
        new_user_model.registred_at = date[0]
        return new_user_model
    
    @staticmethod
    async def get_user_me(user_data: User) -> UserRead:
        user_model = UserRead.model_validate(user_data)
        date = re.search(r'\d{4}-\d{2}-\d{2}', f'{user_model.registred_at}')
        user_model.registred_at = date[0]
        return user_model
    
    @staticmethod
    async def get_another_user(username: str, user_service: UserService) -> UserRead:
        another_user = await user_service.get_user_by_name(username)
        if another_user is None:
            msg = 'User doesnt exist'
            logger.warning(msg=msg)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User doesnt exist :('
            )
        another_user_model = UserRead.model_validate(another_user)
        date = re.search(r'\d{4}-\d{2}-\d{2}', f'{another_user.registred_at}')
        another_user_model.registred_at = date[0]
        return another_user_model

    @staticmethod
    async def logout_current_user(response: Response, user_data: User, user_service: UserService) -> dict:
        response.delete_cookie(key='user_access_token')
        user_model_update = UserUpdate.model_validate(user_data)
        user_model_update.is_active = False
        await user_service.update_user(user_model_update, user_model_update.email)
        return {'message': 'User successfully logged out'}

    @staticmethod
    async def delete_current_user(response: Response, user_data: User, user_service: UserService) -> dict:
        response.delete_cookie(key='user_access_token')
        user_model_data = UserDelete.model_validate(user_data)
        await user_service.delete_one_user(user_model_data.email)
        return {'message': 'User account has been deleted'}
