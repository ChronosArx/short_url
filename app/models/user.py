from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    username: str = Field(max_length=200)
    email: EmailStr = Field(unique=True)
    password: str = Field(min_length=8)
    codes: list["codes"] = Relationship(back_populates="user")


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


"""
class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_name: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]
    password: Mapped[str]
    codes = relationship("Code", back_populates="user")

"""
