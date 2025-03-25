from fastapi import status

from src.exceptions.custom_error import CustomError


class ConflictError(CustomError):
    """
    Server conflict Error
    """
    
    def __init__(self, msg: str):
        super().__init__(status_code=status.HTTP_409_CONFLICT, message=msg)
