from fastapi import APIRouter, Depends, status, Response
from typing import Annotated
from controllers import auth_controller as services
from schemas import auth_schemas as schema
from dependencies import get_db

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/signup",
    response_model=schema.Token,
    status_code=status.HTTP_201_CREATED,
)
async def signup(
    user: schema.UserSignUpSchema,
    db: Annotated[any, Depends(get_db)],
    response: Response,
) -> schema.Token:
    return services.signup(user=user, db=db)


@router.post("/login", status_code=status.HTTP_200_OK, response_model=schema.Token)
async def login(
    user: schema.UserLogInSchema,
    db: Annotated[any, Depends(get_db)],
    response: Response,
) -> schema.Token:
    return services.login(user=user, db=db)
