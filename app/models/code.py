from config.data_base_config import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional


class Code(Base):
    __tablename__ = "code"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    original_url: Mapped[str]
    title: Mapped[Optional[str]]
    code: Mapped[str]
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"))
    user = relationship("User", back_populates="codes")
