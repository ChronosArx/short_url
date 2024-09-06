from pydantic import BaseModel, HttpUrl, Field, AnyHttpUrl


class ShortUrlCreateSchema(BaseModel):
    title: str | None = Field(default=None, description="Only for registered users.")
    original_url: AnyHttpUrl


class ShortUrlSResponseSchema(BaseModel):
    id: int
    title: str | None = Field(
        default=None, description="Only urls created by registered users have title."
    )
    original_url: AnyHttpUrl
    shorten_url: AnyHttpUrl
