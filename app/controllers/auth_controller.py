from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from schemas import auth_schemas as schema
from models.user import User
from utils.generate_hash import getPasswordHash, checkPassword
from utils.generate_token import generate_token


def signup(db: Session, user: schema.UserSignUpSchema):
    hash_password = getPasswordHash(user.password)
    if db.query(User).filter(User.user_name == user.user_name).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User exist!")
    user_db = User(
        user_name=user.user_name,
        email=user.email,
        password=hash_password,
    )
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    access_token = generate_token(user_id=user_db.id, user_name=user_db.user_name)
    refresh_token = generate_token(
        user_id=user_db.id, user_name=user_db.user_name, refresh=True
    )
    return schema.Tokens(access_token=access_token, refresh_token=refresh_token)


def login(db: Session, user: schema.UserLogInSchema):
    user_db = db.query(User).filter(User.user_name == user.user_name).first()
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found!",
        )
    if not checkPassword(user.password, user_db.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The password is incorrect!",
        )
    access_token = generate_token(user_id=user_db.id, user_name=user_db.user_name)
    refresh_token = generate_token(
        user_id=user_db.id, user_name=user_db.user_name, refresh=True
    )
    return schema.Tokens(access_token=access_token, refresh_token=refresh_token)


def new_token(user: str, db: Session):
    user_db = db.query(User).filter(User.user_name == user).first()
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found!",
        )
    access_token = generate_token(user_id=user_db.id, user_name=user_db.user_name)
    return schema.Tokens(access_token=access_token)
