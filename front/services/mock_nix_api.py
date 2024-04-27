from collections import defaultdict
from typing import Dict, List
from services.kv_store import KvStore
from services.nix_api import NixAPI

_LOGGED_KEY = "logged"


class MockNixApi(NixAPI):
    def __init__(self, _kvstore: KvStore) -> None:
        self._kvstore = _kvstore
        self._packages: Dict[str, List[str]] = defaultdict(lambda: [])
        self._packages["store1"] = [
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

    async def register(self, username: str, password: str):
        if username == "kiko":
            raise ValueError()
        self._kvstore.set(_LOGGED_KEY, _LOGGED_KEY)

    async def login(self, username: str, password: str):
        if username == "kiko" and password == "kiko":
            self._kvstore.set(_LOGGED_KEY, _LOGGED_KEY)
            return
        raise ValueError()

    async def is_logged_in(self) -> bool:
        return self._kvstore.get(_LOGGED_KEY) == _LOGGED_KEY

    async def add_store(self, name: str):
        self._packages[name]

    async def rm_store(self, name: str):
        del self._packages[name]

    async def stores(self):
        return self._packages.keys()

    async def add_package(self, store: str, name: str):
        self._packages[store].append(name)

    async def rm_package(self, store: str, package: str):
        ctx = self._packages[store]

        # Find the package
        for i, pkg in enumerate(ctx):
            if pkg.name == package:
                del self._packages[i]
                return

        # Package not found
        raise ValueError(f"Package {package} not found.")

    async def packages(self, store: str) -> List[str]:
        return self._packages[store]

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
