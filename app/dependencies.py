from sqlalchemy.orm import Session
from .core.config import settings
from typing import Annotated
from collections.abc import Generator
from fastapi import Depends


def get_db() -> Generator[Session, None, None]:
    with Session(settings.engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
