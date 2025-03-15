from fastapi import status

from src.exceptions.custom_error import CustomError


class ServerError(CustomError):
    '''
    Critical Server Error
    '''
    
    def __init__(self, msg: str):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Server Error')