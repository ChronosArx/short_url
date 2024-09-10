from fastapi import APIRouter
from ..dependencies import SessionDep
from ..controllers import redirects_controller as services

router = APIRouter(tags=["Redirects"])


@router.get("/{code}")
async def redirect_free(code: str, session: SessionDep):
    """
    Este endpoint recive el codigo generado como identificador unico del url acortado, el url acortado ya se revice con el codigo
    por ende al colocarlo en el navegador este endpoint es usado automaticamente.
    """
    return services.redirect_url(code=code, session=session)
