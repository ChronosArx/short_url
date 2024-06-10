from fastapi import APIRouter, Depends
from typing import Annotated
import auth_services as services
import auth.auth_schema as auth_schema
from share_dependencies.database_dependency import get_db

router = APIRouter()


@router.post("/signup")
async def signup(
    user: auth_schema.UserSignUpSchema, db: Annotated[any, Depends(get_db)]
):
    return services.signup(user=user, db=db)


@router.post("/login")
async def login(user: auth_schema.UserLogInSchema, db: Annotated[any, Depends(get_db)]):
    return services.login(user=user, db=db)
