from fastapi import APIRouter, Depends, Response, status
from typing import Annotated
from .premium_schemas import CreateDomainSchema, CreateCodeSchema
from ..database.database_dependency import get_db
from . import premium_services as services
from ..utils.jwt_encoders import verify_token

router = APIRouter(
    prefix="/premium",
    tags=["Premium"],
)


@router.post(
    "/create_domain",
    dependencies=[Depends(verify_token)],
    status_code=status.HTTP_201_CREATED,
    response_description="Domain was created.",
)
async def create_domain(data: CreateDomainSchema, db: Annotated[any, Depends(get_db)]):
    await services.create_domain(data=data, db=db)
    return


@router.post(
    "/create_custom_code",
    dependencies=[Depends(verify_token)],
    status_code=status.HTTP_201_CREATED,
    response_description="Code was created.",
)
async def create_link(data: CreateCodeSchema, db: Annotated[any, Depends(get_db)]):
    await services.create_code(data=data, db=db)
    return
