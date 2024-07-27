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
    user: schema.UserSignUpSchema,
    db: Annotated[any, Depends(get_db)],
):

    tokens = services.signup(user=user, db=db)
    response = JSONResponse(
        content={"access_token": tokens.access_token, "token_type": "Bearer"}
    )
    response.set_cookie(
        key="refresh_token", value=tokens.refresh_token, httponly=True, secure=True
    )
    return response


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    user_data: Annotated[schema.UserLogInSchema, Depends(OAuth2PasswordRequestForm)],
    db: Annotated[any, Depends(get_db)],
):
    tokens = services.login(user=user_data, db=db)
    response = JSONResponse(
        content={"access_token": tokens.access_token, "token_type": "Bearer"}
    )
    response.set_cookie(
        key="refresh_token", value=tokens.refresh_token, httponly=True, secure=True
    )
    return response


@router.get("/token")
async def get_token(
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(verify_refresh_token_middleware)],
) -> schema.AccessToken:
    return services.new_token(token=token, db=db)
