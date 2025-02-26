import re

from fastapi import HTTPException, Response, status, Request
from sqlalchemy.exc import SQLAlchemyError

from src.dependencies.model_service import UserService
from src.dependencies.password_manager import PasswordManager
from src.dependencies.token_manager import TokenManager
from src.dependencies.security import Security
from src.models.model_user import User
from src.schemas.token_schemas import Token
from src.schemas.user_schemas import UserAuth, UserCreate, UserDelete, UserRead, UserUpdate
from src.logger import logger


class ProfileConfig:
    @staticmethod
    async def register_new_user(response: Response, user_data: UserCreate, user_service: UserService) -> dict:
        """
        Register new User

        Args:
            response (Response): Response to User
            user_data (UserCreate): User data Validation
            user_service (UserService): User DAO service

        Raises:
            HTTPException: status - 409, User is trying to create existing account
            HTTPException: status - 409, User is trying to take existing Username
            HTTPException: status - 400, User input symbols are incorrect
            HTTPException: status - 500, SERVER ERROR

        Returns:
            dict[str, str]: Successfull registration 
        """        
        try:
            user_exist = await user_service.get_user_by_email(user_data.email) # Check if User is already exist (User, None)
            if user_exist:
                msg = 'User already exists'
                extra = user_data.model_dump()
                logger.warning(msg=msg, extra=extra, exc_info=False)  # log
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail={'message': 'User already exists', 'status_code': status.HTTP_409_CONFLICT}
                )
            
            username_exist = await user_service.get_user_by_name(user_data.username) # Check if Username is already taken (User, None)
            if username_exist:
                msg = 'Username is already taken'
                extra = {'username': username_exist}
                logger.warning(msg=msg, extra=extra)  # log
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail={'message':'Username is already taken', 'status_code': status.HTTP_409_CONFLICT}
                )
            
            user_dict = user_data.model_dump()  # Converting Pydantic model (UserCreate) to dict
            if await Security.validate_schemas_data_user(user_dict):    # Check User symbols
                user_dict['password'] = PasswordManager().get_password_hash(user_data.password) # Hashing password
                await user_service.create_user(UserCreate(**user_dict))
                access_token = TokenManager.create_access_token({'sub': str(user_data.email)})  # Creating Token
                response.set_cookie(key='user_access_token', value=access_token, httponly=True, samesite='none') # Only HTTP
                return {'message': 'Successful registration'}
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={'message': 'Use only alphabet letters and numbers', 'status_code': status.HTTP_400_BAD_REQUEST}
                )
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={'message': 'Server Error', 'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR}
            )

    @staticmethod
    async def user_authentication(response: Response, request: Request, user_data: UserAuth, user_service: UserService) -> Token:
        """
        User Login

        Args:
            response (Response): Response to User
            request (Request): Request from User
            user_data (UserAuth): User data Validation
            user_service (UserService): User DAO service

        Raises:
            HTTPException: status - 409, A Logged-in User is trying to Login again
            HTTPException: status - 401, Incorrect email or password
            HTTPException: status - 401, Incorrect email or password
            HTTPException: status - 500, SERVER ERROR

        Returns:
            Token: Token with access token and token_type (Rework on production)
        """        
        try:
            token = request.cookies.get('user_access_token') # Get User cookie 'user_access_token' from request
            if token:   # If token exists => User is already logged-in
                msg = 'User is already login'
                logger.warning(msg=msg)  # log
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail={'message': 'User is already login', 'status_code': status.HTTP_409_CONFLICT}
                )
            
            user = await user_service.get_user_by_email(user_data.email) # Searching for a User in the Database
            if user is None:
                msg = 'User doesnt exist'
                logger.warning(msg=msg)
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail={'message': 'Incorrect email or password', 'status_code': status.HTTP_401_UNAUTHORIZED}
                )
                
            user_model_check = UserAuth.model_validate(user) # Converting SQLAlchemy model to Pydantic model (UserAuth)
            if user_data.email != user_model_check.email or (not PasswordManager().verify_password(user_data.password, user_model_check.password)):
                msg = 'Incorrect email or password'
                extra = {'email': user_data.email, 'password': user_data.password}
                logger.warning(msg=msg, extra=extra)  # log
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail={'message': 'Incorrect email or password', 'status_code': status.HTTP_401_UNAUTHORIZED}
                )
                
            user_model_update = UserUpdate.model_validate(user) # Converting SQLAlchemy model to Pydantic model (UserUpdate)
            if not user_model_update.is_active: # If User account isn't active, change field 'is_active'
                user_model_update.is_active = True
                await user_service.update_user(user_model_update, user_model_update.email)
            
            access_token = TokenManager.create_access_token({'sub': str(user_data.email)}) # Creating access token with User email
            response.set_cookie(key='user_access_token', value=access_token, httponly=True, samesite='none') # Creating cookie for User
            return Token(access_token=access_token, token_type='cookie')
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={'message': 'Server Error', 'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR}
            )

    @staticmethod
    async def update_current_user(response: Response, user_data: User, user_data_update: UserUpdate, user_service: UserService) -> UserRead:
        """
        Update User Account

        Args:
            response (Response): Response to User
            user_data (User): User data (SQLAlchemy Model)
            user_data_update (UserUpdate): User update data Validation
            user_service (UserService): User DAO service

        Raises:
            HTTPException: status - 400, User input symbols are incorrect
            HTTPException: status - 500, SERVER ERROR

        Returns:
            UserRead: Updated User data
        """        
        try:
            new_user_dict = user_data_update.model_dump() # Converting Pydantic model (UserUpdate) to dict
            
            if await Security.validate_schemas_data_user(new_user_dict): # Check User symbols
                new_user_dict['password'] = PasswordManager().get_password_hash(user_data_update.password) # Hashing password
                
                new_user_data: User = await user_service.update_user(UserUpdate(**new_user_dict), user_data.email) # Updating User
                
                #TODO May be create refresh_token?....
                response.delete_cookie(key='user_access_token') # Updating cookie
                access_token = TokenManager.create_access_token({'sub': str(user_data_update.email)}) # Updating cookie
                response.set_cookie(key='user_access_token', value=access_token, httponly=True, samesite='none') # Updating cookie
                
                new_user_model = UserRead.model_validate(new_user_data) # Converting SQLAlchemy model to Pydantic model (UserRead)
                date = re.search(r'\d{4}-\d{2}-\d{2}', f'{new_user_model.registred_at}') # Date type YYYY-MM-DD
                new_user_model.registred_at = date[0]
                return new_user_model
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={'message': 'Use only alphabet letters and numbers', 'status_code': status.HTTP_400_BAD_REQUEST}
                )
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={'message': 'Server Error', 'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR}
            )
    
    @staticmethod
    async def get_user_me(user_data: User) -> UserRead:
        """
        Show current User profile

        Args:
            user_data (User): User data (SQLAlchemy Model)

        Raises:
            HTTPException: status - 500, SERVER ERROR

        Returns:
            UserRead: User data
        """        
        try:
            user_model = UserRead.model_validate(user_data) # Converting SQLAlchemy model to Pydantic model (UserRead)
            date = re.search(r'\d{4}-\d{2}-\d{2}', f'{user_model.registred_at}') # Date type YYYY-MM-DD
            user_model.registred_at = date[0]
            return user_model
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={'message': 'Server Error', 'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR}
            )
    
    @staticmethod
    async def get_another_user(username: str, user_service: UserService) -> UserRead:
        """
        Show another User profile

        Args:
            username (str): Another User username
            user_service (UserService): User DAO service

        Raises:
            HTTPException: status - 404, User doesn't exist
            HTTPException: status - 400, User input symbols are incorrect
            HTTPException: status - 500, SERVER ERROR

        Returns:
            UserRead: User data
        """        
        try:
            if await Security.validate_path_data(username): # Check User symbols
                another_user = await user_service.get_user_by_name(username) # Searching for a User in the Database 
                if another_user is None:
                    msg = "User doesn't exist"
                    logger.warning(msg=msg)  # log
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail={'message': "User doesn't exist :(", 'status_code': status.HTTP_404_NOT_FOUND}
                    )
                    
                another_user_model = UserRead.model_validate(another_user) # Converting SQLAlchemy model to Pydantic model (UserRead)
                date = re.search(r'\d{4}-\d{2}-\d{2}', f'{another_user.registred_at}') # Date type YYYY-MM-DD
                another_user_model.registred_at = date[0]
                return another_user_model
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={'message': 'Use only alphabet letters and numbers', 'status_code': status.HTTP_400_BAD_REQUEST}
                )
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={'message': 'Server Error', 'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR}
            )

    @staticmethod
    async def logout_current_user(response: Response, user_data: User, user_service: UserService) -> dict:
        """
        Current User Logout

        Args:
            response (Response): Response to User
            user_data (User): User data (SQLAlchemy model)
            user_service (UserService): User DAO service

        Raises:
            HTTPException: status - 500, SERVER ERROR

        Returns:
            dict[str, str]: User successfull logout 
        """        
        try:
            response.delete_cookie(key='user_access_token')
            user_model_update = UserUpdate.model_validate(user_data) # Converting SQLAlchemy model to Pydantic model (UserUpdate)
            user_model_update.is_active = False # Change model field to FALSE
            await user_service.update_user(user_model_update, user_model_update.email) # Update User data
            return {'message': 'User successfully logged out'}
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={'message': 'Server Error', 'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR}
            )

    @staticmethod
    async def delete_current_user(response: Response, user_data: User, user_service: UserService) -> dict:
        """
        Delete User account

        Args:
            response (Response): Response to User
            user_data (User): User data (SQLAlchemy model)
            user_service (UserService): User DAO service

        Raises:
            HTTPException: status - 500, SERVER ERROR

        Returns:
            dict[str, str]: User account has been deleted
        """        
        try:
            response.delete_cookie(key='user_access_token')
            user_model_data = UserDelete.model_validate(user_data) # Converting SQLAlchemy model to Pydantic model (UserDelete)
            await user_service.delete_one_user(user_model_data.email) # Delete User from Database
            return {'message': 'User account has been deleted'}
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={'message': 'Server Error', 'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR}
            )
