from pydantic import BaseModel, Field, EmailStr


class UserSignUp(BaseModel):
    username: str = Field(min_length=4)
    email: EmailStr
    password: str = Field(min_length=8)


class UserLogIn(BaseModel):
    username: str
    password: str


class AccessToken(BaseModel):
    access_token: str
    token_type: str

class Tokens(BaseModel):
    access_token: str
    refresh_token: str | None = None


class AccessToken(BaseModel):
    access_token: str
    token_type: str
