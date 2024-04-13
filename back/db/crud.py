from typing import Sequence

from sqlmodel import Session, select

from .models import User
from sqlalchemy import Engine
import bcrypt


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode()


class DB:
    def __init__(self, engine: Engine):
        self.engine = engine

    def create_user(self, username: str, password: str) -> User:
        user = User(username=username, password_hash=hash_password(password))

        with Session(self.engine) as session:
            session.add(user)
            session.commit()

        return user

    def get_password_hash(self, username: str) -> str | None:
        with Session(self.engine) as session:
            statement = select(User).where(User.username == username)
            user = session.exec(statement).first()
        return user.password_hash if user else None

    def get_user_list(self) -> Sequence[User]:
        with Session(self.engine) as session:
            statement = select(User)
            users = session.exec(statement).all()
        return users
