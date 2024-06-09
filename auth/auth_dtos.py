from pydantic import BaseModel


class UserSignUpDTO(BaseModel):
    user_name: str
    email: str
    password: str


class UserLogInDTO(BaseModel):
    user_name: str
    password: str
