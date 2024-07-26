from fastapi import APIRouter, Depends, status, Response
from typing import Annotated
from ..controllers import auth_controller as services
from ..schemas import auth_schemas as schema
from ..dependencies import get_db
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
    response: Response,
) -> schema.Tokens:
    return services.signup(user=user, db=db)


@router.post("/login", status_code=status.HTTP_200_OK, response_model=schema.Tokens)
async def login(
    user: schema.UserLogInSchema,
    db: Annotated[any, Depends(get_db)],
    response: Response,
) -> schema.Tokens:
    return services.login(user=user, db=db)


@router.get("/token")
async def get_token(
    token: Annotated[str, Depends(verify_refresh_token_middleware)],
    db: Annotated[any, Depends(get_db)],
):
    return services.new_token(token=token, db=db)
