from pydantic import BaseModel


class UserSignUpSchema(BaseModel):
    user_name: str
    email: str
    password: str


class UserLogInSchema(BaseModel):
    user_name: str
    password: str
