import re

from fastapi import Response, status, Request
from sqlalchemy.exc import SQLAlchemyError

from src.dependencies.model_service import UserService
from src.dependencies.password_manager import PasswordManager
from src.dependencies.token_manager import TokenManager
from src.dependencies.validation_manager import ValidationManager
from src.exceptions.auth_error import AuthError
from src.exceptions.conflict_error import ConflictError
from src.exceptions.validation_error import ValidationError
from src.exceptions.server_error import ServerError
from src.exceptions.exist_error import ExistError
from src.models.model_user import User
from src.schemas.user_schemas import UserAuth, UserCreate, UserDelete, UserRead, UserUpdate
from src.schemas.response_schema import ResponseSchema
from src.logger import logger
from src.tasks.tasks import send_register_confirmation_email


class ProfileConfig:
    """
    Profile router service
    
    Fields:
        <self> __user_service (UserService): User DAO service
    """
    
    def __init__(self, user_service: UserService):
        self.__user_service = user_service
        
    async def register_new_user(self, response: Response, user_data: UserCreate) -> ResponseSchema:
        """
        Register new User

        Args:
            response (Response): Response to User
            user_data (UserCreate): User data Validation

        Raises:
            ConflictError: status - 409, User is trying to create existing account
            ConflictError: status - 409, User is trying to take existing Username
            ValidationError: status - 400, User input symbols are incorrect
            ServerError: status - 500, SERVER ERROR

        Returns:
            ResponseSchema: {'status_code': 200, 'message': True}
        """
        try:
            # Get User from Database
            user_exist = await self.__user_service.get_user_by_email(user_data.email) # Check if User is already exist (User, None)
            if user_exist:
                msg = 'User already exists'
                extra = user_data.model_dump()
                logger.warning(msg=msg, extra=extra, exc_info=True)  # log
                raise ConflictError('User already exists')
            
            # Check if username exists
            username_exists = await self.__user_service.get_user_by_name(user_data.username) # Check if Username is already taken (User, None)
            if username_exists:
                msg = 'Username is already taken'
                extra = {'username': username_exists}
                logger.warning(msg=msg, extra=extra, exc_info=True) # log
                raise ConflictError('Username is already taken')
            
            # Validation User data
            user_dict = user_data.model_dump()  # Converting Pydantic model (UserCreate) to dict
            if await ValidationManager.validate_schemas_data_user(user_dict):
                # Creating User
                user_dict['password'] = PasswordManager().get_password_hash(user_data.password)
                await self.__user_service.create_user(UserCreate(**user_dict))
                
                # Create token and set Cookie
                access_token = TokenManager.create_access_token({'sub': str(user_data.email)})
                response.set_cookie(key='user_access_token', value=access_token, httponly=True) # Only HTTP
                logger.debug(msg='User created / cookies set') # log
                
                # Celery task (sending confirmation email)
                send_register_confirmation_email.delay(user_dict['email'])
                
                return ResponseSchema(status_code=status.HTTP_200_OK, message=True)
            else:
                msg = 'Use only alphabet letters and numbers'
                extra = {'user_data': user_dict}
                logger.debug(msg=msg, extra=extra, exc_info=True) # log
                raise ValidationError('Use only alphabet letters and numbers')
        except SQLAlchemyError:
            raise ServerError()

    async def user_authentication(self, response: Response, request: Request, user_data: UserAuth) -> ResponseSchema:
        """
        User Login

        Args:
            response (Response): Response to User
            request (Request): Request from User
            user_data (UserAuth): User data Validation

        Raises:
            ConflictError: status - 409, A Logged-in User is trying to Login again
            AuthError: status - 401, Incorrect email or password
            AuthError: status - 401, Incorrect email or password
            ServerError: status - 500, SERVER ERROR

        Returns:
            ResponseSchema: {'status_code': 200, 'message': True}
        """
        try:
            # Get token from cookies and check if User is already logged-in
            token = request.cookies.get('user_access_token') # Get User cookie 'user_access_token' from request
            if token: # If token exists => User is already logged-in
                msg = 'User is already login'
                extra = {'token_info': token}
                logger.warning(msg=msg, extra=extra, exc_info=True)  # log
                raise ConflictError('User is already login')
            
            # Check if User exists in the Database
            user = await self.__user_service.get_user_by_email(user_data.email) # Searching for a User in the Database
            if user is None:
                msg = 'Incorrect email or password'
                logger.warning(msg=msg, exc_info=True)
                raise AuthError(msg='Incorrect email or password')
            
            # Compare User data with data in the Database
            user_model_check = UserAuth.model_validate(user) # Converting SQLAlchemy model to Pydantic model (UserAuth)
            if user_data.email != user_model_check.email or (not PasswordManager().verify_password(user_data.password, user_model_check.password)):
                msg = 'Incorrect email or password'
                extra = {'email': user_data.email, 'password': user_data.password}
                logger.warning(msg=msg, extra=extra, exc_info=True) # log
                raise AuthError(msg='Incorrect email or password')
            
            # Check if User isn't active
            user_model_update = UserUpdate.model_validate(user) # Converting SQLAlchemy model to Pydantic model (UserUpdate)
            if not user_model_update.is_active:
                user_model_update.is_active = True
                await self.__user_service.update_user(user_model_update, user_model_update.email)
            
            # Create token and set Cookie
            access_token = TokenManager.create_access_token({'sub': str(user_data.email)})
            response.set_cookie(key='user_access_token', value=access_token, httponly=True) # Only HTTP
            
            return ResponseSchema(status_code=status.HTTP_200_OK, message=True)
        except SQLAlchemyError:
            raise ServerError()

    async def update_current_user(self, response: Response, user_data: User, user_data_update: UserUpdate) -> UserRead:
        """
        Update User Account

        Args:
            response (Response): Response to User
            user_data (User): User data (SQLAlchemy Model)
            user_data_update (UserUpdate): User update data Validation

        Raises:
            ValidationError: status - 400, User input symbols are incorrect
            ServerError: status - 500, SERVER ERROR

        Returns:
            UserRead: Updated User data
        """
        try:
            # Validation User data
            new_user_dict = user_data_update.model_dump() # Converting Pydantic model (UserUpdate) to dict
            if await ValidationManager.validate_schemas_data_user(new_user_dict):
                # Updating User data
                new_user_dict['password'] = PasswordManager().get_password_hash(user_data_update.password) # Hashing new password
                new_user_data = await self.__user_service.update_user(UserUpdate(**new_user_dict), user_data.email)
                
                #TODO May be create refresh_token?....
                # Recreate the token
                response.delete_cookie(key='user_access_token')
                access_token = TokenManager.create_access_token({'sub': str(user_data_update.email)})
                response.set_cookie(key='user_access_token', value=access_token, httponly=True) # Only HTTP
                
                # Show User data
                new_user_model = UserRead.model_validate(new_user_data) # Converting SQLAlchemy model to Pydantic model (UserRead)
                date = re.search(r'\d{4}-\d{2}-\d{2}', f'{new_user_model.registred_at}') # Date type YYYY-MM-DD
                new_user_model.registred_at = date[0]
                return new_user_model
            else:
                msg = 'Use only alphabet letters and numbers'
                extra = {'new_user_dict': new_user_dict}
                logger.warning(msg=msg, extra=extra, exc_info=True) # log
                raise ValidationError('Use only alphabet letters and numbers')
        except SQLAlchemyError:
            raise ServerError()
    
    async def get_user_me(self, user_data: User) -> UserRead:
        """
        Show current User profile

        Args:
            user_data (User): User data (SQLAlchemy Model)

        Raises:
            ServerError: status - 500, SERVER ERROR

        Returns:
            UserRead: User data
        """
        try:
            # Show User data
            user_model = UserRead.model_validate(user_data) # Converting SQLAlchemy model to Pydantic model (UserRead)
            date = re.search(r'\d{4}-\d{2}-\d{2}', f'{user_model.registred_at}') # Date type YYYY-MM-DD
            user_model.registred_at = date[0]
            
            # From "date", "datetime" to "str"
            for project in user_model.projects:
                project.created_at = str(project.created_at)
                for project_task in project.project_tasks:
                    project_task.created_at = str(project_task.created_at)
                    project_task.updated_at = str(project_task.updated_at)
                    project_task.deadline = str(project_task.deadline)

            for user_task in user_model.user_tasks:
                user_task.created_at = str(user_task.created_at)
                user_task.updated_at = str(user_task.updated_at)
                user_task.deadline = str(user_task.deadline)
            
            return user_model
        except SQLAlchemyError:
            raise ServerError()
    
    async def get_another_user(self, username: str) -> UserRead:
        """
        Show another User profile

        Args:
            username (str): Another User username

        Raises:
            ExistError: status - 404, User doesn't exist
            ValidationError: status - 400, User input symbols are incorrect
            ServerError: status - 500, SERVER ERROR

        Returns:
            UserRead: User data
        """
        try:
            # Validation User data
            if await ValidationManager.validate_path_data(username): # Check User symbols
                # Searching for a User in the Database
                another_user = await self.__user_service.get_user_by_name(username) 
                if another_user is None:
                    msg = "User doesn't exist"
                    logger.warning(msg=msg)  # log
                    raise ExistError(msg="User doesn't exist")
                
                # Show User data
                another_user_model = UserRead.model_validate(another_user) # Converting SQLAlchemy model to Pydantic model (UserRead)
                date = re.search(r'\d{4}-\d{2}-\d{2}', f'{another_user.registred_at}') # Date type YYYY-MM-DD
                another_user_model.registred_at = date[0]
                return another_user_model
            else:
                msg = 'Use only alphabet letters and numbers'
                extra = {'username': username}
                logger.warning(msg=msg, extra=extra, exc_info=True) # log
                raise ValidationError(msg='Use only alphabet letters and numbers')
        except SQLAlchemyError:
            raise ServerError()

    async def logout_current_user(self, response: Response, user_data: User) -> ResponseSchema:
        """
        Current User Logout

        Args:
            response (Response): Response to User
            user_data (User): User data (SQLAlchemy model)

        Raises:
            ServerError: status - 500, SERVER ERROR

        Returns:
            ResponseSchema: {'status_code': 200, 'message': True} 
        """
        try:
            # Delete Cookie
            response.delete_cookie(key='user_access_token')
            
            # Update User data
            user_model_update = UserUpdate.model_validate(user_data) # Converting SQLAlchemy model to Pydantic model (UserUpdate)
            user_model_update.is_active = False # Change model field to FALSE
            await self.__user_service.update_user(user_model_update, user_model_update.email)
            
            return ResponseSchema(status_code=status.HTTP_200_OK, message=True)
        except SQLAlchemyError:
            raise ServerError()

    async def delete_current_user(self, response: Response, user_data: User) -> ResponseSchema:
        """
        Delete User account

        Args:
            response (Response): Response to User
            user_data (User): User data (SQLAlchemy model)

        Raises:
            ServerError: status - 500, SERVER ERROR

        Returns:
            ResponseSchema: {'status_code': 200, 'message': True}
        """
        try:
            # Delete Cookie
            response.delete_cookie(key='user_access_token')
            
            # Delete User from the Database
            user_model_data = UserDelete.model_validate(user_data) # Converting SQLAlchemy model to Pydantic model (UserDelete)
            await self.__user_service.delete_one_user(user_model_data.email)
            
            return ResponseSchema(status_code=status.HTTP_200_OK, message=True)
        except SQLAlchemyError:
            raise ServerError()
