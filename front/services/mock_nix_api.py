from typing import List
from services.kv_store import KvStore
from services.nix_api import NixAPI
from structs.package import Package

_LOGGED_KEY = "logged"
PACKAGES = [
    Package(id=0, name="docker", closure_size=32),
    Package(id=1, name="nginx", closure_size=21),
    Package(id=2, name="slonik", closure_size=1),
    Package(id=3, name="oklahoma", closure_size=1),
    Package(id=4, name="riskolima", closure_size=4),
    Package(id=5, name="kirara", closure_size=32),
    Package(id=6, name="miko", closure_size=21),
    Package(id=7, name="leila", closure_size=1),
    Package(id=8, name="erko", closure_size=1),
    Package(id=9, name="silver", closure_size=4),
    Package(id=10, name="cors", closure_size=32),
    Package(id=11, name="sos", closure_size=21),
    Package(id=12, name="kisa", closure_size=61),
    Package(id=13, name="dicuc", closure_size=1),
    Package(id=14, name="march7", closure_size=4),
    Package(id=15, name="aheron", closure_size=2),
    Package(id=16, name="kli", closure_size=21),
    Package(id=17, name="diona", closure_size=1),
    Package(id=18, name="nahida", closure_size=0),
    Package(id=19, name="yaya", closure_size=4),
    Package(id=20, name="balls", closure_size=7),
]


class MockNixApi(NixAPI):
    def __init__(self, store: KvStore) -> None:
        self.store = store
        self._packages = PACKAGES

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

    def packages(self) -> List[Package]:
        return self._packages

    def rm_package(self, package_id: int):
        # Find the package by ID
        for i, package in enumerate(self._packages):
            if package.id == package_id:
                del self._packages[i]
                return

        # Package not found
        raise ValueError(f"Package with ID {package_id} not found.")
