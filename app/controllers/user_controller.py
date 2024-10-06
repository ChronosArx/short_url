from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..models import Code


# Funcion de retorno para url acortadas por paginación
async def get_all_codes(
    user: int, session: Session, page: int, limit: int
) -> list[Code]:
    statement = select(Code).filter(Code.user_id == user)
    if page is not None and limit is not None:
        offset = (page - 1) * 10
        statement = statement.limit(limit).offset(offset)
    codes = session.exec(statement).all()
    return codes


async def delate_code(id: int, session: Session):
    statement = select(Code).filter(Code.id == id)
    code = session.exec(statement).first()
    if not code:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Short url don't exist"
        )
    session.delete(code)
    session.commit()
    return
