from pytest import fixture
from sqlmodel import create_engine, SQLModel


@fixture()
def engine():
    engine = create_engine("sqlite:///:memory:", echo=True)
    SQLModel.metadata.create_all(engine)
    return engine
