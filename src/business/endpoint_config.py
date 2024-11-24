from fastapi import HTTPException, status, Response
import re

from src.business.auth_config import PasswordManager, TokenManager
from src.schemas.user_schemas import UserCreate, UserAuth, UserUpdate, UserRead, UserDelete
from src.services.project_service import ProjectService
from src.schemas.project_schemas import ProjectCreate, ProjectRead
from src.services.user_service import UserService
from src.schemas.token_schemas import Token
from src.models.model_user import User


class Profile:
    #TODO Validate "username is already exist"
    #TODO After registration give user_access_token
    #TODO User is already login after authorization
    @staticmethod
    async def register_new_user(user_data: UserCreate, user_service: UserService) -> dict:
        user = await user_service.get_user_by_email(user_data.email)
        if user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Пользователь уже существует'
            )
        user_dict = user_data.model_dump()
        user_dict['password'] = PasswordManager().get_password_hash(user_data.password)
        await user_service.create_user(UserCreate(**user_dict))
        return {'message': 'Вы успешно зарегистрированы'}

    @staticmethod
    async def user_authentication(response: Response, user_data: UserAuth, user_service: UserService) -> Token:
        user = await user_service.get_user_by_email(user_data.email)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Неверная почта или пароль'
            )
            
        user_model_check = UserAuth.model_validate(user)
        if user_data.email != user_model_check.email or (not PasswordManager().verify_password(user_data.password, user_model_check.password)):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Неверная почта или пароль'
            )
            
        user_model_update = UserUpdate.model_validate(user)
        if not user_model_update.is_active:
            user_model_update.is_active = True
            await user_service.update_user(user_model_update, user_model_update.email)
        
        access_token = TokenManager.create_access_token({'sub': str(user_data.email)})
        response.set_cookie(key='user_access_token', value=access_token, httponly=True)
        return Token(access_token=access_token, token_type='cookie')

    @staticmethod
    async def get_user_me(user_data: User) -> UserRead:
        user_model = UserRead.model_validate(user_data)
        date = re.search(r'\d{4}-\d{2}-\d{2}', f'{user_model.registred_at}')
        user_model.registred_at = date[0]
        return user_model
    
    #TODO Search another user by username
    @staticmethod
    async def get_another_user(user_id: int, user_service: UserService) -> UserRead:
        another_user = await user_service.get_user_by_id(user_id)
        if another_user is None:
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
        return {'message': 'Пользователь успешно вышел из системы'}

    @staticmethod
    async def delete_current_user(response: Response, user_data: User, user_service: UserService):
        response.delete_cookie(key='user_access_token')
        user_model_data = UserDelete.model_validate(user_data)
        await user_service.delete_one_user(user_model_data.email)
        return {'message': 'Аккаунт пользователя был удалён'}
    

class Project:
    @staticmethod
    async def create_new_project(project_create: ProjectCreate, project_service: ProjectService) -> dict:
        await project_service.create_project(project_create)
        return {'message': 'Проект успешно создан'}
    
    #TODO
    @staticmethod
    async def get_some_project_by_id(project_id: int, project_service: ProjectService):
        project = await project_service.get_project(project_id)
        project_model = ProjectRead.model_validate(project)
        date = re.search(r'\d{4}-\d{2}-\d{2}', f'{project_model.created_at}')
        project_model.created_at = date[0]
        return project_model