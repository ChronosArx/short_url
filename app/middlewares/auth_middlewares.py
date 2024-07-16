from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import ExpiredSignatureError, PyJWTError
import jwt
from typing import Annotated
import dotenv
import os

dotenv.load_dotenv()

TOKEN_ALGORITHM = os.environ.get("TOKEN_ALG")
SECRET = os.environ.get("SECRET")


schema_oauth = OAuth2PasswordBearer(tokenUrl="/login")


def verify_token_middleware(token: Annotated[str, Depends(schema_oauth)]):
    exception = HTTPException(
        status_code=401,
        detail="Credentials Error",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET, algorithms=[TOKEN_ALGORITHM])
        if not payload:
            raise exception
    except ExpiredSignatureError:
        raise exception
    except PyJWTError:
        raise exception

    return token


def get_current_user_middleware(
    token: Annotated[str, Depends(verify_token_middleware)]
):
    payload = jwt.decode(token, SECRET, algorithms=[TOKEN_ALGORITHM])
    return payload["name"]
