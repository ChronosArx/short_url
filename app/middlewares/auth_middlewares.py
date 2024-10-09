from fastapi import HTTPException, Depends, Request, Security
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import ExpiredSignatureError, PyJWTError
import jwt
from typing import Annotated
from ..core.config import settings


schema_oauth = OAuth2PasswordBearer(tokenUrl="apiv1/auth/login")
exception = HTTPException(
    status_code=401,
    detail="Credentials Error",
    headers={"WWW-Authenticate": "Bearer"},
)


def verify_token_middleware(token: Annotated[str, Depends(schema_oauth)]):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
            verify=True,
            options={"verify_exp": True},
        )
        if not payload:
            raise exception
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Credentials Error")
    except PyJWTError:
        raise exception

    return payload


def verify_refresh_token_middleware(request: Request):
    token = request.cookies.get("refresh_token")
    try:
        jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
            verify=True,
            options={"verify_exp": True},
        )
        return token
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Credentials Error")
    except PyJWTError:
        raise exception


def get_current_user_middleware(
    payload: Annotated[str, Depends(verify_token_middleware)]
):
    return payload["sub"]
