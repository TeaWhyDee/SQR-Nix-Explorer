from pytest import fixture
from sqlalchemy import Engine
from sqlmodel import create_engine, SQLModel, Session
from back.db.crud import DB
from back.db.models import User


@fixture()
def engine() -> Engine:
    engine = create_engine("sqlite:///:memory:", echo=True)
    SQLModel.metadata.create_all(engine)
    return engine


@fixture()
def db(engine) -> DB:
    return DB(engine)


@fixture()
def users(engine):
    with Session(engine) as session:
        users = [
            User(username="bob", password_hash="some_hash"),
            User(username="alice", password_hash="another_hash"),
        ]
        session.add_all(users)
        session.commit()

        for user in users:
            session.refresh(user)

    return users
