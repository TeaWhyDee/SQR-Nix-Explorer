from services.kv_store import KvStore

STORE = {}

class StSessKvStore(KvStore):
    def __init__(self, prefix: str = "") -> None:
        self.prefix = prefix

    def get(self, key: str) -> str:
        return STORE.get(self.prefix + key, "")

    def set(self, key: str, value: str):
        STORE[self.prefix + key] = value