from src.logger import logger


class Security:
    @staticmethod
    async def validate_schemas_data_user(data_dict: dict[str, str]) -> bool:
        temp = {key: value for key, value in data_dict.items() if key != 'email'}
        for value in temp.values():
            for let in value:
                if not (let.isalnum()):
                    logger.debug(msg='Validation Error', extra={'dict_info': temp}, exc_info=False)
                    return False
        return True
    
    @staticmethod
    async def validate_shemas_data_project(data_dict: dict[str, str]) -> bool:
        temp = {key: value for key, value in data_dict.items()}
        for value in temp.values():
            for let in value:
                if not (let.isalnum()):
                    logger.debug(msg='Validation Error', extra={'dict_info': temp}, exc_info=False)
                    return False
        return True
    
    @staticmethod
    async def validate_schemas_data_task(data_dict: dict[str, str]) -> bool:
        temp = {key: value for key, value in data_dict.items() if key != 'deadline' and key != 'customer_id' and key != 'performer_id'}
        for value in temp.values():
            for let in value:
                if not (let.isalnum()):
                    logger.debug(msg='Validation Error', extra={'dict_info': temp}, exc_info=False)
                    return False
        return True
    
    @staticmethod
    async def validate_path_data(path_data: str) -> bool:
        for let in path_data:
            if not (let.isalnum()):
                logger.debug(msg='Validation Error', extra={'path_data': path_data}, exc_info=False)
                return False
        return True