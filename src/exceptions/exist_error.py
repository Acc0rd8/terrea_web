from fastapi import status

from src.exceptions.custom_error import CustomError


class ExistError(CustomError):
    '''
    Data exist Error
    '''
    
    def __init__(self, msg: str):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, message=msg)