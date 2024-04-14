from sqlmodel import Session, select

from back.db.models import User, UserStore


def test_create_user(engine):
    user = User(username="bob", password_hash="some_hash")

    with Session(engine) as session:
        session.add(user)
        session.commit()

    with Session(engine) as session:
        statement = select(User)
        results = session.exec(statement).all()

        assert len(results) == 1
        assert results[0].username == "bob"


def test_store(engine, users):
    store = UserStore(id="nix_id", name="Store 1", user_id=users[0].id)

    with Session(engine) as session:
        session.add(store)
        session.commit()

    with Session(engine) as session:
        statement = select(User, UserStore).join(UserStore).where(UserStore.id == "nix_id")
        results = session.exec(statement).all()

        user, store = results[0]
        assert user.id == store.user_id
