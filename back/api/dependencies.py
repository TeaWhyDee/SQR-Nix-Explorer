from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from back.api.config import Settings
from back.api.errors import AuthException
from back.api.schemas.auth import TokenData
from back.db.base import create_db_and_tables, create_engine
from back.db.models import User
from back.db.repository import DB
from back.nix import Nix

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token", auto_error=False)
TokenDep = Annotated[str, Depends(oauth2_scheme)]


# https://fastapi.tiangolo.com/advanced/settings/
@lru_cache
def get_settings() -> Settings:
    return Settings()


SettingsDep = Annotated[Settings, Depends(get_settings)]


async def get_db(settings: SettingsDep) -> DB:
    engine = create_engine(settings.db_engine)
    create_db_and_tables(
        engine
    )  # TODO: remove maybe? we don't need to init db on each start
    return DB(engine)


DBDep = Annotated[DB, Depends(get_db)]


# https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
async def get_current_user(token: TokenDep, settings: SettingsDep, db: DBDep) -> User:
    if token is None:
        raise AuthException("Token was not provided")

    credentials_exception = AuthException("Could not validate credentials")
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.jwt_algorithm]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = db.get_user(token_data.username)
    if user is None:
        raise credentials_exception
    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]


def get_nix(settings: SettingsDep) -> Nix:
    return Nix(stores_root=settings.nix_stores_root_path)


NixDep = Annotated[Nix, Depends(get_nix)]
