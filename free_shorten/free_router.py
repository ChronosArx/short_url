from fastapi import APIRouter, Depends
from share_dependencies.database_dependency import get_db
from typing import Annotated
import free_shorten.free_services as services

router = APIRouter()


@router.get("/short_url_free")
async def get_free_short_url(original_url: str, db: Annotated[any, Depends(get_db)]):
    return services.create_short_url(original_url=original_url, db=db)


@router.get("/{code}")
async def redirect_original(code: str, db: Annotated[any, Depends(get_db)]):
    return services.redirect_url(code=code, db=db)
