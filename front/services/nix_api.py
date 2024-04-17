from abc import ABC, abstractmethod
from typing import List

from structs.package import Package


class NixAPI(ABC):
    @abstractmethod
    def register(self, username: str, password: str):
        pass

    @abstractmethod
    def login(self, username: str, password: str):
        pass

    @abstractmethod
    def is_logged_in() -> bool:
        pass

    @abstractmethod
    def packages(self) -> List[Package]:
        pass

    @abstractmethod
    def rm_package(self, package_id: int):
        pass

    @abstractmethod
    def difference_paths(self, package1: str, package2: str) -> List[str]:
        pass

    @abstractmethod
    def difference_closures(self, package1: str, package2: str) -> List[str]:
        pass
