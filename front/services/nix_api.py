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