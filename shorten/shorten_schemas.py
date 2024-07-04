from pydantic import BaseModel


class CreateShortenUrlSchema(BaseModel):
    original_url: str
