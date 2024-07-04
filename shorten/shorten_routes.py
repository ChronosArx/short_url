from fastapi import APIRouter, Depends
from ..database.database_dependency import get_db
from typing import Annotated
from . import shorten_services as services
from .shorten_schemas import CreateShortenUrlSchema

router = APIRouter(prefix="/shorten", tags=["Free"])


@router.post("/shorten_url")
async def shorten_url(
    original_url: CreateShortenUrlSchema, db: Annotated[any, Depends(get_db)]
):
    return services.create_short_url(original_url=original_url, db=db)
