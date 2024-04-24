from enum import Enum

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from back.db.repository import DBException
from back.nix import NixException


class Types(str, Enum):
    DB = "db"
    NIX = "nix"
    AUTH = "auth"


class ErrorResponse(BaseModel):
    type: Types
    message: str


class AuthException(Exception):
    pass


def add_errors(app: FastAPI) -> FastAPI:
    @app.exception_handler(NixException)
    async def nix_exception_handler(_, exc):
        return JSONResponse(
            status_code=400,
            content=ErrorResponse(type=Types.NIX, message=str(exc)).model_dump(),
        )

    @app.exception_handler(DBException)
    async def db_exception_handler(_, exc):
        return JSONResponse(
            status_code=400,
            content=ErrorResponse(type=Types.DB, message=str(exc)).model_dump(),
        )

    @app.exception_handler(AuthException)
    async def auth_exception_handler(_, exc):
        return JSONResponse(
            status_code=401,
            content=ErrorResponse(type=Types.AUTH, message=str(exc)).model_dump(),
        )

    return app
