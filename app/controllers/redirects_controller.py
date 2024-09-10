from starlette.responses import RedirectResponse
from fastapi import HTTPException, status
from sqlmodel import Session, select
from ..models.code import Code


def redirect_url(code: str, session: Session):
    statement = select(Code).where(Code.code == code)
    code_db = session.exec(statement).first()
    if not code_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return RedirectResponse(url=code_db.original_url)
