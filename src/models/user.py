from ...config.data_base_config import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from .code import Code


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_name: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]
    password: Mapped[str]
    codes: Mapped[List["Code"]] = relationship(back_populates="user")
