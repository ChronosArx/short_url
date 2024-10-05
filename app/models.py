from sqlalchemy.orm import (
    mapped_column,
    Mapped,
    relationship,
    DeclarativeBase,
)
from sqlalchemy import String, ForeignKey
from typing import Optional
from datetime import datetime


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(length=200))
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    codes: Mapped[list["Code"]] = relationship(back_populates="user")


class Code(Base):
    __tablename__ = "codes"
    id: Mapped[int] = mapped_column(primary_key=True)
    original_url: Mapped[str]
    title: Mapped[str] = mapped_column(String(length=200), nullable=True)
    code: Mapped[str] = mapped_column(String(length=6))
    user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )
    user: Mapped[Optional["User"]] = relationship(back_populates="codes")


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id: Mapped[int] = mapped_column(primary_key=True)
    refresh_token: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    expire_date: Mapped[datetime]
