from pytest import fixture
from sqlmodel import Session

from back.db.models import User


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


def test_create_user(db):
    with Session(db.engine) as session:
        results = session.query(User).all()

        assert len(results) == 0

    user = db.create_user("charlie", "password")

    with Session(db.engine) as session:
        statement = session.query(User)
        results = statement.all()

        assert len(results) == 1
        assert results[0].username == "charlie"
        assert results[0].password_hash != "password"
        assert results[0] == user


def test_get_password_hash(db, users):
    password_hash = db.get_password_hash(users[0].username)
    assert password_hash == users[0].password_hash

    password_hash = db.get_password_hash(users[1].username)
    assert password_hash == users[1].password_hash

    password_hash = db.get_password_hash("aboba")
    assert password_hash is None


def test_get_user_list(db, users):
    assert db.get_user_list() == users
