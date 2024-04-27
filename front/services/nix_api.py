from abc import ABC, abstractmethod
from typing import List


class NixAPI(ABC):
    @abstractmethod
    async def register(self, username: str, password: str):
        pass

    @abstractmethod
    async def login(self, username: str, password: str):
        pass

    @abstractmethod
    async def is_logged_in() -> bool:
        pass

    @abstractmethod
    async def add_store(self, name: str):
        pass

    @abstractmethod
    async def rm_store(self, name: str):
        pass

    @abstractmethod
    async def stores(self) -> List[str]:
        pass

    @abstractmethod
    async def add_package(self, name: str):
        pass

    @abstractmethod
    async def rm_package(self, store: str, package: str):
        pass

    @abstractmethod
    async def packages(self, store: str) -> List[str]:
        pass

    @abstractmethod
    async def closure_size(self, store: str, package: str) -> int:
        pass

    @abstractmethod
    async def difference_paths(
        self,
        store1: str,
        store2: str,
    ) -> List[str]:
        pass

    @abstractmethod
    async def difference_closures(
        self, store1: str, package1: str, store2: str, package2: str
    ) -> List[str]:
        pass
