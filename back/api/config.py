# https://fastapi.tiangolo.com/advanced/settings/
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Nix Explorer"

    db_engine: str = "./sqlite.db"

    secret_key: str = "secret"

    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24
