import time

from fastapi import Request

from src.main import app
from src.logger import logger


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    logger.info('Request execution time', extra={
        'process_time': round(process_time, 4)
    })
    return response
