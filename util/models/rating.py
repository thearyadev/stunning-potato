from uuid import UUID

from dataclasses import dataclass

@dataclass
class RatingIn:
    story: int 
    positions: int 
    pussy: int
    shots: int 
    boobs: int
    face: int 
    rearview: int

@dataclass
class Rating:
    uuid: UUID 

    average: float | None 
    story: int
    positions: int
    pussy: int
    shots: int
    boobs: int
    face: int
    rearview: int