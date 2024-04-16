from back.db.models import User
from back.db.repository import DB
from back.utils import verify_password


def authenticate_user(db: DB, username: str, password: str) -> User | None:
    user = db.get_user(username)
    if not user:
        return
    if not verify_password(password, user.password_hash):
        return
    return user
