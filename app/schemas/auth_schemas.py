from pydantic import BaseModel, EmailStr


class UserSignUpSchema(BaseModel):
    user_name: str
    email: EmailStr
    password: str


class UserLogInSchema(BaseModel):
    user_name: str
    password: str


class Tokens(BaseModel):
    access_token: str
    refresh_token: str
