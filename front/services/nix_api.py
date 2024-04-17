from abc import ABC, abstractmethod


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