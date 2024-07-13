from fastapi import APIRouter, Depends, status
from ..dependencies import get_db
from ..middlewares.auth_middlewares import get_current_user, verify_token
from typing import Annotated
from ..controllers import user_controller as services

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/codes")
async def get_all_codes(
    user: Annotated[str, Depends(get_current_user)], db: Annotated[any, Depends(get_db)]
):
    """
    Retorna todos los urls acortados del usuario require token de autentificación
    """
    return await services.get_all_codes(user=user, db=db)


@router.delete(
    "/code/{code_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(verify_token)],
)
async def delate_code(id: int, db: Annotated[any, Depends(get_db)]):
    """
    Elimina uno de los urls acortdos mediante su id
    """
    return services.delate_code(id=id, db=db)
