import os
from functools import lru_cache

from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy import Engine
from sqlmodel import Session

from back.api.dependencies import get_db
from back.db.base import (
    setup_logging,
    create_engine,
    create_db_and_tables,
    remove_db_and_tables,
)
from back.db.models import User
from back.db.repository import DB
from back.main import get_app
from back.utils import hash_password

setup_logging(debug=True)
TEST_DB_PATH = "./.test.db"


@fixture(scope="session")
def engine(worker_id) -> Engine:
    db_path = TEST_DB_PATH + str(worker_id)
    if os.path.exists(db_path):
        os.remove(db_path)

    engine = create_engine(db_path)

    yield engine

    if os.path.exists(db_path):
        os.remove(db_path)


@fixture()
def db(engine) -> DB:
    remove_db_and_tables(engine)
    create_db_and_tables(engine)

    return DB(engine)


@fixture()
def users(db, engine):
    with Session(engine) as session:
        users = [
            User(username="bob", password_hash=hash_password("bob")),
            User(username="alice", password_hash=hash_password("alice")),
        ]
        session.add_all(users)
        session.commit()

        for user in users:
            session.refresh(user)

    return users


@lru_cache
def get_app_cached():
    return get_app(debug=True)


@fixture()
def client(db):
    app = get_app_cached()

    def _get_db():
        return db

    app.dependency_overrides[get_db] = _get_db

    return TestClient(app)
