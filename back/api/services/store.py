from back.api.errors import AuthException
from back.db.models import User, UserStore
from back.db.repository import DBException, DB


def get_store_for_interactions(store_name: str, db: DB, user: User) -> UserStore:
    store = db.get_store(store_name)

    if store is None:
        raise DBException(f"Store {store_name} not found")

    if store.user_id != user.id:
        raise AuthException(
            f"You can't interact with store that you don't own: {store_name}"
        )

    return store
