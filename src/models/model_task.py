from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, text
from datetime import datetime, timezone

from src.database import Base


class Task(Base):
    __tablename__ = 'task'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    project_id: Mapped[int] = mapped_column(ForeignKey('project.id', ondelete='CASCADE'))
    customer_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))
    performer_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))
    created_at: Mapped[datetime] = mapped_column(server_default=text("timezone('utc', now())"))
    updated_at: Mapped[datetime] = mapped_column(server_default=text("timezone('utc', now())"), onupdate=datetime.now(timezone.utc))
    deadline: Mapped[datetime] = mapped_column(nullable=True)
    
    
    project: Mapped['Project'] = relationship(back_populates='project_tasks', lazy='selectin')
    customer: Mapped['User'] = relationship(back_populates='assigned_user_tasks', lazy='selectin', foreign_keys='Task.customer_id')
    performer: Mapped['User'] = relationship(back_populates='user_tasks', lazy='selectin', foreign_keys='Task.performer_id')