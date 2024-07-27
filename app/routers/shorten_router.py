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
    Para acortar el url porfavor ingrese el url mediante el body
    en un campo el cual se llama original_url.
    """
    return controller.create_short_url(original_url=url.original_url, db=db)


@router.post("/shorten_url_by_user")
async def shorten_url_by_user(
    url_data: ShortUrlCreateSchema,
    user: Annotated[str, Depends(get_current_user_middleware)],
    db: Annotated[any, Depends(get_db)],
) -> ShortUrlSResponseSchema:
    """
    Esta funcion es para crear un link acortado pero con la opción de agregar un titulo al link
    esto es para diferencias todos los links que puede tener un usuario registrado y que pueda
    compartir en su debido momento otros links que haya creado
    """
    return controller.create_short_url_by_user(data=url_data, user=user, db=db)
