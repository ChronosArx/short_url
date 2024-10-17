from datetime import datetime, timedelta, timezone
from ..core.config import settings
import jwt


def generate_token(
    user_id: int = None, user_name: str = None, refresh: bool = False
) -> str:
    if refresh:
        expire = datetime.now(tz=timezone.utc) + timedelta(days=settings.EXPIRE_REFRESH)
        new_payload = {"exp": expire, "sub":str(user_id)}
        token = jwt.encode(
            payload=new_payload, key=settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return token
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.EXPIRE_ACCESS)
    new_payload = {
        "sub": str(user_id),
        "name": user_name,
        "exp": expire,
    }
    token = jwt.encode(payload=new_payload, key=settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return token
