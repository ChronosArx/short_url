from pydantic import BaseModel, EmailStr, Field


class UserSignUpSchema(BaseModel):
    username: str = Field(min_length=4)
    email: EmailStr
    password: str = Field(min_length=8)


class UserLogInSchema(BaseModel):
    username: str
    password: str


class AccessToken(BaseModel):
    access_token: str
    token_type: str


class Tokens(BaseModel):
    access_token: str
    refresh_token: str | None = None
