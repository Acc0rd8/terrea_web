from datetime import datetime, timezone

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Task(Base):
    """
    Table 'task'
    """
    
    __tablename__ = 'task'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    project_id: Mapped[int] = mapped_column(ForeignKey('project.id', ondelete='CASCADE'))
    customer_name: Mapped[str] = mapped_column(ForeignKey('user.username', ondelete='CASCADE')) # User name, who created the Task
    performer_name: Mapped[str] = mapped_column(ForeignKey('user.username', ondelete='CASCADE')) # User name, who need to solve the Task
    created_at: Mapped[datetime] = mapped_column(server_default=text("timezone('utc', now())")) # Time when the Task was created
    updated_at: Mapped[datetime] = mapped_column(server_default=text("timezone('utc', now())"), onupdate=datetime.utcnow) # Time when the Task was updated
    deadline: Mapped[datetime] = mapped_column(nullable=True) # datetim | None
    
    
    project: Mapped['Project'] = relationship(back_populates='project_tasks', lazy='selectin') # Many2One
    customer: Mapped['User'] = relationship(back_populates='assigned_user_tasks', lazy='selectin', foreign_keys='Task.customer_name') # Many2One
    performer: Mapped['User'] = relationship(back_populates='user_tasks', lazy='selectin', foreign_keys='Task.performer_name') # Many2One
