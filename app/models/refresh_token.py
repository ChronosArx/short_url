from datetime import datetime
from sqlmodel import SQLModel, Field


class RefreshToken(SQLModel, table=True):
    id: int = Field(primary_key=True)
    refresh_token: str
    user_id: int = Field(foreign_key="user.id")
    expire_date: datetime


class Tokens(SQLModel):
    access_token: str
    refresh_token: str | None = None


class AccessToken(SQLModel):
    access_token: str
    token_type: str
