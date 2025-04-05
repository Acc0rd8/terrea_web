from datetime import datetime

from sqlalchemy import TIMESTAMP, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class User(Base):
    """
    Table 'user'
    """
    
    __tablename__ = 'user'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    registred_at: Mapped[str] = mapped_column(TIMESTAMP, default=datetime.utcnow) # Time when User was registred
    role_id: Mapped[int] = mapped_column(ForeignKey('role.id'), default=1) # By default User has Role 'user'
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False) # If user is active at the site => is_active = True, else is_active = False
    
    projects: Mapped[list['Project']] = relationship(back_populates='owner', order_by='asc(Project.name)', lazy='selectin') # One2Many
    assigned_user_tasks: Mapped[list['Task']] = relationship(back_populates='customer', order_by='asc(Task.name)', lazy='selectin', primaryjoin='User.username == Task.customer_name') # One2Many
    user_tasks: Mapped[list['Task']] = relationship(back_populates='performer', order_by='asc(Task.name)', lazy='selectin', primaryjoin='User.username == Task.performer_name') # One2Many
    
    repr_cols_num = 4
    repr_cols = ('role_id', 'is_active', 'projects')
