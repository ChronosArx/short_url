from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException, status
from ..schemas.user import UserLogIn, UserSignUp, Tokens, AccessToken
from ..models import User
from ..utils.generate_hash import getPasswordHash, checkPassword
from ..utils.generate_token import generate_token
from ..core.config import settings


def signup(session: Session, user: UserSignUp) -> Tokens:
    try:
        hash_password = getPasswordHash(user.password)
        statement = select(User).where(User.username == user.username)
        user_db = session.execute(statement).scalars().one_or_none()
        if user_db:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Username already exists."
            )

        # Created and save a new user in database
        user_db = User(
            username=user.username,
            email=user.email,
            password=hash_password,
        )
        session.add(user_db)
        session.commit()
        session.refresh(user_db)

        # Generate the access token
        access_token = generate_token(user_id=user_db.id, user_name=user_db.username)
        # Generate the refresh token and save this in the database
        refresh_token = generate_token(
            user_id=user_db.id, user_name=user_db.username, refresh=True
        )
        return Tokens(
            access_token=access_token,
            refresh_token=refresh_token,
        )
    except HTTPException as httP_exception:
        raise httP_exception
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal Server error"},
        )


def login(session: Session, user: UserLogIn) -> Tokens:
    try:
        statement = select(User).where(User.username == user.username)
        user_db = session.execute(statement).scalars().one_or_none()
        if not user_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid username or password.",
            )
        if not checkPassword(user.password, user_db.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password.",
            )
        access_token = generate_token(user_id=user_db.id, user_name=user_db.username)
        refresh_token = generate_token(
            user_id=user_db.id, user_name=user_db.username, refresh=True
        )
        return Tokens(
            access_token=access_token,
            refresh_token=refresh_token,
        )
    except HTTPException as httP_exception:
        raise httP_exception
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


def new_token(user_id: int, session: Session):
    try:
        statement = select(User).where(User.id == user_id)
        user_db = session.execute(statement).scalars().one_or_none()
        if not user_db:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error to create the new access token",
            )
        access_token = generate_token(user_id=user_db.id, user_name=user_db.username)
        return AccessToken(access_token=access_token, token_type="Bearer")
    except HTTPException as httP_exception:
        raise httP_exception
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal server error."},
        )
