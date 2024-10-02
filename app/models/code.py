from sqlmodel import SQLModel, Field, Relationship
from pydantic import AnyHttpUrl
from typing import Optional
from .user import User


class Code(SQLModel, table=True):
    id: int = Field(primary_key=True)
    original_url: str
    title: str | None = Field(max_length=200, nullable=True)
    code: str = Field(max_length=6)
    user_id: int | None = Field(foreign_key="code.id", nullable=True)
    user: User | None = Relationship(back_populates="codes")


class ShortUrlCreate(SQLModel):
    original_url: AnyHttpUrl


class ShortUrlCreateByUser(ShortUrlCreate):
    title: str | None = Field(default=None, description="Only for registered users.")


class ShortUrlSResponse(SQLModel):
    id: int | None
    title: str | None = Field(
        default=None, description="Only urls created by registered users have title."
    )
    original_url: AnyHttpUrl | None
    shorten_url: AnyHttpUrl | None
