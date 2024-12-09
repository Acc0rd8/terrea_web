from sqlalchemy import ARRAY, String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class Role(Base):
    __tablename__= 'role'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    permicions: Mapped[list[str]] = mapped_column(ARRAY(item_type=String), nullable=False)

    @staticmethod
    def to_string():
        return 'Role'