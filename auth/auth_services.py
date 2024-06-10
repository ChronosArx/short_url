from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import auth.auth_schema as auth_schema
from ..database import models
from ..utils.generate_hash import getPasswordHash, checkPassword


def signup(db: Session, user: auth_schema.UserSignUpSchema):
    hash_password = getPasswordHash(user.password)
    db_user = models.User(
        user_name=user.user_name,
        email=user.email,
        password=hash_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def login(db: Session, user: auth_schema.UserLogInSchema):
    db_user = (
        db.query(models.User).filter(models.User.user_name == user.user_name).first()
    )
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found!",
        )
    if not checkPassword(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The password is incorrect!",
        )
    return db_user
