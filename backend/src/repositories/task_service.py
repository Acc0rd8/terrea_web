from src.models.model_task import Task
from src.schemas.task_schemas import TaskCreate, TaskUpdate
from src.utils.repository import SQLAlchemyRepository


class TaskService:
    """
    Task DAO service
    
    Fields:
        <self> task_repo (SQLAlchemyRepository): Task repository
    """
    
    def __init__(self, task_repo: SQLAlchemyRepository):
        self.task_repo: SQLAlchemyRepository = task_repo
        
    async def create_task(self, task: TaskCreate, project_id: int, customer_id: int) -> dict:
        task_dict = task.model_dump() # Converting Pydantic model (TaskCreate) to dict
        task_dict.update({'project_id': project_id})
        task_dict.update({'customer_id': customer_id})
        result = await self.task_repo.create_one(task_dict)
        return result
    
    async def get_task(self, task_id: int) -> Task:
        result = await self.task_repo.get_one(id=task_id)
        return result
    
    async def update_task(self, new_task: TaskUpdate, task_id: int) -> Task:
        result = await self.task_repo.update_one(new_data=new_task, id=task_id)
        return result
    
    async def delete_one_task(self, task_id: int) -> dict:
        result = await self.task_repo.delete_one(id=task_id)
        return result
    
    async def delete_all_tasks(self) -> dict:
        result = await self.task_repo.delete_all()
        return result
