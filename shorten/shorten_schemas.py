from pydantic import BaseModel


class CreateShortenUrlSchema(BaseModel):
    original_url: str


class UrlShortenSchema(BaseModel):
    shorten_url: str
