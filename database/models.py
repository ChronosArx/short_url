from .data_base_conf import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import List, Optional


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_name: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]
    password: Mapped[str]
    id_premium_link: Mapped[Optional[int]] = mapped_column(
        ForeignKey("premium_links.id")
    )
    premium_link: Mapped["PremiumLink"] = relationship(back_populates="user")


class FreeUrl(Base):
    __tablename__ = "free_urls"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    original_url: Mapped[str]
    code: Mapped[str]


class PremiumLink(Base):
    __tablename__ = "premium_links"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    custom_link: Mapped[str] = mapped_column(unique=True)
    user: Mapped["User"] = relationship(back_populates="premium_link")
    codes: Mapped[List["CustomCode"]] = relationship()


class CustomCode(Base):
    __tablename__ = "custom_codes"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(unique=True)
    id_premium_link: Mapped[int] = mapped_column(ForeignKey("premium_links.id"))
