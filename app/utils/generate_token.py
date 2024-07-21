from datetime import datetime, timedelta, timezone
import dotenv
import jwt
import os

dotenv.load_dotenv()

TOKEN_ALGORITHM = os.environ.get("TOKEN_ALG")
SECRET = os.environ.get("SECRET")


def generate_token(user_id: int, user_name: str, refresh: bool) -> str:
    if refresh:
        expire = datetime.now(tz=timezone.utc) + timedelta(days=7)
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=10)
    new_payload = {
        "sub": str(user_id),
        "name": user_name,
        "exp": expire,
    }
    token = jwt.encode(payload=new_payload, key=SECRET, algorithm=TOKEN_ALGORITHM)
    return token
