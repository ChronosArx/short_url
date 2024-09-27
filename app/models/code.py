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
