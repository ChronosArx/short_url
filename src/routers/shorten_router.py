from fastapi import APIRouter, Depends, status
from ..dependencies import get_db
from typing import Annotated
from ..controllers import shorten_controller as controller
from ..schemas.shorten_schemas import (
    CreateShortenUrlSchema,
    UrlShortenSchema,
    CreateShortenUrlUserSchema,
)
from ..middlewares.auth_middlewares import verify_token, get_current_user

router = APIRouter(prefix="/shorten", tags=["Free"])


@router.post(
    "/shorten_url", response_model=UrlShortenSchema, status_code=status.HTTP_201_CREATED
)
async def shorten_url(
    url: CreateShortenUrlSchema, db: Annotated[any, Depends(get_db)]
) -> UrlShortenSchema:
    """
    Para acortar el url porfavor ingrese el url mediante el body
    en un campo el cual se llama original_url.
    """
    return controller.create_short_url(original_url=url.original_url, db=db)


@router.post("/shorten_url_by_user", dependencies=[Depends(verify_token)])
async def shorten_url_by_user(
    url_data: CreateShortenUrlUserSchema,
    user: Annotated[str, Depends(get_current_user)],
    db: Annotated[any, Depends(get_db)],
):
    """
    Esta funcion es para crear un link acortado pero con la opción de agregar un titulo al link
    esto es para diferencias todos los links que puede tener un usuario registrado y que pueda
    compartir en su debido momento otros links que haya creado
    """
    return controller.create_short_url_by_user(data=url_data, user=user, db=db)
