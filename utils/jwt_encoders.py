from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import ExpiredSignatureError, PyJWTError
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from typing import Annotated
import os

load_dotenv()

token_algorithm = os.environ.get("TOKEN_ALG")
secret = os.environ.get("SECRET")


schema_oauth = OAuth2PasswordBearer(tokenUrl="login")


def generate_access_token(user_id: int):
    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=15)
    new_payload = {"sub": str(user_id), "exp ": expire.timestamp()}
    token = jwt.encode(payload=new_payload, key=secret, algorithm=token)
    return token


def generate_refresh_token():
    pass


def verify_token(token: Annotated[str, Depends(schema_oauth)]):
    exception = HTTPException(
        status_code=401,
        detail="Error de Credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, secret, algorithms=token_algorithm)
        if not payload:
            raise exception
    except ExpiredSignatureError:
        raise exception
    except PyJWTError:
        raise exception
