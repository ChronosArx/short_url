from fastapi import APIRouter, Depends, status
from ..database.database_dependency import get_db
from ..utils.jwt_encoders import get_current_user, verify_token
from typing import Annotated
from . import user_services as services

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/codes")
async def get_all_codes(
    user: Annotated[str, Depends(get_current_user)], db: Annotated[any, Depends(get_db)]
):
    return await services.get_all_codes(user, db=db)


@router.delete(
    "/code/{code_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(verify_token)],
)
async def delate_code(id: int, db: Annotated[any, Depends(get_db)]):
    return services.delate_code(id=id, db=db)
