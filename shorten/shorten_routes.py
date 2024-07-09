from fastapi import APIRouter, Depends
from ..database.database_dependency import get_db
from typing import Annotated
from . import shorten_services as services
from .shorten_schemas import (
    CreateShortenUrlSchema,
    UrlShortenSchema,
    CreateShortenUrlUserSchema,
)
from ..utils.jwt_encoders import verify_token, get_current_user

router = APIRouter(prefix="/shorten", tags=["Free"])


@router.post("/shorten_url", response_model=UrlShortenSchema)
async def shorten_url(
    url: CreateShortenUrlSchema, db: Annotated[any, Depends(get_db)]
) -> UrlShortenSchema:
    """
    Para acortar el url porfavor ingrese el url mediante el body
    en un campo el cual se llama original_url.
    """
    return services.create_short_url(original_url=url.original_url, db=db)


@router.post("/shorten_url_by_user", dependencies=[Depends(verify_token)])
async def shorten_url_by_user(
    url_data: CreateShortenUrlUserSchema,
    user: Annotated[str, Depends(get_current_user)],
    db: Annotated[any, Depends(get_db)],
):
    return services.create_short_url_by_user(data=url_data, user=user, db=db)
