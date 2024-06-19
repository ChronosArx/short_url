from fastapi import APIRouter, Depends
from ..database.database_dependency import get_db
from typing import Annotated
from . import free_services as services

router = APIRouter(prefix="/free", tags=["Free"])


@router.get("/create_short_url_free")
async def create_free_short_url(original_url: str, db: Annotated[any, Depends(get_db)]):
    return services.create_short_url(original_url=original_url, db=db)
