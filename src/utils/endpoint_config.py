from fastapi import HTTPException, status, Response
import re

from src.utils.profile_config import get_password_hash, verify_password, create_access_token
from src.schemas.user_schemas import UserCreate, UserAuth, UserUpdate, UserRead, UserDelete
from src.services.project_service import ProjectService
from src.schemas.project_schemas import ProjectCreate
from src.services.user_service import UserService
from src.schemas.token_schemas import Token
from src.models.model_user import User


class Profile:
    @staticmethod
    async def register_new_user(user_data: UserCreate, user_service: UserService) -> dict:
        user = await user_service.get_user(user_data.email)
        if user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Пользователь уже существует'
            )
        user_dict = user_data.model_dump()
        user_dict['password'] = get_password_hash(user_data.password)
        await user_service.create_user(UserCreate(**user_dict))
        return {'message': 'Вы успешно зарегистрированы'}

    @staticmethod
    async def user_authentication(response: Response, user_data: UserAuth, user_service: UserService) -> Token:
        user = await user_service.get_user(user_data.email)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Неверная почта или пароль'
            )
            
        user_check = UserAuth.model_validate(user)
        if user_data.email != user_check.email or (not verify_password(user_data.password, user_check.password)):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Неверная почта или пароль'
            )
            
        user_update = UserUpdate.model_validate(user)
        if not user_update.is_active:
            user_update.is_active = True
            await user_service.update_user(user_update, user_update.email)
        
        access_token = create_access_token({'sub': str(user_data.email)})
        response.set_cookie(key='user_access_token', value=access_token, httponly=True)
        return Token(access_token=access_token, token_type='cookie')

    @staticmethod
    async def get_user_me(user_data: User) -> UserRead:
        user_dict = UserRead.model_validate(user_data)
        date = re.search(r'\d{4}-\d{2}-\d{2}', f'{user_dict.registred_at}')
        user_dict.registred_at = date[0]
        return user_dict

    @staticmethod
    async def logout_current_user(response: Response, user_data: User, user_service: UserService) -> dict:
        response.delete_cookie(key='user_access_token')
        user_update = UserUpdate.from_orm(user_data)
        user_update.is_active = False
        await user_service.update_user(user_update, user_update.email)
        return {'message': 'Пользователь успешно вышел из системы'}

    @staticmethod
    async def delete_current_user(response: Response, user_data: User, user_service: UserService):
        response.delete_cookie(key='user_access_token')
        user_data = UserDelete.from_orm(user_data)
        await user_service.delete_one_user(user_data.email)
        return {'message': 'Аккаунт пользователя был удалён'}
    

class Project:
    @staticmethod
    async def create_new_project(project_create: ProjectCreate, project_service: ProjectService) -> dict:
        await project_service.create_project(project_create)
        return {'message': 'Проект успешно создан'}