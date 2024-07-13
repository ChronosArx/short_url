from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..schemas import auth_schemas as schema
from ..models.user import User
from ..utils.generate_hash import getPasswordHash, checkPassword
from ..middlewares.auth_middlewares import generate_access_token


def signup(db: Session, user: schema.UserSignUpSchema):
    hash_password = getPasswordHash(user.password)
    if db.query(User).filter(User.user_name == user.user_name).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User exist!")
    db_user = User(
        user_name=user.user_name,
        email=user.email,
        password=hash_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    token = generate_access_token(user_id=db_user.id, user_name=db_user.user_name)
    return schema.Token(access_token=token)


def login(db: Session, user: schema.UserLogInSchema):
    db_user = db.query(User).filter(User.user_name == user.user_name).first()
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

    return schema.Token(access_token=token)
