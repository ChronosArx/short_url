from ..core.config_data_base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from pydantic import AnyHttpUrl
from .user import User


class Code(SQLModel, table=True):
    id: int = Field(primary_key=True)
    original_url: str
    title: str = Field(max_length=200)
    code: str = Field(max_length=6)
    user_id: int | None = Field(foreign_key="user.id")
    user: User | None = Relationship(back_populates="codes")


class ShortUrlCreate(SQLModel):
    title: str | None = Field(default=None, description="Only for registered users.")
    original_url: AnyHttpUrl


class ShortUrlSResponse(SQLModel):
    id: int
    title: str | None = Field(
        default=None, description="Only urls created by registered users have title."
    )
    original_url: AnyHttpUrl
    shorten_url: AnyHttpUrl


"""
class Code(Base):
    __tablename__ = "code"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    original_url: Mapped[str]
    title: Mapped[Optional[str]]
    code: Mapped[str]
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"))
    user = relationship("User", back_populates="codes")
"""
