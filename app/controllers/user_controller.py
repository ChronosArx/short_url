from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session
from ..models.user import User
from ..models.code import Code


# Funcion de retorno para url acortadas por paginación
async def get_all_codes(user: dict, db: Session, page: int, limit: int) -> list[Code]:
    query = db.query(Code).filter(Code.user_id == user["user_id"])
    if page is not None and limit is not None:
        ofset = (page - 1) * 10
        query = query.limit(limit).offset(ofset)
    codes = query.all()
    return codes


async def delate_code(id: int, db: Session):
    code = db.query(Code).filter(Code.id == id).first()
    if not code:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Short url don't exist"
        )
    db.delete(code)
    db.commit()
    return
