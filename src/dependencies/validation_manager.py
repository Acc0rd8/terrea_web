from src.logger import logger


class ValidationManager:
    @staticmethod
    async def validate_schemas_data_user(data_dict: dict[str, str]) -> bool:
        temp = {key: value for key, value in data_dict.items() if key != 'email' and key != 'is_active'} # Create dict with user_data fields, excpet 'email' field
        for value in temp.values():
            for let in value:
                if not (let.isalnum() or let == '_'):
                    logger.debug(msg='Validation Error', extra={'dict_info': temp}, exc_info=False) # log
                    return False
        return True
    
    @staticmethod
    async def validate_shemas_data_project(data_dict: dict[str, str]) -> bool:
        temp = {key: value for key, value in data_dict.items()} # Create dict with project_data fields
        for value in temp.values():
            for let in value:
                if not (let.isalnum() or let == '_' or let == ' '):
                    logger.debug(msg='Validation Error', extra={'dict_info': temp}, exc_info=False) # log
                    return False
        return True
    
    @staticmethod
    async def validate_schemas_data_task(data_dict: dict[str, str]) -> bool:
        temp = {key: value for key, value in data_dict.items() if key != 'deadline' and key != 'customer_id' and key != 'performer_id'} # Create dict with task_data fields, except 'deadline', 'customer_id' and 'performer_id' fields
        for value in temp.values():
            for let in value:
                if not (let.isalnum() or let == '_' or let == ' '):
                    logger.debug(msg='Validation Error', extra={'dict_info': temp}, exc_info=False) # log
                    return False
        return True
    
    @staticmethod
    async def validate_path_data(path_data: str) -> bool: # Validate form data
        for let in path_data:
            if not (let.isalnum() or let == '_'):
                logger.debug(msg='Validation Error', extra={'path_data': path_data}, exc_info=False) # log
                return False
        return True