from sqlalchemy import String, Integer, TIMESTAMP, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime

from src.database import Base
    
    
class User(Base):
    __tablename__ = 'user'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    registred_at: Mapped[str] = mapped_column(TIMESTAMP, default=datetime.datetime.utcnow, nullable=False)
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey('role.id'), default=1)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    projects: Mapped[list['Project']] = relationship(lazy='subquery')
    
    repr_cols_num = 4
    repr_cols = ('role_id', 'is_active')
