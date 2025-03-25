from fastapi import status

from src.exceptions.custom_error import CustomError


class ValidationError(CustomError):
    """
    Data validation Error
    """
    
    def __init__(self, msg: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, message=msg)
