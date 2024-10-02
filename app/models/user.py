from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr


class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    username: str = Field(max_length=200)
    email: str
    password: str
    codes: list["Code"] = Relationship(back_populates="codes")


class UserSignUp(SQLModel):
    username: str = Field(min_length=4)
    email: EmailStr
    password: str = Field(min_length=8)


class UserLogIn(SQLModel):
    username: str
    password: str


class AccessToken(SQLModel):
    access_token: str
    token_type: str
