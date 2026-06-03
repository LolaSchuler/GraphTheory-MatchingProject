from dataclasses import dataclass


@dataclass
class Quotas:
    general: int
    technological: int
    professional: int


@dataclass
class SpecialtyBonus:
    general: int
    technological: int
    professional: int


@dataclass
class Selection:
    academy_bonus: int
    minimum_grade: int
    specialty_bonus: SpecialtyBonus


@dataclass
class School:
    id: str
    name: str
    academy: str
    capacity: int
    quotas: Quotas
    selection: Selection
