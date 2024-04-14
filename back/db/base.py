import logging

from sqlalchemy import Engine
from sqlmodel import SQLModel, create_engine as create_engine_sqlmodel


def setup_logging(debug: bool = False):
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level, format="%(asctime)s.%(msecs)03d - %(message)s", datefmt="%H:%M:%S"
    )

    if debug:
        sql_logger = logging.getLogger("sqlalchemy")
        sql_logger.setLevel(logging.INFO)


def create_engine(filename: str) -> Engine:
    sqlite_url = f"sqlite:///{filename}"

    return create_engine_sqlmodel(sqlite_url)


def create_db_and_tables(engine: Engine):
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    setup_logging()
    create_db_and_tables(create_engine(":memory:"))
