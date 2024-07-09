from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session
from ..database import models


async def get_all_codes(user: str, db: Session) -> list[models.Code]:
    user = db.query(models.User).filter(models.User.user_name == user).first()
    return user.codes


async def delate_code(id: int, db: Session):
    code = db.query(models.Code).filter(models.Code.id == id).first()
    if not code:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Short url don't exist"
        )
    db.delete(code)
    db.commit()
    return
