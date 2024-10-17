from fastapi import APIRouter, Depends, status, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from ..controllers import auth_controller as services
from ..schemas.user import UserLogIn, UserSignUp, Tokens, AccessToken
from ..dependencies import SessionDep
from ..middlewares.auth_middlewares import get_current_user_middleware

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/signup",
    response_model=Tokens,
    status_code=status.HTTP_201_CREATED,
)
async def signup(
    response: Response,
    user: UserSignUp,
    session: SessionDep,
):
    """
    EndPoint que recive nombre de usuario, email, y password, el nombre de usuario debe tener minimo 4 caractener y la contraseña 8, crea un nuevo usuario y retorna por medio del body
    un access token y un refresh token el cual se envia por medio de las cookies.
    """
    tokens = services.signup(user=user, session=session)
    response.set_cookie(
        key="refresh_token", value=tokens.refresh_token, httponly=True, secure=True
    )
    return tokens


@router.post("/login", status_code=status.HTTP_200_OK, response_model=Tokens)
async def login(
    user_data: Annotated[UserLogIn, Depends(OAuth2PasswordRequestForm)],
    session: SessionDep,
    response: Response,
):
    """
    EndPoint que recive tanto nombre de usuario como contraseña para hacer login recive un access token por medio
    del body en la respuesta y un refresh token por medio de las cookies.
    """
    tokens = services.login(user=user_data, session=session)
    response.set_cookie(
        key="refresh_token", value=tokens.refresh_token, httponly=True, secure=True
    )
    return tokens

@router.get('/logout', status_code=status.HTTP_200_OK)
async def logout(response:Response):
    response.delete_cookie('refresh_token')


@router.get("/token", response_model=AccessToken)
async def get_token(
    session: SessionDep,
    user_id: Annotated[str, Depends(get_current_user_middleware)],
) -> AccessToken:
    """
    Este endpoint recive el refresh token atravez de cookies, para poder optener un nuevo access token
    """
    return services.new_token(user_id=user_id, session=session)
