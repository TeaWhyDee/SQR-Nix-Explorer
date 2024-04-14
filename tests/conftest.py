from pytest import fixture
from sqlalchemy import Engine
from sqlmodel import create_engine, Session

from back.db.base import setup_logging, create_engine, create_db_and_tables
from back.db.crud import DB
from back.db.models import User

setup_logging(debug=True)


@fixture()
def engine() -> Engine:
    engine = create_engine(":memory:")
    create_db_and_tables(engine)
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
