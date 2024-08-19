from pydantic import BaseModel, HttpUrl, Field


class ShortUrlCreateSchema(BaseModel):
    title: str | None = Field(default=None, description="Only for registered users.")
    original_url: HttpUrl


class ShortUrlSResponseSchema(BaseModel):
    id: int
    title: str | None = Field(
        default=None, description="Only urls created by registered users have title."
    )
    original_url: HttpUrl
    shorten_url: HttpUrl
