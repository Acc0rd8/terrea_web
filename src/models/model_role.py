from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, ARRAY

from src.database import Base


class Role(Base):
    __tablename__= 'role'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    permicions: Mapped[list[str]] = mapped_column(ARRAY(item_type=String), nullable=False)

