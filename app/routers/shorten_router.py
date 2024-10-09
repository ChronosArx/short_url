from fastapi import APIRouter, Depends, status
from starlette.responses import StreamingResponse
from ..dependencies import SessionDep
from typing import Annotated
from ..controllers import shorten_controller as controller
from ..schemas.code import ShortUrlCreate, ShortUrlSResponse, ShortUrlCreateByUser
from ..middlewares.auth_middlewares import get_current_user_middleware


router = APIRouter(prefix="/shorten", tags=["Shorten Urls"])


@router.post(
    "/shorten_url",
    response_model=ShortUrlSResponse,
    status_code=status.HTTP_201_CREATED,
)
async def shorten_url(url: ShortUrlCreate, session: SessionDep):
    """
    EndPoint para acortar el url, ingrese el url mediante el body
    en un campo el cual se llama original_url.
    """
    return controller.create_short_url(
        original_url=str(url.original_url), session=session
    )


@router.post("/shorten_url_by_user", status_code=status.HTTP_201_CREATED)
async def shorten_url_by_user(
    url_data: ShortUrlCreateByUser,
    user: Annotated[int, Depends(get_current_user_middleware)],
    session: SessionDep,
) -> ShortUrlSResponse:
    """
    Endpoint para crear un url acortado con titulo, solo los usuarios logeados pueden colocar un titulo para el url acortado
    """
    return controller.create_short_url_by_user(
        data=url_data, user=user, session=session
    )


@router.get(
    "/obtain_qr",
    response_class=StreamingResponse,
    responses={
        200: {
            "description": "Retorna un código QR en formato PNG",
        }
    },
)
async def get_qr(url: ShortUrlCreate):
    img_qr = controller.generate_qr(url=url.original_url)
    return StreamingResponse(
        img_qr, media_type="image/png", status_code=status.HTTP_201_CREATED
    )
