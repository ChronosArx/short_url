from pydantic import BaseModel
from datetime import datetime


class Tokens(BaseModel):
    access_token: str
    refresh_token: str | None = None


class AccessToken(BaseModel):
    access_token: str
    token_type: str
