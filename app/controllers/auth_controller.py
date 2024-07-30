from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..schemas import auth_schemas as schema
from ..models.user import User
from ..models.refresh_token import RefreshToken
from ..utils.generate_hash import getPasswordHash, checkPassword
from ..utils.generate_token import generate_token, verify_env_variables
from datetime import datetime, timedelta, timezone
import dotenv
import os

dotenv.load_dotenv()
EXPIRE_REFRESH = os.environ.get("EXPIRE_REFRESH")
verify_env_variables()
EXPIRE_REFRESH = float(EXPIRE_REFRESH)


def save_refresh_token(token: str, user_id: int, db: Session):
    try:
        refresh_token = RefreshToken(
            refresh_token=token,
            user_id=user_id,
            expire_date=datetime.now(tz=timezone.utc) + timedelta(days=EXPIRE_REFRESH),
        )
        db.add(refresh_token)
        db.commit()
        db.refresh(refresh_token)
        return refresh_token
    except Exception as e:
        print(e)


def signup(db: Session, user: schema.UserSignUpSchema):
    hash_password = getPasswordHash(user.password)
    try:
        if db.query(User).filter(User.user_name == user.user_name).first():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="User exist!"
            )

        # Created and save a new user in database
        user_db = User(
            user_name=user.user_name,
            email=user.email,
            password=hash_password,
        )
        db.add(user_db)
        db.commit()
        db.refresh(user_db)

        # Generate the access token
        access_token = generate_token(user_id=user_db.id, user_name=user_db.user_name)
        # Generate the refresh token and save this in the database
        refresh_token = generate_token(
            user_id=user_db.id, user_name=user_db.user_name, refresh=True
        )
        refresh_db = save_refresh_token(token=refresh_token, user_id=user_db.id, db=db)

        return schema.Tokens(
            access_token=access_token,
            refresh_token=refresh_db.refresh_token,
        )
    except Exception as e:
        print(e)
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal Server error"},
        )


def login(db: Session, user: schema.UserLogInSchema):
    try:
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

        refresh_db = save_refresh_token(token=refresh_token, user_id=user_db.id, db=db)

        return schema.Tokens(
            access_token=access_token,
            refresh_token=refresh_db.refresh_token,
        )
    except Exception as e:
        print(e)
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal server error"},
        )


def new_token(token: str, db: Session):
    try:
        refresh_db = (
            db.query(RefreshToken).filter(RefreshToken.refresh_token == token).first()
        )
        if not refresh_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Credentials error!"
            )
        user_db = db.query(User).filter(User.id == refresh_db.user_id).first()
        if not user_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found!",
            )
        access_token = generate_token(user_id=user_db.id, user_name=user_db.user_name)
        return schema.AccessToken(access_token=access_token, token_type="Bearer")
    except Exception as e:
        print(e)
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal server error."},
        )
