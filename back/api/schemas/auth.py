from sqlmodel import SQLModel

from back.db.models import UserBase, UserWithID


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(UserBase):
    pass


class UserCreate(UserBase):
    password: str


class UserInfo(UserWithID):
    pass
