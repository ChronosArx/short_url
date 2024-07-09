from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from . import auth_schema as schema
from ..database import models
from ..utils.generate_hash import getPasswordHash, checkPassword
from ..utils.jwt_encoders import generate_access_token


def signup(db: Session, user: schema.UserSignUpSchema):
    hash_password = getPasswordHash(user.password)
    if db.query(models.User).filter(models.User.user_name == user.user_name).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User exist!")
    db_user = models.User(
        user_name=user.user_name,
        email=user.email,
        password=hash_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    token = generate_access_token(user_id=db_user.id, user_name=db_user.user_name)
    return token


def login(db: Session, user: schema.UserLogInSchema):
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
    token = generate_access_token(user_id=db_user.id, user_name=db_user.user_name)
    return token
