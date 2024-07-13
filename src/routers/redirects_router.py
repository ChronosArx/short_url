from fastapi import APIRouter, Depends
from typing import Annotated
from ..dependencies import get_db
from ..controllers import redirects_controller as services

router = APIRouter(tags=["Redirects"])


@router.get("/{code}")
async def redirect_free(code: str, db: Annotated[any, Depends(get_db)]):
    return services.redirect_url_free(code=code, db=db)
