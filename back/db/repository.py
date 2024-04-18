from typing import Sequence

from sqlalchemy import Engine
from sqlmodel import Session, select

from back.db.models import User, UserStore
from back.utils import hash_password


class DBException(Exception):
    pass


class DB:
    def __init__(self, engine: Engine):
        self.engine = engine

    def get_user(self, username: str) -> User | None:
        with Session(self.engine) as session:
            statement = select(User).where(User.username == username)
            user = session.exec(statement).first()

        return user

    def create_user(self, username: str, password: str) -> User:
        if self.get_user(username) is not None:
            raise DBException(f"User {username} already exists")

        user = User(username=username, password_hash=hash_password(password))

        with Session(self.engine) as session:
            session.add(user)
            session.commit()
            session.refresh(user)

        return user

    def get_password_hash(self, username: str) -> str:
        user = self.get_user(username)

        if user is None:
            raise DBException(f"User {username} not found")

        return user.password_hash

    def get_user_list(self) -> Sequence[User]:
        with Session(self.engine) as session:
            statement = select(User)
            users = session.exec(statement).all()

        return users

    def get_store(self, store_name: str) -> UserStore | None:
        with Session(self.engine) as session:
            statement = select(UserStore).where(UserStore.name == store_name)
            store = session.exec(statement).first()

        return store

    def create_store(self, user: User, store_name: str, store_id: str) -> UserStore:
        if self.get_store(store_name) is not None:
            raise DBException(f"Store {store_name} already exists")

        store = UserStore(name=store_name, user_id=user.id, id=store_id)

        with Session(self.engine) as session:
            session.add(store)
            session.commit()
            session.refresh(store)

        return store

    def remove_store(self, store_id: str) -> None:
        with Session(self.engine) as session:
            statement = select(UserStore).where(UserStore.id == store_id)
            store = session.exec(statement).first()

            if store is None:
                raise DBException(f"Store {store_id} not found")

            session.delete(store)
            session.commit()

    def get_store_owner(self, store_id: str) -> User | None:
        with Session(self.engine) as session:
            statement = select(User).join(UserStore).where(UserStore.id == store_id)
            user = session.exec(statement).first()

        return user

    def get_user_stores(self, username: str) -> Sequence[UserStore]:
        with Session(self.engine) as session:
            statement = select(UserStore).join(User).where(User.username == username)
            stores = session.exec(statement).all()

        return stores
