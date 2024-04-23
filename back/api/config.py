# https://fastapi.tiangolo.com/advanced/settings/
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_engine: str = "./sqlite.db"

    secret_key: str = "secret"

    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24

    nix_stores_root_path: str = "./.stores/"
