from dataclasses import dataclass


@dataclass
class Package:
    id: str
    name: str
    closure_size: int

    def __eq__(self, other):
        if not isinstance(other, Package):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)
