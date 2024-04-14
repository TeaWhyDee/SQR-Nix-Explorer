from sqlmodel import Session

from back.db.models import User, UserStore


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


def test_create_store(db, users):
    store = db.create_store(users[0], "Store 1", "nix_id")

    with Session(db.engine) as session:
        results = session.query(UserStore).all()

    assert len(results) == 1
    assert results[0] == store
    assert results[0].user_id == users[0].id
