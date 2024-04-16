from pytest import raises
from sqlmodel import Session, select

from back.db.repository import DBError
from back.db.models import User, UserStore


def test_create_user(db):
    with Session(db.engine) as session:
        results = session.exec(select(User)).all()

    assert len(results) == 0

    user = db.create_user("charlie", "password")

    with Session(db.engine) as session:
        results = session.exec(select(User)).all()

    assert len(results) == 1
    assert results[0].username == "charlie"
    assert results[0].password_hash != "password"
    assert results[0] == user

    with raises(DBError):
        db.create_user("charlie", "password")


def test_get_password_hash(db, users):
    password_hash = db.get_password_hash(users[0].username)
    assert password_hash == users[0].password_hash

    password_hash = db.get_password_hash(users[1].username)
    assert password_hash == users[1].password_hash

    with raises(DBError):
        db.get_password_hash("aboba")


def test_get_user_list(db, users):
    assert db.get_user_list() == users


def test_create_store(db, users):
    store = db.create_store(users[0], "Store 1", "nix_id")

    with Session(db.engine) as session:
        results = session.exec(select(UserStore)).all()

    assert len(results) == 1
    assert results[0] == store
    assert results[0].user_id == users[0].id


def test_get_store_owner(db, users):
    store = db.create_store(users[0], "Store 1", "nix_id")

    owner = db.get_store_owner(store.id)
    assert owner == users[0]

    owner = db.get_store_owner("aboba")
    assert owner is None


def test_get_user_stores(db, users):
    store1 = db.create_store(users[0], "Store 1", "nix_id")
    store2 = db.create_store(users[0], "Store 2", "nix_id2")
    store3 = db.create_store(users[1], "Store 3", "nix_id3")

    stores = db.get_user_stores(users[0].username)
    assert stores == [store1, store2]

    stores = db.get_user_stores(users[1].username)
    assert stores == [store3]

    stores = db.get_user_stores("aboba")
    assert stores == []
