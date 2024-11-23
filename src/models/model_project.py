from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import text

from src.database import Base


class Project(Base):
    __tablename__ = 'project'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=text("timezone('utc', now())"))
    
    tasks: Mapped[list['Task']] = relationship(lazy='subquery')