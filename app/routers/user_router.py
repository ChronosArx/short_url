from fastapi import APIRouter, Depends, status
from ..dependencies import SessionDep
from ..middlewares.auth_middlewares import (
    get_current_user_middleware,
    verify_token_middleware,
)
from typing import Annotated
from ..controllers import user_controller as services

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/codes")
async def get_all_codes(
    user: Annotated[str, Depends(get_current_user_middleware)],
    session: SessionDep,
    page: int = None,
    limit: int = None,
):
    """
    EndPoint que retorna todos los urls acorados que hay asociados al usuario logeado
    """
    return await services.get_all_codes(
        user=user, session=session, page=page, limit=limit
    )


@router.delete(
    "/code/{code_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(verify_token_middleware)],
)
async def delate_code(code_id: int, session: SessionDep):
    """
    Endpoint que elimina un url acortado por medio de su id.
    """
    return await services.delate_code(id=code_id, session=session)
