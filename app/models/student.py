from dataclasses import dataclass

@dataclass
class Wish:
    school: str
    rank: int

@dataclass
class Student:
    id: str
    specialty: str
    grade: float
    academy: str
    wishes: list[Wish]