from fastapi import APIRouter, Depends, status
from ..dependencies import get_db
from typing import Annotated
from ..controllers import shorten_controller as controller
from ..schemas.shorten_schemas import ShortUrlCreateSchema, ShortUrlSResponseSchema
from ..middlewares.auth_middlewares import get_current_user_middleware


router = APIRouter(prefix="/shorten", tags=["Shorten Urls"])


@router.post(
    "/shorten_url",
    response_model=ShortUrlSResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def shorten_url(
    url: ShortUrlCreateSchema, db: Annotated[any, Depends(get_db)]
) -> ShortUrlSResponseSchema:
    """
    EndPoint para acortar el url, ingrese el url mediante el body
    en un campo el cual se llama original_url.
    """
    return controller.create_short_url(original_url=str(url.original_url), db=db)


@router.post("/shorten_url_by_user", status_code=status.HTTP_201_CREATED)
async def shorten_url_by_user(
    url_data: ShortUrlCreateSchema,
    user: Annotated[str, Depends(get_current_user_middleware)],
    db: Annotated[any, Depends(get_db)],
) -> ShortUrlSResponseSchema:
    """
    Endpoint para crear un url acortado con titulo, solo los usuarios logeados pueden colocar un titulo para el url acortado
    """
    return controller.create_short_url_by_user(data=url_data, user=user, db=db)
