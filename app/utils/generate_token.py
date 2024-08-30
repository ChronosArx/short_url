from datetime import datetime, timedelta, timezone
import dotenv
import jwt
import os

dotenv.load_dotenv()

TOKEN_ALGORITHM = os.environ.get("TOKEN_ALG")
SECRET = os.environ.get("SECRET")
EXPIRE_ACCESS = os.environ.get("EXPIRE_ACCESS")
EXPIRE_REFRESH = os.environ.get("EXPIRE_REFRESH")

EXPIRE_ACCESS = float(EXPIRE_ACCESS)
EXPIRE_REFRESH = float(EXPIRE_REFRESH)


def verify_env_variables():
    if not (EXPIRE_ACCESS and EXPIRE_REFRESH and SECRET and TOKEN_ALGORITHM):
        raise Exception("Environment variables are missing")


def generate_token(
    user_id: int = None, user_name: str = None, refresh: bool = False
) -> str:
    verify_env_variables()
    if refresh:
        expire = datetime.now(tz=timezone.utc) + timedelta(days=EXPIRE_REFRESH)
        new_payload = {"exp": expire}
        token = jwt.encode(payload=new_payload, key=SECRET, algorithm=TOKEN_ALGORITHM)
        return token
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_ACCESS)
    new_payload = {
        "sub": str(user_id),
        "name": user_name,
        "exp": expire,
    }
    token = jwt.encode(payload=new_payload, key=SECRET, algorithm=TOKEN_ALGORITHM)
    return token
