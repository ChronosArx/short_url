from starlette.responses import RedirectResponse
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..database import models


def redirect_url(code: str, db: Session):
    code_db = db.query(models.Code).filter(models.Code.code == code).first()
    if not code_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return RedirectResponse(url=code_db.original_url)