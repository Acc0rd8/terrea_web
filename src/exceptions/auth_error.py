from fastapi import status

from src.exceptions.custom_error import CustomError


class AuthError(CustomError):
    '''
    Authentication Error
    '''
    
    def __init__(self, msg: str):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, message=msg)