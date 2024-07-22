from datetime import datetime, timedelta, timezone
import dotenv
import jwt
import os

dotenv.load_dotenv()

TOKEN_ALGORITHM = os.environ.get("TOKEN_ALG")
SECRET = os.environ.get("SECRET")
SECRET_REFRESH = os.environ.get("SECRET_REFRESH")
EXPIRE_ACCESS = float(os.environ.get("EXPIRE_ACCESS"))
EXPIRE_REFRESH = float(os.environ.get("EXPIRE_REFRESH"))


def generate_token(user_id: int | None, user_name: str | None, refresh: bool) -> str:
    if not EXPIRE_ACCESS | EXPIRE_REFRESH | SECRET | TOKEN_ALGORITHM | SECRET_REFRESH:
        raise Exception("Environment variables are missing")
    if refresh:
        expire = datetime.now(tz=timezone.utc) + timedelta(days=EXPIRE_REFRESH)
        new_payload = {"exp": expire}
        token = jwt.encode(payload=new_payload, key=SECRET, algorithm=TOKEN_ALGORITHM)
        return token
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_REFRESH)
    new_payload = {
        "sub": str(user_id),
        "name": user_name,
        "exp": expire,
    }
    token = jwt.encode(payload=new_payload, key=SECRET, algorithm=TOKEN_ALGORITHM)
    return token
