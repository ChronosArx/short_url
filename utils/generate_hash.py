import bcrypt


def getPasswordHash(password: str):
    passwordHashed = bcrypt.hashpw(password=password.encode(), salt=bcrypt.gensalt())
    return str(passwordHashed)


def checkPassword(password: str, hashed: str):
    hash_to_encode = hashed[1:].replace("'", "")  # Quita formato de binario con el que se guardo
    if bcrypt.checkpw(password.encode(), hash_to_encode.encode()):
        return True
    return False
