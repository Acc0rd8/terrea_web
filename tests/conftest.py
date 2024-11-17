import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from typing import AsyncGenerator

from src.database import get_async_session
from src.config import settings
from src.main import app


engine_test = create_engine(settings.TEST_DATABASE_URL, echo=True)
session_test = sessionmaker(engine_test, expire_on_commit=True)


