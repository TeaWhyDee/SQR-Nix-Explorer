from typing import Dict, List
from services.kv_store import KvStore
from services.nix_api import NixAPI

_LOGGED_KEY = "logged"

PACKAGES: Dict[str, List[str]] = {}
PACKAGES["store1"] = [
    "docker",
    "nginx",
    "slonik",
    "oklahoma",
    "riskolima",
    "kirara",
    "miko",
    "leila",
    "erko",
    "silver",
    "cors",
    "sos",
    "kisa",
    "dicuc",
    "march7",
    "aheron",
    "kli",
    "diona",
    "nahida",
    "yaya",
    "balls",
]


class MockNixApi(NixAPI):
    def __init__(self, _kvstore: KvStore) -> None:
        self._kvstore = _kvstore

    async def register(self, username: str, password: str):
        if username == "kiko":
            raise ValueError()
        self._kvstore.set(_LOGGED_KEY, _LOGGED_KEY)

    async def login(self, username: str, password: str):
        if username == "kiko" and password == "kiko":
            self._kvstore.set(_LOGGED_KEY, _LOGGED_KEY)
            return
        raise ValueError()

    async def logout(self):
        self._kvstore.set(_LOGGED_KEY, '')

    async def is_logged_in(self) -> bool:
        return self._kvstore.get(_LOGGED_KEY) == _LOGGED_KEY

    async def add_store(self, name: str):
        PACKAGES[name] = []

    async def rm_store(self, name: str):
        del PACKAGES[name]

    async def stores(self):
        return list(PACKAGES.keys())

    async def add_package(self, store: str, name: str):
        PACKAGES[store].append(name)

    async def rm_package(self, store: str, package: str):
        ctx = PACKAGES[store]

        # Find the package
        for i, pkg in enumerate(ctx):
            if pkg.name == package:
                del PACKAGES[i]
                return

        # Package not found
        raise ValueError(f"Package {package} not found.")

    async def packages(self, store: str) -> List[str]:
        return PACKAGES[store]

    async def closure_size(self, store: str, package: str) -> int:
        return 3

    async def difference_paths(self, store1: str, store2: str) -> List[str]:
        return [
            "path1",
            "path2",
            "path3",
            "path4",
        ]

    async def difference_closures(
        self, store1: str, package1: str, store2: str, package2: str
    ) -> List[str]:
        return [
            "closure1",
            "closure2",
            "closure3",
            "closure4",
        ]
