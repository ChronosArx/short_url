from database.data_base_conf import Base
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_name: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]
    password: Mapped[str]


class FreeUrl(Base):
    __tablename__ = "free_urls"
    id: Mapped[str] = mapped_column(primary_key=True, autoincrement=True)
    original_url: Mapped[str]
    code: Mapped[str]
