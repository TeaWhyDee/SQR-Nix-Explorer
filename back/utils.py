# https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
from datetime import timedelta, datetime, timezone
from functools import lru_cache

from bcrypt import checkpw, hashpw, gensalt
from jose import jwt


@lru_cache
def verify_password(plain_password, hashed_password) -> bool:
    return checkpw(plain_password.encode(), hashed_password.encode())


@lru_cache
def hash_password(password: str) -> str:
    return hashpw(password.encode(), gensalt()).decode()


def create_access_token(data: dict, expires_delta: timedelta, jwt_secret_key: str, jwt_algorithm: str) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, jwt_secret_key, algorithm=jwt_algorithm)
    return encoded_jwt
