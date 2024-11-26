from sqlalchemy import ForeignKey, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from src.database import Base
    
    
class User(Base):
    __tablename__ = 'user'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    registred_at: Mapped[str] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    role_id: Mapped[int] = mapped_column(ForeignKey('role.id'), default=1)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    
    projects: Mapped[list['Project']] = relationship(back_populates='owner', order_by='asc(Project.name)', lazy='selectin')
    user_tasks: Mapped[list['Task']] = relationship(back_populates='performer', order_by='asc(Task.name)', lazy='selectin')
    
    repr_cols_num = 4
    repr_cols = ('role_id', 'is_active', 'projects')