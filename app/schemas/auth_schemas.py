from pydantic import BaseModel, EmailStr


class UserSignUpSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogInSchema(BaseModel):
    username: str
    password: str


class Tokens(BaseModel):
    access_token: str
    refresh_token: str | None = None
