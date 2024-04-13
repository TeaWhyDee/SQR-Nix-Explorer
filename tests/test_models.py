from sqlmodel import Session, select

from back.db.models import User


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
