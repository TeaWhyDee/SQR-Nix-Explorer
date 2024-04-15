# https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
from bcrypt import checkpw, hashpw, gensalt


def verify_password(plain_password, hashed_password) -> bool:
    return checkpw(plain_password.encode(), hashed_password.encode())


def hash_password(password: str) -> str:
    return hashpw(password.encode(), gensalt()).decode()
