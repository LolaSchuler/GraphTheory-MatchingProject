from dataclasses import dataclass


@dataclass
class Wish:
    id: str
    rank: int


@dataclass
class Student:
    id: str
    specialty: str
    grade: float
    academy: str
    capacity: int
    wishes: list[Wish]
