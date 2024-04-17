from services.kv_store import KvStore
from services.nix_api import NixAPI

_LOGGED_KEY = "logged"

class MockNixApi(NixAPI):
    def __init__(self, store: KvStore) -> None:
        self.store = store

    def register(self, username: str, password: str):
        if username == "kiko":
            raise ValueError()
        self.store.set(_LOGGED_KEY, _LOGGED_KEY)

    def login(self, username: str, password: str):
        if username == "kiko" and password == "kiko":
            self.store.set(_LOGGED_KEY, _LOGGED_KEY)
            return
        raise ValueError()

    def is_logged_in(self) -> bool:
        return self.store.get(_LOGGED_KEY) == _LOGGED_KEY