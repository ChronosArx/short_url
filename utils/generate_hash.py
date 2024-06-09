import bcrypt


def getPasswordHash(password: str):
    passwordHashed = bcrypt.hashpw(password=password.encode(), salt=bcrypt.gensalt())
    return str(passwordHashed)


def checkPassword(password: str, hashed):
    if bcrypt.checkpw(password.encode(), hashed):
        return True
    return False