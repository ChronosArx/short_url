import bcrypt


def getPasswordHash(password: str) -> str:
    password_hashed = bcrypt.hashpw(password=password.encode(), salt=bcrypt.gensalt())
    password_hashed_str = password_hashed.hex()
    return str(password_hashed_str)


def checkPassword(password: str, password_hashed: str) -> bool:
    password_hashed_bytes = bytes.fromhex(password_hashed)
    return bcrypt.checkpw(password.encode(), password_hashed_bytes)
