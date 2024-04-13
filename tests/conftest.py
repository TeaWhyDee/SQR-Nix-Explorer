from pytest import fixture
from sqlalchemy import Engine
from sqlmodel import create_engine, SQLModel
from back.db.crud import DB


@fixture()
def engine() -> Engine:
    engine = create_engine("sqlite:///:memory:", echo=True)
    SQLModel.metadata.create_all(engine)
    return engine


@fixture()
def db(engine) -> DB:
    return DB(engine)
