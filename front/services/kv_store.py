from abc import ABC, abstractmethod


class KvStore(ABC):
    @abstractmethod
    def get(self, key: str) -> str:
        pass

    @abstractmethod
    def set(self, key: str, value: str):
        pass