from fastapi import APIRouter, Depends
from typing import Annotated
from ..database.database_dependency import get_db
from . import redirects_services as services

router = APIRouter(tags=["Redirects"])


@router.get("/{code}")
async def redirect_free(code: str, db: Annotated[any, Depends(get_db)]):
    return services.redirect_url_free(code=code, db=db)
