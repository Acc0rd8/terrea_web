from celery import Celery

from src.config import settings


app_celery = Celery(
    'tasks', 
    broker=f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}',
    include=['src.tasks.tasks']
)