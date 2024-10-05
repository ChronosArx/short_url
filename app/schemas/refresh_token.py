from sqlmodel import SQLModel, Field
from datetime import datetime


class Tokens(SQLModel):
    access_token: str
    refresh_token: str | None = None


class AccessToken(SQLModel):
    access_token: str
    token_type: str
