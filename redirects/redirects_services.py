from starlette.responses import RedirectResponse
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..database import models


def redirect_url_free(code: str, db: Session):
    free_url = db.query(models.FreeUrl).filter(models.FreeUrl.code == code).first()
    if not free_url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return RedirectResponse(url=free_url.original_url)
