from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from back.api.dependencies import DBDep, SettingsDep
from back.api.schemas.auth import Token, UserCreate, UserInfo
from back.api.services.user import authenticate_user
from back.utils import create_access_token

auth = APIRouter(prefix="/auth", tags=["Auth"])


# ===== USER =====
@auth.post("/register", response_model=UserInfo)
def register(user: UserCreate,
             db: DBDep):
    user = db.create_user(user.username, user.password)
    return user


@auth.post("/token")
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: DBDep,
        settings: SettingsDep
) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=expires_delta,
        jwt_secret_key=settings.secret_key,
        jwt_algorithm=settings.jwt_algorithm
    )
    return Token(access_token=access_token, token_type="bearer")
