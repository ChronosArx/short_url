from pydantic import BaseModel, EmailStr, Field


class UserSignUpSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogInSchema(BaseModel):
    user_name: str = Field(..., alias="username")
    password: str


class AccessToken(BaseModel):
    access_token: str
    token_type: str


class Tokens(BaseModel):
    access_token: str
    refresh_token: str | None = None
