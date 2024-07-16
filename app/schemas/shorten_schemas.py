from pydantic import BaseModel, AnyUrl, Field


class ShortUrlCreateSchema(BaseModel):
    title: str | None = Field(default=None, description="Only for registered users.")
    original_url: str


class ShortUrlSResponseSchema(BaseModel):
    id: int
    title: str | None = Field(
        default=None, description="Only urls created by registered users have title."
    )
    original_url: AnyUrl
    shorten_url: AnyUrl
