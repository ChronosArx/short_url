from sqlmodel import Session, select
from fastapi import HTTPException, status
from ..models.user import User, UserLogIn, UserSignUp
from ..models.refresh_token import RefreshToken, Tokens, AccessToken
from ..utils.generate_hash import getPasswordHash, checkPassword
from ..utils.generate_token import generate_token, verify_env_variables
from datetime import datetime, timedelta, timezone
import dotenv
import os

dotenv.load_dotenv()
EXPIRE_REFRESH = os.environ.get("EXPIRE_REFRESH")
verify_env_variables()
EXPIRE_REFRESH = float(EXPIRE_REFRESH)


def save_refresh_token(token: str, user_id: int, session: Session):
    try:
        refresh_token = RefreshToken(
            refresh_token=token,
            user_id=user_id,
            expire_date=datetime.now(tz=timezone.utc) + timedelta(days=EXPIRE_REFRESH),
        )
        session.add(refresh_token)
        session.commit()
        session.refresh(refresh_token)
        return refresh_token
    except Exception as e:
        print(e)


def signup(session: Session, user: UserSignUp) -> Tokens:
    hash_password = getPasswordHash(user.password)
    try:
        statement = select(User).where(User.username == user.username)
        user_db = session.exec(statement).first()
        if user_db:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Username already exists."
            )

        # Created and save a new user in database
        user_db = User(
            user_name=user.username,
            email=user.email,
            password=hash_password,
        )
        session.add(user_db)
        session.commit()
        session.refresh(user_db)

        # Generate the access token
        access_token = generate_token(user_id=user_db.id, user_name=user_db.user_name)
        # Generate the refresh token and save this in the database
        refresh_token = generate_token(
            user_id=user_db.id, user_name=user_db.user_name, refresh=True
        )
        refresh_db = save_refresh_token(
            token=refresh_token, user_id=user_db.id, session=session
        )

        return Tokens(
            access_token=access_token,
            refresh_token=refresh_db.refresh_token,
        )
    except HTTPException:
        raise
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal Server error"},
        )


def login(session: Session, user: UserLogIn) -> Tokens:
    try:
        statement = select(User).where(User.username == user.username)
        user_db = session.exec(statement).first()
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
        access_token = generate_token(user_id=user_db.id, user_name=user_db.user_name)
        refresh_token = generate_token(
            user_id=user_db.id, user_name=user_db.user_name, refresh=True
        )

        refresh_db = save_refresh_token(
            token=refresh_token, user_id=user_db.id, session=session
        )

        return Tokens(
            access_token=access_token,
            refresh_token=refresh_db.refresh_token,
        )
    except HTTPException:
        raise
    except Exception as e:
        print(e)
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal server error"},
        )


def new_token(token: str, session: Session):
    try:
        statement = select(RefreshToken).where(RefreshToken.refresh_token == token)
        refresh_db = session.exec(statement).first()
        if not refresh_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials."
            )
        user_db = session.query(User).filter(User.id == refresh_db.user_id).first()
        if not user_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid username.",
            )
        access_token = generate_token(user_id=user_db.id, user_name=user_db.user_name)
        return AccessToken(access_token=access_token, token_type="Bearer")
    except HTTPException:
        raise
    except Exception as e:
        print(e)
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal server error."},
        )
