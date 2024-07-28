from fastapi import APIRouter, Depends
from typing import Annotated
from ..dependencies import get_db
from ..controllers import redirects_controller as services

router = APIRouter(tags=["Redirects"])


@router.get("/{code}")
async def redirect_free(code: str, db: Annotated[any, Depends(get_db)]):
    """
    Este endpoint recive el codigo generado como identificador unico del url acortado, el url acortado ya se revice con el codigo
    por ende al colocarlo en el navegador este endpoint es usado automaticamente.
    """
    return services.redirect_url(code=code, db=db)
