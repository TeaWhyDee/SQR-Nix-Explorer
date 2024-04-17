from typing import List
from services.kv_store import KvStore
from services.nix_api import NixAPI
from structs.package import Package

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
    
    def packages(self) -> List[Package]:
        return [
            Package(name="docker", closure_size=32),
            Package(name="nginx", closure_size=21),
            Package(name="slonik", closure_size=1),
            Package(name="oklahoma", closure_size=1),
            Package(name="riskolima", closure_size=4),
            Package(name="kirara", closure_size=32),
            Package(name="miko", closure_size=21),
            Package(name="leila", closure_size=1),
            Package(name="erko", closure_size=1),
            Package(name="silver", closure_size=4),
            Package(name="cors", closure_size=32),
            Package(name="sos", closure_size=21),
            Package(name="kisa", closure_size=61),
            Package(name="dicuc", closure_size=1),
            Package(name="march7", closure_size=4),
            Package(name="aheron", closure_size=2),
            Package(name="kli", closure_size=21),
            Package(name="diona", closure_size=1),
            Package(name="nahida", closure_size=0),
            Package(name="yaya", closure_size=4),
            Package(name="balls", closure_size=7),
        ]
        
    def difference_paths(self, package1: str, package2: str) -> List[str]:
        return [
            'path1',
            'path2',
            'path3',
            'path4',
        ]
    
    def difference_closures(self, package1: str, package2: str) -> List[Package]:
        return [
            'closure1',
            'closure2',
            'closure3',
            'closure4',
        ]