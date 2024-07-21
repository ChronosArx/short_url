from datetime import datetime, timedelta, timezone
import dotenv
import jwt
import os

dotenv.load_dotenv()

TOKEN_ALGORITHM = os.environ.get("TOKEN_ALG")
SECRET = os.environ.get("SECRET")
EXPIRE_ACCESS = float(os.environ.get("EXPIRE_ACCESS"))
EXPIRE_REFRESH = float(os.environ.get("EXPIRE_REFRESH"))


def generate_token(user_id: int, user_name: str, refresh: bool) -> str:
    if not EXPIRE_ACCESS | EXPIRE_REFRESH | SECRET | TOKEN_ALGORITHM:
        raise Exception("Environment variables are missing")
    if refresh:
        expire = datetime.now(tz=timezone.utc) + timedelta(days=EXPIRE_REFRESH)
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_REFRESH)
    new_payload = {
        "sub": str(user_id),
        "name": user_name,
        "exp": expire,
    }
    token = jwt.encode(payload=new_payload, key=SECRET, algorithm=TOKEN_ALGORITHM)
    return token
