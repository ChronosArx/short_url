from fastapi import APIRouter, Depends
from typing import Annotated
import auth.auth_services as services
import auth.auth_schema as schema
from database.database_dependency import get_db

router = APIRouter()


@router.post("/signup")
async def signup(user: schema.UserSignUpSchema, db: Annotated[any, Depends(get_db)]):
    return services.signup(user=user, db=db)


@router.post("/login")
async def login(user: schema.UserLogInSchema, db: Annotated[any, Depends(get_db)]):
    return services.login(user=user, db=db)
