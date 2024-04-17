from dataclasses import dataclass


@dataclass
class Package:
    name: str
    closure_size: int