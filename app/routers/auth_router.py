from fastapi import APIRouter, Depends, status, Response
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from ..controllers import auth_controller as services
from ..schemas import auth_schemas as schema
from ..dependencies import get_db
from sqlalchemy.orm import Session
from ..middlewares.auth_middlewares import verify_refresh_token_middleware

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/signup",
    response_model=schema.Tokens,
    status_code=status.HTTP_201_CREATED,
)
async def signup(
    response: Response,
    user: schema.UserSignUpSchema,
    db: Annotated[any, Depends(get_db)],
):
    """
    EndPoint que recive nombre de usuario, email, y password, crea un nuevo usuario y retorna por medio del body
    un access token y un refresh token el cual se envia por medio de las cookies.
    """
    tokens = services.signup(user=user, db=db)
    response.set_cookie(
        key="refresh_token", value=tokens.refresh_token, httponly=True, secure=True
    )
    return tokens


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    user_data: Annotated[schema.UserLogInSchema, Depends(OAuth2PasswordRequestForm)],
    db: Annotated[any, Depends(get_db)],
    response: Response,
):
    """
    EndPoint que recive tanto nombre de usuario como contraseña para hacer login recive un access token por medio
    del body en la respuesta y un refresh token por medio de las cookies.
    """
    tokens = services.login(user=user_data, db=db)
    response.set_cookie(
        key="refresh_token", value=tokens.refresh_token, httponly=True, secure=True
    )
    return tokens


@router.get("/token")
async def get_token(
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(verify_refresh_token_middleware)],
) -> schema.AccessToken:
    """
    Este endpoint recive el refresh token atravez de cookies, para poder optener un nuevo access token
    """
    return services.new_token(token=token, db=db)
