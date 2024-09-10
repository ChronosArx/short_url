from ..core.config_data_base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from datetime import datetime
from sqlmodel import SQLModel, Field


class RefreshToken(SQLModel, table=True):
    id: int = Field(primary_key=True)
    refresh_token: str
    user_id: int = Field(foreign_key="user.id")
    expire_date: datetime


class Tokens(SQLModel):
    access_token: str
    refresh_token: str | None = None


class AccessToken(SQLModel):
    access_token: str
    token_type: str


"""
class RefreshToken(Base):
    __tablename__ = "refresh_token"
    id: Mapped[int] = mapped_column(primary_key=True)
    refresh_token: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    expire_date: Mapped[datetime]
"""
