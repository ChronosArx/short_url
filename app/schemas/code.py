from pydantic import BaseModel, AnyHttpUrl, Field
from typing import Optional


class ShortUrlCreate(BaseModel):
    original_url: AnyHttpUrl


class ShortUrlCreateByUser(ShortUrlCreate):
    title: str | None = Field(default=None, description="Only for registered users.")


class ShortUrlSResponse(BaseModel):
    id: int | None
    title: str | None = Field(
        default=None, description="Only urls created by registered users have title."
    )
    original_url: AnyHttpUrl | None
    shorten_url: AnyHttpUrl | None
