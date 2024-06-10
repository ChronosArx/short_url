from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from fastapi import HTTPException, status
from database import models
from utils.generate_codes import generate_short_code


def create_short_url(original_url: str, db: Session):
    code = generate_short_code()
    new_short_url = models.FreeUrl(original_url=original_url, code=code)
    db.add(new_short_url)
    db.commit()
    db.refresh(new_short_url)
    return f"http://localhost/{new_short_url.code}"


def redirect_url(code: str, db: Session):
    free_url = db.query(models.FreeUrl).filter(models.FreeUrl.code == code).first()
    if not free_url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return RedirectResponse(url=free_url.original_url)
