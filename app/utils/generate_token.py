from datetime import datetime, timedelta, timezone
import dotenv
import jwt
import os

dotenv.load_dotenv()

TOKEN_ALGORITHM = os.environ.get("TOKEN_ALG")
SECRET = os.environ.get("SECRET")


def generate_access_token(user_id: int, user_name: str):
    expire = datetime.now(tz=timezone.utc) + timedelta(seconds=10)
    new_payload = {
        "sub": str(user_id),
        "name": user_name,
        "exp": expire,
    }
    token = jwt.encode(payload=new_payload, key=SECRET, algorithm=TOKEN_ALGORITHM)
    return token
