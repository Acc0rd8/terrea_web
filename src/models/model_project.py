from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import text

from src.database import Base


class Project(Base):
    __tablename__ = 'project'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=text("timezone('utc', now())"))
    owner_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))
    
    owner: Mapped['User'] = relationship(back_populates='projects', lazy='selectin')
    project_tasks: Mapped[list['Task']] = relationship(back_populates='project', lazy='selectin')