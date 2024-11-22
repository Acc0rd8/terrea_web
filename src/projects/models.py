from sqlalchemy import ForeignKey, text, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone

from src.database import Base


class Project(Base):
    __tablename__ = 'project'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=text("timezone('utc', now())"))
    
    tasks: Mapped[list['Task']] = relationship()
    

class Task(Base):
    __tablename__ = 'task'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    project_id: Mapped[int] = mapped_column(ForeignKey('project.id', ondelete='CASCADE'))
    created_at: Mapped[datetime] = mapped_column(server_default=text("timezone('utc', now())"))
    updated_at: Mapped[datetime] = mapped_column(server_default=text("timezone('utc', now())"), onupdate=datetime.now(timezone.utc))
    deadline: Mapped[datetime] = mapped_column(nullable=True)
    
    project: Mapped['Project'] = relationship()