from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from fastapi import status
from .premium_schemas import CreateDomainSchema, CreateCodeSchema
from ..database import models


async def create_domain(data: CreateDomainSchema, db: Session):
    user_db = (
        db.query(models.User).filter(models.User.user_name == data.user_name).first()
    )
    if not user_db:
        raise HTTPException(
            detail="User not found", status_code=status.HTTP_404_NOT_FOUND
        )
    new_domain = models.PremiumLink(custom_domain=data.custom_domain, user=user_db)
    db.add(new_domain)
    db.commit()
    db.refresh(new_domain)
    return new_domain


async def create_code(data: CreateCodeSchema, db: Session):
    user_db = (
        db.query(models.User).filter(models.User.user_name == data.user_name).first()
    )
    if not user_db:
        raise HTTPException(
            detail="User not found", status_code=status.HTTP_404_NOT_FOUND
        )
    new_code = models.CustomCode(
        code=data.code,
        original_url=data.original_url,
        id_premium_link=user_db.premium_link.id,
    )
    db.add(new_code)
    db.commit()
    db.refresh(new_code)
    return new_code
